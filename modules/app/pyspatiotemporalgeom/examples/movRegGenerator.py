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
import argparse
import random
import math

def generateViaCommandLine():
    '''
    Run the moving region generator via command line.  Interpret the options and generate reagions as indicated.

    This is the main function.
    '''

    parser = argparse.ArgumentParser( description='Generates random moving regions with respect to the input parameters.  Moving regions are written to an output file.  Run with default values for an example. The output file contains movig regions represented as a sequence of triangles.  Coordinates are double precision floating point values stored in hexidecimal.', epilog='Thanks for using this program!')
    parser.add_argument( '-j', '--heading', type=float, default = 90, help='The initial heading of the moving region in degrees.' )
    parser.add_argument( '-J', '--headingchange', type=float, default=0, help='The amount of degrees a heading may change between frames. Values are 0-360. The amount of change in heading will [headingchange] multiplied by a random number between 0 and 1.' )
    parser.add_argument( '-d', '--distance', type=float, default=10, help='The amount of distance that a region covers between frames.')
    parser.add_argument( '-D', '--distancechange', type=float, default=1, help='The amount of change allowed to the distance that a region covers between frames. A random number between 0 and [distancechange]  will be multiplied by [distance] to get the amount of distance covered between a frame.')
    parser.add_argument( '-s', '--size', type=float, default=1, help='The scale factor for the amount of change in the size of a region between frames.')
    parser.add_argument( '-S', '--sizechange', type=float, default=1, help='A random value from the range 1 to [sizechange] will be multiplied with the [size] value to add variance in the size change between frames. ')
    parser.add_argument( '-f', '--frames', type=int, default=5, help='The number of frames to create for each moving region.')
    parser.add_argument( '-c', '--complexity', type=int, default=50, help='A higher number leads to more complex regions. This is the number of line segments used to generate a random region.  Note that the generated region may have many more line segments, since this is a number of randomly generated segments that may self intersect.')
    parser.add_argument( '-o', '--output', default='a.out', help='The output filename. Default output file name is a.out.')
    parser.add_argument( '-a', '--append', action='store_true', help='If set, output will be appended to the output file. Otherwise,  if a file with the same name exists,  it is clobbered.')
    parser.add_argument( '-m', '--minxy', type=float, default=100, help='the mimium x and y values that a region may have in its first frame.')
    parser.add_argument( '-M', '--maxxy', type=float, default=200, help='the maxium x and y values that a region may have in its first frame.')
    parser.add_argument( '-v', '--verbose', type=int, default = 0, help='Set the verbosity level.  Max value is 3.  Each higher level triggers more verbose output')

    # parse the args and do some error correcting.
    args = parser.parse_args()
    args.heading = abs( args.heading % 360)
    args.headingchange = abs(args.headingchange % 360)
    args.distancechange = abs( args.distancechange)
    if args.verbose > 0:    
        print args 

    #open the output file
    outfile = open(args.output, 'w' )

    # generate the regions at each frame
    rList = []
    minx = args.minxy
    miny = args.minxy
    maxx = args.maxxy
    maxy = args.maxxy
    dist = args.distance
    heading = args.heading
    regSize = args.size
    for i in range( args.frames ):
        #rList.append( region.getRandomRegion( args.regionComplexity, minxy, maxxy ) )
        #print len( r1 )/2
        # update the bbox for the next region
        # get the distance to travel
        if args.distancechange != 1:
            dmul = random.uniform(.75, args.distancechange )
            dist = (args.distance * dmul)
       
        # get the heading to travel
        if args.headingchange > 0:
            hmul = random.uniform(-1, 1)
            heading = ((args.headingchange / 2) * hmul) + heading
        
        # get the change in size
        if args.size != 1:
            regSize = args.size
        if args.sizechange != 1:
            smul = random.uniform( 1, args.sizechange )
            regSize = (args.size * smul)

        # update the bbox for the next frame
        if args.distancechange != 1:
            rads = math.radians(heading)
            offx = dist * math.cos( rads )
            offy = dist * math.sin( rads )
            minx = minx + offx
            maxx = maxx + offx
            miny = miny + offy
            maxy = maxy + offy
         
        # resize the bbox if necessary
        if args.size != 1 or args.sizechange != 1:
            offset = (((maxx - minx) * regSize) - (maxx - minx ) )/2.0 
            minx = minx - offset
            maxx = maxx + offset
            offset = (((maxy - miny) * regSize) - (maxy - miny ) )/2.0 
            miny = miny - offset
            maxy = maxy + offset

        if args.verbose >=2: 
            print 'Values for next frame: distance: , ', dist,  ', heading: ', heading, ' , size: ', regSize
            print 'minx: ', minx, '  maxx: ', maxx, '  miny: ',  miny, '  maxy: ', maxy 

        r1 = []
        count = 0
        complexity = args.complexity
        while( len(r1) == 0 ):
            count+=1
            r1 = region.getRandomRegion( complexity, minX = minx, minY = miny, maxX= maxx, maxY= maxy ) 
            if count % 5 == 0:
                complexity += 10
            if count >= 200:
                print( 'Error generating region,  could not generate a random region with the current values:')
                print ('distance: , ', dist,  ', heading: ', heading, ' , size: ', regSize )
                print ('minx: ', minx, '  maxx: ', maxx, '  miny: ',  miny, '  maxy: ', maxy )
                print ('complexity: ',  complexity)
                exit()
        writeRegionToHexFile( r1, outfile, i )



def writeRegionToHexFile( r1, outFile, regionID = 0 ):
    '''
    Function to write a region to an output file. 

    Input:
        
        * ``r1``: A region in halfsegment format

        * ``outFile``: a file object open for writing

    '''
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
          outFile.write( hexx1 + ' ' + hexy1 + ' '+  hexx2 + ' ' + hexy2+' ' + str(la) +' '+str(lb)+ ' ' + str( regionID ) +'\n')

if __name__ == '__main__':
    generateViaCommandLine()


