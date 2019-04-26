#    Copyright (c) 2014 Mark McKenney
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.


import pyspatiotemporalgeom.utilities.segLibrary as segLibrary
import pyspatiotemporalgeom.utilities.hsegLibrary as hsegLibrary
import pyspatiotemporalgeom.utilities.regionOverlayGrid as grid
import struct


def pointInPolygon(x, y, poly):
  ''' 
  Point in polygon test.  Works for complex regions (multiple faces, holes, faces in holes, etc.)


  **Input:**

  + x: the X value of the point to be tested
  + y: the Y valu of the point to be tested
  + poly: a list of 2D segments in the usual format: :math:`((x1,y1),(x2,y2))`

  **Output:**

  + boolean value.  `True` if the point is **in** the polygon **OR** if the point is **on** the boundary.  `False` otherwise

  Note, this may be sensitive to floating poitn rounding errors, might need to allow some tolerance in the left hand turn test.
  '''
  results = []
  inside = 0
  for s in poly:
          
          if s[0][1] == s[1][1]:
                  continue
          if s[1] < s[0]:
                  s = (s[1], s[0])
          if s[0][0] <= x and s[1][0] > x and segLibrary.isLeftTurn(s[0], s[1], (x,y))  <= 0:
                  inside += 1
  return inside % 2 != 0


def getRandomIntegerRegion( numRandomSegsToGenerate = 50, percentOfSegsToRemove = .05 ):
        '''

        The output of this function will have INTEGER coordinates.  This constraint greatly increases
        the computation time of this function.  In general, the non-integer version is much faster, 
        and is fine for most uses.

        generates a region from random segments.
        input:

          **numRandomSegsToGenerate**: the number of random segs to generate.  The actual region
               will have many fewer segs than this.  Higher numbers will typically generate more complex regions.
               The region will be constructed by intersecting the reandom segs, and finding a region
               among the resulting segs.
           
           **percentOfSegsToRemove**: Once random segments are generated and intersected such that all
               segments only intersect at endpoints, some segments will be removed at random.
               This parameter indicates the percentage of overall segs that will be removed. A 
               higher number typically causes regions to have less regular shapes.  Note that a high percentage
               may require a larger number of random segs to be generated.
        
        returns:
             
             **hsegs**:  an ordered list of half segments with valid labels.  
                 
                 A **half segment** is a tuple with the following:
                      ((x,y)(x,y), labelAbove, labelBelow)
                     
                     labels are integral values
                     
                     an interior label will be positive.  An exterior label will be -1.  The side of the hseg
                     on which the interior (exterior) of the region lies will have an interior (exterior) label.
                 
                 hsegs will be ordered in half segment order
                 
                 Each cycle in hsegs will have its own unique label number
        '''

        if numRandomSegsToGenerate == None:
                numRandomSegsToGenerate = 50
        if percentOfSegsToRemove == None:
                percentOfSegsToRemove = .05
        #random.seed()
        # got a bunch of random segs with integer endpoints     
        segs = segLibrary.createRandomSegs( numRandomSegsToGenerate )
        # find their intersections, but make sure endpoints are integers
        segLibrary.calcNonIntersectingSegsIntEndPoints(segs)
        #randomly remove some of the segs
        segs = segLibrary.removeRandSegs( segs, percentOfSegsToRemove )
        # create a region, favoring large (as in... containing lots of segments) cycles
        hsegs = hsegLibrary.extractAllLargeValidCycles( segs )
        return hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs )

