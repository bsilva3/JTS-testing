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





import random
import multiprocessing

#from numba import autojit

def createRandomSegs( numSegs, minVal=0, maxVal=10000 , **kwargs ):
        '''
        Create a bunch of random line segments within a bounding box.  Segments may or may not intersect,
        but collinear and overlapping segments are not allowed..
        Duplicates will be removed.  

        **input**:

        numSegs: The number of random line segments to create

        minVal: the lowest value allowed as an X or Y value to construct a point

        maxVal: the largest value allowed as an X or Y value to construct a point

        if a rectangular bounding box is required,  use keyword arguments as follows:

        minX: the lowest value allowed as an X value to construct a point
        
        minY: the lowest value allowed as an Y value to construct a point
        
        maxX: the greatest value allowed as an X value to construct a point
        
        maxY: the greatest value allowed as an X value to construct a point
        '''
        minVal = int( minVal )
        maxVal = int( maxVal )
        minX = minVal
        minY = minVal
        maxX = maxVal
        maxY = maxVal
        for key, value in kwargs.items():
            if key == 'minX':
                minX = int(value)
            elif key == 'minY':
                minY = int(value)
            elif key == 'maxX':
                maxX = int(value)
            elif key == 'maxY':
                maxY = int(value)
            else: 
                print ('invalid argument to createRandomSegs: {0} = {1}'.format( key, value) )
                exit()
        random.seed()
        RL = []
        for i in range( 0, numSegs ):
                s = ((random.randint(minX, maxX), random.randint(minY, maxY)), (random.randint(minX, maxX), random.randint(minY, maxY))  )
                if s[0] < s[1]:
                  RL.append( s )
                elif s[1] < s[0]: 
                  RL.append( (s[1],s[0]) )

        # remove dups
        RL = list( set(RL) )

        # remove collinear and overlapping
        finals = []
        for i in range( len( RL)-1):
                keepIt = True
                for j in range( i+1, len(RL) ):
                        if isCollinearAndOverlapping( RL[i], RL[j] ):
                                keepIt = False
                                break
                if keepIt:
                        finals.append( RL[i] )
        return finals


def calcNonIntersectingSegsIntEndPoints( segs ):
        '''
        take a set of line segments.  
        
        1. Snap all end points to intergers
        2. Break all segs at intersection points.  

        the result may have floating point values at intersection points.
        This is not such a useful function.  Typically, you would use on of the other line segment
        intersection functions.

        **input**: segs: a list of line segments of the format [((x1,y1),(x2,y2)),((x3,y3),(x4,y4)),...]

        **output**: a list of line segments, same structure as input.
        '''
        segs = calcNonIntersectingSegs( segs )
        # now round
        segs = [ ((int(round(s[0][0])),int(round(s[0][1]))), (int(round(s[1][0])),int(round(s[1][1])))) for s in segs]

        # order teh points, remove segs that are actually points
        newSegs =[]

        for s in segs:
                if s[0] < s[1]:
                  newSegs.append( s )
                elif s[1] < s[0]:
                  newSegs.append( (s[1],s[0]) )
        # remove any intersecting segs

        segs = newSegs
        #print 'REMOVE INTERSECTING INTEGER SEGS'
        newSegs = []
        for i in range( len( segs ) - 1 ):
                keepIt = True
                for j in range( i+1, len( segs ) ):
                        if isCollinearAndOverlapping( segs[i], segs[j] ):
                                keepIt = False
                                break
                        # now if the segs share an endpoint, we can assume
                        # they do not intersect
                        if segs[i][0] == segs[j][0] or segs[i][0] == segs[j][1] or segs[i][1] == segs[j][0] or segs[i][1] == segs[j][1]:
                                continue
                        # if they are collinear, they do not intersect
                        x1 = segs[i][0][0]
                        y1 = segs[i][0][1] 
                        x2 = segs[i][1][0] 
                        y2 = segs[i][1][1] 
                        x3 = segs[j][0][0] 
                        y3 = segs[j][0][1] 
                        x4 = segs[j][1][0] 
                        y4 = segs[j][1][1]
                        
                        denom = float( ((y4-y3)*(x2-x1)) - ((x4-x3)*(y2-y1)) )
                        if denom == 0.0:   #lines are parallel
                                continue
                
                        ua = ((x4-x3)*(y1-y3))-((y4-y3)*(x1-x3))
                        ua = ua / denom
                        ub = ((x2-x1)*(y1-y3))-((y2-y1)*(x1-x3))
                        ub = ub / denom
                        
                        #if we get here, lines are not parallel, not overlapping
                        # and don't share an endpoint
                        # see if there is an intersection
                        if 0.0 <= ua and ua <= 1.0 and 0.0 <= ub and ub <= 1.0:
                                #intersection!
                                keepIt = False
                                break
                if keepIt:
                        newSegs.append( segs[i] )
        if len(segs ) > 0:
                newSegs.append( segs[ len( segs)-1] )
                
        print 'end'
        return newSegs


def collinear( L, R, tolerance = 0.0000001 ):
        '''
        Test if two line segments are collinear within a tolerance.

        **input**: 

        L: a line segment: ((x1,y1),(x2,y2))

        R: a line segment like L

        tolerance:   a tolerance value.  Set to 0 for exact collinearity test, higher for greater tolerance.
        
        **output**:

        boolean value
        '''
        if tolerance != 0:
                # will be collinear if l1,l2,r1 and l1,l2,r2 are all within collinear tolerance
                # uses left turn test.
                p1x = L[0][0]
                p1y = L[0][1]
                p2x = L[1][0]
                p2y = L[1][1]
                p3x = R[0][0]
                p3y = R[0][1]
                v1 = ((p3y - p1y) * (p2x - p1x)) - ((p2y - p1y) * (p3x - p1x))
                p3x = R[1][0]
                p3y = R[1][1]
                v2 = ((p3y - p1y) * (p2x - p1x)) - ((p2y - p1y) * (p3x - p1x))
                negT = tolerance*-1
                return negT <= v1 and v1 <= tolerance and negT <= v2 and v2 <= tolerance
        else:
                x1 = L[0][0]
                y1 = L[0][1]
                x2 = L[1][0]
                y2 = L[1][1]
                x3 = R[0][0]
                y3 = R[0][1]
                x4 = R[1][0]
                y4 = R[1][1]
                
                denom = ((y4-y3)*(x2-x1)) - ((x4-x3)*(y2-y1))
                if denom == 0.0:
                        return True
                return False


