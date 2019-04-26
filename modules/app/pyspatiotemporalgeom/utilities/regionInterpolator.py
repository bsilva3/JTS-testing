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




from pyspatiotemporalgeom.utilities import hsegLibrary
from pyspatiotemporalgeom.utilities import segLibrary
import math
import collections
from pyspatiotemporalgeom.utilities import convexHull
import pyspatiotemporalgeom.region as region
from pyspatiotemporalgeom.utilities import triangleLibrary


def prepRegionForInterpolation( hsegs ):
        '''
        This function is used to prepare regions for interpolation.
        
        It is expected that this function is only useful for the ``interpolateRegions()`` function.

        First, connected cycles in a region are identified (cycles that touch).  Then connected cycles are relabeled so the interior label is identical for each group of connected cycles.  Then vertical connector segments are added.  The point sequence of an outercycle walk is computed.  The convex hull of that sequence is computed. Finally, labels are assigned for concavity mappings.

        ASSUMPTIONS:
        
        1. ``hsegs`` is a valid region in hseg order returned from region.createRegionFromSegs() or any of the region creation functions.
        2. Each cycle in the region has its own unique label, and -1 for exterior labels.

        RETURNS teh following as a tuple:

        1. Returns the region with cycles labeled for interoplation
        2. Returns the convex hull points in CCW sequence
        3. Returns the cycle mapping.
        4. Returns list of connected cycles
        5. Returns a dict that maps a point to a list of cycles connected to that point
        '''
        # find which cycles are connected
        cycleConnectionMapList = hsegLibrary.getConnectedCycleMapping( hsegs )

        # relabel touching cycles to label of the cycle that comes first in hseg order
        hsegs = hsegLibrary.relabelTouchingCyclesToFirstCycleNum( hsegs, cycleConnectionMapList )
        # add halfsegments such that every cycle is connected to some an enclosing cycle, or 
        # adjacent cycle.  After this step, cycles will form a connected graph
        hsegs = hsegLibrary.addVerticalConnectorsPS( hsegs, len( cycleConnectionMapList )-1 )

        # get points in CCW order around outer cycle of region
        poiList = hsegLibrary.getOuterWalkPointSequence( hsegs )
        # compute the convex hull of the region
        hull = convexHull.getHullFromSequence( poiList )
        # assign labels to cycles and connectors to reflect concavities
        hsegs = hsegLibrary.assignCycleLabelsForConcavityMapping( hsegs )
        # get mappings of connected cycles
        mapping, hsegs, connCycleLists, poiToCycLabelDict = hsegLibrary.getConnectedCycleMappingConcav( hsegs )

        return hsegs, hull, mapping, connCycleLists, poiToCycLabelDict



def angleFromVertical( seg ):
        '''
        A utility to compute the angle a segment forms with a vertical line emanating downwards from the least end point of the segment.

        Input: A line segment ((x1,y1),(x2,y2))

        Returns: an angle in degrees

        '''
        PI = math.pi
        p = seg[0]
        q = seg[1]
        px = p[0]
        py = p[1]
        qx = q[0]
        qy = q[1]

        # check if angle is 0, 360, or 180
        if px == qx:
                if py > qy:
                        return 0
        
                else:
                        return 180
        #check if angle is 90 or 270
        if py == qy:
                if px < qx:
                        return 90
                else:
                        return 270
        #translate points to origin
        qx = qx-px
        qy = qy-py
        # get angle from x axis
        angle = math.atan2( qx, qy) *(180/PI)
        
        if qx < 0:
                angle *= -1
                angle += 90
        elif qy < 0:
                angle = 180 - angle + 270
        else:
                angle = 90-angle
        #shift the angle to orient from the vertical
        angle += 90
        if angle > 360:
                angle = angle - 360
        return angle

def writeTrisToFile( triTup, fileName ):
        '''
        Write triangles to a file.

        This was used during debugging.

        expects an iterable containing iterables ( a list of lists).
        
        Each iterable contained in the first contains triangles.  
        
        A trianlge is a 3 tuple of points (p0, p1, p2) == ( (x0,y0,z0), (x1,y1,z1), (x2,y2,z2) ) or 3d points
        
        A point is a 3 tuple.  
        
        Input: 

        triTup = (listofTris1, listofTris2,...) 
        
        where listofTrisX = [t1, t2, t3,...]
        
        where tX = (p1,p2,p3) 
        
        where pX=(x0, y0, z0,)
        
        Prints the contents to a file named fileName.  will clobber that file
        '''
        f = open( fileName, 'w')
        for triList in triTup:
                if triList != None:
                        for t in triList:
                                s1 = str(t[0][0])+' '+ str(t[0][1])+' '+ str(t[0][2])+' '+ str(t[1][0])+' '+ str(t[1][1])+' '+ str(t[1][2]) + '\n'
                                s2 = str(t[0][0])+' '+ str(t[0][1])+' '+ str(t[0][2])+' '+ str(t[2][0])+' '+ str(t[2][1])+' '+ str(t[2][2]) + '\n'
                                s3 = str(t[2][0])+' '+ str(t[2][1])+' '+ str(t[2][2])+' '+ str(t[1][0])+' '+ str(t[1][1])+' '+ str(t[1][2]) + '\n'
                                f.write( s1 )
                                f.write( s2 )
                                f.write( s3 )
                        f.write( '\n')
        f.close()