def getRandomRegion( numRandomSegsToGenerate = 50,  minBound=0, maxBound=10000,  percentOfSegsToRemove = .05, **kwargs ):
        '''
        
        generates a region from random segments.
        input:

          **numRandomSegsToGenerate**: the number of random segs to generate.  The actual region
               will have many fewer segs than this.  Higher numbers will typically generate more complex regions.
               The region will be constructed by intersecting the reandom segs, and finding a region
               among the resulting segs.
           
           **percentOfSegsToRemove**: Once random segments are generated and intersected such that all
               segments only intersect at endpoints, some segments will be removed at random.
               This parameter indicates the percentage of overall segs that will be removed. A 
               higher number typically causes regions to have less regular shapes.  Note that a high percentage
               may require a larger number of random segs to be generated.
       

        if a rectangular bounding box is required,  use **keyword arguments** as follows:

        **minX**: the lowest value allowed as an X value to construct a point
        
        **minY**: the lowest value allowed as an Y value to construct a point
        
        **maxX**: the greatest value allowed as an X value to construct a point
        
        **maxY**: the greatest value allowed as an X value to construct a point

        returns:
             
             **hsegs**:  an ordered list of half segments with valid labels.  
                 
                 A **half segment** is a tuple with the following:
                      ((x,y)(x,y), labelAbove, labelBelow)
                     
                     labels are integral values
                     
                     an interior label will be positive.  An exterior label will be -1.  The side of the hseg
                     on which the interior (exterior) of the region lies will have an interior (exterior) label.
                 
                 hsegs will be ordered in half segment order
                 
                 Each cycle in hsegs will have its own unique label number
        '''

        aminX = minBound
        aminY = minBound
        amaxX = maxBound
        amaxY = maxBound
        for key, value in kwargs.items():
            if key == 'minX':
                aminX = value
            elif key == 'minY':
                aminY = value
            elif key == 'maxX':
                amaxX = value
            elif key == 'maxY':
                amaxY = value
            else: 
                print ('invalid argument to getRandomRegion: {0} = {1}'.format( key, value) )
                exit()

        #random.seed()
        # got a bunch of random segs with integer endpoints     
        segs = segLibrary.createRandomSegs( numRandomSegsToGenerate, minX=aminX, minY=aminY, maxX = amaxX, maxY = amaxY )
        # convert to floats
        segs = [((float(s[0][0]),float(s[0][1])), (float(s[1][0]), float(s[1][1])) ) for s in segs]
        newSegs = []
        for s in segs:
                if s[0] < s[1]:
                        newSegs.append( s )
                else:
                        newSegs.append( (s[1],s[0]) )
        segs = newSegs
        # find their intersections
        segs = grid.breakSegments( segs ) 
        #segs = segLibrary.calcNonIntersectingSegs(segs)
        #randomly remove some of the segs
        segs = segLibrary.removeRandSegs( segs, percentOfSegsToRemove )
        # create a region, favoring large (as in... containing lots of segments) cycles
        hsegs = hsegLibrary.extractAllLargeValidCycles( segs )
        return hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs )

def createRegionFromSegs( segs ):
        '''
        Constructs a well formed region from an input set line segments.  
        
        input:

        **segs**: a list of line segments in the format [((x1,y1),(x2,y2)),((x3,y3),(x4,y4)),...]
        Intersecting segments will be broken at intersection points.  If not cycle is present, no region
        will be returned.

        returns:
             
             **hsegs**:  an ordered list of half segments with valid labels.  
                 
                 A **half segment** is a tuple with the following:
                      ((x,y)(x,y), labelAbove, labelBelow)
                     
                     labels are integral values
                     
                     an interior label will be positive.  An exterior label will be -1.  The side of the hseg
                     on which the interior (exterior) of the region lies will have an interior (exterior) label.
                 
                 hsegs will be ordered in half segment order
                 
                 Each cycle in hsegs will have its own unique label number
        '''
        if segs == None or len(segs) == 0:
                return []
        segs = [((float(s[0][0]),float(s[0][1])), (float(s[1][0]), float(s[1][1])) ) for s in segs]
        newSegs = []
        for s in segs:
                if s[0] < s[1]:
                        newSegs.append( s )
                else:
                        newSegs.append( (s[1],s[0]) )
        segs = newSegs
        segs = grid.breakSegments( segs ) 
        #segs = segLibrary.calcNonIntersectingSegs( segs )
        hsegs = hsegLibrary.labelUniqueCycles( segs )
        return hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs )

def createRegionFavorLargeCyclesFromSegs( segs ):
        '''
        Behavior is similar to *createRegionFromSegs*, however, *createRegionFromSegs* will tend to return many
        smaller cycles if given input with many intersecting segments.  This function will tend to return fewer 
        larger cycles.  One side effect of this is that no two cycles will share an endpoint in the resulting 
        region returned from this function.  In other words, all cycles are disjoint, although cycles may be inside
        other cycles.
        '''
  
        if segs == None or len(segs) == 0:
                return []
        newSegs = [];
        for s in segs:
                if segLibrary.poiComp( s[0], s[1] ) == 1:
                        s = (s[1], s[0] )
                if( s[0] != s[1] ):
                        newSegs.append( s )
        segs = newSegs
        segs = grid.breakSegments( segs ) 
        #segs = segLibrary.calcNonIntersectingSegs( segs )
        return hsegLibrary.extractAllLargeValidCycles( segs )

def getOuterCycle( hsegs ):
        '''
        extracts the leftmost outer cycle from a region (the first one encountered in halfsegment order)

        input:

        **hsegs**:  a well formed region represented as a list of halfsegments.

        output:

        **hseg list**: a well formed region represented as a list of halfsegments.  The region will contain a single 
        cycle and no holes (i.e., a *simple* region).
        '''
        if hsegs == None or len(hsegs) == 0:
                return []
        return giveUniqueLabelToEachCycle( hsegs, True )

def giveUniqueLabelToEachCycle( hsegs, getOnlyOuterCycle = False ):
        ''' 
        takes an input region, and alters its interior labels such that each individual cycle
        in the region has its own unique interior label number. Cycles that share a point (cycles 
        that touch at a point) also have their own cycle numbers. If the second argument is true, only the 
        leftmost outer cycle will be returned

        input:

        **hsegs**: a well formed region as a list of halfsegments

        **getOnlyOuterCycle**: default value = False.  If set to True, will return only a single cycle; the leftmost outer cycle in the region

        output:

        **hseg list**: a well-formed region represented as a list of halfsegments.  Each minimal cycle will have a unique interior label number,
        '''
        if hsegs == None or len(hsegs) == 0:
                return []
        segs = [h[0] for h in hsegs if hsegLibrary.isLeft( h ) ]
        hsegs = hsegLibrary.labelUniqueCycles( segs, getOnlyOuterCycle )
        return hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs )

def createCountPartition( segList, laList, lbList ):
        '''

        **NOTE**.  The output of this function is automatically written to a file.  see the source code...


        Creates a spatial partition from a set of regions.  Each resulting segment will also have a label that
        indicates how many region interiors (from the original set of regions) lies above and below the segment.
        So, we essentially get a heat map of vector regions.  Each segment in a cycle in the resulting partition 
        will have the same interior label (for the interior of the cycle), since that cycle represents the area covered 
        by a fixed numeber of input regions.

        **ASSUMPTIONS**
        
        1. segList contains line segments representing a set of well-formed regions
        2. laList and lbList are parallel arrays with segList indicating the labels of their associated segment. 
        3. laList and lbList contain values of 1 and -1 (1 for interior, -1 for exterior)
        4. See the following paper for details: M. McKenney, B. Olsen, "Algorithms for Fundamental Spatial Aggregate Operations Over Regions," BIGSPATIAL at 21st ACM SIGSPATIAL International Symposium on Advances in Geographic Information Systems, November 2013, Orlando, FL, USA.

        input:
          
        **segList**: A list of line segments representing a SET of well formed regions.  To generate this set from a 2 hseg representations, you would extract the segs from each hseg list, and then concatenate them into a single list.

        **laList**: a list of label values.  The first value corresponds to the above label of the first segment in the seg list, the second corresponds to the second segment in the segList, etc. MUST HAVE A VALUE OF -1 (exterior)  or 1 (interior).

        **lbList**: Similar to laList, but representing the label (whether the interior or extior of the associated region) lies below the segment.  MUST HAVE A VALUE OF -1 (exterior)  or 1 (interior).
        '''

        if segList == None or laList == None or lbList == None or len( segList )== 0 or len( laList ) == 0 or len( lbList ) == 0 or len(segList) != len( laList ) or len( segList ) != len( lbList ) or len( laList) != len( lbList ):
                return [],[],[]
        sr,la,lb = segLibrary.calcNonIntersectingSegs( segList,  laList, lbList )
        

        # write the results to a file
        outfile = open( 'zcountIntermediateNon_Rob_Check.txt','w' )
        for i in range( len( sr ) ):
                seg = sr[i]
                s=struct.pack('>d', seg[0][0] )
                hexx1 = ''.join('%.2x' % ord(c) for c in s) # get hex vals from bin string s
                s=struct.pack('>d', seg[0][1])
                hexy1 = ''.join('%.2x' % ord(c) for c in s) # get hex vals from bin string s
                s=struct.pack('>d', seg[1][0])
                hexx2 = ''.join('%.2x' % ord(c) for c in s) # get hex vals from bin string s
                s=struct.pack('>d', seg[1][1])
                hexy2 = ''.join('%.2x' % ord(c) for c in s) # get hex vals from bin string s
    #output the line to the new file
                outfile.write( hexx1 + ' ' + hexy1 + ' '+  hexx2 + ' ' + hexy2+' ' + str(la[i]) +' '+str(lb[i])+ '\n')
        outfile.close()
        print zip( sr, la, lb)
        print 'done intersections'
        
        s,la,lb = segLibrary.countInteriors( sr, la, lb) 
        return s,la,lb

