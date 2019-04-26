# Copyright (c) 2014 Mark McKenney
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
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




'''
intervalRegion.py
  
Code to define and manipulate interval regions

'''

from pyspatiotemporalgeom.utilities import segLibrary
from pyspatiotemporalgeom.utilities import triangleLibrary
import pyspatiotemporalgeom.region as region
import traceback


def getRegionAtTime(intervalRegion, time):
    '''
    Extract a region from an interval region.

    **Input:**

    + `intervalRegion`:  a valid interval region.  For example, one generated with http://www.cs.siue.edu/~marmcke/docs/pyspatiotemporalgeom/highLevelModules.html#pyspatiotemporalgeom.intervalRegion.interpolateRegions
    + `time`: A time value (floating point number)

    **Output:**

    + a list of segments where segments have the type: :math:`((x1,y1),(x2,y2))`.  The segments will form a valid region.
    '''
    tri = intervalRegion
    lineSegs = []
    min_time = 0.0
    max_time = 0.0
    time1 = 0.0
    time2 = 0.0
    time3 = 0.0
    calculatedDiff = 0.0
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0

    triangle = tri[0]
    time1 = triangle[0][2]
    time2 = triangle[1][2]
    time3 = triangle[2][2]

    # get min and max time
    min_time = min(time1, time2, time3)
    max_time = max(time1, time2, time3)

    # take care of the edge cases
    if time == min_time:
        for t in tri:
            if t[0][2] == min_time:
                lineSegs.append(( (t[0][0], t[0][1]), (t[1][0], t[1][1]) ))
        return lineSegs

    if time == max_time:
        for t in tri:
            if t[0][2] == max_time:
                lineSegs.append(( (t[0][0], t[0][1]), (t[1][0], t[1][1]) ))
        return lineSegs

    if max_time < time or min_time > time:
        print("Invalid time range for triangle")
        return lineSegs

    # get time difference
    timeDiff = max_time - min_time
    # get scaled time; the result is a percentage 	e.g.) 0.10
    multiplier = round((time - min_time) / float(timeDiff), 2)

    for t in tri:
        s1 = (t[2], t[0])
        s2 = (t[2], t[1])
        if t[0][2] < t[2][2]:  #make sure lower z value is 1st in the seg
            s1 = (t[0], t[2])
            s2 = (t[1], t[2])
        x1 = ((s1[1][0] - s1[0][0]) * multiplier) + s1[0][0]
        y1 = ((s1[1][1] - s1[0][1]) * multiplier) + s1[0][1]
        x2 = ((s2[1][0] - s2[0][0]) * multiplier) + s2[0][0]
        y2 = ((s2[1][1] - s2[0][1]) * multiplier) + s2[0][1]
        # add line segment
        lineSegs.append(((x1, y1), (x2, y2)))

    return lineSegs


from pyspatiotemporalgeom.utilities import regionInterpolator