def appendToAnimationFile( triList, fileObject, numFrames = 100 ):
        '''
        For an triangle list defining a moving region over a single time interval (for instance, one element of the tuple returned by ``interpolateRegions()``), write snapshots of that region as it moves over the time interval.  In essence, create files that show an animation of the moving region. 

        Input --

        triList: A list of triangles in the usual format: ``( (x0,y0,z0), (x1,y1,z1), (x2,y2,z2) )``

        fileObject: An open file object that the snapshot will be written to.

        numFrames: The number of snapshots to generate (the number of frames in thr resulting animation if one were to create a movie out of them).
        '''
        if triList == None:
                return
        if not isinstance(triList, collections.Iterable) or numFrames < 1:
                raise Exception( 'triList must be iterable and numFrames > 0')
        numer  = 0.0
        denom = numFrames
        for i in range( numFrames+1 ):
                multiplier = numer/denom
                for t in triList:
                        # get the segs representing endpoint movement
                        s1 = (t[2], t[0])
                        s2 = (t[2], t[1])
                        if t[0][2] < t[2][2]:  #make sure lower z value is 1st in the seg
                                s1 = (t[0], t[2])
                                s2 = (t[1], t[2])
                        if i == 0 and t[3]: # check if its a boundary print
                                x1,y1,z1 = s1[0]
                                x2,y2,z2 = s2[0]
                                fileObject.write( str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+'\n') 
                        elif i == numFrames and t[3]:
                                x1,y1,z1 = s1[1]
                                x2,y2,z2 = s2[1]
                                fileObject.write( str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+'\n') 
                        elif i > 0  and i < numFrames:
                                x1 = ((s1[1][0]-s1[0][0])*multiplier)+s1[0][0]
                                y1 = ((s1[1][1]-s1[0][1])*multiplier)+s1[0][1]
                                #z1 = ((s1[1][2]-s1[0][2])*multiplier)+s1[0][2]
                                x2 = ((s2[1][0]-s2[0][0])*multiplier)+s2[0][0]
                                y2 = ((s2[1][1]-s2[0][1])*multiplier)+s2[0][1]
                                #z2 = ((s2[1][2]-s2[0][2])*multiplier)+s2[0][2]
                                fileObject.write( str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+'\n') 
                numer+=1
                fileObject.write('\n')
        
        
        
def writeHsegsToTextFile( fileName, hsegs ):
        '''
        Used in debugging.  Open a file named *filename* and clobber it if it exists.  Then write all the halfsegments in the list ``hsegs`` to that file.  1 hseg per line, each point and label seperated by a space.
        '''

        f = open( fileName, 'w' )
        for h in hsegs:
                if hsegLibrary.isLeft( h ):
                        outStr = str(h[0][0][0]) +' ' +str(h[0][0][1]) +' ' +str(h[0][1][0]) +' ' +str(h[0][1][1]) +' ' +str(h[1]) +' ' +str(h[2]) +'\n'
                        f.write( outStr )
        f.close()
def writeSegsToTextFile( fileName, segs ):
        f = open( fileName, 'w' )
        for h in segs:
                outStr = str(h[0][0]) +' ' +str(h[0][1]) +' ' +str(h[1][0]) +' ' +str(h[1][1]) +' 1 1\n'
                f.write( outStr )
        f.close()

