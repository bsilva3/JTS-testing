
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

from pyspatiotemporalgeom.utilities import mapLibrary
import pyspatiotemporalgeom.region as region


def createAMapFromSomeCycles():
    '''
    Shows how to create a map from input cycles.  

    Note that this same functionality can be used to create a map from **complex regions**
    without modification.


    The example here takes 3 input regions and returns a map such that an area covered by
    multiple regions carries the labels of ALL input regions that cover it.

    At the end of the function, the user is left with a list of segs, a parallel list of above and below
    labels correspinding to the segs, and a dictionary that maps the end label to a set of input labels.

    The regions in this function overlap. the scene looks as follows:

    .. image:: zstatic/examplesCreateAMapFromSomeCyclesIn.*
        :width: 6in

    Once the map is created, the labelling occurs as follows:

    .. image:: zstatic/examplesCreateAMapFromSomeCyclesOut.*
        :width: 6in

    '''
    # create some cycles
    c1 = [((1,1),(6,2)),((6,2),(5,6)),((5,6),(1,6)),((1,6),(1,1))]
    c2 = [((2,4),(5,1)),((5,1),(11,4)),((11,4),(5,8)),((5,8),(2,4))]
    c3 = [((3,4),(5,6)),((5,6),(3,6)),((3,6),(3,4))]
    # get them labeled
    # note that if the regions are will formed, one can call hsegLibaray.labelUniqueCycles()
    # it will be MUCH faster as it does not check for segment intersections within a region.
    r1 = region.createRegionFromSegs( c1 )
    r2 = region.createRegionFromSegs( c2 )
    r3 = region.createRegionFromSegs( c3 )

    # the labels will not be unique to each cycle, so we need to relabel with unique
    # labels per cycle.  Also, we need segs for the map stuff, not hsegs
    r1 = [ h for h in r1 if h[0][0] < h[0][1]]
    r1 = [ (h[0],-1, 2) if h[1] < 0 else (h[0],2,-1) for h in r1]
    r2 = [ h for h in r2 if h[0][0] < h[0][1]]
    r2 = [ (h[0],-1, 4) if h[1] < 0 else (h[0],4,-1) for h in r2]
    r3 = [ h for h in r3 if h[0][0] < h[0][1]]
    r3 = [ (h[0],-1, 6) if h[1] < 0 else (h[0],6,-1) for h in r3]
   
    print r1
    print r2
    print r3

    #concatinate
    allR = r1+r2+r3
    allC, allLa, allLb = zip(*allR )
    
    print allC
    print allLa
    print allLb

    # make the map
    segs, la, lb = mapLibrary.breakSegsAndPreserveSegLabels( allC, allLa, allLb)
    
    print '\nbroken segs:\n',
    for i in zip( segs, la, lb ):
        print i
    
    rsegs, rla, rlb, index2labelDict = mapLibrary.createMapFromCycles( segs, la, lb )
    print '\nfinal segs:'
    outSegs = zip( rsegs, rla, rlb)
    outSegs.sort()
    for i in outSegs:
        print i, 'la:', index2labelDict[ i[1] ], 'lb:', index2labelDict[ i[2] ]

if __name__ == "__main__":

    createAMapFromSomeCycles()
    
   


