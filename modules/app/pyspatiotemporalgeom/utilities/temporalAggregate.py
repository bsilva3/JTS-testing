# Copyright (c) 2014 Mark McKenney
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
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


import pyspatiotemporalgeom.region as region
import pyspatiotemporalgeom.intervalRegion as intervalRegion
from pyspatiotemporalgeom.utilities import hsegLibrary

# DEBUG
#import matplotlib.pyplot as plt
#from mplot3d.axes3d import Axes3D
#import matplotlib.lines as mlines
#from matplotlib.colors import colorConverter
#from mplot3d.art3d import Poly3DCollection
#from matplotlib.collections import PolyCollection, LineCollection


def createProjectedSegsWithIDs(triangles):
    '''
    Extracts segments out of the given triangles and assigns a numeric value to each segment

    **Input:**

    + `triangles`:

    **Output:**

    + a list of segments that have a unique identifier
    '''
    projectedSegs = []
    segID = 0
    for tri in triangles:
        projectedSegs.append((segID, (tri[0][0], tri[0][1]), (tri[1][0], tri[1][1])))
        segID += 1
        projectedSegs.append((segID, (tri[0][0], tri[0][1]), (tri[2][0], tri[2][1])))
        segID += 1
        projectedSegs.append((segID, (tri[1][0], tri[1][1]), (tri[2][0], tri[2][1])))
        segID += 1

    return projectedSegs