def interpolate(r1,r2, startTime, endTime, noTriIntersectionChecks = False ):
        '''
        This is where the magic happens.  Create an interpolation between two well-formed regions over a time interval (defined by ``startTime`` and ``endTime``) such that at every instant within that time interval, the region resulting from the interpolation at that instant conforms to the type definition of complex regions as defined in [1].  Note that the various region generators and region creation functions int he region.py file create well formed regions according to [1].  In otherwords, the moving region resulting from this function conforms to the type definition of moving regions in [2].

        This function is an extension of the algorithm in [3] to handle both simple (1 simple cycle with no holes) regions and complex regions.

        
        [1] Markus Schneider and Thomas Behr. 2006. Topological relationships between complex spatial objects. ACM Trans. Database Syst. 31, 1 (March 2006), 39-81. DOI=10.1145/1132863.1132865 http://doi.acm.org/10.1145/1132863.1132865

        [2] Ralf Hartmut Guting, Michael H. Bohlen, Martin Erwig, Christian S. Jensen, Nikos A. Lorentzos, Markus Schneider, and Michalis Vazirgiannis. 2000. A foundation for representing and querying moving objects. ACM Trans. Database Syst. 25, 1 (March 2000), 1-42. DOI=10.1145/352958.352963 http://doi.acm.org/10.1145/352958.352963

        [3] Mark McKenney and James Webb. 2010. Extracting moving regions from spatial data. In Proceedings of the 18th SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS '10). ACM, New York, NY, USA, 438-441. DOI=10.1145/1869790.1869856 http://doi.acm.org/10.1145/1869790.1869856

        Input:
          
        1. r1, r2: two well formed regions represented as lists of hlafsegments.  Any of the region creation functions in region.py will do.
        2. startTime, endTime:  two numbers defining a time interval.  These numbers are used as the 3D dimension when extrapolating into 3D space.
        3. noTriIntersectionChecks. See paper [3].  The algorithm first creates an interpolation between the input regions.  It is possible that the interpolation will result in a self-intersecting region at some point.  The triangle/triangle intersection test is then performed.  This test is very computationally intensive (especially for python) and can take a LONG time to compute.  If you pass a ``True`` for this argument, the tri/tri intersection test is skipped, and the interpolation returned AS-IS (possibly with self-intersections).  This makes the algorithm :math:`O(n \lg n)` instead of :math:`O(n^2)`.

        Output:

        A 3-tuple.  See [3].  The algorithm will create at MOST, 3 interval regions to describe the interpolation of r1 to r2 over the defined time interval.  Not all 3 interval regions are always required, so 1 or 2 of the values in the tuple may be ``None``, but a 3 tuple is ALWAYS returned.  If the ``noTriIntersectionChecks`` argument is set to ``True``, or the original interpolation succeeds, then the return value will look like this: ``(None, triList, None)``.

        Any non-``None`` value in the return tuple will be a list of trinagles describing the movinement of line segments in r1 as they travel across the defined interval to r2 (between intermediate states of r1 and r2 if necessary).
        
        '''
        r1, r1Hull, r1LabelMapping, r1ConnCycLists, r1PoiToCycLabelDict  = prepRegionForInterpolation( r1 )
        r2, r2Hull, r2LabelMapping, r2ConnCycLists, r2PoiToCycLabelDict  = prepRegionForInterpolation( r2 )
        
        r1ConnectorSegSet = set( [h[0] for h in r1 if h[1] == -h[2] and( h[1] == 2 or h[2] == 2 or h[1]==1 or h[2]==1)  ] )
        r2ConnectorSegSet = set( [h[0] for h in r2 if h[1] == -h[2] and( h[1] == 2 or h[2] == 2 or h[1]==1 or h[2]==1) ] )
        
        r1HullTris, r2HullTris, r1ConcTris, r1ConcHullSeg, r2ConcTris, r2ConcHullSeg = createMotionPlan( r1, r1Hull, r1ConnCycLists, r1PoiToCycLabelDict, r2, r2Hull, r2ConnCycLists, r2PoiToCycLabelDict, startTime, endTime)
        
        printList = [r1HullTris+r2HullTris]
        printList.append( [t for clist in r1ConcTris for t in clist] )
        printList.append(  [t for clist in r2ConcTris for t in clist] )
        # DEBUG -- uncomment the following
        #writeTrisToFile( printList, 'debug_tri3d_initial.txt')
        
        if noTriIntersectionChecks:
                # create the return list
                triList = r1HullTris+r2HullTris
                triList.extend( [t for clist in r1ConcTris for t in clist] )
                triList.extend( [t for clist in r2ConcTris for t in clist] )
                return( None, triList, None )           
        
        # check for tri tri intersections
        # can do this in parallel
        # need to check hull tris against all concavity tris
        # Not a true statement::: a tri from a hull to a hull will never intersect a concavity tri
        intersectingConcs = []
        for t in r1HullTris:
                for i,tList in enumerate( r1ConcTris ):
                        for c in tList:
                                if triangleLibrary.triangle3DTriangle3DIntersection( t,c ):
                                        intersectingConcs.append( ((i,1), (i,1) ) )
                                        break
                
        for t in r2HullTris:
                for i,tList in enumerate( r2ConcTris ):
                        for c in tList:
                                if triangleLibrary.triangle3DTriangle3DIntersection( t,c ):
                                        intersectingConcs.append( ((i,2), (i,2) ) )
                                        break
                                        
        # need to check concavity tris against each other
        # make lists of all concavity tris, and their concav ID
        c1AllConcTris = [ (c,i,1) for i,cList in enumerate( r1ConcTris ) for c in cList]
        c2AllConcTris = [ (c,i,2) for i,cList in enumerate( r2ConcTris ) for c in cList]
        c1AllConcTris = c1AllConcTris+ c2AllConcTris 

        for i in range( len(c1AllConcTris)-1):
                for j in range( i+1, len( c1AllConcTris ) ):
                        c1 = c1AllConcTris[i]
                        c2 = c1AllConcTris[j]
                        if triangleLibrary.triangle3DTriangle3DIntersection( c1[0], c2[0] ):
                                intersectingConcs.append( ((c1[1],c1[2]), (c2[1],c2[2]) ) )
        
