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
import struct
import sys


def generateRegionAndWriteHexToFile():
  '''
  Sample function showing how to generate a random region 
  and write it in hexadecimal format to a text file (for portability)
  '''
  if len( sys.argv ) < 5:
      print 'usage: ', sys.argv[0],'  numStartSegs minBound maxBound outputHexFile'
      exit()
  if len( sys.argv ) >= 5:
      num = int( sys.argv[1] )
      minBound = int( sys.argv[2] )
      maxBound = int( sys.argv[3] )
      outfileName = sys.argv[4]
      outfile = open(outfileName, 'w' )
  r1 = region.getRandomRegion( num, minBound, maxBound )
  print 'writing file'
  #write it out
  for h in r1:
      if h[0][0] < h[0][1]:
          seg = h[0]
          s=struct.pack('>d', seg[0][0] )
          hexx1 = ''.join('%.2x' % ord(c) for c in s) # get hex vals from bin string s
          s=struct.pack('>d', seg[0][1])
          hexy1 = ''.join('%.2x' % ord(c) for c in s) # get hex vals from bin string s
          s=struct.pack('>d', seg[1][0])
          hexx2 = ''.join('%.2x' % ord(c) for c in s) # get hex vals from bin string s
          s=struct.pack('>d', seg[1][1])
          hexy2 = ''.join('%.2x' % ord(c) for c in s) # get hex vals from bin string s
           #output the line to the new file
          la = h[1]
          if la < 0:
              la = 0
          if la > 0:
              la = 1
          lb = h[2]
          if lb < 0:
              lb = 0
          if lb > 0:
              lb = 1
          outfile.write( hexx1 + ' ' + hexy1 + ' '+  hexx2 + ' ' + hexy2+' ' + str(la) +' '+str(lb)+ '\n')
  outfile.close()
  print len( r1 )/2

if __name__ == '__main__':
  generateRegionAndWriteHexToFile()


