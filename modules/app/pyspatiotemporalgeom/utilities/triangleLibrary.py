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


import math
from pyspatiotemporalgeom.utilities import segLibrary

'''
Functions to manipulate triangles.


'''

def dot( u, v ):
        ''' 
        returns dot product of vectors u and v
        
        u and v are 3-tuples representing a 3D point: ``(x,y,z)``

        This function is used to compute triangle/triangle intersections

        Returns a number
        '''
        return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]

def crossProduct( v, u ):
        '''
        returns cross product of u and v

        u and v are 3-tuples representing a 3D point: ``(x,y,z)``

        This function is used to compute triangle/triangle intersections

        Returns a 3-tuple of numbers (a 3D point): ``(x,y,z)``
        '''
        return( (v[1]*u[2]-u[1]*v[2]), (-v[0]*u[2]+u[0]*v[2]),(v[0]*u[1]-u[0]*v[1]) )


def triangle3DTriangle3DIntersectionPoint( tri1, tri2 ):
        '''
        Input:  two triangles of the form: ``((x1,y1,z1),(x2,y2,z2),(x3,y3,z3))``

        .. warning::

          triangles always have points [0] and [1] from the same slice. In other words, for the representation listed above, z1 = z2 ALWAYS. 
        
          Both triangles cover the same time interval.  So, the the Z values will be the same among both intput triangles.

        So ... always make segs with [0][2] and [1][2] for tri tri intersection
        
        Triangles that share an edge are not considered intersecting.  This function does return true if two triangles meet at a point and that
        point lies on the boundary of the triangles.

        This function returns a single point of intersection.  If a segment from one triangle is coplanar with the other triangle,
        this function will not return an intersection point.  ``triangle3DTriangle3DIntersection( tri1, tri2 )`` will consider such a 
        pair of triangles to be overlapping and will return true.  However, THIS function only returns an intersection point if 
        there is a SINGLE intersection point between a line segment from one triangle and  the other triangle.

        **Input**:

            tri1, tri2
                Two triangles of the form: 
                
                ``tri1 = ((x1,y1,z1),(x2,y2,z2),(x3,y3,z3))``
                
                ``tri1 = ((x4,y4,z4),(x5,y5,z5),(x6,y6,z6))``

                Where ``z1 == z2 and z4==z5 and ((z1 == z4 and z3 == z6) or (z1 == z6 and z3 == z4))``

                Also, the triangles cover the same interval in the ``Z`` dimension. so a Z value that appears in ``tri1`` also appears in ``tri2``

        **Returns**:
        
        A list of points where a point is defined as ``(x,y)``

        ``[(x1,y1,zn), ..., (xn,yn, zn)]`` 
            For every point at which a triangle edge intersects the opposing triangle at a single point, that point will appear in the list.
        
        ``[]``
            An empty list, otherwise.  

        .. warning:: 
          
            triangle with shared edges but disjoint interiors return ``False``
        
        This function uses the general intersection test that makes no assumptions about the orientations of triangles.
        '''
        t1s1 = (tri1[0], tri1[2] )
        t1s2 = (tri1[1], tri1[2] )
        t2s1 = (tri2[0], tri2[2] )
        t2s2 = (tri2[1], tri2[2] )
        retList = []
        val = segment3DTriangle3DIntersection( t1s1, tri2 )
        if val[0] == 1:
                retList.append( val[1] ) 
        val = segment3DTriangle3DIntersection( t1s2, tri2 )
        if val[0] == 1:
                retList.append( val[1] ) 
        val = segment3DTriangle3DIntersection( t2s1, tri1 )
        if val[0] == 1:
                retList.append( val[1] ) 
        val= segment3DTriangle3DIntersection( t2s2, tri1 )
        if val[0] == 1:
                retList.append( val[1] ) 
        return retList