#               evapConcs = set(r1ConcsThatIntersectWithHullTris)
#               condenseConcs = set(r2ConcsThatIntersectWithHullTris)
        evapConcs = set()
        condenseConcs =set()
        # remove duplicate mappings.  a mapping will be ordered first by sliceID 1 or 2, and then by concID
        for i,cmap in enumerate( intersectingConcs ):
                #intersecting conc map s a tuple with ((concID, sliceID), (concID, sliceID))
                if cmap[1][1] < cmap[0][1] or (cmap[1][1] == cmap[0][1] and cmap[1][0] < cmap[0][0]):
                        intersectingConcs[i] = (cmap[1], cmap[0])
        intersectingConcsSet = set()
        for cmap in intersectingConcs:
                intersectingConcsSet |= set([cmap])

        # now put concs in the appropriate set.  We only need to get rid of 1 conc if there is an intersection
        # if a conc is already in a evap or condense set, we don't need to do anything else.
        # otherwise, use the first concID in the tuple.  It will favor slice 1 and lower conc IDs
        for cmap in intersectingConcsSet:
                if cmap[0][1] == 1 and cmap[0][0] in evapConcs: continue
                elif cmap[1][1] == 1 and cmap[1][0] in evapConcs: continue
                elif cmap[0][1] == 2 and cmap[0][0] in condenseConcs: continue
                elif cmap[1][1] == 2 and cmap[1][0] in condenseConcs: continue
                elif cmap[0][1] == 1: evapConcs |= set([cmap[0][0]])
                else: condenseConcs |= set([cmap[0][0]])
                        
        
        # split times indicate the time boundaries for evapping and condensing steps
        # make changes to them here for more dynamic time interval time splitting mechanisms
        # right now its just a static split.  
        splitTime1 = 1.2 * startTime
        splitTime2 = 0.8 * endTime
        # create triangles for offending concs.  append the hull seg to the tri, make a region out of it, triangulate it
        #evap tris are planar in the original region.  We will need to find a point int he dest region and make 
        # 1 motion tri to it for each edge of a evapTri
        evapTris = []
        evapMotionSegs = []
        for i in evapConcs:
                # get the conc segs
                concSegs = [((ct[0][0], ct[0][1]), (ct[1][0],ct[1][1])) for ct in r1ConcTris[i]]
                # conc segs need to move in place for condense step
                for s in concSegs: # create in place movement for conc boundaries
                        if s not in r1ConnectorSegSet:  # do not put it in
                                evapMotionSegs.append( (s[0]+(splitTime1,), s[1]+(splitTime1,), s[0]+(startTime,), False) )
                                evapMotionSegs.append( (s[0]+(startTime,), s[1]+(startTime,), s[1]+(splitTime1,), True) )
                if r1ConcHullSeg[i] != None:
                        concSegs.append( r1ConcHullSeg[i] )
                # triangulate it
                hsegs = region.createRegionFromSegs( concSegs )
                # DEBUG -- uncomment the following 2 lines
                #writeHsegsToTextFile( 'debug_tri_hsegs_evap'+str(i)+'.txt', hsegs )
                #writeSegsToTextFile( 'debug_tri_segs_evap'+str(i)+'.txt', concSegs )
                theTris =  hsegLibrary.triangulate( hsegs )
                theTris = [ t+(i,) for t in theTris ]
                evapTris.extend( theTris )
        
        # create mappings.  triangles map to points in thier interior Always map from point to seg
        # use midpoint of one tri boundary, then midpoint of that to the other tri point
        # So... point is always in the lower time, seg in the upper time
        for t in evapTris:
                midX = (t[0][0]+t[1][0])/2.0
                midY = (t[0][1]+t[1][1])/2.0
                midX = (midX + t[2][0]) /2.0
                midY = (midY + t[2][1]) /2.0
                p = (midX, midY)
                validAtBoundary =  (r1ConcHullSeg[t[3]]!= None and segLibrary.isCollinearAndOverlapping( (t[0], t[1]), r1ConcHullSeg[t[3]] )) or (t[0],t[1]) in r1ConnectorSegSet or (t[1],t[0]) in r1ConnectorSegSet
                evapMotionSegs.append( (t[0]+(splitTime1,), t[1]+(splitTime1,), p+(startTime,), validAtBoundary) )
                validAtBoundary =  (r1ConcHullSeg[t[3]]!= None and segLibrary.isCollinearAndOverlapping( (t[0], t[2]), r1ConcHullSeg[t[3]] )) or (t[0],t[2]) in r1ConnectorSegSet or (t[2],t[0]) in r1ConnectorSegSet
                evapMotionSegs.append( (t[0]+(splitTime1,), t[2]+(splitTime1,), p+(startTime,), validAtBoundary) )
                validAtBoundary =  (r1ConcHullSeg[t[3]]!= None and segLibrary.isCollinearAndOverlapping( (t[1], t[2]), r1ConcHullSeg[t[3]] )) or (t[1],t[2]) in r1ConnectorSegSet or (t[2],t[1]) in r1ConnectorSegSet
                evapMotionSegs.append( (t[1]+(splitTime1,), t[2]+(splitTime1,), p+(startTime,), validAtBoundary) )
        
        # repeat for condense segs
        condTris = []
        condMotionSegs = []
        for i in condenseConcs:
                # get the conc segs
                concSegs = [((ct[0][0], ct[0][1]), (ct[1][0],ct[1][1])) for ct in r2ConcTris[i]]
                # conc segs need to move in place for condense step
                for s in concSegs: # create in place movement for conc boundaries
                        if s not in r2ConnectorSegSet:  # do not put it in
                                condMotionSegs.append( (s[0]+(splitTime2,), s[1]+(splitTime2,), s[0]+(endTime,), False) )
                                condMotionSegs.append( (s[0]+(endTime,), s[1]+(endTime,), s[1]+(splitTime2,), True) )
                if r2ConcHullSeg[i] != None:
                        concSegs.append( r2ConcHullSeg[i] )
                # triangulate it
                hsegs = region.createRegionFromSegs( concSegs )
                # DEBUG -- uncomment the following 2 line
                #writeHsegsToTextFile( 'debug_tri_hsegs_cond'+str(i)+'.txt', hsegs )
                #writeSegsToTextFile( 'debug_tri_segs_cond'+str(i)+'.txt', concSegs )
                theTris = hsegLibrary.triangulate( hsegs )
                theTris = [ t+(i,) for t in theTris ]
                condTris.extend( theTris )

        # create mappings from interior points.  
        for t in condTris:
                midX = (t[0][0]+t[1][0])/2.0
                midY = (t[0][1]+t[1][1])/2.0
                midX = (midX + t[2][0]) /2.0
                midY = (midY + t[2][1]) /2.0
                p = (midX, midY)
                validAtBoundary = (r2ConcHullSeg[t[3]]!= None and segLibrary.isCollinearAndOverlapping( (t[0], t[1]), r2ConcHullSeg[t[3]] )) or (t[0],t[1]) in r2ConnectorSegSet or (t[1],t[0]) in r2ConnectorSegSet
                condMotionSegs.append( (t[0]+(splitTime2,), t[1]+(splitTime2,), p+(endTime,), validAtBoundary) )
                validAtBoundary =  (r2ConcHullSeg[t[3]]!= None and segLibrary.isCollinearAndOverlapping( (t[0], t[2]), r2ConcHullSeg[t[3]] )) or (t[0],t[2]) in r2ConnectorSegSet or (t[2],t[0]) in r2ConnectorSegSet
                condMotionSegs.append( (t[0]+(splitTime2,), t[2]+(splitTime2,), p+(endTime,), validAtBoundary) )
                validAtBoundary =  (r2ConcHullSeg[t[3]]!= None and segLibrary.isCollinearAndOverlapping( (t[1], t[2]), r2ConcHullSeg[t[3]] )) or (t[1],t[2]) in r2ConnectorSegSet or (t[2],t[1]) in r2ConnectorSegSet
                condMotionSegs.append( (t[1]+(splitTime2,), t[2]+(splitTime2,), p+(endTime,), validAtBoundary) )
        
        # create intermediate regions.  remove segs from offending concs, add in the hullseg
        # create evap intermediate region.  Map segs to themselves except for segs in evap concs
        allInterval1Tris = None
        if len( evapMotionSegs ) > 0: # we need to add the evap step
                # all segs map to themselves, except for the evap segs, which already have motion tris
                interval1Tris = []
                for t in r1HullTris:
                        interval1Tris.append( (t[0], t[1], (t[0][0], t[0][1], splitTime1) ) )
                        interval1Tris.append( ( (t[0][0],t[0][1], splitTime1), (t[1][0], t[1][1], splitTime1), t[1] ) )
                for i,cList in enumerate( r1ConcTris ):
                        if i not in evapConcs:
                                for t in cList:
                                        if  ( (t[0][0],t[0][1]), (t[1][0], t[1][1])) not in r1ConnectorSegSet: # dont put it in
                                                interval1Tris.append( (t[0], t[1], (t[0][0], t[0][1], splitTime1)) )
                                                interval1Tris.append( ( (t[0][0],t[0][1], splitTime1), (t[1][0], t[1][1], splitTime1), t[1] ) )
                allInterval1Tris = interval1Tris + evapMotionSegs
        else:
                splitTime1 = startTime
        # repeat for condense concs
        allInterval3Tris = None
        if len( condMotionSegs ) > 0:
                interval3Tris = []
                for t in r2HullTris:
                        interval3Tris.append( (t[0], t[1], (t[0][0], t[0][1], splitTime2)) )
                        interval3Tris.append( ( (t[0][0],t[0][1], splitTime2), (t[1][0], t[1][1], splitTime2), t[1] ) )
                for i,cList in enumerate( r2ConcTris ):
                        if i not in condenseConcs:
                                for t in cList:
                                        if  ( (t[0][0],t[0][1]), (t[1][0], t[1][1])) not in r2ConnectorSegSet: # dont put it in
                                                interval3Tris.append( (t[0], t[1], (t[0][0], t[0][1], splitTime2)) )
                                                interval3Tris.append( ( (t[0][0],t[0][1], splitTime2), (t[1][0], t[1][1], splitTime2), t[1] ) )
                allInterval3Tris = interval3Tris + condMotionSegs
        else:
                splitTime2 = endTime
        # finally creat the mid interval.  add all r1 hull tris and r2 hull tris, with the updated time stamps
        # add all conc tris with updated time stamps that are not in either of the condense or evap sets
        # add hull segs for conc tris that are in the evap and condense sets, and map them to whatever point the concavity had mapped to
        allInterval2Tris = None
        if allInterval1Tris == None and allInterval3Tris == None:
                # just return the original mapping
                allInterval2Tris = r1HullTris + r2HullTris
                for cList in r1ConcTris:
                        allInterval2Tris.extend( cList )
                for cList in r2ConcTris:
                        allInterval2Tris.extend( cList )
        
        else:
                #add hull tris
                r1HullTris = [( (t[0][0],t[0][1], splitTime1),(t[1][0],t[1][1], splitTime1), (t[2][0],t[2][1], splitTime2))  for t in r1HullTris]
                r2HullTris = [( (t[0][0],t[0][1], splitTime2),(t[1][0],t[1][1], splitTime2), (t[2][0],t[2][1], splitTime1))  for t in r2HullTris]
                allInterval2Tris = r1HullTris + r2HullTris
                # add non evapped or condensed conc tris
                for i,cList in enumerate( r1ConcTris ):
                        if i not in evapConcs:
                                for t in cList:
                                        allInterval2Tris.append( ((t[0][0],t[0][1], splitTime1),(t[1][0],t[1][1], splitTime1), (t[2][0],t[2][1], splitTime2)) )
                for i,cList in enumerate( r2ConcTris ):
                        if i not in condenseConcs:
                                for t in cList:
                                        allInterval2Tris.append( ((t[0][0],t[0][1], splitTime2),(t[1][0],t[1][1], splitTime2), (t[2][0],t[2][1], splitTime1)) )
                # add hull tris for the evapped/ condensed concs
                for i in evapConcs:
                        h = r1ConcHullSeg[i]
                        if h != None:   # will be none if it is a hole /nestedhole/cyc configuration that attaches
                                mapPoi = r1ConcTris[i][0][2] # conclist, tri, map-to point
                                mapPoi = ( mapPoi[0], mapPoi[1], splitTime2 )
                                allInterval2Tris.append( ((h[0][0],h[0][1], splitTime1),(h[1][0],h[1][1], splitTime1), mapPoi) )
                for i in condenseConcs:
                        h = r2ConcHullSeg[i]
                        if h != None:  # will be none if it is a hole /nestedhole/cyc configuration that attaches
                                mapPoi = r2ConcTris[i][0][2] # conclist, tri, map-to point
                                mapPoi = ( mapPoi[0], mapPoi[1], splitTime1 )
                                allInterval2Tris.append( ((h[0][0],h[0][1], splitTime2),(h[1][0],h[1][1], splitTime2), mapPoi) )
        
        # now test for boundary existence.  A segment only shows up on a boundary if it appears exactly once 
        allInterval1Tris = checkBoundaryExistence( allInterval1Tris )
        allInterval2Tris = checkBoundaryExistence( allInterval2Tris )
        allInterval3Tris = checkBoundaryExistence( allInterval3Tris )
        #Finished!
        return (allInterval1Tris, allInterval2Tris, allInterval3Tris )


