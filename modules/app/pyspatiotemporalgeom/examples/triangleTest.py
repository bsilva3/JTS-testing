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

'''
traingleTest.py

example functions using the triangleLibrary.py functions
'''

from pyspatiotemporalgeom.utilities import triangleLibrary

def verticalSegTraingleTest():
  '''
  test various configurations of triangles and vertical segments intersecting
  '''

  tri1 = ((1,1,1),(5,2,1),(1,1,10)) # 1 stem is vertical in Z dimension
  tri2 = ((1,1,1),(5,2,1),(3,8,10)) # tilts
  tri3 = ((1,1,1),(5,1,1),(3,1,10)) #stands up straight
  tri4 = ((2,2,2),(4,3,2),(4,3,10)) # stands straight, but stem2 is vertical
  tri5 = ((2,2,2),(4,3,2),(8,5,10)) # the tip is out away from the base seg
  seg1 = ((1,1,0),(1,1,11)) # overlap stem with tri1
  seg2 = ((5,2,0),(5,2,11)) # grazes tri1 at point
  seg3 = ((3,1,0),(3,1,11)) # intersects tri3 in seg interior and at set end point
  seg4 = ((2,1,0),(2,1,11)) # intersects tri3 in 2 seg interiors
  seg5 = ((3,4,0),(3,4,11)) # intersect tri2 in its interior
  seg6 = ((4,3,1),(4,3,11)) # shares a stem with tri4
  seg7 = ((8,5,1),(8,5,11)) # grazes the tip of tri5

  val = triangleLibrary.verticalSegment3DAndTriangle3DIntersection( seg1, tri1 )
  print 'should get 2 points based on', seg1, tri1
  print val,'\n'
  val = triangleLibrary.verticalSegment3DAndTriangle3DIntersection( seg2, tri1 )
  print 'should get 1 point based on', seg2, tri1
  print val,'\n'
  val = triangleLibrary.verticalSegment3DAndTriangle3DIntersection( seg3, tri3 )
  print 'should get 2 points based on', seg3, tri3
  print val,'\n'
  val = triangleLibrary.verticalSegment3DAndTriangle3DIntersection( seg4, tri3 )
  print 'should get 2 points based on', seg4, tri3
  print val,'\n'
  val = triangleLibrary.verticalSegment3DAndTriangle3DIntersection( seg5, tri2 )
  print 'should get 1 point based on', seg5, tri2
  print val,'\n'
  val = triangleLibrary.verticalSegment3DAndTriangle3DIntersection( seg6, tri4 )
  print 'should get 2 point based on', seg6, tri4
  print val,'\n'
  val = triangleLibrary.verticalSegment3DAndTriangle3DIntersection( seg7, tri5 )
  print 'should get 1 point based on', seg7, tri5
  print val,'\n'



if __name__ == '__main__':
    verticalSegTraingleTest() 