def union( hsegs1, hsegs2 ):
        ''' 
        Computes the union of two well formed regions.

        Assumes that hsegs1 and hsegs2 are valid regions, for instance, they have been created with def createRegionFromSegs.
        
        regions are assumed to have valid labelling.  This function will relabel them to compute the union
        
        input:

        **hsegs1**: a well formed and properly labeled region.

        **hsegs2**: a well formed and properly labeled region.

        output:

        an hseg list consisiting of the union of the input regions.

        '''
        if hsegs1 == None:
                hsegs1 = list()
        if hsegs2 == None:
                hsegs2 == list()
        if len( hsegs1 ) == 0:
                return hsegs2
        if len( hsegs2 ) == 0:
                return hsegs1
        if len(hsegs1) == 0 and len( hsegs2) == 0:
                return []
        # get the segs
        segs1 = [ h[0] for h in hsegs1 if hsegLibrary.isLeft( h ) ]
        segs2 = [ h[0] for h in hsegs2 if hsegLibrary.isLeft( h ) ]
        
        # get the bboxs
        s1maxx = max( [x[0] for y in segs1 for x in y] )
        s1minx = min( [x[0] for y in segs1 for x in y] )
        s1maxy = max( [x[1] for y in segs1 for x in y] )
        s1miny = min( [x[1] for y in segs1 for x in y] )
        s2maxx = max( [x[0] for y in segs2 for x in y] )
        s2minx = min( [x[0] for y in segs2 for x in y] )
        s2maxy = max( [x[1] for y in segs2 for x in y] )
        s2miny = min( [x[1] for y in segs2 for x in y] )
        # check for overlap in x AND y direction
        if not( (s1maxx >= s2maxx and s1minx >= s2maxx) or ( s1maxx <= s2minx and s1minx <= s2minx) or (s1maxy >= s2maxy and s1miny >= s2maxy) or ( s1maxy <= s2miny and s1miny <= s2miny)):
                # get the broken segs
                resultSegs1, resultSegs2 = segLibrary.segIntersection( segs1, segs2 )
        
                # get the regions
                hsegs1 = hsegLibrary.labelUniqueCycles( resultSegs1 )
                hsegs1 = hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs1 )
                hsegs2 = hsegLibrary.labelUniqueCycles( resultSegs2 )
                hsegs2 = hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs2 )
                # keep just the left hsegs
                hsegs1 = [h for h in hsegs1 if hsegLibrary.isLeft( h ) ]
                hsegs2 = [h for h in hsegs2 if hsegLibrary.isLeft( h ) ]
                # union will keep all hsegs out of the other or on with matching interabove
                s1, la1, lb1 = [ list(z) for z in zip(* hsegs1 )] 
                s2, la2, lb2 = [ list(z) for z in zip(* hsegs2 )] 

                # keep the ones out of the opposing region
                resultSet = set();
                resultSet |= segLibrary.keepOuterBoundary( s1, la1, lb1, s2, la2, lb2 )
                resultSet |= segLibrary.keepOuterBoundary(  s2, la2, lb2, s1, la1, lb1 )
                
                # make a region out of it
                resultList = list( resultSet )

                hsegs = hsegLibrary.labelUniqueCycles( resultList )
                return hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs )

        else:
                resultList = list()
                for s in segs1:
                        resultList.append( s );
                for s in segs2:
                        resultList.append( s )
                resultSet = set( resultList )
                resultList = list( resultSet ) 
                # create the region this code copied from createRegionFromsegs, minus the seg intersection function call
                
                hsegs = hsegLibrary.labelUniqueCycles( resultList )
                return hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs )


def difference( hsegs1, hsegs2 ):
        ''' 
        NON-symmetric difference.  for R1 and R2, 
        defined as R1 - (R1 \cap R2).
        
        Regions are asssumed to have valid labelling.
        this function will return a properly labeled region
      
        input:

        **hsegs1**: a well formed and properly labeled region.

        **hsegs2**: a well formed and properly labeled region.

        output:

        an hseg list consisiting of the difference of the input regions.
        '''


        if hsegs1 == None or len(hsegs1) == 0:
                return []
        if hsegs2 == None or len(hsegs2) == 0:
                return hsegs1
        # get the segs
        segs1 = [ h[0] for h in hsegs1 if hsegLibrary.isLeft( h ) ]
        segs2 = [ h[0] for h in hsegs2 if hsegLibrary.isLeft( h ) ]
        
        # get the bboxs
        s1maxx = max( [x[0] for y in segs1 for x in y] )
        s1minx = min( [x[0] for y in segs1 for x in y] )
        s1maxy = max( [x[1] for y in segs1 for x in y] )
        s1miny = min( [x[1] for y in segs1 for x in y] )
        s2maxx = max( [x[0] for y in segs2 for x in y] )
        s2minx = min( [x[0] for y in segs2 for x in y] )
        s2maxy = max( [x[1] for y in segs2 for x in y] )
        s2miny = min( [x[1] for y in segs2 for x in y] )
        # check for overlap in x AND y direction
        if not( (s1maxx >= s2maxx and s1minx >= s2maxx) or ( s1maxx <= s2minx and s1minx <= s2minx) or (s1maxy >= s2maxy and s1miny >= s2maxy) or ( s1maxy <= s2miny and s1miny <= s2miny)):
                # get the intersection
                hsegsInter = intersection( hsegs1, hsegs2 )
                if len( hsegsInter ) == 0:
                        return hsegs1
                
                # now do the difference
                # get the segs
                segs1 = [ h[0] for h in hsegs1 if hsegLibrary.isLeft( h ) ]
                segs2 = [ h[0] for h in hsegsInter if hsegLibrary.isLeft( h ) ]
                
                # get the broken segs
                resultSegs1, resultSegs2 = segLibrary.segIntersection( segs1, segs2 )
                        # get the regions
                hsegs1 = hsegLibrary.labelUniqueCycles( resultSegs1 )
                hsegs1 = hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs1 )
                hsegs2 = hsegLibrary.labelUniqueCycles( resultSegs2 )
                hsegs2 = hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs2 )
                # keep just the left hsegs
                hsegs1 = [h for h in hsegs1 if hsegLibrary.isLeft( h ) ]
                hsegs2 = [h for h in hsegs2 if hsegLibrary.isLeft( h ) ]

                # union will keep all hsegs out of the other or on with matching interabove
                s1, la1, lb1 = [ list(z) for z in zip(* hsegs1 )] 
                s2, la2, lb2 = [ list(z) for z in zip(* hsegs2 )] 

                # keep the ones out of the opposing region
                resultSet = set();
                resultSet |= segLibrary.keepOuterBoundary( s1, la1, lb1, s2, la2, lb2, False )
                resultSet |= segLibrary.keepInnerBoundary(  s2, la2, lb2, s1, la1, lb1, False )
                # make a region out of it
                resultList = list( resultSet )

                hsegs = hsegLibrary.labelUniqueCycles( resultList )
                return hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs )
        else:
                return hsegs1


