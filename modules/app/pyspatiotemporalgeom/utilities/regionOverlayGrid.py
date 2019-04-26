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

from pyspatiotemporalgeom.utilities import segLibrary
import math
import bisect



def breakSegmentsRedBlue( r1, r2, cellsPerSeg = 3):
    '''
    Red Blue line intersection.  Self intersections in the red set or blue set are not discovered

    Given a bunch of line segments, break them at intersection points.  Handles overlapping segments appropriately (duplicates are removed).

    Input:

    r1
        A list of segments of the form ``((x1,y1),(x2,y2))``

    cellsPerSeg
        an integer indicating how many cells (roughly) a segment should fall into.  This is computed based on the average length of line segments in ``r1``.

    Output:

    A list of segments such that segments only overlap at end points.

    '''

    # While we have the segs, get the average size of a cell
    sumOfr1Len=0
    for s in r1:
        sumOfr1Len = sumOfr1Len + (((s[0][0]-s[1][0])*(s[0][0]-s[1][0]))+((s[0][1]-s[1][1])-(s[0][1]-s[1][1]))) 
    avgR1Len=math.sqrt( sumOfr1Len/len( r1 ))
    #print 'avg r1 len', avgR1Len
    sumOfr2Len=0
    for s in r2:
        sumOfr2Len = sumOfr2Len + (((s[0][0]-s[1][0])*(s[0][0]-s[1][0]))+((s[0][1]-s[1][1])-(s[0][1]-s[1][1]))) 
    avgR2Len=math.sqrt( sumOfr2Len/len( r2 ))
    #print 'avg r2 len', avgR2Len
    avgLen = math.sqrt( (sumOfr1Len+sumOfr2Len)/(len(r1)+len(r2)) )
    #print 'avg total len', avgLen
    
    # assign each segment roughly ``cellsPerSeg``
    cellSize = avgLen/cellsPerSeg

    #then give each seg an index
    # and reassign r1
    # we are also adding an integer to indicate if the interior
    indexedR1 = []
    indexedR2 = []
    for i in xrange( len( r1 ) ):
        indexedR1.append( (r1[i][0],r1[i][1],i) )
    r1 = indexedR1
    for i in xrange( len( r2 ) ):
        indexedR2.append( (r2[i][0],r2[i][1],i) )
    r2 = indexedR2
    
    # assign the cells
    cellDict1 = dict()
    cellDict2 = dict()
    usedCells1 = set()
    usedCells2 = set()

    assignCells( r1, cellSize, cellDict1, usedCells1 )
    assignCells( r2, cellSize, cellDict2, usedCells2 )

    usedCells = usedCells1 & usedCells2
    #print 'num used cells:', len( usedCells)
    
    #for keys in usedCells:
    #    print keys, '1 ' , cellDict1[keys], '2 ', cellDict2[keys]

    pois1 = []
    pois2 = []
    # look for the intersection points
    for key in usedCells:
        for s1 in cellDict1[key]:
            for s2 in cellDict2[key]:
                # compute intersection point.
                x1 = s1[0][0]
                y1 = s1[0][1]
                x2 = s1[1][0]
                y2 = s1[1][1]
                x3 = s2[0][0]
                y3 = s2[0][1]
                x4 = s2[1][0]
                y4 = s2[1][1]

                # check for colinear overlapping case
                if segLibrary.isCollinearAndOverlapping( s1, s2 ):
                        ll = x1
                        lu = x2
                        rl = x3
                        ru = x4
                        # if theya are near vertical, use the y vals
                        if abs( x1-x2) < 0.0000001:
                                ll = y1
                                lu = y2 
                                rl = y3 
                                ru = y4 
                        if rl < ll and ll < ru:
                                intersectPoi = (s2[2],(x1, y1))
                                pois2.append( intersectPoi )
                        if rl < lu and lu < ru:
                                intersectPoi = (s2[2],(x2, y2))
                                pois2.append( intersectPoi )
                        if ll < rl and rl < lu:
                                intersectPoi = (s1[2],(x3, y3))
                                pois1.append( intersectPoi )
                        if ll < ru and ru < lu:
                                intersectPoi = (s1[2],(x4, y4))
                                pois1.append( intersectPoi )
                        continue

                # if an end point is shared, no intersection
                if s1[0] == s2[0] or s1[0] == s2[1] or s1[1] == s2[0] or s1[1] == s2[1]:
                    continue

                denom = ((y4-y3)*(x2-x1)) - ((x4-x3)*(y2-y1))
                if denom == 0.0:   #lines are parallel, no intersection
                    continue

                ua = ((x4-x3)*(y1-y3))-((y4-y3)*(x1-x3))
                ua = ua / denom
                ub = ((x2-x1)*(y1-y3))-((y2-y1)*(x1-x3))
                ub = ub / denom
                # if we get here, the lines are not parallel.  they must intersect somewhere
                # check for intersections in a seg interior
                # record the segs so that we can construct the resulting segs
                if 0.0 < ua and ua < 1.0 and 0.0 <= ub and ub <= 1.0:
                        x = x1 + (ua * (x2-x1) )
                        y = y1 + (ua * (y2-y1) )
                        intersectPoi = (s1[2],(x, y))
                        if intersectPoi[1] != s1[0] and intersectPoi[1] != s1[1]:
                            pois1.append( intersectPoi )
                                
                if  0.0 < ub and ub < 1.0 and 0.0 <= ua and ua <= 1.0:
                        x = x1 + (ua * (x2-x1) )
                        y = y1 + (ua * (y2-y1) )
                        intersectPoi = (s2[2],(x, y))
                        if intersectPoi[1] != s2[0] and intersectPoi[1] != s2[1]:
                            pois2.append( intersectPoi )

    pois1 = list(set( pois1 ))
    pois2 = list(set( pois2 ))
    pois1.sort()
    pois2.sort()
    
    #print 'done intersect, now build'
    # build the resulting segs
    r1 = segLibrary.constructSegs( pois1, r1 )
    r2 = segLibrary.constructSegs( pois2, r2 )
    r1 = segLibrary.snapEndPoints( r1 )
    r2 = segLibrary.snapEndPoints( r2 )
    #print 'done build'
    return (r1,r2) 

