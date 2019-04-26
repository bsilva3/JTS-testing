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



import pyspatiotemporalgeom.region as region
import pyspatiotemporalgeom.intervalRegion as intervalRegion






def createIntervalRegionAndComputeTemporalAggregate():
  '''
  An example using the temporal coverage aggregate function.  For now, that function works only on a single interval region at a time and returns the information from which an aggregate may be computed.  We need a few more helper functions to get a full aggregate.  See the documentation for ``pyspatiotemporalgeom.intervalRegion.getTemporalCoverageGeometriesAndTimes()`` for the details.

  Create 2 random regions.  Interpolate them.  Use 1 of the interval regions returned from the interpolate function to call the aggregate function.

  The operation is described in :

  M. McKenney, R. Frye, Z. Benchly, and L. Maughan, Temporal Coverage Aggregates Over Moving Region Streams. IWGS at 22nd ACM SIGSPATIAL I    nternational Symposium on Advances in Geographic Information Systems, November 2014, Dallas, TX, USA

  '''
    
  #c1 = [((1,1),(3,1)),((1,1),(2,3)),((2,3),(3,1))]
  #c2 = [((4,2),(6,2)),((4,2),(5,4)),((5,4),(6,2))]
  #c3 = [((2,2),(3,2)),((2,2),(3,3)),((3,2),(3,3))]
  #R1 = region.createRegionFromSegs( c1 )
  #R2 = region.createRegionFromSegs( c3 )
    
  R1 =region.getRandomRegion(20)
  R2 =region.getRandomRegion(20)
  #Interpolate Regions
  print 'interpolating regions'
  arr = intervalRegion.interpolateRegions(R1, R2, 0, 100);
  triangles = []
  # MM extend the list so we do not end up with a bunch of sublists
  triangles.extend(arr[1])

  # MM now we can print the triangles
  triFile = open( 'ztriFile3d.txt', 'w' )
  for tri in arr[1]:
      s = str(tri[0][0]) +' '+ str(tri[0][1]) + ' ' + str(tri[0][2]) + ' ' + str( tri[1][0] ) + ' '  + str( tri[1][1]) +' ' +str(tri[1][2])+'\n'
      triFile.write( s )

      s = str(tri[0][0]) +' '+ str(tri[0][1]) + ' ' + str(tri[0][2]) + ' ' + str( tri[2][0] ) + ' '  + str( tri[2][1]) +' ' +str(tri[2][2])+'\n'
      triFile.write( s )
      
      s = str(tri[1][0]) +' '+ str(tri[1][1]) + ' ' + str(tri[1][2]) + ' ' + str( tri[2][0] ) + ' '  + str( tri[2][1]) +' ' +str(tri[2][2])+'\n'
      triFile.write( s )
   
  
  # MM this should get some intersection points
  print 'compute the coverage aggregates:'
  point2DurationDict = intervalRegion.getTemporalCoverageGeometriesAndTimes(triangles)
  for item in point2DurationDict.items():
      print item
  # MM now put the verticals in an output file
  #vertFile = open ( 'zvertFile3d.txt', 'w')
  #vertFile.write ('E\nM\n')
  #for item in point2DurationDict.items():
  #    vertFile.write( str( item[0][0]) + ' ' + str( item[0][1] ) + ' ' + '-5 '+str( item[0][0]) + ' ' + str( item[0][1] ) + ' ' + '105\n'   )

if __name__ == '__main__':
  createIntervalRegionAndComputeTemporalAggregate()