def intersection( hsegs1, hsegs2 ):
        '''
        Assumes that hsegs1 and hsegs2 are valid regions, created with def createRegionFromSegs.
           
        regions are assumed to have valid labelling.  
        
        This function will relabel them to compute the intersction
        
        
        input:

        **hsegs1**: a well formed and properly labeled region.

        **hsegs2**: a well formed and properly labeled region.

        output:

        an hseg list consisiting of the intersection of the input regions.

        '''
        # check for empty input
        if hsegs2 == None or len(hsegs2) == 0:
                return list()
        if hsegs1 == None or len( hsegs1) == 0:
                return list()
        # get the segs
        segs1 = [ h[0] for h in hsegs1 if hsegLibrary.isLeft( h ) ]
        segs2 = [ h[0] for h in hsegs2 if hsegLibrary.isLeft( h ) ]
        # get the bboxs
        s1maxx = max( [x[0] for y in segs1 for x in y] )
        s1minx = min( [x[0] for y in segs1 for x in y] )
        s1maxy = max( [x[1] for y in segs1 for x in y] )
        s1miny = min( [x[1] for y in segs1 for x in y] )
        s2maxx = max( [x[0] for y in segs2 for x in y] )
        s2minx = min( [x[0] for y in segs2 for x in y] )
        s2maxy = max( [x[1] for y in segs2 for x in y] )
        s2miny = min( [x[1] for y in segs2 for x in y] )
        # check for overlap in x AND y direction
        if (s1maxx >= s2maxx and s1minx >= s2maxx) or ( s1maxx <= s2minx and s1minx <= s2minx) or (s1maxy >= s2maxy and s1miny >= s2maxy) or ( s1maxy <= s2miny and s1miny <= s2miny):
                return list()

        # get the broken segs
        resultSegs1, resultSegs2 = grid.overlayHalfsegmentInput( hsegs1, hsegs2)

        
        #f = open( 'zzztmpout1.txt','w')
        #resultSegs1.sort()
        #for s in resultSegs1:
        #    x = str( s[0][0][0] ) + ' ' + str( s[0][0][1] ) +  ' ' + str( s[0][1][0] ) + ' '+ str( s[0][1][1]) + ' ' +str( s[1] ) +' ' 
        #    if s[2]:
        #        x = x + '1' + '\n'
        #    else:
        #        x = x + '0' + '\n'
        #    f.write( x )
        #f.close()
        #f = open( 'zzztmpout2.txt','w')
        #resultSegs2.sort()
        #for s in resultSegs2:
        #    x = str( s[0][0][0] ) + ' ' + str( s[0][0][1] ) +  ' ' + str( s[0][1][0] ) + ' '+ str( s[0][1][1]) + ' ' +str( s[1] ) +' ' 
        #    if s[2]:
        #        x = x + '1' + '\n'
        #    else:
        #        x = x + '0' + '\n'
        #    f.write( x )
        #f.close()


        #resultSegs1, resultSegs2 = segLibrary.segIntersection( segs1, segs2 )
        finalResult = []
        # keep segs from r1 that are in r2
        for s in resultSegs1:
            if s[1] == 1 and not s[2]:
                finalResult.append( s[0] )
        # keep segs from r2 that are in r1
        for s in resultSegs2:
            if s[1] == 1 and not s[2]:
                finalResult.append( s[0] )
        #for s in finalResult:
        #    print s
        # keep ON segs if interioBelow flag is the same
        onSegsr1 = [s for s in resultSegs1 if s[2] ]
        onSegsr2 = [s for s in resultSegs2 if s[2] ]
        onList = list( set(onSegsr1) & set(onSegsr2) )
        #print 'onlist'
        for s in onList:
            #print s[0]
            finalResult.append( s[0] )
        print 'done final'
        #f = open( 'zzztmpout.txt','w')
        #finalResult.sort()
        #for s in finalResult:
        #    x = str( s[0][0] ) + ' ' + str( s[0][1] ) +  ' ' + str( s[1][0] ) + ' '+ str( s[1][1]) +'\n'
        #    f.write( x )
        #f.close()
        # build halfsegments
        hsegs = hsegLibrary.labelUniqueCycles( finalResult )
        hsegs = hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs )
        print 'done hsegs'
        return hsegs

        # get the regions
        hsegs1 = hsegLibrary.labelUniqueCycles( resultSegs1 )
        hsegs1 = hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs1 )
        hsegs2 = hsegLibrary.labelUniqueCycles( resultSegs2 )
        hsegs2 = hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs2 )
        # keep just the left hsegs
        hsegs1 = [h for h in hsegs1 if hsegLibrary.isLeft( h ) ]
        hsegs2 = [h for h in hsegs2 if hsegLibrary.isLeft( h ) ]

        # union will keep all hsegs out of the other or on with matching interabove
        s1, la1, lb1 = [ list(z) for z in zip(* hsegs1 )]
        s2, la2, lb2 = [ list(z) for z in zip(* hsegs2 )] 

        # keep the ones out of the opposing region
        resultSet = set();
        resultSet |= segLibrary.keepInnerBoundary( s1, la1, lb1, s2, la2, lb2 )
        resultSet |= segLibrary.keepInnerBoundary(  s2, la2, lb2, s1, la1, lb1 )

        # make a region out of it
        resultList = list( resultSet )

        hsegs = hsegLibrary.labelUniqueCycles( resultList )
        return hsegLibrary.switchLabelsForCorrectCycleLabelling( hsegs )