def breakSegments( r1, cellsPerSeg = 3):
    '''
    
    given a bunch of line segments, break them at intersection points.  Handles overlapping segments appropriately (duplicates are removed).

    Input:

    r1
        A list of segments of the form ``((x1,y1),(x2,y2))``

    cellsPerSeg
        an integer indicating how many cells (roughly) a segment should fall into.  This is computed based on the average length of line segments in ``r1``.

    Output:

    A list of segments such that segments only overlap at end points.

    '''

    # make sure all segs have left most point first
    r1 = [  s if s[0] < s[1] else (s[1], s[0]) for s in r1 ]
    
    # get avg length of segs
    sumOfr1Len=0
    for s in r1:
        sumOfr1Len = sumOfr1Len + (((s[0][0]-s[1][0])*(s[0][0]-s[1][0]))+((s[0][1]-s[1][1])-(s[0][1]-s[1][1]))) 
    avgR1Len=math.sqrt( sumOfr1Len/len( r1 ))
    
    # assign each segment roughly ``cellsPerSeg``
    cellSize = avgR1Len/cellsPerSeg

    #then give each seg an index
    # and reassign r1
    # we are also adding an integer to indicate if the interior
    indexedR1 = []
    for i in xrange( len( r1 ) ):
        indexedR1.append( (r1[i][0],r1[i][1],i) )
    r1 = indexedR1
    
    # Assign the cells
    cellDict1 = dict()
    usedCells1 = set()
    assignCells( r1, cellSize, cellDict1, usedCells1 )

    # for any cells that have more than 1 seg, compute intersections among them

    pois1 = []
    # look for the intersection points
    for key in cellDict1:
        for i in range( len( cellDict1[key] )-1 ):
            for j in range(i+1, len( cellDict1[key] ) ):
                # compute intersection point.
                s1 = cellDict1[key][i]
                s2 = cellDict1[key][j]
                x1 = s1[0][0]
                y1 = s1[0][1]
                x2 = s1[1][0]
                y2 = s1[1][1]
                x3 = s2[0][0]
                y3 = s2[0][1]
                x4 = s2[1][0]
                y4 = s2[1][1]

                # check for colinear overlapping case
                if segLibrary.isCollinearAndOverlapping( s1, s2 ):
                        ll = x1
                        lu = x2
                        rl = x3
                        ru = x4
                        # if theya are near vertical, use the y vals
                        if abs( x1-x2) < 0.0000001:
                                ll = y1
                                lu = y2 
                                rl = y3 
                                ru = y4 
                        if rl < ll and ll < ru:
                                intersectPoi = (s2[2],(x1, y1))
                                pois1.append( intersectPoi )
                        if rl < lu and lu < ru:
                                intersectPoi = (s2[2],(x2, y2))
                                pois1.append( intersectPoi )
                        if ll < rl and rl < lu:
                                intersectPoi = (s1[2],(x3, y3))
                                pois1.append( intersectPoi )
                        if ll < ru and ru < lu:
                                intersectPoi = (s1[2],(x4, y4))
                                pois1.append( intersectPoi )
                        continue

                # if an end point is shared, no intersection
                if s1[0] == s2[0] or s1[0] == s2[1] or s1[1] == s2[0] or s1[1] == s2[1]:
                    continue

                denom = ((y4-y3)*(x2-x1)) - ((x4-x3)*(y2-y1))
                if denom == 0.0:   #lines are parallel, no intersection
                    continue

                ua = ((x4-x3)*(y1-y3))-((y4-y3)*(x1-x3))
                ua = ua / denom
                ub = ((x2-x1)*(y1-y3))-((y2-y1)*(x1-x3))
                ub = ub / denom
                # if we get here, the lines are not parallel.  they must intersect somewhere
                # check for intersections in a seg interior
                # record the segs so that we can construct the resulting segs
                if 0.0 < ua and ua < 1.0 and 0.0 <= ub and ub <= 1.0:
                        x = x1 + (ua * (x2-x1) )
                        y = y1 + (ua * (y2-y1) )
                        intersectPoi = (s1[2],(x, y))
                        if intersectPoi[1] != s1[0] and intersectPoi[1] != s1[1]:
                            pois1.append( intersectPoi )
                                
                if  0.0 < ub and ub < 1.0 and 0.0 <= ua and ua <= 1.0:
                        x = x1 + (ua * (x2-x1) )
                        y = y1 + (ua * (y2-y1) )
                        intersectPoi = (s2[2],(x, y))
                        if intersectPoi[1] != s2[0] and intersectPoi[1] != s2[1]:
                            pois1.append( intersectPoi )

    pois1 = list(set( pois1 ))
    pois1.sort()
    
    #print 'done intersect, now build'
    # build the resulting segs
    r1 = segLibrary.constructSegs( pois1, r1 )
    #print 'done build'

    r1 = segLibrary.snapEndPoints( r1 )
    return r1