def isCollinearAndOverlapping( L,R, tolerance = .0000001 ):
        '''
        test if two segments are both collinear AND overlapping.  Collinearity within a tolerance is allowed.

        **input**:

        L: a line segment with format ((x1,y1),(x2,y2))

        R: line segment with structure as L

        tolerance: set to 0 for exact collinearity test.  Otherwise, allows *almost* collinear to count as collinear

        **returns**:

        *True* if L and R are collinear within tolerance and overlapping

        *False* otherwise
        '''
        if L == None or R == None:
                return False

        if L == R or L == (R[1], R[0]):
                return True

        if collinear( L, R, tolerance ):
                if L[0][0] == L[1][0] or R[0][0] == R[1][0]: #vertical segs:
                        vals = [ (L[0][1],'l') , (L[1][1],'l'), (R[0][1],'r'), (R[1][1],'r') ]
                else:
                        vals = [ (L[0][0],'l') , (L[1][0],'l'), (R[0][0],'r'), (R[1][0],'r') ]
                vals.sort( key = lambda x:x[0])
                # check for overlapping
                #first two vals the same, overlapping
                # middle two vals the same, not overlapping
                # first tow labels same, not verlapping
                # first two lavels same or middl vals same -> not overlapping
                return not( vals[0][1] == vals[1][1] or vals[1][0] == vals[2][0])
        return False
# take a list of segs, return a list of segs that only intersect at end points
# a seg is a tuple ((x1, y1), (x2, y2))

def calcIntersectionPointsRedBlueParallelWrapper( argTup ):
        segs1, segs2, indexList1, indexList2, q = argTup
        ip1, ip2 =  calcIntersectionPointsRedBlue( segs1, segs2, indexList1, indexList2 )
        q.put( (ip1, ip2 ) )

def calcIntersectionPointsRedBlue( segs1, segs2, indexList1 = None, indexList2 = None ):
        '''
        computes intersection points between red and blue segs.
        
        * assumes seg snapping has taken place
        
        * assumes segs are ALL floats for end points
        
        * Index lists are used if strip decomposition has been performed.  
        
        * Otherwise, pass None and everything will be taken care of
        
        **output**:

        (pois1,pois2): a tuple.  pois1 is a list of intersection points occuring in segs1.  pois2 is a list of intersection points occurrin in segs2.
        A point in pois1 or pois2 has the strucutre: intersectPoi = (0,(0.0,0.0)).  The first integer is the index of the line segment in which the intersection point occurs.

        '''
        #Find intersections between segs1 and segs 2.
        # build the broken segs
        intersectPoi = (0,(0.0,0.0))
        pois1 = []
        pois2 = []

        if indexList1 == None:
                indexList1 = range( len( segs1 ) )
        if indexList2 == None:
                indexList2 = range( len( segs2 ) )
        lfloat = float
        lisCollinearAndOverlapping = isCollinearAndOverlapping
        for i in range( len( segs1 ) ):
                for j in range( len( segs2 ) ):
                        x1 = lfloat( segs1[i][0][0] )
                        y1 = lfloat( segs1[i][0][1] )
                        x2 = lfloat( segs1[i][1][0] )
                        y2 = lfloat( segs1[i][1][1] )
                        x3 = lfloat( segs2[j][0][0] )
                        y3 = lfloat( segs2[j][0][1] )
                        x4 = lfloat( segs2[j][1][0] )
                        y4 = lfloat( segs2[j][1][1] )
                        
                        #most segs don't interact.  do a simple bbox test
                        xamax = x1 if x1 > x2 else x2
                        xamin = x1 if x1 < x2 else x2
                        xbmax = x3 if x3 > x4 else x4
                        xbmin = x3 if x3 < x4 else x4
                        yamax = y1 if y1 > y2 else y2
                        yamin = y1 if y1 < y2 else y2
                        ybmax = y3 if y3 > y4 else y4
                        ybmin = y3 if y3 < y4 else y4
                        
                        if (xamin > xbmax or xamax < xbmin or yamax < ybmin or yamin > ybmax ):
                                continue

                        denom = ((y4-y3)*(x2-x1)) - ((x4-x3)*(y2-y1))
                        if lisCollinearAndOverlapping( segs1[i], segs2[j] ):
                                ll = segs1[i][0][0]
                                lu = segs1[i][1][0]
                                rl = segs2[j][0][0]
                                ru = segs2[j][1][0]
                                if ll == lu:
                                        ll = segs1[i][0][1]
                                        lu = segs1[i][1][1]
                                        rl = segs2[j][0][1]
                                        ru = segs2[j][1][1]
                                if rl < ll and ll < ru:
                                        intersectPoi = (indexList2[j],(segs1[i][0][0], segs1[i][0][1]))
                                        pois2.append( intersectPoi )
                                if rl < lu and lu < ru:
                                        intersectPoi = (indexList2[j],(segs1[i][1][0], segs1[i][1][1]))
                                        pois2.append( intersectPoi )
                                if ll < rl and rl < lu:
                                        intersectPoi = (indexList1[i],(segs2[j][0][0], segs2[j][0][1]))
                                        pois1.append( intersectPoi )
                                if ll < ru and ru < lu:
                                        intersectPoi = (indexList1[i],(segs2[j][1][0], segs2[j][1][1]))
                                        pois1.append( intersectPoi )
                                continue

                        if segs1[i][0] == segs2[j][0] or segs1[i][0] == segs2[j][1] or segs1[i][1] == segs2[j][0] or segs1[i][1] == segs2[j][1]:
                                continue

                        if denom == 0.0:   #lines are parallel
                                continue
                
                        ua = ((x4-x3)*(y1-y3))-((y4-y3)*(x1-x3))
                        ua = ua / denom
                        ub = ((x2-x1)*(y1-y3))-((y2-y1)*(x1-x3))
                        ub = ub / denom
                        # if we get here, the lines are not parallel.  they must intersect somewhere
                        # first check if two segs intersect in their interiors
                        # record the segs so that we can construct the resulting segs
                        if 0.0 < ua and ua < 1.0 and 0.0 <= ub and ub <= 1.0:
                                x = x1 + (ua * (x2-x1) )
                                y = y1 + (ua * (y2-y1) )
                                intersectPoi = (indexList1[i],(x, y))
                                if intersectPoi[1] != segs1[i][0] and intersectPoi[1] != segs1[i][1]:
                                        pois1.append( intersectPoi )
                                        
                        if  0.0 < ub and ub < 1.0 and 0.0 <= ua and ua <= 1.0:
                                x = x1 + (ua * (x2-x1) )
                                y = y1 + (ua * (y2-y1) )
                                intersectPoi = (indexList2[j],(x, y))
                                if intersectPoi[1] != segs2[j][0] and intersectPoi[1] != segs2[j][1]:
                                        pois2.append( intersectPoi )
        # now we have all intersections, make all resulting segs
        return (pois1,pois2)


