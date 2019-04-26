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



from collections import deque
import math

'''
Functions to compute a convex hull of a series of points
'''



def angleFromVertical( seg ):
        '''
        Computes the angle (in degrees) formed by extending a ray vertically through 
        the leftmost end point of the segment, and rotating it counter-clockwise
        until overlaps with the segment.

        **input**
        
        seg: A line segment in the format ((x1,y1),(x2,y2))

       **output**
       
       the angle in degrees

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


def getHullFromSequence( pois ):
        '''
        Returns the convex hull of a list of points.
        Uses the Graham's Scan technique (with associated floating point rounding problems)

        **input**:

          pois:  A list of points of the format: [(x1,y1),(x2,y2),...(xn,yn)]

        **output**:

          a list of points that, traversed in order, form the convex hull of the input points
        '''

        #graham scan
        #error checking
        if len( pois ) < 3:
                return None

        elif len(pois ) == 3:
                return pois
        #sort pois by angle with min poi in poiCmp order
        firstPoi = pois.pop( 0 )
        pois.sort( key = lambda p: angleFromVertical( (firstPoi, p) ) )
        pois = [p for i,p in enumerate( pois ) if i == len(pois)-1 or pois[i] != pois[i+1]]
        # now do the scanning
        hull = deque()
        hull.appendleft( firstPoi )
        hull.appendleft( pois[0] )
        for i in range( 1, len( pois) ):
            while  len(hull) > 1 and isLeftTurn( hull[1], hull[0], pois[i])  < 0:
            #while isLeftTurn( hull[1], hull[0], pois[i])  < 0: 
                hull.popleft()
            hull.appendleft( pois[i] )
        hull.reverse()
        return list(hull)


def getHullFromSequenceMelkman( pois ):
        '''
        !!! This function does not quite work, but the general algorithm is there.  Use as a reference only!!

        Returns the convex hull of a list of points.
        Uses the Melkmans' Algorithm technique (with associated floating point rounding problems)

        **input**:

        pois:  A list of points of the format: [(x1,y1),(x2,y2),...(xn,yn)]

        **output**:

        a list of points that, traversed in order, form the convex hull of the input points
        '''

        #error checking
        if len( pois ) < 3:
                return None

        elif len(pois ) == 3:
                return pois
        pois.append( pois[0] )
        #pois.append( pois[0] )
        hull = deque()
        index = 0
        #pois
        v0=None
        v1=None
        v2=None
        vi=None
        dt=None
        dt1=None
        db=None
        db1=None
        firstPoi = pois[0]
        v0 = firstPoi
        v1 = pois[1]
        v2 = pois[2]
        index = 2
        #initialization: orient initial convex hull for CCW direction
        if isLeftTurn( v0, v1, v2) >= 0:
                hull.extendleft( (v2, v0, v1, v2) )
                dt = v2
                dt1 = v1
                db = v2
                db1 = v0
        else:
                hull.extendleft( (v2, v1, v0, v2) )
                dt = v2
                dt1 = v0
                db = v2
                db1 = v1
        index +=1               
        while index < len( pois ):
                # get next not handled point
                vi = pois[index]
                #if vi == firstPoi: break
                #if vi != firstPoi:
                # do left turn test repeatedly to redote convexity
                # use > instead of >= so collinear hull points dont get discarded
                # this check checks if a current point is inside  the hull by 
                # looking at the LHTtest turn from front and back of the current hull
                # loop skips any points that inside the hull
                while (isLeftTurn( dt1, dt, vi) > 0 or dt == vi) and (isLeftTurn( db, db1, vi ) > 0 or db1 == vi) and index < len(pois)-1: #and isLeftTurn( dt, vi,db )<0 and index < len(pois)-1:
                        index +=1
                        vi = pois[index]
                #check if we are at end
                #if index == len( pois)-1:
                #       if isLeftTurn( dt, vi,db )>=0:
                #               hull.appendleft( vi )
                #       break
                # we now have a point that we cannot rule out as being inside the hull
                # add it to the current hull, and check if convexity is broken
                while isLeftTurn( dt1, dt, vi ) < 0:
                        hull.popleft( )
                        dt = hull[0]
                        dt1 = hull[1]
                hull.appendleft( vi )   
                # repeat for the bottom of the stack
                while isLeftTurn( db, db1, vi ) <=0:
                        hull.pop()
                        db = hull[len(hull)-1]
                        db1 = hull[len(hull)-2]
                hull.append( vi )
                index +=1
                # update vars for next time
                dt = hull[0]
                dt1 = hull[1]
                db = hull[len(hull)-1]
                db1 = hull[len(hull)-2]
        hull.pop()
        #rotate the hull so the first point is the first in the poiList
        # deques are optimized for rotation rather than indexed access.  So rotate until the 
        # desired point is at the front
        while hull[0] != pois[0]:
                hull.rotate(1)
        hull.append( firstPoi )
        # check for a CCW rotation
        if isLeftTurn( hull[0], hull[1], hull[2]) < 0:
                hull.reverse()
        hull.pop()
        listhull = list(hull)
                
        return listhull


def isLeftTurn( p1,p2,p3):
        '''
        Indicates if the person traveling from point p1 to point p2 and then on to point p3 
        must take a left or right turn at p2 in order to reach p3.
  
        The approach is to use the sign of the area of the triangle formed by the points
        (actually the square, since the area is not divided by 2)

        **input**:

        p1,p2,p3: points of the form (x,y)

        **output**:
        
        -1 -- if a left turn was made
        0  -- if the points are collinear
        1  -- if a right turn was made
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