def overlayHalfsegmentInput( r1, r2, cellsPerSeg = 3 ):
    ''' 
    A wrapper for ``def overlay(r1, r2, cellsPerSeg = 3 ):``

    This function accepts regions defined by a list of halfsegments.

    A halfsegment has the structure ``((x1, y1),(x2,y2),la, lb)`` where ``la`` and ``lb`` indicate if the interior if the region lies above or below the shalfsegment.  An interior label is greater than 0.  An exterior label is 0 or less.

    '''
    # first convert the hsegs to segs with an interiorBelow
    # flag (is the interior of the region below the seg
    r1 = [ (s[0][0],s[0][1],s[2]) for s in r1 if s[0][0] < s[0][1]]
    r2 = [ (s[0][0],s[0][1],s[2]) for s in r2 if s[0][0] < s[0][1]]
    return overlay( r1, r2, cellsPerSeg )

def overlay(r1, r2, cellsPerSeg = 3 ):
    '''
    Perform an overlay of r1 and r2
   
    .. warning::

        We assume the first end point in the tuple is less than the second.  Otherwise, the algorithm will not return correct results.

    Input:

    r1, r2
        A list of labeled segments.  Segments have the following structure:

        ``((x1,y1),(x2,y2),interiorBelow)`` where ``interiorBelow > 0`` if the interior of the region lies below the segment, ``< 0`` otherwise

    cellsPerSeg
        an integer indicating how many cells (roughly) a segment should fall into.  This is computed based on the average length of line segments in ``r1`` and ``r2``.

    Output:

    (resultR1, resultR2)
        A tuple containing two lists.  Each list is the respective input regions line segments broken where they intersect line segments from the other region.  Furthermore, each line segment carries a label consisting of a 1 or a 0 and boolean flag.  The boolean flag indicates if a line segment is equal to a line segment in the opposing result region.  The label indicates if the seg lies in the interior of the opposing region, or if it is equivalent to a line seg in the opposing region, if the interior of the opposing region lies below the seg.
    '''


    # While we have the segs, get the average size of a cell
    sumOfr1Len=0
    for s in r1:
        sumOfr1Len = sumOfr1Len + (((s[0][0]-s[1][0])*(s[0][0]-s[1][0]))+((s[0][1]-s[1][1])-(s[0][1]-s[1][1]))) 
    avgR1Len=math.sqrt( sumOfr1Len/len( r1 ))
    #print 'avg r1 len', avgR1Len
    sumOfr2Len=0
    for s in r2:
        sumOfr2Len = sumOfr2Len + (((s[0][0]-s[1][0])*(s[0][0]-s[1][0]))+((s[0][1]-s[1][1])-(s[0][1]-s[1][1]))) 
    avgR2Len=math.sqrt( sumOfr2Len/len( r2 ))
    #print 'avg r2 len', avgR2Len
    avgLen = math.sqrt( (sumOfr1Len+sumOfr2Len)/(len(r1)+len(r2)) )
    #print 'avg total len', avgLen
    
    # assign each segment roughly ``cellsPerSeg``
    cellSize = avgLen/cellsPerSeg

    #then give each seg an index
    # and reassign r1
    # we are also adding an integer to indicate if the interior
    indexedR1 = []
    indexedR2 = []
    for i in xrange( len( r1 ) ):
        indexedR1.append( (r1[i][0],r1[i][1],i,r1[i][2]) )
    r1 = indexedR1
    for i in xrange( len( r2 ) ):
        indexedR2.append( (r2[i][0],r2[i][1],i,r2[i][2]) )
    r2 = indexedR2
    
    # get the min/max x, y vals
    # xvals = [s[0][0] for s in r1] + [s[1][0] for s in r2]
    # xmin = min( xvals )
    # xmax = max( xvals )
    # yvals = [s[0][1] for s in r1] + [s[1][1] for s in r2]
    # ymin = min( yvals )
    # ymax = max( yvals )

    # xdif = xmax - xmin
    # ydif = ymax - ymin
    # cellSize = max( xdif,ydif ) * gridScalar
    
    # assign the cells
    cellDict1 = dict()
    cellDict2 = dict()
    usedCells1 = set()
    usedCells2 = set()

    assignCells( r1, cellSize, cellDict1, usedCells1 )

    assignCells( r2, cellSize, cellDict2, usedCells2 )

    usedCells = usedCells1 & usedCells2
    #print 'num used cells:', len( usedCells)
    #for keys in usedCells:
    #    print keys, '1 ' , cellDict1[keys], '2 ', cellDict2[keys]

    pois1 = []
    pois2 = []
    # look for the intersection points
    for key in usedCells:
        for s1 in cellDict1[key]:
            for s2 in cellDict2[key]:
                # compute intersection point.
                x1 = s1[0][0]
                y1 = s1[0][1]
                x2 = s1[1][0]
                y2 = s1[1][1]
                x3 = s2[0][0]
                y3 = s2[0][1]
                x4 = s2[1][0]
                y4 = s2[1][1]

                # check for colinear overlapping case
                if segLibrary.isCollinearAndOverlapping( s1, s2 ):
                        ll = x1
                        lu = x2
                        rl = x3
                        ru = x4
                        # if theya are near vertical, use the y vals
                        if abs( x1-x2) < 0.0000001:
                                ll = y1
                                lu = y2 
                                rl = y3 
                                ru = y4 
                        if rl < ll and ll < ru:
                                intersectPoi = (s2[2],(x1, y1))
                                pois2.append( intersectPoi )
                        if rl < lu and lu < ru:
                                intersectPoi = (s2[2],(x2, y2))
                                pois2.append( intersectPoi )
                        if ll < rl and rl < lu:
                                intersectPoi = (s1[2],(x3, y3))
                                pois1.append( intersectPoi )
                        if ll < ru and ru < lu:
                                intersectPoi = (s1[2],(x4, y4))
                                pois1.append( intersectPoi )
                        continue

                # if an end point is shared, no intersection
                if s1[0] == s2[0] or s1[0] == s2[1] or s1[1] == s2[0] or s1[1] == s2[1]:
                    continue

                denom = ((y4-y3)*(x2-x1)) - ((x4-x3)*(y2-y1))
                if denom == 0.0:   #lines are parallel, no intersection
                    continue

                ua = ((x4-x3)*(y1-y3))-((y4-y3)*(x1-x3))
                ua = ua / denom
                ub = ((x2-x1)*(y1-y3))-((y2-y1)*(x1-x3))
                ub = ub / denom
                # if we get here, the lines are not parallel.  they must intersect somewhere
                # check for intersections in a seg interior
                # record the segs so that we can construct the resulting segs
                if 0.0 < ua and ua < 1.0 and 0.0 <= ub and ub <= 1.0:
                        x = x1 + (ua * (x2-x1) )
                        y = y1 + (ua * (y2-y1) )
                        intersectPoi = (s1[2],(x, y))
                        if intersectPoi[1] != s1[0] and intersectPoi[1] != s1[1]:
                            pois1.append( intersectPoi )
                                
                if  0.0 < ub and ub < 1.0 and 0.0 <= ua and ua <= 1.0:
                        x = x1 + (ua * (x2-x1) )
                        y = y1 + (ua * (y2-y1) )
                        intersectPoi = (s2[2],(x, y))
                        if intersectPoi[1] != s2[0] and intersectPoi[1] != s2[1]:
                            pois2.append( intersectPoi )

    pois1 = list(set( pois1 ))
    pois2 = list(set( pois2 ))
    pois1.sort()
    pois2.sort()
    
    #print 'done intersect, now build'
    # build the resulting segs
    r1 = segLibrary.constructSegs( pois1, r1 )
    r2 = segLibrary.constructSegs( pois2, r2 )
    #print 'done build'
    r1 = segLibrary.snapEndPoints( r1 )
    r2 = segLibrary.snapEndPoints( r2 )
    
    if False:
        print 'result r1'
        r1.sort()
        for s in r1:
            print s

        print 'result r2'
        r2.sort()
        for s in r2:
            print s
    
    r1Final = computeTopology( r1, usedCells2, cellDict2, cellSize )
    r2Final = computeTopology( r2, usedCells1, cellDict1, cellSize )
    #print '--------------- done topo'
    if False:
        print 'result 1'
        r1Final.sort()
        for s in r1Final:
            print s

        print 'result 2'
        r2Final.sort()
        for s in r2Final:
            print s
    return (r1Final, r2Final)