def segIntersection(  segs1, segs2 ):
        ''' intersect segs1 and segs2 .  returns a tuple containing 2 lists: 1 list has segs1 broken at intersection points with segments in segs2, and vice versa.

        thus calls the reb/blue intersection function, but actually returns the resulting line segs (the arrangment), instead of just the intersection points.


        There is code use a multi-threaded scheme based on strip decomposition of the embedding space, but it is commented out at the moment.
        
        The call to snapEndPoints call will make sure all segs are left, and snap endpoints that are very close to be the slame point.

        **input**:

        segs1: a list of line segments.

        segs2: a list of line segments.

        **output**: (resgs1, rsegs2):  a tuple.  resgs1 is segs1 with segments broken at intersection points with segments in segs2.  same for rsegs2.
        
        '''
        # get rid of too small segs
        segs1 = [((float(s[0][0]),float(s[0][1])), (float(s[1][0]), float(s[1][1])) ) for s in segs1]
        segs2 = [((float(s[0][0]),float(s[0][1])), (float(s[1][0]), float(s[1][1])) ) for s in segs2]
        segs1 = snapEndPoints(  segs1 ) 
        segs2 = snapEndPoints(  segs2 ) 

        maxx1 = max( [x[0] for y in segs1 for x in y] )
        minx1 = min( [x[0] for y in segs1 for x in y] )
        maxx2 = max( [x[0] for y in segs2 for x in y] )
        minx2 = min( [x[0] for y in segs2 for x in y] )
        if maxx1 < maxx2:
                maxx1 = maxx2
        if minx1 > minx2:
                minx1 = minx2
        num1 = len( segs1 )
        num2 = len( segs2 )
        if num1 < num2:
                num1 = num2
        numStrips = int(num1 *.01)
        if numStrips < 2:
                numStrips = 2


        s1, index1, segs1 = stripDecomposition( segs1, None, None, minx1, maxx1, numStrips )
        s2, index2, segs2 = stripDecomposition( segs2, None, None, minx1, maxx1, numStrips )
        # now we have the strip decomposed segs, call the seg Intersections
        interPois1 = []
        interPois2 = []

        multThreads = False
        if multThreads:
                numThreads = multiprocessing.cpu_count() #4 #len( s1 )
                pool = multiprocessing.Pool(numThreads)
                manager = multiprocessing.Manager()
                q = manager.Queue()
                qList = []
                for i in range( len( s1 ) ):
                        qList.append( q )
                argTup = zip( s1, s2, index1, index2, qList )
                pool.map(calcIntersectionPointsRedBlueParallelWrapper, argTup)
                for i in range( len( s1 ) ):
                        ip1, ip2 = q.get()
                #               ip1, ip2 =  calcIntersectionPointsRedBlue( s1[i], s2[i], index1[i], index2[i] )
                        interPois1.extend( ip1 )
                        interPois2.extend( ip2 )
                pool.close()
                pool.join()
        else:
                for i in range( len( s1 ) ):
                        ip1, ip2 =  calcIntersectionPointsRedBlue( s1[i], s2[i], index1[i], index2[i] )
                        interPois1.extend( ip1 )
                        interPois2.extend( ip2 )
        # build resulting segs

        rsegs1 = constructSegs( interPois1, segs1 )
        rsegs2 = constructSegs( interPois2, segs2 )

        rsegs1 = snapEndPoints( rsegs1 ) 
        rsegs2 = snapEndPoints( rsegs2 )

        return rsegs1, rsegs2

def isLeftTurn( p1,p2,p3):
        '''
        tests if when traveling from point p1 to point p2, and then on to p3, whether the traveler must make a left or right turn at p2 in order to reach p3.

        uses sign of the area of the triangle computation.

        **input**:

        p1,p2,p3: points of the format (x,y)

        **output**:

        -1 if a left turn is needed

        0 if the points are collinear

        1 if a right turn is needed
        '''
        p1x = p1[0]
        p1y = p1[1]
        p2x = p2[0]
        p2y = p2[1]
        p3x = p3[0]
        p3y = p3[1]
        result =  ((p3y - p1y) * (p2x - p1x)) - ((p2y - p1y) * (p3x - p1x))
        if result > 0:
                return 1
        elif result == 0:
                return 0
        return -1

def keepOuterBoundary( origSegs1, laList1, lbList1, origSegs2, laList2, lbList2, keepEqualWithSameLA = True):
        '''
        input segs are Labeled segs!
        
        point in polygon test for each seg
        
        test if segs from seg1 are out of  seg2
        
        * Assumes non interior intersecting segs (except for equivalent segs).
        * Assumes all segs have floating point end points
        * Assumes end point snapping is done

        **Note that the use of segIntersection(origSegs1, origSegs2) satisfies all assumptions**
        
        Used for region set operations!

        **output** a list of segments in the usual format.
        '''
        #perform strip decomposition
        maxx1 = max( [x[0] for y in origSegs1 for x in y] )
        minx1 = min( [x[0] for y in origSegs1 for x in y] )
        maxx2 = max( [x[0] for y in origSegs2 for x in y] )
        minx2 = min( [x[0] for y in origSegs2 for x in y] )
        if maxx1 < maxx2:
                maxx1 = maxx2
        if minx1 > minx2:
                minx1 = minx2
        num1 = len( origSegs1 )
        num2 = len( origSegs2 )
        if num1 < num2:
                num1 = num2
        numStrips = int(num1 *.01)
        if numStrips < 2:
                numStrips = 2

        s1, la1,lb1, index1, segs1, laList1, lbList1 = stripDecomposition( origSegs1, laList1, lbList1, minx1, maxx1, numStrips )
        s2, la2,lb2, index2, segs2, laList2, lbList2, bounds = stripDecompositionWithBounds( origSegs2, laList2, lbList2, minx1, maxx1, numStrips )
        lisLeftTurn = isLeftTurn
        rset = set()
        for i in range( len( s1 ) ):
                for j,s in enumerate(s1[i]) :
                        if s[0][0] < bounds[i] or s[0][0] > bounds[i+1]:
                                continue
                        count = 0
                        if s  in s2[i]:
                                sIndex = s2[i].index( s )
                                if ((la1[i][j] > 0 and la2[i][sIndex] > 0) or (la1[i][j] <= 0 and la2[i][sIndex] <= 0 )) and keepEqualWithSameLA:
                                        rset |= set([s])
                                elif (not((la1[i][j] > 0 and la2[i][sIndex] > 0) or (la1[i][j] <= 0 and la2[i][sIndex] <= 0 ))) and not keepEqualWithSameLA: 
                                        rset |= set([s])
                                continue
                        else:
                                for r in s2[i]:
                                        if r[0][0] == r[1][0]: #skip verticals
                                                continue
                                        if s[0] == r[0]: # share a left end point
                                                if lisLeftTurn( r[0], r[1], s[1] ) == 1:
                                                        count += 1
                                        elif r[0][0] <= s[0][0] and s[0][0] < r[1][0]: # r spans s's left point
                                                if lisLeftTurn( r[0], r[1], s[0] ) == 1:
                                                        count += 1
                                # if count is even, s in outised of r.  Otherwise, its inside
                                                        
                        if count % 2 == 0:
                                rset |= set([s])
        return rset