def triangle3DTriangle3DIntersection( tri1, tri2 ):
        '''
        Input:  two triangles of the form: ``((x1,y1,z1),(x2,y2,z2),(x3,y3,z3))``

        .. warning::

          triangles always have points [0] and [1] from the same slice. In other words, for the representation listed above, z1 = z2 ALWAYS. 
        
          Both triangles cover the same time interval.  So, the the Z values will be the same among both intput triangles.

        So ... always make segs with [0][2] and [1][2] for tri tri intersection
        
        Triangles that share an edge are not considered intersecting.  This function does return true if two triangles meet at a point and that
        point lies on the boundary of the triangles.  

        **Input**:

            tri1, tri2
                Two triangles of the form: 
                
                ``tri1 = ((x1,y1,z1),(x2,y2,z2),(x3,y3,z3))``
                
                ``tri1 = ((x4,y4,z4),(x5,y5,z5),(x6,y6,z6))``

                Where ``z1 == z2 and z4==z5 and ((z1 == z4 and z3 == z6) or (z1 == z6 and z3 == z4))``

                Also, the triangles cover the same interval in the ``Z`` dimension. so a Z value that appears in ``tri1`` also appears in ``tri2``

        **Returns**:

        ``True`` 
            if the triangles intersect in their interior or at a point along their boundaries
        
        ``False`` 
            if the triangle's interiors do not intersect.  

        .. warning:: 
          
            triangle with shared edges but disjoint interiors return ``False``
        
        This function uses the general intersection test that makes no assumptions about the orientations of triangles.
        '''
        t1s1 = (tri1[0], tri1[2] )
        t1s2 = (tri1[1], tri1[2] )
        t2s1 = (tri2[0], tri2[2] )
        t2s2 = (tri2[1], tri2[2] )

        if segment3DTriangle3DIntersection( t1s1, tri2 )[0] > 0:
                return True
        elif segment3DTriangle3DIntersection( t1s2, tri2 )[0] > 0:
                return True
        elif segment3DTriangle3DIntersection( t2s1, tri1 )[0] > 0:
                return True
        elif segment3DTriangle3DIntersection( t2s2, tri1 )[0] > 0:
                return True
        #       tri1 = (tri1[1], tri1[0], tri1[2] )
        #       tri2 = (tri2[1], tri2[0], tri2[2] )
        return False



def triangle3DTriangle3DIntersection( tri1, tri2 ):
        '''
        Input:  two triangles of the form: ``((x1,y1,z1),(x2,y2,z2),(x3,y3,z3))``

        .. warning::

          triangles always have points [0] and [1] from the same slice. In other words, for the representation listed above, z1 = z2 ALWAYS. 
        
          Both triangles cover the same time interval.  So, the the Z values will be the same among both intput triangles.

        So ... always make segs with [0][2] and [1][2] for tri tri intersection
        
        Triangles that share an edge are not considered intersecting.  This function does return true if two triangles meet at a point and that
        point lies on the boundary of the triangles.  

        **Input**:

            tri1, tri2
                Two triangles of the form: 
                
                ``tri1 = ((x1,y1,z1),(x2,y2,z2),(x3,y3,z3))``
                
                ``tri1 = ((x4,y4,z4),(x5,y5,z5),(x6,y6,z6))``

                Where ``z1 == z2 and z4==z5 and ((z1 == z4 and z3 == z6) or (z1 == z6 and z3 == z4))``

                Also, the triangles cover the same interval in the ``Z`` dimension. so a Z value that appears in ``tri1`` also appears in ``tri2``

        **Returns**:

        ``True`` 
            if the triangles intersect in their interior or at a point along their boundaries
        
        ``False`` 
            if the triangle's interiors do not intersect.  

        .. warning:: 
          
            triangle with shared edges but disjoint interiors return ``False``
        
        This function uses the general intersection test that makes no assumptions about the orientations of triangles.
        '''
        t1s1 = (tri1[0], tri1[2] )
        t1s2 = (tri1[1], tri1[2] )
        t2s1 = (tri2[0], tri2[2] )
        t2s2 = (tri2[1], tri2[2] )

        if segment3DTriangle3DIntersection( t1s1, tri2 )[0] > 0:
                return True
        elif segment3DTriangle3DIntersection( t1s2, tri2 )[0] > 0:
                return True
        elif segment3DTriangle3DIntersection( t2s1, tri1 )[0] > 0:
                return True
        elif segment3DTriangle3DIntersection( t2s2, tri1 )[0] > 0:
                return True
        #       tri1 = (tri1[1], tri1[0], tri1[2] )
        #       tri2 = (tri2[1], tri2[0], tri2[2] )
        return False


