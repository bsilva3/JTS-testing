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


# 2 ways to import
import pyspatiotemporalgeom.region as region
from pyspatiotemporalgeom.utilities import segLibrary

def exampleCreateRandomRegionsAndIntesect():
  '''
  An example that creates two random regions and computes their intersection.
  '''
  r1 = region.getRandomRegion( 200 )
  r2 = region.getRandomRegion( 200 )
  print 'length of input regions (number of halfsegments) and their intersection'
  print len( r1 ), ' ', len(r2 )
  print region.intersection( r1, r2 )

def exampleCreateRegionFromSegsAndIntersect():
  '''
  An example showing how to create a region from a list of line segments.
  The intersection of two regions is then computed
  '''

  segs1=[ ((1,1),(5,1)),((5,1),(3,5)),((3,5),(1,1)) ]
  segs2=[ ((1,2),(4,1)),((4,1),(5,1)),((5,1),(1,3)),((1,3),(1,2)) ]

  segs3=[ ((5,1),(5,2)),((5,2),(6,2)),((6,2),(5,1)) ]
  segs4 = [((1,1),(5,5)),((3,1),(3,5)),((2,5),(5,4)),((1,1),(2,2))]
  segs5 = [((0,4),(3,0)),((3,0),(8,4)),((8,4),(0,4))]
  r1 = region.createRegionFromSegs( segs1 )
  r2 = region.createRegionFromSegs( segs2 )
  print 'the intersection of two regions created from lists of segments'
  print  region.intersection( r1, r2 )


def exampleSegmentIntersection():
  '''
  An example showing how calcNonntersectingSegs.
  All segment intersections are computed, and the segments
  are all broken at the intersection points.
  '''
  s  = [((1,1),(6,6)),((2,1),(5,6)),((3,1),(3,6)),((2,4),(4,2.1)),((9.00001,9.00001),(9.00001, 9.00002))]
  s2 = [((5,1),(5,6))]
  print '\n\n\n\nintersections within a set of segs'
  print 'input :', s
  print 'output:',
  r= segLibrary.calcNonIntersectingSegs( s )
  print r
  print' \n\n\nintersections between 2 sets of segs:'
  r1, r2 = segLibrary.segIntersection( s, s2 )
  print r1
  print '--'
  print r2
  print '----'

if __name__ == '__main__':
  exampleCreateRandomRegionsAndIntesect() 
  exampleCreateRegionFromSegsAndIntersect() 
  exampleSegmentIntersection()