def interpolateRegions(region1, region2, startTime, endTime, noTriIntersectionChecks=False):
    '''
    This is just a wrapper that calls ``pyspatiotemporalgeom.utilities.regionInterpolater.interpolate()``.  The documentation for that function is copied here:

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
    return regionInterpolator.interpolate(region1, region2, startTime, endTime, noTriIntersectionChecks)


def getTemporalCoverageGeometriesAndTimes(intervalRegion, endPoints = None):
    '''
    Compute temporal coverage geometries and their associated times.  Currently, only constructs point geomoetries, but this will change in future releases.

    See the following paper for details:

    M. McKenney, R. Frye, Z. Benchly, and L. Maughan, "Temporal Coverage Aggregates Over Moving Region Streams." IWGS at 22nd ACM SIGSPATIAL International Symposium on Advances in Geographic Information Systems, November 2014, Dallas, TX, USA f

    **Input:**

    + intervalRegion:  A list of triangles such that triangles have the format: :math:`((x1,y1,z1),(x2,y2,z2),(x3,y3,z3))` and :math:`z1=z2`.  The triangles must form a valid interval region; for example, an interval region returned by the function: pyspatiotemporalgeom.intervalRegion.interpolateRegions(region1, region2, startTime, endTime, noTriIntersectionChecks=False) (http://www.cs.siue.edu/~marmcke/docs/pyspatiotemporalgeom/highLevelModules.html#pyspatiotemporalgeom.intervalRegion.interpolateRegions)

    **Output:**

    A `dict()` mapping points to a list of durations that the particular point is covered by the interval region (if the duration is non-zero)

    '''

    DEBUG = False
    #MM project out of time
    triangles = intervalRegion
    projectedSegs = []
    for tri in triangles:
        projectedSegs.append(((tri[0][0], tri[0][1]), (tri[1][0], tri[1][1])))
        projectedSegs.append(((tri[0][0], tri[0][1]), (tri[2][0], tri[2][1])))
        projectedSegs.append(((tri[1][0], tri[1][1]), (tri[2][0], tri[2][1])))

    #MM get the min and max Z values
    zList = [tri[0][2] for tri in triangles]
    zList.extend([tri[1][2] for tri in triangles])
    zList.extend([tri[2][2] for tri in triangles])
    zSet = set(zList)

    # get min and max z values
    minIntervalTime = min(zSet)
    maxIntervalTime = max(zSet)
    minZ = minIntervalTime - 1
    maxZ = maxIntervalTime + 1

    # get non intersecting segments
    NonIntersectingSegs = segLibrary.calcNonIntersectingSegs(projectedSegs, None, None)

    if endPoints == None:
      endPoints = []
      # MM end points should just be end points.  lets call things what they are
      for x in NonIntersectingSegs:
        endPoints.append((x[0][0], x[0][1]))
        endPoints.append((x[1][0], x[1][1]))
        #MM get rid of duplicate points (using a set)
      endPoints = list(set(endPoints))
      #MM now we have the end points.  lets make the rays

    rays = []
    for e in endPoints:
      rays.append(((e[0], e[1], minZ), (e[0], e[1], maxZ)))

    #MM now we have the end points and rays.  lets print them out
    if DEBUG:
        raysFile = open('zrays.txt', 'w')
        for r in rays:
            raysFile.write(str(r[0][0]) + ' ' + str(r[0][1]) + ' ' + str(r[0][2]) + ' ' + str(r[1][0]) + ' ' + str(
                r[1][1]) + ' ' + str(r[1][2]) + '\n')
        raysFile.close()
        epFile = open('zendPoints.txt', 'w')
        for e in endPoints:
            epFile.write(str(e[0]) + ' ' + str(e[1]) + ' ' + str(e[0]) + ' ' + str(e[1]) + '\n')
        epFile.close()

    #MM Now we do the ray triangle intersection
    #MM first find ALL intersection points
    intersectionPoints = []
    for ray in rays:
        # for all rays, we need to keep the intersection points at the temporal boundaries.
        # This allows to test if a ray pierces the interior of an intervel boundary region
        # without intersecting a traingle.  So, for every ray, just add those at the beginning.
        # duplicate points get removed later.
        intersectionPoints.extend([(ray[0][0], ray[0][1], minIntervalTime), (ray[0][0], ray[0][1], maxIntervalTime)])
        for tri in triangles:
            result = triangleLibrary.verticalSegment3DAndTriangle3DIntersection(ray, tri)
            if len(result) > 0:
                intersectionPoints.extend(result)

    #MM remove duplicates
    intersectionPoints = list(set(intersectionPoints))
    #MM sort them.  results in points sorted by time
    intersectionPoints.sort()

    if DEBUG:
        print '\n\nINTERPOINTS\n', intersectionPoints

    #MM last thing. We are getting some intersection point duplicates due to rounding errors.  Remove those
    # JM - this is a problem with trying to get time for the sorted points list
    keepList = [intersectionPoints[0]]

    for p1 in intersectionPoints:
        p = keepList[len(keepList) - 1]
        if p[0] == p1[0] and p[1] == p1[1] and (p1[2] - p[2] <= 0.0000001 and p1[2] - p[2] >= -0.0000001):
            continue
        keepList.append(p1)
    # end for loop

    intersectionPoints = keepList

    if DEBUG:
        print '\n\nkeep points\n', intersectionPoints


    #MM HERE IS WHERE THE BIG WORK BEGINS.
    # for each pair of intersection points that match on X and Y, and are temporally adjacent in Z,
    #   get a point in between the Z vals.
    #   Extract the region at that Z val
    #   perform point in poly

    # JM - start here with the refactor
    # get the appropriate points.  We will use a tuple that contains:
    # the X,Y values of the point, the Z val to do the point in poly test at.  The zVals of the adjacent points.
    testList = []
    for i in range(len(intersectionPoints) - 1):
        p = intersectionPoints[i]
        p1 = intersectionPoints[i + 1]
        if p[0] == p1[0] and p[1] == p1[1]:
            # would show multiple times with different z values
            # print p
            testList.append((p[0], p[1], (p[2] + ((p1[2] - p[2]) / 2)), p[2], p1[2]))

    if DEBUG:
        print '\n\ntestList: \n:', testList

    if DEBUG:
        print 'Point in polygon on all points\n\n'

    pointToTimeDict = getPointToTimeDictionary(triangles, testList)

    # MM -- The geometry calculations work until here.  At this point, the problem seems that the ray/tri intersections returned incorrect Z values for many intersections.
    # MM -- Fixed above line.  There were some ordering issues and calculation issues in getRegionAtTime and at the seg3d/verticalseg3d intersection function.  fixed now.
    if DEBUG:
        # MM print the dict!
        print '\n\nTotalTimes:'
        for x in pointToTimeDict.items():
            print x
        print '\n\n'
        triFile = open('ztriFile3d.txt', 'w')
        # JM append triangles to file
        for tri in triangles:
            s = str(tri[0][0]) + ' ' + str(tri[0][1]) + ' ' + str(tri[0][2]) + ' ' + str(tri[1][0]) + ' ' + str(
                tri[1][1]) + ' ' + str(tri[1][2]) + '\n'
            triFile.write(s)

            s = str(tri[0][0]) + ' ' + str(tri[0][1]) + ' ' + str(tri[0][2]) + ' ' + str(tri[2][0]) + ' ' + str(
                tri[2][1]) + ' ' + str(tri[2][2]) + '\n'
            triFile.write(s)

            s = str(tri[1][0]) + ' ' + str(tri[1][1]) + ' ' + str(tri[1][2]) + ' ' + str(tri[2][0]) + ' ' + str(
                tri[2][1]) + ' ' + str(tri[2][2]) + '\n'
            triFile.write(s)
        triFile.write('E\n')
        # JM append all test points to file
        for point in testList:
            print 'here ', point
            s = str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + ' '
            # JM incremented the points by 2 so they show up on the 3D plot
            s += str(point[0] + 2) + ' ' + str(point[1] + 2) + ' ' + str(point[2] + 2) + '\n'
            triFile.write(s)
        triFile.close()
    return pointToTimeDict


def maxPointCoverage(points):
    '''
    This returns the point or points with the maximum coverage time.

    **Input:**

    + `points`: the points to be checked

    **Output:**

    + a list of points that cover the maximum coverage
    '''
    maxPoints = []
    maxValue = 0
    for item in points:
        if (item[1][0] >= maxValue):
            maxValue = item[1][0]
    for item in points:
        if (item[1][0] == maxValue):
            maxPoints.append[item]
    return maxPoints


def minPointCoverage(points):
    '''
    This returns the point or points with the minimum coverage time.

    **Input:**

    + `points`: the points to be checked

    **Output:**

    + a list of points that cover the minimum coverage
    '''
    minPoints = []
    minValue = 0
    for item in points:
        if (item[1][0] <= minValue):
            minValue = item[1][0]
    for item in points:
        if (item[1][0] == minValue):
            minPoints.append[item]
    return minPoints


def findWhatLineIntersectionPointBelongsTo(points, segs):
    '''
    Figures out what points come from what segments

    **Input:**

    + `points`: List of points to check
    + `segs`: List of segments

    **Output:**

    + a list of points that pass the collinear value tests
    '''
    passedPoints = []
    for point in points:
        for seg in segs:
            # left turn check
            collinearValue = segLibrary.collinearValue(seg[1], seg[2], point)
            # check collinearValue
            if collinearValue >= -0.0001 and collinearValue <= 0.0001 \
                    and min(seg[1][0], seg[2][0], point[0]) != point[0] \
                    and max(seg[1][0], seg[2][0], point[0]) != point[0]:
                passedPoints.append((seg[0], point))
    # JM - remove duplicates
    sortedPoints = list(set(passedPoints))
    return sortedPoints


def getPointToTimeDictionary(tris, intersectionPointList, DEBUG=False):
    '''
    Appends time with corresponding points and returns the points as a dictionary (if the points pass the polygon test)

    **Input:**

    + `tris`:
    + `intersectionPointList`: List of intersection points

    **Output:**

    + a dictionary of intersection points with times
    '''

    # MM HERE --  actually do the point in  poly tests and count up the time covered. testPoints has everything we need
    # check time before or after calculation
    pointToTimeDict = dict()
    for i, point in enumerate(intersectionPointList):
        # JM get list of line segs at the time specified (point[2])
        lineSegs = getRegionAtTime(tris, point[2])
        # JM test the point
        inOrOut = region.pointInPolygon(point[0], point[1], lineSegs)
        if DEBUG:
            # now we output some points and some polys to test:
            tmpFile = open('zpip' + str(inOrOut) + str(i) + '.txt', 'w')
            print '----', i, inOrOut, lineSegs
            tmpFile.write(str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[0]) + ' ' + str(point[1]) + '\n')
            for s in lineSegs:
                tmpFile.write(str(s[0][0]) + ' ' + str(s[0][1]) + ' ' + str(s[1][0]) + ' ' + str(s[1][1]) + '\n')
            tmpFile.close()
        # if test passes, add up time
        if inOrOut == True:
            if point not in pointToTimeDict:
                pointToTimeDict[(point[0], point[1])] = []
            pointToTimeDict[(point[0], point[1])].append((point[4] - point[3]))

    return pointToTimeDict