def verticalSegment3DAndTriangle3DIntersection( ray, tri):
  '''
  This function returns the points of intersection between a triangle in 3D and vertical 3D segment.
  
  If a ray and a traingle are co-planar and intersect, they will intersect at 2 points (unless the ray grazes the tip of the triangle, in which case they will intersect at a single point). If the ray is collinear and overlapping a segment, this will return the segment end points.  
  
  .. warning:: 
  
    Again, as with all the functions in this file, we are assuming rays that are vertical in the z (temporal) dimension and triangles in the usual format: tri: :math:`((x1,y1,z1),(x2,y2,z2),(x3,y3,z3))` where :math:`z1 == z2`.  So... the triangle always has a segment that is in the Z plane.
  
  The function will check explicitly for intersection between the segment and each triangle edge (using a leftHandTurn test). The approach for this is to project the triangle segments to 2d space;  then, find which projected segs :math:`s1,s2` contain the point :math:`p` induced by projecting the vertical segment out of the Z dimension.  Finally, the z dimension of the intersection of :math:`s1` and :math:`p` are computed, and likewise for :math:`s2`.
  
  Becuase 1 triangle seg is always planar in the Z dimension, we refer to the triangle edges as the **base** (the one planar in the Z dimension) and **stem1** and **stem2**.  The base may be at the top (highest Z value) or bottom of the triangle.  The stems always share one end point.  

  Input: 
  
  * tri: a triangle of the form: ``((x1,y1,z1),(x2,y2,z2),(x3,y3,z3))``
  * (triangles always have points [0] and [1] from the same slice. In other words, for the representation listed above, z1 = z2 ALWAYS.)
  * ray: a line segment of the form ((x1,y1,z1),(x2,y2,z2)) that is vertical in the Z dimension and that spans the Z dimension of the triangle

  Returns:

  * a list containing 0, 1, or 2 3D points: [],  [((x,y,z),(x2,y2,z2))] or [((x,y,z))].  The segment may graze the triangle at a point or along a segment, it may enter and then leave a co-planar triangle, or it may miss the triangle.

  '''
  
  result = set()
  # get the segments.
  base =  ( tri[0], tri[1] )
  stem1 = ( tri[0], tri[2] )
  stem2 = ( tri[1], tri[2] )

  basep = ((base[0][0], base[0][1]),(base[1][0], base[1][1] ))
  stem1p = ((stem1[0][0], stem1[0][1]),(stem1[1][0], stem1[1][1] ))
  stem2p = ((stem2[0][0], stem2[0][1]),(stem2[1][0], stem2[1][1] ))
  rayp = (ray[0][0],ray[0][1])
  
  # make sure the least point comes first.
  if basep[1] < basep[0]:
      basep = (basep[1], basep[0])
      base = (base[1], base[0])

  if stem1p[1] < stem1p[0]:
      stem1p = (stem1p[1], stem1p[0])
      stem1 = (stem1[1], stem1[0])

  if stem2p[1] < stem2p[0]:
      stem2p = (stem2p[1], stem2p[0])
      stem2 = (stem2[1], stem2[0])

  # easy checks:  is the rayp equal to any of the projected end points?
  # 1: ray collinear and overlapping with a line
  if rayp == stem1p[0] and rayp == stem1p[1]:
      return stem1
  elif rayp == stem2p[0] and rayp == stem2p[1]:
      return stem2

  # 2: ray grazes the triangle
  # projected ray is a tri point, and the end points of the segs starting at that point
  # are in the same X direction from the point (the same side if the ray point in the X direction)
  if rayp == ( tri[0][0], tri[0][1] ) and((rayp[0] - tri[1][0]) < 0 == (rayp[0] - tri[2][0]) < 0):
      return tri[0]
  elif rayp == ( tri[1][0], tri[1][1] ) and((rayp[0] - tri[0][0]) < 0 == (rayp[0] - tri[2][0]) < 0):
      return tri[1]
  if rayp == ( tri[2][0], tri[2][1] ) and((rayp[0] - tri[1][0]) < 0 == (rayp[0] - tri[0][0]) < 0):
      return tri[2]
  
  # 3: ray pierces into the triangle at a triangle vertex, or ray is on the interior of a triangle edge
  # both cases are handled here in case the ray pierces into the triangle at a meeting of segs, and 
  # then breaks out of the triangle at a seg interior (or vice versa)
  #
  # First, we check stem1.
  thePoint = verticalSegment3DAndSegment3DIntersection( rayp, stem1 )
  if thePoint != None:
      result |= set( thePoint )
  # now stem2
  thePoint = verticalSegment3DAndSegment3DIntersection( rayp, stem2 )
  if thePoint != None:
      result |= set( thePoint )
  # now the base/top of the tru
  thePoint = verticalSegment3DAndSegment3DIntersection( rayp,base )
  if thePoint != None:
      result |= set( thePoint )
  
  # if we have result points, the intersection involved a triangle segment and we are finished
  if len( result ) != 0:
    return list( result )

  # Finally, if we get here, we have found no intersection with an edge of the triangle.  Lets
  # check for an interior triangle interseciton.  Plan of attack:
  # project the triangle out of Z, use left hand turn tests to find if the point is in the interior.
  # If the point is in the interior, use the full traingle/segment intersection  

  triP1 = (tri[0][0], tri[0][1])
  triP2 = (tri[1][0], tri[1][1])
  triP3 = (tri[2][0], tri[2][1])
  # now we have to check the orientation of our triangle
  if segLibrary.isLeftTurn( triP1, triP2, triP3) >= 0:
    tmp = triP2
    triP2 = triP3
    triP3 = tmp
    # sanity check
    if segLibrary.isLeftTurn( triP1, triP2, triP3) >= 0:
        # Removed this becuase of coplanar triangles and rays.  That intersection should be caught elswhere, but we need to double check   
        #print 'triangle orientation error!!'
        #exit()
        return []
  # now do the left hand turn tests
  if segLibrary.isLeftTurn( triP1, triP2, rayp ) < 0 and segLibrary.isLeftTurn( triP2, triP3, rayp ) < 0 and segLibrary.isLeftTurn( triP3, triP1, rayp ) < 0:
    # the point is in the triangle
    # call the full segment/triangle intersection
    resTuple = segment3DTriangle3DIntersection( ray, tri)
    if resTuple[0] != 1:
        print 'Error, expected an intersection point and didn\'t get one'
        exit()
    resultList = [ resTuple[1] ]
    return resultList
  # if we get here, there was no intersection!
  return []
  
 