def keepInnerBoundary( origSegs1, laList1, lbList1, origSegs2, laList2, lbList2, keepEqualWithSameLA = True):
        '''
        input segs are Labeled segs!
        
        point in polygon test for each seg
        
        test if segs from seg1 are out of  seg2
        
        * Assumes non interior intersecting segs (except for equivalent segs).
        * Assumes all segs have floating point end points
        * Assumes end point snapping is done
        
        **Note that the use of segIntersection(origSegs1, origSegs2) satisfies all assumptions**


        Used to compute set operations between regions!  keep the segments from origSegs1 that are inside or on
        origSegs2, but take into account the labeling.  

        returns a list of segments in the usual format.
        
        
        '''
        #perform strip decomposition
        maxx1 = max( [x[0] for y in origSegs1 for x in y] )
        minx1 = min( [x[0] for y in origSegs1 for x in y] )
        maxx2 = max( [x[0] for y in origSegs2 for x in y] )
        minx2 = min( [x[0] for y in origSegs2 for x in y] )
        if maxx1 < maxx2:
                maxx1 = maxx2
        if minx1 > minx2:
                minx1 = minx2
        num1 = len( origSegs1 )
        num2 = len( origSegs2 )
        if num1 < num2:
                num1 = num2
        numStrips = int(num1 *.01)
        if numStrips < 2:
                numStrips = 2

        s1, la1,lb1, index1, segs1, laList1, lbList1 = stripDecomposition( origSegs1, laList1, lbList1, minx1, maxx1, numStrips )
        s2, la2,lb2, index2, segs2, laList2, lbList2, bounds = stripDecompositionWithBounds( origSegs2, laList2, lbList2, minx1, maxx1, numStrips )
        lisLeftTurn = isLeftTurn
        rset = set()
        for i in range( len( s1 ) ):
                for j,s in enumerate(s1[i]) :
                        if s[0][0] < bounds[i] or s[0][0] > bounds[i+1]:
                                continue
                        count = 0
                        if s  in s2[i]:
                                sIndex = s2[i].index( s )
                                if ((la1[i][j] > 0 and la2[i][sIndex] > 0) or (la1[i][j] <= 0 and la2[i][sIndex] <= 0)) and keepEqualWithSameLA:
                                        rset |= set([s])
                                elif (not((la1[i][j] > 0 and la2[i][sIndex] > 0) or (la1[i][j] <= 0 and la2[i][sIndex] <= 0 ))) and not keepEqualWithSameLA: 
                                        rset |= set([s])
                                continue
                        else:
                                for r in s2[i]:
                                        if r[0][0] == r[1][0]: #skip verticals
                                                continue
                                        if s[0] == r[0]: # share a left end point
                                                if lisLeftTurn( r[0], r[1], s[1] ) == 1:
                                                        count += 1
                                        elif r[0][0] <= s[0][0] and s[0][0] < r[1][0]: # r spans s's left point
                                                if lisLeftTurn( r[0], r[1], s[0] ) == 1:
                                                        count += 1
                                # if count is even, s in outised of r.  Otherwise, its inside
                                                        
                        if count % 2 == 1:
                                rset |= set([s])
        return rset

def keepOnOrIn( origSegs1, origSegs2 ):
        '''
        point in polygon test for each seg
        
        test if segs from seg1 are in or on seg2
        
        Assumes non interior intersecting segs.  

        **output**: a list of segs from origsegs1 that lie inside or ON the region defined by origSegs2
        '''
        #make sure we are all floats
        segs1 = [ ((float(s[0][0]), float(s[0][1])), (float(s[1][0]), float(s[1][1]))) for s in origSegs1 ]
        segs2 = [ ((float(s[0][0]), float(s[0][1])), (float(s[1][0]), float(s[1][1]))) for s in origSegs2 ]
        rset = set()
        for s in segs1 :
                count = 0
                if s in segs2:
                        rset |= set([s])
                else:
                        for r in segs2:
                                if r[0][0] == r[1][0]: #skip verticals
                                        continue
                                if s[0] == r[0]: # share a left end point
                                        if isLeftTurn( r[0], r[1], s[1] ) == 1:
                                                count += 1
                                elif r[0][0] <= s[0][0] and s[0][0] < r[1][0]: # r spans s's left point
                                        if isLeftTurn( r[0], r[1], s[0] ) == 1:
                                                count += 1
                # if count is even, s in outised of r.  Otherwise, its inside
                
                if count % 2 == 1:
                        rset |= set([s])
        return rset

def keepIn( origSegs1, origSegs2 ):
        '''
        point in polygon test for each seg
        
        test if segs from seg1 are in seg2
        
        Assumes non interior intersecting segs.  

        **output**: a list of segs from origsegs1 that lie inside the region defined by origSegs2
        '''
        #make sure we are all floats
        segs1 = [ ((float(s[0][0]), float(s[0][1])), (float(s[1][0]), float(s[1][1]))) for s in origSegs1 ]
        segs2 = [ ((float(s[0][0]), float(s[0][1])), (float(s[1][0]), float(s[1][1]))) for s in origSegs2 ]
        rset = set()
        for s in segs1 :
                count = 0
                for r in segs2:
                        if r[0][0] == r[1][0]: #skip verticals
                                continue
                        if s[0] == r[0]: # share a left end point
                                if isLeftTurn( r[0], r[1], s[1] ) == 1:
                                        count += 1
                        elif r[0][0] <= s[0][0] and s[0][0] < r[1][0]: # r spans s's left point
                                if isLeftTurn( r[0], r[1], s[0] ) == 1:
                                        count += 1
                # if count is even, s in outised of r.  Otherwise, its inside
                
                if count % 2 == 1:
                        rset |= set([s])
        return rset
                
def countInteriors( segs, laList, lbList ):
        ''' 
        marks each segment with ALL interiors it bounds.
        
        assumes a list of segs describing multiple regions that 
        intersect only at endpoints, and no duplicates (these are already taken care of).
        
        Assumes left end point less than right endpoint.

        **output**: a tuple (segs, laList, lbList)
        '''
        #make sure we are all floats
        segs = [ ((float(s[0][0]), float(s[0][1])), (float(s[1][0]), float(s[1][1]))) for s in segs ]
        retLa = [la for la in laList ]
        retLb = [lb for lb in lbList ]
        for i in range( len(retLa) ):
                if laList[i] -lbList[i] == 0:
                        retLa[i] = 0
                        retLb[i] = 0
                if laList[i] -lbList[i] < 0:
                        retLa[i] = retLa[i] + laList[i] -lbList[i] 
                        retLb[i] = retLb[i] + laList[i] -lbList[i] 
        for i in range( len( segs) ):
                for j in range( len(segs ) ):
                        if i == j:
                                continue
                        s = segs[i]
                        r = segs[j]
                        if r[0][0] == r[1][0] : #skip verticals
                                continue
                        if s[0] == r[0]: # share a left end point
                                if isLeftTurn( r[0], r[1], s[1] ) == 1:
                                        retLa[i] = retLa[i] + (laList[j] - lbList[j] )
                                        retLb[i] = retLb[i] + (laList[j] - lbList[j] )
                        elif  r[0][0] <= s[0][0] and s[0][0] < r[1][0]: # r spans s's left point
                                if isLeftTurn( r[0], r[1], s[0] ) == 1:
                                        retLa[i] = retLa[i] + (laList[j] - lbList[j] )
                                        retLb[i] = retLb[i] + (laList[j] - lbList[j] )
        return segs, retLa, retLb