def checkBoundaryExistence( tris ):
        ''' Becuase of the way the interpolation algorithm works, some segments do not actually exist at the temporal extrema of the interval.  This function appends a boolean to each triangle indicating if the segment portion of the trinagle should be printed (exists) at the temporal extrema of the interval.
        '''

        # only include segs in the boundary if they occur exactly once
        # otherwise its triangles converging on each other.  Tris converging on hull
        # segs have already been removed
        if tris == None:
                return None
        #resTris = []
        #for t in tris:
        #       if len(t) == 3:
        #               resTris.append( (t[0], t[1], t[2], True) )
        #       else:
        #               resTris.append( t )
        #return resTris
        seenSet = set()
        seenTwiceSet = set()            
        for t in tris:
                # get the seg portion, make sure first point is less than second
                if len( t) == 4 and t[3] == False:
                        continue
                s = (t[0], t[1])
                if not( s[0][0] < s[1][0] or ( s[0][0] == s[1][0] and s[0][1] < s[1][1] )):
                        s = (t[1], t[0])
                if s not in seenSet:
                        seenSet |= set([s])
                else:
                        seenTwiceSet |= set([s])
        resTris = []
        #triangle whose seg is not in seenTwiceSet exist at boundary, otherwise it does not
        for t in tris:
                # get the seg portion, make sure first point is less than second
                s = (t[0], t[1])
                if not( s[0][0] < s[1][0] or ( s[0][0] == s[1][0] and s[0][1] < s[1][1] )):
                        s = (t[1], t[0])
                if s in seenTwiceSet:
                        # does not exist at boundary
                        resTris.append( (t[0], t[1], t[2], False) )
                else:
                        val = True
                        if len( t ) == 4:
                                val = t[3]
                        resTris.append( (t[0], t[1], t[2], val) )
        
        return resTris
                

