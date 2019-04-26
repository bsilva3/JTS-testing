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

import pyspatiotemporalgeom.intervalRegion as intervalRegion
import pyspatiotemporalgeom.region as region
def exampleCreateRandomRegionsAndInterpolate():
  '''
  An example that creates two random regions and interpolates them to create a moving region.

  See the documentation for pyspatiotemporalgeom.movingRegion.interpolateRegions() for more details.
  '''
  r1 = []
  r2 = []
  while len( r1 ) == 0 or len( r2 ) == 0:
    r1 = region.getRandomRegion( 50 )
    r2 = region.getRandomRegion( 50 )
  print 'length of input regions (number of halfsegments)'
  print len( r1 ), ' ', len(r2 )
  print 'interpolating: '
  print intervalRegion.interpolateRegions( r1, r2, 10, 20 )

if __name__ == '__main__':
  exampleCreateRandomRegionsAndInterpolate() 