def stripDecomposition( segs, laList = None, lbList = None, minx = None, maxx = None, forceNumStrips = None ):
        ''' See docstring for stripDecompositionWithBounds '''
        retTup = stripDecompositionWithBounds( segs, laList, lbList, minx, maxx, forceNumStrips )
        retTup = retTup[:len(retTup)-1]
        return retTup

def stripDecompositionWithBounds( segs, laList = None, lbList = None, minx = None, maxx = None, forceNumStrips = None ):
        ''' returns a list of lists.  each list will contain copies of the segs
        that fall into that strip.  Stips are equal length, and will be based 
        on the min and max xvalues of the segs, unless specific min and max 
        values are passed.

        is the laList and lbList are == None, no label lists are returned

        returns the lists of strip segs, the lists of their labels (if lists are not none)
        the list of indexes mapping to the original seg in newly sorted list segs
        the list of newly sorted above labels (if labels are passed in )
        the list of newly sorted below labels (if labels are passed in )
        the list of segment boundaries containin
        '''
        returnLists = True
        if laList == None:
                returnLists = False
                laList = [0] * len( segs )
                lbList = [0] * len( segs )

        newSegs = []
        for s in segs:
                if s[0] < s[1]:
                        newSegs.append( s )
                else:
                        newSegs.append( (s[1],s[0]) )
        segs = newSegs
        #strip decomposition
        numStrips = len( segs ) * .01
        numStrips = int( numStrips )
        if numStrips < 2: 
                numStrips = 2
        if forceNumStrips != None:
                numStrips = forceNumStrips
        if maxx == None:
                maxx = max( [x[0] for y in segs for x in y] )
        if minx == None:        
                minx = min( [x[0] for y in segs for x in y] )
        if minx > maxx:
                tmp = minx
                minx = maxx
                maxx = tmp
        if minx == maxx:
                if returnLists:
                        return [ segs ], [laList], [lbList] [ range( len( segs ) ) ], segs, laList, lbList, [minx, maxx]
                else:
                        return [ segs ], [ range( len( segs ) ) ], segs, [minx, maxx]

        minx = float( minx )
        maxx = float( maxx )
        numBound = numStrips+1
        bounds = [0]*numBound
        bounds[0] = minx
        bounds[ numBound-1] = maxx
        # make the internal boundaries
        boundWidth = (maxx-minx)/ float( numStrips )
        prevBound = minx
        for i in range( 1, numStrips ):
                bounds[i] = prevBound + boundWidth
                prevBound = bounds[i]

        # sort the input segs
        zippedList =  zip( segs, laList, lbList)
        zippedList.sort( key=lambda x:  (x[0][0][0],x[0][0][1],x[0][1][0],x[0][1][1]))
        segs,laList,lbList = [ list(z) for z in zip(* zippedList )]

        # finally, make the seg lists
        segStrips = []
        laStrips = []
        lbStrips = []
        indexStrips = []
        for i in range( numStrips ):
                segStrips.append( list() )
                laStrips.append( list() )
                lbStrips.append( list() )
                indexStrips.append( list() )
        # fill up the seg lists
        boundStart = 1
        for i in range( len(segs) ):
                currSeg = segs[i]
                la = laList[i]
                lb = lbList[i]
                for j in range( boundStart, numBound ):
                        currMin = bounds[j-1]
                        currMax = bounds[j]
                        if currSeg[0][0] > currMax:
                                # done with this strip
                                boundStart += 1
                                continue
                        if currSeg[1][0] < currMin:
                                # done with this seg
                                break
                        # otherwise, the seg is in the strip
                        segStrips[j-1].append( currSeg )
                        laStrips[j-1].append( la )
                        lbStrips[j-1].append( lb )
                        indexStrips[j-1].append( i )
        # figure out if actual gained from the decomp
        sum = 0
        for i in range(len( segStrips ) ):
                sum += len(segStrips[i]) * len(segStrips[i] )
        if forceNumStrips != None or sum < len( segs) * len( segs ):
                if returnLists:
                        return segStrips, laStrips, lbStrips, indexStrips, segs, laList, lbList, bounds
                return segStrips, indexStrips, segs, bounds
        else:
                if returnLists:
                        return [ segs ], [laList], [lbList], [ range( len( segs ) ) ], segs,laList, lbList, bounds
                else:
                        return [ segs ], [ range( len( segs ) ) ], segs, bounds
                                
                
def calcNonIntersectingSegs( segs, laList = None, lbList = None ):
        '''
        break segs at intersection points.  Preserve labels if they are present.
        
        Uses a strip decomposition scheme to speed things up

        **input**: 
        
        segs: a list of segments in the usual format [((x1,y2),(x2,y2)),((x3,y3),(x4,y4)),...]

        laList, lbList: parallel arrays with segs, indicating label values. 

        **output**: a list of segs in the usual format.

        if label lists are passed in, the output is a tuple: (segs, laList, lblist)
        '''
        # get the strips
        returnLists = True
        if laList == None:
                returnLists = False
                laList = [0] * len( segs )
                lbList = [0] * len( segs )

        # get rid of too small segs
        segs = [((float(s[0][0]),float(s[0][1])), (float(s[1][0]), float(s[1][1])) ) for s in segs]
        segs, laList, lbList = [ list(z) for z in zip(* snapEndPointsWithLabels( zip( segs, laList, lbList) )) ]
        #snap end points returns left segs
        # get the strips
        segStrips, laStrips, lbStips, indexStrips, segs, laList, lbList =  stripDecomposition( segs, laList, lbList )

        # get the intersection points
        interPois = list()
        multThreads = False
        if multThreads:
                numThreads = multiprocessing.cpu_count() #4 #len( s1 )
                pool = multiprocessing.Pool(numThreads)
                manager = multiprocessing.Manager()
                q = manager.Queue()
                qList = []
                for i in range( len( segStrips ) ):
                        qList.append( q )
                argTup = zip( segStrips, laStrips, lbStips, indexStrips, qList )

                pool.map(calcIntersectionPointsParallelWrapper, argTup)
                len( segStrips)
                for i in range( len( segStrips ) ):
                        ip1 = q.get()
                        interPois.extend( ip1 )
                pool.close()
                pool.join()
        else:
                
                for i in range( len( segStrips ) ):
                        interPois.extend(  calcIntersectionPoints( segStrips[i], laStrips[i], lbStips[i], indexStrips[i] ) )
        

        # now we have all intersections, make all resulting segs
        segs, laList, lbList = constructSegsWithLabels( interPois, segs, laList, lbList )
        # get rid of too small segs
        segs, laList, lbList = [ list(z) for z in zip(* snapEndPointsWithLabels( zip( segs, laList, lbList) )) ]

        
        if returnLists:
                return segs, laList, lbList
        return segs