def writeRegionToFile( theRegion, theFileName ):
        '''
        Write the region to a file.
        
        file will be a text file.  Floating point rounding WILL happen in the float to text conversion.
        Only use this if floating point rounding is OK (for instance, for visualizing the region).

        The resulting file will have 1 halfsegment per line.  Both left and right halfsegments are written.  The file will have the following format:

        x1 y1 x2 y2 x3 y3 x4 y4 la lb
        ...
      
        input:
          
        **theRegion**: A list of halfsegments

        **theFilename**: the name of the file that will be written.

        '''
        theFileObject = open( theFileName, 'w')
        for h in theRegion:
                if hsegLibrary.isLeft( h )  or h[0][0] == h[0][1]:
                        s1 = str( h[0][0][0])+' '+str(h[0][0][1])+' '+str( h[0][1][0])+' '+str(h[0][1][1])+' '+ str(h[1])+' '+ str(h[2])  +' ' + '\n'
                        theFileObject.write( s1 )
        theFileObject.close()

def writeRegionToHexFile( theRegion, theFileName ):

        '''
        Write the region to a file in HEXADECIMAL FORMAT.  Meant to be a more portable file with a format
        that is easy to read and process in any programming language.  NOTE that endianness is NOT checked for!
        
        file will be a text file.  Floating point values are represented as hexadecimal, and thus, are represented 
        EXACTLY in floating point format.  Use this if you need the exact floating point values.

        The resulting file will have 1 halfsegment per line.  Both left and right halfsegments are written.  The file will have the following format (except each floating point number will be in hexadecimal format labels are just represented as text):

        x1 y1 x2 y2 x3 y3 x4 y4 la lb
        ...
      
        input:
          
        **theRegion**: A list of halfsegments

        **theFilename**: the name of the file that will be written.

        '''
        theFileObject = open( theFileName, 'w')
        for h in theRegion:
                if hsegLibrary.isLeft( h )  or h[0][0] == h[0][1]:
                        x1 = struct.pack('>d', h[0][0][0])
                        hexx1 = ''.join('%.2x' % ord(c) for c in x1)
                        y1 = struct.pack('>d', h[0][0][1])
                        hexy1 = ''.join('%.2x' % ord(c) for c in y1)
                        x2 = struct.pack('>d', h[0][1][0])
                        hexx2 = ''.join('%.2x' % ord(c) for c in x2)
                        y2 = struct.pack('>d', h[0][1][1])
                        hexy2 = ''.join('%.2x' % ord(c) for c in y2)
                        s1 = hexx1 + ' ' + hexy1 + ' ' + hexx2 + ' ' + hexy2 + ' ' + str(h[1]) + ' ' + str(h[2]) + ' ' + '\n'
                        theFileObject.write( s1 )
        theFileObject.close()