def createIntervalRegionAndComputeTemporalAggregate(R1,R2):
    '''
    Interpolate regions R1,R2.  Use 1 of the interval regions returned from the interpolate function to call the aggregate function.
    
    Get the points with maximal coverage.Find if it contains cycles.
    
    Extracts points with maximum coverage,segments that are not part of cycles,cycles with maximal temporal coverage for the given regions if present
    
    *input*:
    
        **R1,R2**: two regions which are an ordered list of half segments with valid labels.  
                 
                    A **half segment** is a tuple with the following:
                      ((x,y)(x,y), labelAbove, labelBelow)
                     
                     labels are integral values
                     
                     an interior label will be positive.  An exterior label will be -1.  The side of the hseg
                     on which the interior (exterior) of the region lies will have an interior (exterior) label.
                 
                 hsegs will be ordered in half segment order
                 
                 Each cycle in hsegs will have its own unique label number
    
    *returns*:
    
       **tuple**: tuple consists of the :
                    1. points with maximum duration :
                        [((x,y),[z]),((x,y),[z])..] if present else ['None']

                    2. segments that are not part of cycles :
                         [((x1,y1),(x2,y2)),((x1,y1),(x2,y2))..] if present else ['None']

                    3. cycles with maximum duration. 
                         [((x,y)(x,y), labelAbove, labelBelow)..] if present else ['None']
    
    '''
    
    #print 'interpolating regions'
    arr = intervalRegion.interpolateRegions(R1, R2, 0, 100);
    #print arr
    triangles = []
    
    # MM extend the list so we do not end up with a bunch of sublists
    triangles.extend(arr[1])  
    #print triangles
    
    # MM this should get some intersection points
    #print 'compute the coverage aggregates:'
    point2DurationDict = intervalRegion.getTemporalCoverageGeometriesAndTimes(triangles)

    # create projected segments with IDs to help identify where intersection points come from
    projectedSegsWithIDs = createProjectedSegsWithIDs(triangles)
        
    # find what segments the points come from
    # after getting the points, sort the list
    pointsWithSegIDs = intervalRegion.findWhatLineIntersectionPointBelongsTo(point2DurationDict, projectedSegsWithIDs)
    pointsWithSegIDs.sort()
    
    # this is where the slope is calculated
    # the slopes will be used to sort by the points by x or y
    segsWithIDsAndSlopes = []
    for seg in projectedSegsWithIDs:
        rise = (seg[2][1] - seg[1][1])
        run = (seg[2][0] - seg[1][0])
        if run == 0:
            #print 'Run is 0'
            continue
        slope = rise / run
        segsWithIDsAndSlopes.append((seg[0], slope))
    
    # points is used function input
    points = point2DurationDict.items()
    #print points
    maxPoints = []
    minPoints = []

    # find max
    #print("\nMax")
    maxValue = 0
    for item in points:  #this will set the max value
        if (item[1][0] >= maxValue):
            maxValue = item[1][0]
    for item in points:  #this will display the max values
        if (item[1][0] == maxValue):
            maxPoints.append(item)
            #print item
    #print("\n")

    #print("\nMin")
    minValue = 100
    for item in points:  #this will set the min value
        if (item[1][0] <= minValue and item[1][0] > 0):
            minValue = item[1][0]
    for item in points:  #this will display the min values
        if (item[1][0] == minValue):
            minPoints.append(item)
            #print item
    
    max_points_return_val=[]
    if maxPoints :
        max_points_return_val=[maxPoints]
    else :
        max_points_return_val=['None']
            
    # finding the segments for max points        
    maxPointsWithSegs=[] 
    maxPoiNotFound=[]      
    for points in maxPoints :
        flag=0
        for p in pointsWithSegIDs :
            if p[1][0] == points[0][0] and p[1][1] == points[0][1] :
                maxPointsWithSegs.append((p[0],points))  
                flag=1      
        if flag != 1 :
            maxPoiNotFound.append(points)
    #print 'max points with segments='
    maxPointsWithSegs.sort()
    
    # If max points are not found in pointsWithSedIDs then search in projectedSegsWithIDs
    for m in maxPoiNotFound:
        for pr in projectedSegsWithIDs :
            if (pr[1][0] == m[0][0] and pr[1][1] == m[0][1]) or (pr[2][0] == m[0][0] and pr[2][1] == m[0][1]) :
                maxPointsWithSegs.append((pr[0],m))
                
    #print "maxpoints=",maxPointsWithSegs    
    
    # this is where the slopes are put into play
    # all the points with the same seg id will be put into a temp list
    # depending on the slope of the segment, the list will be sorted by x or y
    sortedPoints = []
    for seg in segsWithIDsAndSlopes:
        temp = []
        for point in maxPointsWithSegs:
            if point[0] != seg[0]:
                continue
            temp.append(point)
        if seg[1] > 1:
           # print 'Seg id ', seg[0], ' sorted by y'
            temp.sort(key=lambda point: point[1][0][1])
            sortedPoints.extend(temp)
        else:
           # print 'Seg id ', seg[0], ' sorted by x'
            temp.sort(key=lambda point: point[1][0][0])
            sortedPoints.extend(temp)
    
    # checks all points
    # if the next point has the same segment id, get the midpoint and append to the list
    listOfMidPointsToBeChecked = []
    for p in range(0, len(sortedPoints)):
        if p + 1 != len(sortedPoints):
            if sortedPoints[p][0] == sortedPoints[p + 1][0]:
                xMidPoint = (sortedPoints[p][1][0][0] + sortedPoints[p + 1][1][0][0]) / 2
                yMidPoint = (sortedPoints[p][1][0][1] + sortedPoints[p + 1][1][0][1]) / 2
                listOfMidPointsToBeChecked.append( (xMidPoint, yMidPoint, sortedPoints[p][0]) )

    # JM - just checking if list if empty or not
    # JM - not sure what to do if the list is empty
    if len(listOfMidPointsToBeChecked) == 0:
        print 'List is empty. Exiting...'
        exit()
     
    # send the midpoint(s) list to get coverage times for the midpoint(s)
    # find what segments the midpoints come from
    newList = intervalRegion.getTemporalCoverageGeometriesAndTimes(triangles, listOfMidPointsToBeChecked)
    
    segments = []
    # make a list with temporal coverage of midpoints and segment number 
    for n in newList.items() :
        for l in listOfMidPointsToBeChecked :
            if n[0][0]==l[0] and n[0][1]==l[1] :
                segments.append((l,n[1]))           
    #print "segments=",segments   
     
    # find whether the midpoint has same temporal coverage as adjacent points    
    final_segments = []
    for s in segments :
        for m in maxPointsWithSegs :
            if m[0]==s[0][2] and m[1][1] == s[1] :
                final_segments.append(m)        
    final_segments.sort() 
    #print "points with segments and max coverage=",final_segments
    
    i=0
    input_tofind_cycles = []
    # set the input as ((x1,y1),(x2,y2)) for function labelUniqueCycles()
    for l in range(0,len(final_segments),2):
        input_tofind_cycles.append((final_segments[i][1][0],final_segments[i+1][1][0]))
        i=i+2
        
    #print "segments whose mid-point has same coverage as end-points=",input_tofind_cycles
    
    # find whether there are any cycles or not
    cycles=hsegLibrary.labelUniqueCycles(input_tofind_cycles)    
    
    if cycles :
        #print "cycles present from the given segments",cycles
        max_seg_return_val=[]
        for seg in input_tofind_cycles :
            for c in cycles :
                if (c[0]==seg) :
                    max_seg_return_val.append(seg)
        if max_seg_return_val :
            max_points_return_val.append(max_seg_return_val)    
        else :
            max_points_return_val.append(['None'])           
        max_points_return_val.append(cycles)
    else :
        #print "no cycles present"
        if input_tofind_cycles :
            max_points_return_val.append(input_tofind_cycles)
        else :
            max_points_return_val.append(['None'])            
        max_points_return_val.append(['None'])
    
    return_val=tuple(max_points_return_val)
    ''' 
    # DEBUG : plots the maximum segments and cycles if present.
        
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from matplotlib.colors import colorConverter
    import matplotlib.lines as mlines
    from matplotlib.collections import PolyCollection, LineCollection

    fig = plt.figure()
    ax = Axes3D(fig)
    
    # plot the triangles from interpolation
    i=0
    verts=[]
    cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.1)
    for tri in range(len(triangles)) :
        x = triangles[i][0]
        y = triangles[i][1]
        z = triangles[i][2]
        verts = [[x, y,z]]
        poly = Poly3DCollection(verts, facecolors = [cc('r'), cc('g'), cc('b'),
                                           cc('y')])
        poly.set_alpha(0.1)
        ax.add_collection3d(poly,zs=z,zdir='y')
        i=i+1
    
    edges=[]
    edge=[]
    # plot max points
    for maxplot in maxPoints :
        x=maxplot[0][0]
        y=maxplot[0][1]
        z=maxplot[1][0]
        edges=(x,y,z)
        edge.append(edges)
    plt.plot(*zip(*edge),marker='p',color='g',ls='')   
    
    min_edge1=[]
    # plot min points
    for minplot in minPoints  :
        x=minplot[0][0]
        y=minplot[0][1]
        z=minplot[1][0]
        min_edge=(x,y,z)
        
        min_edge1.append(min_edge)
    plt.plot(*zip(*min_edge1),marker='p',color='b',ls='')   
    
    ##
    fin_edge1=[]
    # plot the points which has same temporal coverage as the midpoint
    for m in final_segments  :
        x=m[1][0][0]
        y=m[1][0][1]
        z=m[1][1][0]
        
        fin_edge=(x,y,z)
        
        fin_edge1.append(fin_edge)
    plt.plot(*zip(*fin_edge1),marker='o',color='w',ls='') 
    ##
    # plot the cycles if any
    if cycles :
        print "cycles present"
        for c in cycles :
            plt.plot([c[0][0][0],c[0][1][0]],[c[0][0][1],c[0][1][1]],'c--')
        cyan_line = mlines.Line2D([], [], color='cyan',linestyle='--',
                          linewidth=5, label='cycle')
        plt.legend(handles=[cyan_line])    
    else :
        print " no cycles present "
          
    ax.set_xlabel('X')
    ax.set_xlim3d(0, 20000)
    ax.set_ylabel('Y')
    ax.set_ylim3d(0, 20000)
    ax.set_zlabel('Time')
    ax.set_zlim3d(0, 100)
    plt.show()
    '''
    return return_val
    