def calcIntersectionPointsParallelWrapper( argTup ):
        segs1, laList, lbList, indexList, q = argTup
        ip1 =  calcIntersectionPoints( segs1, laList, lbList, indexList, )
        q.put( ip1 )

def calcIntersectionPoints( segs, laList = None, lbList = None, indexList = None ):
        '''
        computes the intersection points between segments in the list segs.  labels are updated for overlapping segs, but not intersecting segs.
        
        .. note::

            Labels are preserved for all segs that do not **overlap** with another segment.  If two segments overlap, their labels
            are summed.

            The `constructSegsWithLabels()` function will preserve these labels and thier sums.  

            If the desire is to keep track of which areas are covered by cycles with particular labels, use the `mapLibrary` versions of these functions to
            construct a map
        
        segs is in the usual format: [((x1,y1),(x2,y2)),((x3,y3),(x4,y4)),...]

        **output**:  a list of indexed points.  An indexed point has the format: (index,(x,y)) where index is the index of the seg in which the intersetion point occurred.

        **Assumes, that snapEndPoints has already been called**

        **Use constructSegsWithLabels to build back the actual segs broken at intersection points**
        '''
        if laList == None:
                laList = [0] * len( segs )
                lbList = [0] * len( segs )
        if indexList == None:
                indexList = range( len( segs ) )
        lfloat = float
        #floatify
        #segs = [((float(s[0][0]),float(s[0][1])), (float(s[1][0]), float(s[1][1])) ) for s in segs]
        # get rid of too small segs
        #segs, laList, lbList = [ list(z) for z in zip(* snapEndPointsWithLabels( zip( segs, laList, lbList) )) ]
        #part 1.  find all intersection points
        # intersect poi gets index of intersecting segs and the point, and the label vals after the point
        intersectPoi = (0,(0.0,0.0), 0,0)
        pois = []
        for i in range( len( segs ) - 1 ):
                for j in range( i+1, len( segs ) ):
                        x1 = lfloat( segs[i][0][0] )
                        y1 = lfloat( segs[i][0][1] )
                        x2 = lfloat( segs[i][1][0] )
                        y2 = lfloat( segs[i][1][1] )
                        x3 = lfloat( segs[j][0][0] )
                        y3 = lfloat( segs[j][0][1] )
                        x4 = lfloat( segs[j][1][0] )
                        y4 = lfloat( segs[j][1][1] )
                        #most segs don't interact.  do a simple bbox test
                        xamax = x1 if x1 > x2 else x2
                        xamin = x1 if x1 < x2 else x2
                        xbmax = x3 if x3 > x4 else x4
                        xbmin = x3 if x3 < x4 else x4
                        yamax = y1 if y1 > y2 else y2
                        yamin = y1 if y1 < y2 else y2
                        ybmax = y3 if y3 > y4 else y4
                        ybmin = y3 if y3 < y4 else y4
                        
                        if (xamin > xbmax or xamax < xbmin or yamax < ybmin or yamin > ybmax ):
                                continue
                                        
                        denom = ((y4-y3)*(x2-x1)) - ((x4-x3)*(y2-y1))
                        if isCollinearAndOverlapping( segs[i], segs[j] ):
                                ll = segs[i][0][0]
                                lu = segs[i][1][0]
                                rl = segs[j][0][0]
                                ru = segs[j][1][0]
                                if ll == lu:
                                        ll = segs[i][0][1]
                                        lu = segs[i][1][1]
                                        rl = segs[j][0][1]
                                        ru = segs[j][1][1]
                                if rl < ll and ll < ru:
                                        intersectPoi = (indexList[j],(segs[i][0][0], segs[i][0][1]), laList[i]+laList[j], lbList[i]+lbList[j])
                                        pois.append( intersectPoi )
                                        intersectPoi = (indexList[i],(segs[i][0][0], segs[i][0][1]), laList[i]+laList[j], lbList[i]+lbList[j])
                                        pois.append( intersectPoi )
                                if rl < lu and lu < ru:
                                        intersectPoi = (indexList[j],(segs[i][1][0], segs[i][1][1]), laList[j], lbList[j])
                                        pois.append( intersectPoi )
                                if ll < rl and rl < lu:
                                        intersectPoi = (indexList[i],(segs[j][0][0], segs[j][0][1]), laList[i]+laList[j], lbList[i]+lbList[j])
                                        pois.append( intersectPoi )
                                        intersectPoi = (indexList[j],(segs[j][0][0], segs[j][0][1]), laList[i]+laList[j], lbList[i]+lbList[j])
                                        pois.append( intersectPoi )
                                if ll < ru and ru < lu:
                                        intersectPoi = (indexList[i],(segs[j][1][0], segs[j][1][1]), laList[i], lbList[i])
                                        pois.append( intersectPoi )
                                if ll == rl:
                                        # if the first part of the segs overlap, we need to update the labels in construc segs
                                        intersectPoi = (indexList[j],(segs[i][0][0], segs[i][0][1]), laList[i]+laList[j], lbList[i]+lbList[j])
                                        pois.append( intersectPoi )
                                        intersectPoi = (indexList[i],(segs[j][0][0], segs[j][0][1]), laList[i]+laList[j], lbList[i]+lbList[j])
                                        pois.append( intersectPoi )
                                continue
                        if denom == 0.0:   #lines are parallel
                                continue
                        
                        if segs[i][0] == segs[j][0] or segs[i][0] == segs[j][1] or segs[i][1] == segs[j][0] or segs[i][1] == segs[j][1]:
                                # lines share an endpoint and are not parall.  They do not intersect in interiors
                                continue


                        ua = ((x4-x3)*(y1-y3))-((y4-y3)*(x1-x3))
                        ua = ua / denom
                        ub = ((x2-x1)*(y1-y3))-((y2-y1)*(x1-x3))
                        ub = ub / denom
                        # if we get here, the lines are not parallel.  they must intersect somewhere
                        # first check if two segs intersect in their interiors
                        # record the segs so that we can construct the resulting segs
                        if 0.0 < ua and ua < 1.0 and 0.0 <= ub and ub <= 1.0:
                                x = x1 + (ua * (x2-x1) )
                                y = y1 + (ua * (y2-y1) )
                                intersectPoi = (indexList[i],(x, y), laList[i], lbList[i])
                                if intersectPoi[1] != segs[i][0] and intersectPoi[1] != segs[i][1]:
                                        pois.append( intersectPoi )
                                        
                        if  0.0 < ub and ub < 1.0 and 0.0 <= ua and ua <= 1.0:
                                x = x1 + (ua * (x2-x1) )
                                y = y1 + (ua * (y2-y1) )
                                intersectPoi = (indexList[j],(x, y), laList[j], lbList[j])
                                if intersectPoi[1] != segs[j][0] and intersectPoi[1] != segs[j][1]:
                                        pois.append( intersectPoi )
        return pois