def createMotionPlan( r1, r1Hull, r1ConCycles, r1PoiToCycLabelDict, r2, r2Hull, r2ConCycles, r2PoiToCycLabelDict, startTime, endTime ):
        '''
        Used in the interpolateRegions function to actuallt create trinagles.
        
        create motion triangles from r1 to r2.  start time must be earlier than end time.
        r1 must be the earlier (source) region, r2 the later (destination) region
        
        walk the outer cycles (cycles with a 2 label from the prep functions above) and convex hulls concurrently
        any concavities map to a single point on the opposing region.  Any cycles are treated as concavities.
        connectors other than connectors with a 2,-2 label will disappear...poof
        '''
        index1 = 0
        index2 = 0
        hullIndex1 = 0
        hullIndex2 = 0
        #last seg will be largest around first dom point
        lastIndex1 = 0
        lastIndex2 = 0
        while r1[lastIndex1+1][0][0] == r1Hull[0]: lastIndex1+=1
        while r2[lastIndex2+1][0][0] == r2Hull[0]: lastIndex2+=1                
        # create a hash table for the seg portions mapped to their index
        r1IndexLookup = dict()
        for i, h in enumerate( r1 ):
                r1IndexLookup[h[0]] = i
        # create a hash table for the seg portions mapped to their index
        r2IndexLookup = dict()
        for i, h in enumerate( r2 ):
                r2IndexLookup[h[0]] = i
        # classes to hold the resulting tris
        r1HullTris = []
        r2HullTris = []
        r1ConcTris = []
        r2ConcTris = []
        r1ConcHullSeg = []
        r2ConcHullSeg = []
        
        # whichever region has advanced a hull seg will have an entire seg in the mapping.  start off assuming that is r1
        mapR1Seg = True
        # put the start hull poi at the end so we don't have to do a bunch of if statements to wrap around
        r1Hull.append( r1Hull[0] )
        r2Hull.append( r2Hull[0] )
        #r1HullSeg = r1Hull[hullIndex1], r1Hull[hullIndex1+1]
        #r2HullSeg = r2Hull[hullIndex2], r2Hull[hullIndex2+1]
        #r1CurrSeg = r1[index1][0]
        #r2CurrSeg = r2[index2][0]
        #walk'em
        while True:
                if mapR1Seg:
                        # we will map the seg or concavity chain starting at the current hull poi.  go ahead and update the hull index
                        hullIndex1 += 1
                        # if the seg is a hull seg, just map it p from the r2 seg
                        if  r1[index1][0][1] == r1Hull[ hullIndex1 ]: 
                                r1HullTris.append(  (r1[index1][0][0]+(startTime,), r1[index1][0][1]+(startTime,), r2Hull[hullIndex2]+(endTime,) ) )
                                if r1[index1][0][0] in r1PoiToCycLabelDict:
                                        r1ConcTris.append( [] )
                                        currListIndex = len(r1ConcTris)-1
                                        r1ConcHullSeg.append( None ) # no closing Hull hseg, all interior cycles 
                                        cycNumList = r1PoiToCycLabelDict.pop( r1[index1][0][0] )
                                        for cycID in cycNumList:
                                                for h in r1ConCycles[cycID]:
                                                        if hsegLibrary.isLeft( h ):
                                                                r1ConcTris[currListIndex].append(  (h[0][0]+(startTime,), h[0][1]+(startTime,), r2Hull[hullIndex2]+(endTime,) ) )
                                index1 = hsegLibrary.getNextOuterCycleWalkIndex( r1[index1], r1, r1IndexLookup )
                        else:
                                #we are on an r1 concavity.  map until we get to the next hull poi
                                r1ConcTris.append( [] )
                                currListIndex = len(r1ConcTris)-1
                                r1ConcHullSeg.append( (r1Hull[hullIndex1-1], r1Hull[hullIndex1]) )
                                while r1[index1][0][0] != r1Hull[ hullIndex1 ]:
                                        r1ConcTris[currListIndex].append( (r1[index1][0][0]+(startTime,), r1[index1][0][1]+(startTime,), r2Hull[hullIndex2]+(endTime,) ) )
                                        #Insert connected structures that touch here too
                                        if r1[index1][0][0] in r1PoiToCycLabelDict:
                                                cycNumList = r1PoiToCycLabelDict.pop( r1[index1][0][0] )
                                                for cycID in cycNumList:
                                                        for h in r1ConCycles[cycID]:
                                                                if hsegLibrary.isLeft( h ):
                                                                        r1ConcTris[currListIndex].append( (h[0][0]+(startTime,), h[0][1]+(startTime,), r2Hull[hullIndex2]+(endTime,) ) )
                                        index1 = hsegLibrary.getNextOuterCycleWalkIndex( r1[index1], r1, r1IndexLookup )
                else:   #we are mapping an R2 seg.  Do the same as above, but map to r2
                        # we will map the seg or concavity chain starting at the current hull poi.  go ahead and update the hull index
                        hullIndex2 += 1
                        # if the seg is a hull seg, just map it p from the r1 seg
                        if  r2[index2][0][1] == r2Hull[ hullIndex2 ]:
                                r2HullTris.append(  (r2[index2][0][0]+(endTime,), r2[index2][0][1]+(endTime,), r1Hull[hullIndex1]+(startTime,) ) )
                                if r2[index2][0][0] in r2PoiToCycLabelDict:
                                        r2ConcTris.append( [] )
                                        currListIndex = len(r2ConcTris)-1
                                        r2ConcHullSeg.append( None ) # no closing Hull hseg, all interior cycles 
                                        cycNumList = r2PoiToCycLabelDict.pop( r2[index2][0][0] )
                                        for cycID in cycNumList:
                                                for h in r2ConCycles[cycID]:
                                                        if hsegLibrary.isLeft( h ):
                                                                r2ConcTris[currListIndex].append(  (h[0][0]+(endTime,), h[0][1]+(endTime,), r1Hull[hullIndex1]+(startTime,) ) )
                                index2 = hsegLibrary.getNextOuterCycleWalkIndex( r2[index2], r2, r2IndexLookup )
                        else:
                                #we are on an r1 concavity.  map until we get to the next hull poi
                                r2ConcTris.append( [] )
                                currListIndex = len(r2ConcTris)-1
                                r2ConcHullSeg.append( (r2Hull[hullIndex2-1], r2Hull[hullIndex2]) )
                                while r2[index2][0][0] != r2Hull[ hullIndex2 ]:
                                        r2ConcTris[currListIndex].append( (r2[index2][0][0]+(endTime,), r2[index2][0][1]+(endTime,), r1Hull[hullIndex1]+(startTime,) ) )
                                        #Insert connected structures that touch here too
                                        if r2[index2][0][0] in r2PoiToCycLabelDict:
                                                cycNumList = r2PoiToCycLabelDict.pop( r2[index2][0][0] )
                                                for cycID in cycNumList:
                                                        for h in r2ConCycles[cycID]:
                                                                if hsegLibrary.isLeft( h ):
                                                                        r2ConcTris[currListIndex].append( (h[0][0]+(endTime,), h[0][1]+(endTime,), r1Hull[hullIndex1]+(startTime,) ) )
                                        index2 = hsegLibrary.getNextOuterCycleWalkIndex( r2[index2], r2, r2IndexLookup )
                if hullIndex1 == len( r1Hull)-1 and hullIndex2 == len( r2Hull )-1:
                        #done
                        break
                
                #now pick if we map the r1 hull set or the r2 hull set in the next round
                if hullIndex1 == len( r1Hull )-1:
                        mapR1Seg = False
                        continue
                elif hullIndex2 == len( r2Hull )-1:
                        mapR1Seg = True
                        continue
                else:
                        h1angle = angleFromVertical( (r1Hull[hullIndex1], r1Hull[hullIndex1+1]) )
                        h2angle = angleFromVertical( (r2Hull[hullIndex2], r2Hull[hullIndex2+1]) )
                        if h2angle < h1angle:
                                mapR1Seg = False
                        else:
                                mapR1Seg = True
                
        return r1HullTris, r2HullTris, r1ConcTris, r1ConcHullSeg, r2ConcTris, r2ConcHullSeg
                