def verticalSegment3DAndSegment3DIntersection( verticalSegProjectedTo2D, seg3D ):
  '''
  find the intersection point of a vertical segment (projected out of the Z dimension) and 3D segment (if it exists.).  If there
  is no intersection, a ``None`` value is returned.

  Input:

  * verticalSegProjectedTo2D: a point tuple ``(x,y)`` defining a vertical line in 3D
  * seg3D: a 3d line segment tuple: ``((x1,y1,z1),(x2,y2,z2))``

  Returns:

  * A ``list()`` containing 1 or 2 intersection points.  A point is a tuple ``(x,y,z)``. The x and y values of the intersection point will always be equal to the values in ``lineProjected`` if the intersection point exists. Or...
  * ``None`` if there is no intersection
  '''
  result = set()
  rayp = verticalSegProjectedTo2D 
  stem1 = seg3D
  stem1p = ((stem1[0][0], stem1[0][1]),(stem1[1][0], stem1[1][1] ))

  # make sure the least point comes first.
  if stem1p[1] < stem1p[0]:
      stem1p = (stem1p[1], stem1p[0])
      stem1 = (stem1[1], stem1[0])

  # from completeness, check for a collinear line.  This test is also done in verticalSegment3DAndTriangle3DIntersection(), but we 
  # might call this function independent of that one...
  if rayp == stem1p[0] and rayp == stem1p[1]:
    result |= set( [ stem1[0], stem1[1] ] )
  # check if the ray goes through an end point
  elif rayp == stem1p[0]:           # check left end point of stem1
    result |= set( [stem1[0]] )
  elif rayp == stem1p[1]:         # check right end point of stem1
    result |= set( [stem1[1]] )
  elif ((stem1p[0][0] < rayp[0] and stem1p[1][0]> rayp[0]) or (stem1p[0][0] == stem1p[1][0] and stem1p[0][1] < rayp[1] and stem1p[1][1]> rayp[1])) and  math.fabs( segLibrary.collinearValue( stem1p[0], rayp, stem1p[1])) < 0.000001:   
    # seg spans the ray point and is collinear (the ray point  is on the line segment interior)
    # find where on the non-projected seg the point lies.
    #step 1.  figure out how far along the projected seg the point lies using x vals (or y in the case of verticals)
    xbig = stem1p[1][0]
    xsmall = stem1p[0][0]
    pointx = rayp[0]
    if xbig == xsmall:
        xbig = stem1p[1][1]
        xsmall = stem1p[0][1]
        pointx = rayp[1]
    multiplier = (float(pointx)-xsmall) / (xbig-xsmall)
    #step 2.  get the z value.  Remember, we already handled the case if
    # point is a seg end point, so it will always be an interior point here.
    # easy case is if the segment is in the Z plane
    if stem1[0][2] == stem1[1][2]:
      result |= set( [(rayp[0], rayp[1], stem1[0][2])] )
      return list( result )
    # tougher case, the seg is not in the Z plane
    zvalbig = stem1[1][2]
    zvalsmall = stem1[0][2]
    zval = ((zvalbig-zvalsmall)*multiplier)+zvalsmall
    if zvalbig < zvalsmall:
        tmp = zvalbig
        zvalbig=zvalsmall
        zvalsmall = tmp
        zval = zvalbig - ((zvalbig-zvalsmall)*multiplier)
    # zval indicates the Z value assuming that the seg starts from zSmall.  If in fact, 
    # we reversed the seg end points above, we actuallly need to compute the Z val from larger Z value
    # in that case, zval = zvalbig - ((zvalbig-zvalsmall)*multiplier)
    
    # now we have the result point on the stem1 seg.  need to do stem2 seg
    result |= set( [(rayp[0],rayp[1],zval)] )
    return list( result )
  return list( result )