def collinearValue( p1,p2,p3):
        '''
        uses the left hand turn test based on the sign of the area of the trianngle defiened by points p1,p2, and p3, except that the actual value is returned.  This is useful if you want to see how close the three points are to being collinear.  
        
        Left hand turn test assumes you are traveling from p1 to p2 and then on to p3, and indicates if you must make a left or right turn at p2 to reach p3.

        **input**: 3 points, p1, p2, p3 of the format (x,y)

        **output**: the signed area of the square enclosing the triangle defined by the given points.
       
        * will return a 0 if p1, p2,p3 are exactly collinear
        
        * will return positive value if it forms a left turn
        
        * will return neg value if it forms a right turn
        '''
        
        p1x = p1[0]
        p1y = p1[1]
        p2x = p2[0]
        p2y = p2[1]
        p3x = p3[0]
        p3y = p3[1]
        return  ((p3y - p1y) * (p2x - p1x)) - ((p2y - p1y) * (p3x - p1x))


def collinearPoints( p1, p2, p3, tolerance = 0.0000001):
    '''
    uses left hand turn test to indicate if three points are collinear.

    **input**
    
    p1,p2,p3
        3 points of the form ``(x,y)``

    tolerance
        If the absolute value of the value computed by the left hand turn test is smaller that tolerance, it is considered colinear
    
    **output**

    boolean value
    '''
    p1x = p1[0]
    p1y = p1[1]
    p2x = p2[0]
    p2y = p2[1]
    p3x = p3[0]
    p3y = p3[1]
    value = ((p3y - p1y) * (p2x - p1x)) - ((p2y - p1y) * (p3x - p1x))
    return math.abs( value ) < tolerance

def indexedPoiCmp( p1, p2 ):
        '''
        comparison of indexed points for sorting.

        order is based on index, then x values the y values.

        **input**: p1 and p2, two indexed points of the format (index,(x,y))

        **output**: 

        -1 if p1 < p2

        0 if p1 == p2

        1 if p1 > p2
        '''
        if p1 == p2:
                return 0
        if p1[0] < p2[0] or (p1[0] == p2[0] and p1[1][0]< p2[1][0] ) or (p1[0] == p2[0] and p1[1][0] == p2[1][0] and p1[1][1] < p2[1][1] ):
                return -1
        return 1
def constructSegs( pois, segs  ):
        '''
        Red/blue line intersection returns a list of indexed points such that the points indicate where line segment intersections occurred, and the index indicates in which line segment the intersection occurred. This function jsut breaks the line segments at those points

        ***input**: 

        pois: a list of indexed poins of the format (index,(x,y)) where index is the index of a seg in segs

        segs: a list of segments in the usual format [((x1,y1),(x2,y2)),((x3,y3),(x4,y4)),...]

        **output**: 

        a list of segs in the usual format.
        '''
  
        #define return list
        retList = []
        poiSet = set( pois )
        pois = list(poiSet)
        pois = sorted( pois, cmp = indexedPoiCmp )

        resIndex = 0;
        for i in range( len( segs ) ):
                currSeg = segs[i]
                # if there are intersections in this seg, start makin new segs
                while resIndex < len(pois) and pois[resIndex][0] == i:
                        # make the first half of the split seg
                        currSeg = (currSeg[0], pois[resIndex][1])
                        retList.append( currSeg )
                        # make the second half of the split seg
                        currSeg = segs[i]
                        currSeg = ( pois[resIndex][1], currSeg[1] )
                        resIndex += 1
                
                currSeg = (currSeg[0],segs[i][1])
                retList.append( currSeg )
        # now all segs are made
        # remove dups
        segSet = set( retList )
        retList = list( segSet )
        # remove degenerate
        retList = [ s for s in retList if s[0] != s[1] ]
        #retList = checkNumRobustness( retList )
        #retList.sort( key = lambda x: (x[0][0][0],x[0][0][1], x[0][1][0], x[0][1][1]))
        return retList
        

def constructSegsWithLabels( pois, segs, laList, lbList ):
        '''
        See documentation for  constructSegs( pois, segs  ).

        This function works the same as that one, but preserves labelling.

        laList and lbList are parallel lists with segs.  When a seg is split at an intersection point, the labels are adjusted accordingly.

        '''
        #define return list
        retList = []
        retLaList = []
        retLbList = []
        pois = sorted( pois, cmp = indexedPoiCmp )
        resIndex = 0;
        for i in range( len( segs ) ):
                currSeg = segs[i]
                currLa = laList[i]
                currLb = lbList[i]
                # if there are intersections in this seg, start makin new segs
                while resIndex < len(pois) and pois[resIndex][0] == i:
                        # make the first half of the split seg
                        currSeg = (currSeg[0], pois[resIndex][1])
                        retList.append( currSeg )
                        retLaList.append( currLa )
                        retLbList.append( currLb )
                        # make the second half of the split seg
                        currSeg = segs[i]
                        currSeg = ( pois[resIndex][1], currSeg[1] )
                        currLa =  pois[resIndex][2]
                        currLb =  pois[resIndex][3]
                        resIndex += 1
                        if resIndex < len(pois) and pois[resIndex][0] == pois[resIndex-1][0] and pois[resIndex][1] == pois[resIndex-1][1] and ( pois[resIndex][2] != pois[resIndex-1][2] or  pois[resIndex][3] != pois[resIndex-1][3] ) and  (pois[resIndex-1][2] != laList[i] or  pois[resIndex-1][3] != lbList[i]):
                                pois[resIndex] = pois[resIndex-1]

                currSeg = (currSeg[0],segs[i][1])
                retList.append( currSeg )
                retLaList.append( currLa )
                retLbList.append( currLb )
        # now all segs are made
        # remove dups
        segSet = set(zip(retList, retLaList, retLbList) )
        retList = list( segSet )
        # remove degenerate
        retList = [ s for s in retList if s[0][0] != s[0][1] ]
        #retList = checkNumRobustness( retList )
        #retList.sort( key = lambda x: (x[0][0][0],x[0][0][1], x[0][1][0], x[0][1][1]))
        return [list(u) for u in zip(*retList)]


def snapEndPoints( segs ):
        ''' 
        Does 2 things:

        1. if any segs are too short (below a hard coded threshold, they are removed.  Too short segs cause issues in sorting and intersection computations
        2. if two segs have end points that are super close together, but that are not identical, one of those end points is shifted to the other. A rather clever algorithm using hash tables does this very quickly

        This function does NOT identify segment end points that are super close to another segment interior.  In other words, this is not a full on snap rounding implementation, it jsut handles very close end points.

        **input**: A list of segments in the usual format: [((x1,y1),(x2,y2)),((x3,y3),(x4,y4)),...] 
        
        **output**: a list of segments that have been snapped at end points. 
        '''

        lalist = [0]*len(segs)
        lblist = [0]*len(segs)
        newSegs = zip( segs, lalist, lblist)
        return list(zip(*snapEndPointsWithLabels( newSegs ) )[0])