def computeTopology( r1, usedCells2, cellDict2, cellSize ):
    '''

    This is meant to be called from the ``overlay`` function

    Computes the topolgy of r1 with respect to a region r2.  r2 is not passed directly; rather, a cell dictionary that maps cells to the segments that lie in that cell are passed.  Also, a set of cells that appear in cellDict2 (the keys of the dict) are passed.

    NOTE: ``cellSize`` should be the size used to create the ``cellDict2``

    INPUT:

    r1
        a list of segs where each seg is has an index, and a interiorBelow label:  ((x1,y1),(x2,y2),index,interiorBelow)

    usedCells2
        They keys of the cellDict2

    cellDict2
        A dict mapping a cell to the segs in that cell
    '''
    # figure out the topology
    # the segments in the cellDict contain an interiorBelow flag.
    # so we we can stop as soon as we find the nearest segment.
    
    # make a sorted list out of used cells
    cells2 = list( usedCells2 )
    cells2.sort()
    
    finalR1Segs = []
    # grab a seg, do the point in poly with it
    for s in r1:
        boundsOtherReg = False
        count = 0
        closestDistance = 999999999.0
        closestSlope = -999999999.0
        colinSeg = False
        # find the cell of its left end point:
        x0 = s[0][0]
        y0 = s[0][1]
        y1 = s[1][1]
        cellX = int (x0 // cellSize)  +1
        cellY = int (y0 // cellSize)  +1
        # if a left Y end point is on a cell boundary and 
        # the segs extends down, record the upper cell, and adust start
        if math.fmod(y0, cellSize) == 0.0 and y0 > y1:
            cellY -= 1
        # now we got the cell:
        #print '==========='
        #print 'seg, cell:', s , cellX, cellY
        # find the first occurrence of the cell in the list
        index = bisect.bisect_left( cells2, (cellX, cellY) )
        cells2Len = len( cells2)
        if index > 0 and index < cells2Len and cells2[index][0] > cellX:
            index -=1
        # now do a ray shoot down the column
        while not boundsOtherReg and closestDistance == 999999999.0 and index < cells2Len and index >=0 and cells2[index][0] == cellX:
            # find the closest spanning seg in the cell.
            # if cannot find one in this cell, continue to the next
            
            #print 'looking cell: ' , cells2[index]
            #examine each cell in the cell
            for s2 in cellDict2[cells2[index]]:
                #print 's: ', s, ' s2: ', s2
                
                # this test was to only look at a segment once if it is in multiple cells.
                # we no longer need the test with known input topology
                #if index > 0 and cells2[index-1][0] == cellX and s2 in cellDict2[cells2[index-1]]:
                #    continue
                s2IsVert =  s2[0][0] == s2[1][0]
                # if s2 is vertical
                if s2IsVert:
                    #print 'vert'
                    #skip it unless s1 is also vertical
                    if segLibrary.collinear( s, s2 ):
                        # if s[0] is on s2, then s bounds r2.  mark it accordingly
                        #print 'colin'
                        if s2[0][1] <= s[0][1] and s[0][1] < s2[1][1]:
                            #print 'spans!'
                            boundsOtherReg = True
                            # we can now definitively assign topology for this seg
                            count = 0
                            if s2[3] > 0:
                                # the interio of r2 lies below this seg
                                count = 1
                            break
                    else:
                        continue
                # here, s2 is not vertical
                # check the span
                if not( s2[0][0] <= s[0][0] and s[0][0]< s2[1][0] ):
                    #print 'no span'
                    continue
                # now we know the span is good
                # check colin
                if segLibrary.collinear( s, s2 ):
                    #print 'span colin'
                    boundsOtherReg = True
                    # we can now definitively assign topology for this seg
                    count = 0
                    if s2[3] > 0:
                        # the interio of r2 lies below this seg
                        count = 1
                    break
                # here they are not colinear.  check if s[0] is on s2
                checkPoint = s[0]
                endPointOnS2 = False
                turnVal =  segLibrary.collinearValue( s2[0], s2[1], checkPoint)
                if checkPoint == s2[0] or (-0.0000001 < turnVal and turnVal < 0.000001):
                    endPointOnS2 = True
                    checkPoint  = s[1]
                    turnVal =  segLibrary.collinearValue( s2[0], s2[1], checkPoint)
                    #print 'same endpoint'
                if turnVal > 0:
                    # we now have a seg in r2 that is below this seg.  we need to compute its distance
                    #print ' spans and s2 below'
                    if endPointOnS2:
                        # the end point is on s2, but s2 is below s1.
                        # distance is 0.  need to find if this is the nearest
                        # assign closest slope!
                        # we handle verticals seperately, so they are not a problem
                        # if the current closes dist is >0, then this is the closes we have seen so far
                        # otherwise, check the slope
                        thisSlope= (s2[1][1]-s2[0][1])/(s2[1][0]-s2[0][0])
                        if closestDistance > 0 or (closestDistance == 0 and thisSlope > closestSlope):
                            #print 'closest slope'
                            closestDistance = 0
                            closestSlope = thisSlope
                            # we can now  assign topology for this seg
                            #but it may get updated later
                            count = 0
                            if s2[3] <= 0:
                                # the interio of r2 lies below this seg
                                count = 1
                    elif closestDistance > 0:
                        # get the distance between the segs
                        # we have the left end point of s1.  
                        # get they y value of s2 at s1.x
                        # we know they span and s1.x is not on s2
                        x = s[0][0]
                        s2y = 0
                        if s[0][0] == s2[0][0]:
                            s2y = s2[0][1]
                        else:
                            s2y = ((s2[1][1]*x - s2[1][1]*s2[0][0]-s2[0][1]*x + s2[0][1]*s2[0][0]) / (s2[1][0]-s2[0][0]))+s2[0][1]
                        theDist = s[0][1]-s2y
                        #if theDist < 0:
                        #    print 'negative dist!!!'
                        #    exit()
                        theSlope = (s2[1][1]-s2[0][1])/(s2[1][0]-s2[0][0])
                        if theDist < closestDistance or (theDist == closestDistance and theSlope > closestSlope)  :
                            #print 'closest dist', s2[3]
                            closestDistance = theDist
                            closestSlope = theSlope
                            count = 0
                            if s2[3] <= 0:
                                #print 'count 1'
                                # the interio of r2 lies below this seg
                                count = 1

            index -= 1
        #print 'count', count
        finalR1Segs.append( (s, count, boundsOtherReg ) )
    return finalR1Segs


def assignCells( r1, cellSize, r1Dict, usedCellSet ):
    '''
        find cells using left hand turn test
    '''

    for s in r1:
        # print '-assign', s
        x1 = s[0][0]
        y1 = s[0][1]
        x2 = s[1][0]
        y2 = s[1][1]
    
        # get the starting and ending grids
        startGridX = int (x1 // cellSize) +1  
        startGridY = int (y1 // cellSize)  +1
        endGridX = int (x2 // cellSize)  +1
        endGridY = int (y2 // cellSize)  +1
        goingUp = True
        if y2-y1 < 0:
            goingUp = False
        x = startGridX
        y = startGridY

        while True:
            #print x,y,cellSize, x*cellSize, y*cellSize, endGridX, endGridY, goingUp
            # add the  grid
            if (x,y) not in r1Dict:
                r1Dict[(x,y)] = list()
            r1Dict[(x,y)].append( s )
            usedCellSet |= set( [(x,y)] )
            # check if we are on a boundary and add those cells
            addedLeft = False   # record if we added cell to left
            addedDown = False   # record if we added cell on bottom
            if math.fmod(x1, cellSize ) == 0.0:
                #print 'added', x-1,y
                addedLeft = True
                # x value is on a boundary.  it will be on the larger boundary 
                # (due to mod math), so we need to add the cell to the left
                if (x-1,y) not in r1Dict:
                    r1Dict[(x-1,y)] = list()
                r1Dict[(x-1,y)].append( s )
                usedCellSet |= set( [(x-1,y)] )
            # check if we add cell below because we are on the boundary
            # if line goes down, we might duplicate the seg in that cell.  CHECK BACK
            if math.fmod( y1, cellSize ) == 0.0:
                addedDown = True
                if (x,y-1) not in r1Dict:
                    r1Dict[(x,y-1)] = list()
                r1Dict[(x,y-1)].append( s )
                usedCellSet |= set( [(x,y-1)] )
                #print 'added', x,y-1
            # if we were on both the left and down boundary, we were on the corner! 
            # add the diagonal cell.
            if addedLeft and addedDown:
                if (x-1,y-1) not in r1Dict:
                    r1Dict[(x-1,y-1)] = list()
                r1Dict[(x-1,y-1)].append( s )
                usedCellSet |= set( [(x-1,y-1)] )
                #print 'added', x-1,y-1
            
            if x >= endGridX and ((goingUp and y >= endGridY) or (not goingUp and y<= endGridY)):
                break

            # figure out which cell to visit next
            # if the line goes next through the upper, lower, or left cells
            # then adjust accordingly. If it goes through the point to a diagonal
            # cell, go directly there, it will add the other cells based on the 
            # boundary mod math
            #So... first check the diagonal points
            diagX = x * cellSize
            diagHiY = y * cellSize
            diagLoY = (y-1) * cellSize
            # now see if our line goes through (diagX, diagHiY) or (diagX, diagLoY)
            colinValueHi = segLibrary.collinearValue( (x1,y1),(diagX, diagHiY), (x2,y2) )
            colinValueLo = segLibrary.collinearValue( (x1,y1),(diagX, diagLoY), (x2,y2) )
            if abs( colinValueHi ) < 0.0000001:
                # it goes through the upper diagonal
                x += 1
                y += 1
            elif colinValueHi > 0:
                # it goes through the upper cell bound
                y += 1
            elif abs( colinValueLo ) < 0.0000001:
                # it goes through the lower diagonal
                x += 1
                y -= 1
            elif colinValueLo > 0:
                # it goes through the right boundary
                x += 1
            else:
                # it goes through the lower boundary
                y -= 1
    #print 'dict:', r1Dict
    #print 'usedCell', usedCellSet

def assignCellsOld( r1, cellSize, r1Dict, usedCellSet):
    ''' 
    This is DEPRECATED.  do not use.  left over as a reference.
    
    Assign segments to cells.  Uses a modified Bresenham's algorithm

    r1
        list of segments defining regions

    cellSize
        size of a cell
    
    r1Dict
        Output value:  Modified by the function
        
        a dictionay of cell->list of segs. cell is just an x,y.  Segs are ((x1,y1),(x2,y2))

    usedCellsSet
        A set of cell addresses used.  Output value: Modified by the function.

    Notes:
        If a segment is placed in 2 adjacent cells in the Y direction, it will
        be placed in the uppermost cell once, and twice in the lower cells.
        This is so the ray shooting test will still work.
    '''

    # first get the bbox of the scene


    # now we know how big each grid cell should be
    # time to put segs in thier place
    # dict is cell to list of seg indexes mapping

    for s in r1:
        # get the cells

        # if the line is steep, switch the x's and y's
        isSteep = abs(s[1][1]-s[0][1] ) > abs( s[1][0]-s[0][0] )
        if not isSteep:
            x0 = s[0][0]
            y0 = s[0][1]
            x1 = s[1][0]
            y1 = s[1][1]
        else:
            x0 = s[0][1]
            y0 = s[0][0]
            x1 = s[1][1]
            y1 = s[1][0]


        # get the starting and ending grids
        startGridX = int (x0 // cellSize)  
        startGridY = int (y0 // cellSize)  
        endGridX = int (x1 // cellSize)  
        endGridY = int (y1 // cellSize)  
        
        #print '----- Assign seg: ', s, 'steep: ', isSteep 
        #print 'start xy end xy: ', startGridX, startGridY, endGridX, endGridY

        # we assume that portions of aline (end points for example) that 
        # are on a cell boundary are pushd *up* a cell.  This cuases 
        # a slight problem in calculations below, so go ahead and 
        # record the *up* cell, and then adjust the cell down

        # if a left Y end point is on a cell boundary and 
        # the segs extends down, record the upper cell, and adust start
        if math.fmod(y0, cellSize) == 0.0 and y0 > y1:
            if isSteep:
                if (startGridY, startGridX) not in r1Dict:
                    r1Dict[ (startGridY, startGridX) ] = list()
                r1Dict[ (startGridY, startGridX) ].append( s )
                usedCellSet |= set( [(startGridY, startGridX)] )
                #print 'added 1', startGridY, startGridX
            else:
                if (startGridX, startGridY) not in r1Dict:
                    r1Dict[ (startGridX, startGridY) ] = list()
                r1Dict[ (startGridX, startGridY) ].append( s )
                usedCellSet |= set( [(startGridX, startGridY)] )
                #print 'added 1', startGridX, startGridY
            startGridY -= 1


        # if the X value of the right end point is on a boundary, record
        # the *up* (in this case *right* ) cell, then adjust end
        if math.fmod(x1, cellSize) == 0:
            if isSteep:
                if (endGridY, endGridX) not in r1Dict:
                    r1Dict[ (endGridY, endGridX) ] = list()
                r1Dict[ (endGridY, endGridX) ].append( s )
                usedCellSet |= set( [(endGridY, endGridX)] )
                #print 'added 2', endGridY, endGridX
            else:
                if (endGridX, endGridY) not in r1Dict:
                    r1Dict[ (endGridX, endGridY) ] = list()
                r1Dict[ (endGridX, endGridY) ].append( s )
                usedCellSet |= set( [(endGridX, endGridY)] )
                #print 'added 2', endGridX, endGridY 
            endGridX -= 1

        # now the main loop. 
       
       
        # !!!! This was an error in the c++ version   !!!!
        # !!!! that resulted in missing intersections !!!!
        # becuase we switch the Xs and Ys for steeps,
        # startGridX might be greater than endGridX
        # The loop below this wants to loop *up*
        # (range(3,1) returns a an empty list!)
        if endGridX < startGridX:
            startGridX, endGridX = endGridX, startGridX
            startGridY, endGridY = endGridY, startGridY 

        # get some numbers to check if extra cells need to be added 
        # so we don't have to worry about rounding so much.
        if y0 == y1:
            error = 0
        else:
            error = (y0 - ((startGridY * cellSize) + (cellSize / 2))) / cellSize
        if x0 == x1:
            slope = 0
        else: 
            slope = (y1 - y0) / (x1 - x0)
        currentY = startGridY
        
        #print 'startx, endx', startGridX, endGridX
        #print 'starty, endy', startGridY, endGridY
        for currentX in xrange( startGridX, endGridX ):
            #print 'currx curry', currentX, currentY
            if isSteep:
                # insert the segment
                if (currentY, currentX) not in r1Dict:
                    r1Dict[ (currentY, currentX) ] = list()
                r1Dict[ (currentY, currentX) ].append( s )
                usedCellSet |= set( [(currentY, currentX)] )
                #print 'added 3', currentY, currentX
                # check if additional cell should be added
                if slope < 0 and error < 0:
                    currentY -= 1
                    if (currentY, currentX) not in r1Dict:
                        r1Dict[ (currentY, currentX) ] = list()
                    r1Dict[ (currentY, currentX) ].append( s )
                    usedCellSet |= set( [(currentY, currentX)] )
                    #print 'added 4', currentY, currentX
                    currentY += 1
                if slope > 0 and error > 0:
                    currentY += 1
                    if (currentY, currentX) not in r1Dict:
                        r1Dict[ (currentY, currentX) ] = list()
                    r1Dict[ (currentY, currentX) ].append( s )
                    usedCellSet |= set( [(currentY, currentX)] )
                    #print 'added 5', currentY, currentX
                    currentY -= 1
            else:
                # same thig but for NOT steeps
                # insert the segment
                if (currentX, currentY) not in r1Dict:
                    r1Dict[ (currentX, currentY) ] = list()
                r1Dict[ (currentX, currentY) ].append( s )
                usedCellSet |= set( [(currentX, currentY)] )
                #print 'added 6', currentX, currentY
                # check if additional cell should be added
                if slope > 0 and error > 0:
                    currentY += 1
                    if (currentX, currentY) not in r1Dict:
                        r1Dict[ (currentX, currentY) ] = list()
                    r1Dict[ (currentX, currentY) ].append( s )
                    usedCellSet |= set( [(currentX, currentY)] )
                    #print 'added 7', currentX, currentY
                    currentY -= 1
                if slope < 0 and error < 0:
                    currentY -= 1
                    if (currentX, currentY) not in r1Dict:
                        r1Dict[ (currentX, currentY) ] = list()
                    r1Dict[ (currentX, currentY) ].append( s )
                    usedCellSet |= set( [(currentX, currentY)] )
                    #print 'added 8', currentX, currentY
                    currentY += 1
            error += slope
            if slope > 0 and error > 0.5:
                # adjust Y up
                error -= 1
                currentY += 1
            elif slope < 0 and error < -0.5:
                error += 1
                currentY -= 1

        # handle the last cell
        if isSteep:
            if (currentY, endGridX) not in r1Dict:
                r1Dict[ (currentY, endGridX) ] = list()
            r1Dict[ (currentY, endGridX) ].append( s )
            usedCellSet |= set( [(currentY, endGridX)] )
            #print 'added 9', currentY, endGridX
        else:
            if (endGridX, currentY) not in r1Dict:
                r1Dict[ (endGridX, currentY) ] = list()
            r1Dict[ (endGridX, currentY) ].append( s )
            usedCellSet |= set( [(endGridX, currentY)] )
            #print 'added 10', endGridX, currentY


        
if __name__ == "__main__":
    
    import pyspatiotemporalgeom.region as region
    r3 = [((1,2),(5,2)),((1,2),(4,4)),((4,4),(5,2))] 
    r4 = [((1,1),(6,1)),((1,1),(3,5)),((3,5),(6,1))] 
    r5 = [((2,2),(8,3)),((8,3),(8,8)),((8,8),(2,8)),((2,8),(4,4)),((4,4),(2,2))] 
    r6 = [((3,7),(4,5)),((4,5),(8,5)),((8,5),(8,4)),((8,4),(9,4)),((9,4),(8,6)),((8,6),(8,7)),((8,7),(7,8)),((7,8),(5,8)),((5,8),(3,7))] 
    
    r1 = [((1,1),(2,7)),((2,7),(10,1)),((10,1),(1,1))] 
    r2 = [((1,1),(6,1)),((1,1),(3,5)),((3,5),(6,1))] 
    r1 = region.createRegionFromSegs( r5 )
    r2 = region.createRegionFromSegs( r6 )
    print 'genr1'
    r1 = region.getRandomRegion( 500 )
    print 'genr2'
    r2 = region.getRandomRegion( 500 )
    print 'length of input regions (number of halfsegments)'
    print len( r1 ), ' ', len(r2 )

    PRINTOUT = True
    print 'inter'
    result = region.intersection( r1, r2 )
    # if PRINTOUT:
    #     for s in result:
    #         print s
    exit( )
    
    
    print 'overlay regions'
    result = overlayHalfsegmentInput( r1, r2, 3 )
    exit()
    res1 = result[0]
    res1.sort()
    res2 = result[1]
    res2.sort()
    result = (res1,res2)
    if PRINTOUT:
        for s in result:
            for x in s:
                print x
    

    r1 = [ s[0] for s in r1 if s[0][0] < s[0][1] ] 
    r2 = [ s[0] for s in r2 if s[0][0] < s[0][1] ] 
    
    print 'red/blue intersection'
    res1,res2 = breakSegmentsRedBlue( r1, r2, 3 )
    if PRINTOUT:
        print 'r1'
        res1.sort()
        for s in res1:
            print s
        print 'r2'
        res2.sort()
        for s in res2:
            print s

    
    r1 = r1+r2
    print 'breaking segs'
    res = breakSegments( r1, 3)
    if PRINTOUT:
        res.sort()
        for s in res:
            print s



#Here is the old version of the topology computiation.  It ray shoots
#across th entire scene.
def computeTopologyOld( r1, usedCells2, cellDict2, cellSize ):
    # figure out the topology
    # the segments in the cellDict contain an interiorBelow flag.
    # so we we can stop as soon as we find the nearest segment.
    
    # make a sorted list out of used cells
    cells2 = list( usedCells2 )
    cells2.sort()
    
    finalR1Segs = []
    # grab a seg, do the point in poly with it
    for s in r1:
        boundsOtherReg = False
        count = 0
        colinSeg = False
        # find the cell of its left end point:
        x0 = s[0][0]
        y0 = s[0][1]
        y1 = s[1][1]
        cellX = int (x0 // cellSize)  
        cellY = int (y0 // cellSize)  
        # if a left Y end point is on a cell boundary and 
        # the segs extends down, record the upper cell, and adust start
        if math.fmod(y0, cellSize) == 0.0 and y0 > y1:
            cellY -= 1
        # now we got the cell:
        #print '==========='
        #print 'seg, cell:', s , cellX, cellY
        # find the first occurrence of the cell in the list
        index = bisect.bisect_left( cells2, (cellX, cellY) )
        cells2Len = len( cells2)
        if index > 0 and index < cells2Len and cells2[index][0] > cellX:
            index -=1
        # now do a ray shoot down the column
        while index < cells2Len and index >=0 and cells2[index][0] == cellX:
            #print 'looking cell: ' , cells2[index]
            #examine each cell in the cell
            for s2 in cellDict2[cells2[index]]:
                #print 's2: ', s2
                
                # this test was to only look at a segment once if it is in multiple cells.
                # we no longer need the test with known input topology
                if index > 0 and cells2[index-1][0] == cellX and s2 in cellDict2[cells2[index-1]]:
                    continue
                s2IsVert =  s2[0][0] == s2[1][0]
                # if s2 is vertical
                if s2IsVert:
                    #print 'vert'
                    #skip it unless s1 is also vertical
                    if segLibrary.collinear( s, s2 ):
                        # if s[0] is on s2, then s bounds r2.  mark it accordingly
                        #print 'colin'
                        if s2[0][1] <= s[0][1] and s[0][1] < s2[1][1]:
                            #print 'spans!'
                            boundsOtherReg = True
                            continue
                    else:
                        continue
                # here, s2 is not vertical
                # check the span
                if not( s2[0][0] <= s[0][0] and s[0][0]< s2[1][0] ):
                    #print 'no span'
                    continue
                # now we know the span is good
                # check colin
                if segLibrary.collinear( s, s2 ):
                    #print 'span colin'
                    boundsOtherReg = True
                    continue
                # here they are not colinear.  check if s[0] is on s2
                checkPoint = s[0]
                turnVal =  segLibrary.collinearValue( s2[0], s2[1], checkPoint)
                if checkPoint == s2[0] or (-0.0000001 < turnVal and turnVal < 0.000001):
                    checkPoint  = s[1]
                    turnVal =  segLibrary.collinearValue( s2[0], s2[1], checkPoint)
                    #print 'same endpoint'
                if turnVal > 0:
                    # make sure we only count the seg once.  only count it
                    # if the intersection of a vertical and this one occurs in
                    # the cell.
                    #print 'LHT!'
                    count += 1
            index -= 1
        #print 'count', count
        finalR1Segs.append( (s, count % 2, boundsOtherReg ) )
    return finalR1Segs