def segment3DTriangle3DIntersection( seg, tri ):
        '''
        
        Test if a triangle and a 3D segment intersect. Whereas some of the other functions assume a vertical segment in the Z dimension, this function assumes NO orientation of the segment.  It can be pointing in any direction.

        To convert this algorithm to use rays, change the line:
            
        ``if r <= 0.0 or r >= 1.0:``
        
        to:
        
        ``if r <= 0.0:``

        **Input:** 
        
        + ``seg`` is a lien segment of the usual format ((x1,y1),(x2,y2))
        + ``tri`` is a triangle a tuple of 3, 3D points.  Triangle vertices in arbitrary order
        
        **Returns:** a tuple containing a value indicating the type of intersection, and the actual intersection point (if it exists, ``None`` otherwise):
        
        ``(value, point)`` where ``value`` is:

        * -1: triangle is degenerate (seg or a point)
        * 0: disjoint
        * 1: intersect in unique point
        * 2: intersects in the same plane. (the intersection is a line segment)  
        
        and ``point`` is :

        * ``None`` if there is no intersection point (either no intersection or intersection is a line)
        * ``(x,y,z)`` the point of intersection
        
        This function is modeled from triangle ray intersection algorithm at http://geomalgorithms.com/body_a06-_intersect-2.html#intersect3D_RayTriangle(),
        although this algorithm is different to handle specific intersection cases differently.  Comments are included that identify
        portions specific to our intersection needs
        The code at http://geomalgorithms.com/body_a06-_intersect-2.html#intersect3D_RayTriangle() has the following copyright:
        
        .. code-block:: c

          //Copyright 2001 softSurfer, 2012 Dan Sunday
          // This code may be freely used and modified for any purpose
          // providing that this copyright notice is included with it.
          // SoftSurfer makes no warranty for this code, and cannot be held
          // liable for any real or imagined damage resulting from its use.
          // Users of this code must verify correctness for their application.
        
        '''
        #rename seg to ray
        ray = seg   
        
        # easy test.  if the ray is a tri seg, return not intersecting
        # we don't consider a ray that is identical to a triangle edge to be intersecting
        tsegs = ((tri[0], tri[1] ), (tri[1], tri[0] ), (tri[0], tri[2] ), (tri[2], tri[0] ), (tri[1], tri[2] ), (tri[2], tri[1] ))
        if ray in tsegs:
                return 0,None

        
        SMALL_NUM = 0.00000001
        #u v n will be triangle vectors
        # dir, w0 and w will be ray vectors
        # r, a, b will be params to calc ray-plane intersect
        
        # get triangle edge vects and normal to plane
        u = (tri[1][0]-tri[0][0], tri[1][1]-tri[0][1], tri[1][2]-tri[0][2])
        v = (tri[2][0]-tri[0][0], tri[2][1]-tri[0][1], tri[2][2]-tri[0][2])
        n = crossProduct( u,v )
        if n == (0,0,0):
                return -1,None #degenerate
        dir = (ray[1][0]-ray[0][0], ray[1][1]-ray[0][1], ray[1][2]-ray[0][2]) #ray direction vect
        w0 = (ray[0][0]-tri[0][0], ray[0][1]-tri[0][1], ray[0][2]-tri[0][2])
        a = float( -1*dot( n, w0 ) )
        b = float( dot( n, dir ) )
        if math.fabs( b ) < SMALL_NUM: #ray is parallel to tri
                if a == 0:  # ray lies in tri
                        return 2,None  # ray overlaps the triangle
                else:
                        return 0,None #ray disjoint from plane
        # get intersect point of ray with triangle plane
        r = a/float(b)
        #check if intersect is beyond end of seg.  For a ray, only test with 0.0
        # we use <= and >= becuase we don't care abount end point intersections
        if r <= 0.0 or r >= 1.0: 
                return 0,None
        #get the intersection point of the seg and plane
        I = ( ray[0][0]+r*dir[0], ray[0][1]+r*dir[1], ray[0][2]+r*dir[2]  )
        #find if the point is inside the tri
        uu = dot( u, u)
        uv = dot( u, v)
        vv = dot( v, v)
        w = ( I[0]-tri[0][0], I[1]-tri[0][1], I[2]-tri[0][2] )
        wu = dot( w, u)
        wv = dot( w, v)
        D = uv*uv - uu*vv
        # get and test the parametric coords
        s = (uv*wv - vv*wu)/float(D)
        if s < 0.0 or s > 1.0: # I is outside tri
                return 0,None
        t = (uv*wu - uu*wv)/float(D)
        if t < 0.0 or (s+t) > 1.0: # I is outside tri
                return 0,None
        return 1,I  # intersection!  I is in the tri