def snapEndPointsWithLabels( segs ):
        ''' takes a list of LABELED segs, removes too short segs, and snaps too close end points together
            ASSUMES segs end points are ALL floats
        '''

        # make sure all segs are left
        newSegs = []
        for s in segs:
                if s[0][0] < s[0][1]:
                        newSegs.append( s )
                else:
                        newSegs.append( ((s[0][1],s[0][0]), s[1], s[2] ) )
        segs = newSegs
        # remove any segs with identical end points
        newSegs = []
        for s in segs:
                if s[0][0] != s[0][1]:
                        newSegs.append( s )
        segs = newSegs

        # find any too short segs
        tooShortSet = set()
        for s in segs:
                x1 = s[0][0][0]
                y1 = s[0][0][1]
                x2 = s[0][1][0]
                y2 = s[0][1][1]
                if (((x2-x1)*(x2-x1)) + ((y2-y1)*(y2-y1))) < (.0000000001):     #distance formula.  check against squared dist
                        tooShortSet |= set( [ s[0] ] )
        if len( tooShortSet ) == 0:
                return segs

        # create a dict for too short mappings
        # will tell which endpoints should shift to which other end points
        snapDict = dict()
        for s in tooShortSet:
                snapDict[s[0]] = s[1]

        # loop over snap dict, condensing chains of too short segs
        chainConnect = True
        while chainConnect:
                chainConnect = False
                for k,v in snapDict.items():
                        if v in snapDict:
                                snapDict[k] = snapDict[v]
                                chainConnect = True

        # any segs with an endpoint on a too short seg gets snapped to its right end point
        # if a seg changes from left to right, we need to flip its label
        newSegs = []
        for s in segs:
                if s[0][0] in snapDict:
                        s = ((snapDict[s[0][0]], s[0][1] ),s[1],s[2])
                if s[0][1] in snapDict:
                        s = ((s[0][0], snapDict[s[0][1]] ), s[1], s[2])
                if s[0][1] < s[0][0]:
                        s = ((s[0][1], s[0][0]), s[2],s[1])
                newSegs.append( s )
        segs = [s for s in newSegs if s[0][0] != s[0][1] ]
        # make sure they are all left and remove dups
        segSet = set(segs)
#       for s in segs:
#               if s[0][0] <s[0][1]:
#                       segSet |= set([s])
#               else:
#                       segSet |= set( [((s[0][1], s[0][0]),s[1], s[2])] )
        segs = list(segSet)
        return segs
                        
def checkNumRobustnes( segs ):
        ''' 
        DO NOT USE!!!

        This function was intended to remove errors introduced by floating point rounding, but it takes a long time 
        to compute, and doesn't actually fix the main problems.

        INSTEAD.. use snapEndPoints()
         
        takes labeld segs (same structure as left halfsegs)
        '''
        #print 'start', len(segs)
        #get rid of any too short segs
        goodSegs = []
        for s in segs:
                #if the seg is < .0001 in len, get rid of it
                x1 = s[0][0][0]
                y1 = s[0][0][1]
                x2 = s[0][1][0]
                y2 = s[0][1][1]
                if (((x2-x1)*(x2-x1)) + ((y2-y1)*(y2-y1))) < (.0001*.0001):     #distance formula.  check against squared dist
                        continue
                goodSegs.append( s )
#       print 'GOODSEGS:', len( goodSegs )

        # make a list of all points
        allPoints = []
        for s in goodSegs:
                allPoints.append( s[0][0] )
                allPoints.append( s[0][1] )
        # sort the points
#       print 'sortnow'
        allPoints = sorted( allPoints )
#       print 'ALLPOINTS', len( allPoints )

        #remove duplicates
        noDupPoints = []
        for i in range( len( allPoints)-1 ):
                if allPoints[i] != allPoints[i+1]:
                        noDupPoints.append( allPoints[i] )
        if len(allPoints)>1:
                lastIndex = len(allPoints)-1
                if allPoints[lastIndex] != allPoints[lastIndex-1]:
                        noDupPoints.append( allPoints[lastIndex] )
        #print 'NODUPS', len(noDupPoints )
        # find all points that violate the closeness constraint
        badPoints = set()
        for i in range( len( noDupPoints ) ):
                x = noDupPoints[i][0]
                y = noDupPoints[i][1] 
                pointisgood = True
                
                if i > 0:
                        xn1 = noDupPoints[i-1][0] 
                        yn1 = noDupPoints[i-1][1]
                        if (((x-xn1)*(x-xn1)) + ((y-yn1)*(y-yn1))) < (.0001*.0001):     #distance formula.  check against squared dist
                                pointisgood = False
                if i < len(noDupPoints)-1:
                        x1 = noDupPoints[i+1][0] 
                        y1 = noDupPoints[i+1][1] 
                        if (((x-x1)*(x-x1)) + ((y-y1)*(y-y1))) < (.0001*.0001): #distance formula.  check against squared dist
                                pointisgood = False
                if not pointisgood:
                        badPoints.add( noDupPoints[i] )
#       print 'BADPOINTS', len( badPoints )
        #only keep segs that have both endpoints in goodPoints
        if len(badPoints) == 0:
                finalSegs = goodSegs
        else:
#               print 'goodsegs: ', len(goodSegs )
                finalSegs = [ s for s in goodSegs if s[0][0] not in badPoints and s[0][1] not in badPoints ]
#       print 'end', len(finalSegs)
        return finalSegs




def removeRandSegs( segs, percentToRemove = .05 ):
        '''
        Remove some segments at random from a list of segs.

        This is used by the generateRandomRegion functions to increase the amount of randomness.

        **input**:

        segs: a list of line segments, with the usual format: [((x1,y1),(x2,y2)),((x3,y3),(x4,y4)),...]

        percentToRemove:  A real number n such that 0 <= n <= 1 indicating the percentage of segments to remove.
        
        **output**: 

        a list of segs.
        '''
        if percentToRemove < 0 or percentToRemove >= 1:
                raise Exception( 'invalid percentage.  Value v should be 0 <= v < 1' )

        # remove 5% of the segs at random
        numToRemove = int( percentToRemove * len( segs ) )
        if numToRemove == 0:
                numToRemove = 1
        removeIndexes = [ random.randint(0, len(segs)-1-i ) for  i in range( numToRemove ) ]
        #       for i in range( numToRemove ):
        #           randIndex = random.randint(0, len(segs)-1-i )
        #                       removeIndexes.append( randIndex )
        removeIndexes.sort()
        for i in range( len(removeIndexes)-1,0, -1):
                segs.pop( removeIndexes[i] )

        #               segs[:] = [ item for index,item in enumerate( segs) if index not in removeIndexes]
        return segs

