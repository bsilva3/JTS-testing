
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

from pyspatiotemporalgeom.utilities import temporalAggregate
import pyspatiotemporalgeom.region as region

def createIntervalRegionUsingRandomRegion():
    
    '''
    Generates a region from random segments and computes the temporal aggregate as described in:
   
    M. McKenney, R. Frye, Z. Benchly, and L. Maughan, Temporal Coverage Aggregates Over Moving Region Streams. IWGS at 22nd ACM SIGSPATIAL I    nternational Symposium on Advances in Geographic Information Systems, November 2014, Dallas, TX, USA
   
   *returns*:
             
    **hsegs**
        an ordered list of half segments with valid labels.  
        
        A **half segment** is a tuple with the following:
             ((x,y)(x,y), labelAbove, labelBelow)
            
        labels are integral values
            
        an interior label will be positive.  An exterior label will be -1.  The side of the hseg
        on which the interior (exterior) of the region lies will have an interior (exterior) label.
        
        hsegs will be ordered in half segment order
        
        Each cycle in hsegs will have its own unique label number


    '''

    
    R1 = region.getRandomRegion(20)
    R2 = region.getRandomRegion(20)
    
    r=temporalAggregate.createIntervalRegionAndComputeTemporalAggregate(R1,R2);
    print"points with maximum duration,segments that are not part of cycles,cycles with maximum duration =",r
    
def createIntervalRegionUsingcreateRegionFromSegs():
    
    '''
    Computes a temporal aggregate operation on a single interval region.  The region is specified within the function, as opposed to a randomly generated segment.  See the following for a description of the operation:
    
    M. McKenney, R. Frye, Z. Benchly, and L. Maughan, Temporal Coverage Aggregates Over Moving Region Streams. IWGS at 22nd ACM SIGSPATIAL International Symposium on Advances in Geographic Information Systems, November 2014, Dallas, TX, USA
    
    *returns*:

    hsegs
        an ordered list of half segments with valid labels.  

        A **half segment** is a tuple with the following: ((x,y)(x,y), labelAbove, labelBelow)

        labels are integral values

        an interior label will be positive.  An exterior label will be -1.  The side of the hseg
        on which the interior (exterior) of the region lies will have an interior (exterior) label.

        hsegs will be ordered in half segment order

        Each cycle in hsegs will have its own unique label number

    '''
    
    #case1 : have cycles
    R11=[((2500,2000),(5000,7500)),((5000,7500),(1500,6000)),((1500,6000),(2500,2000))]
    R12=[((5500,4000),(7500,10000)),((7500,10000),(2200,8000)),((2200,8000),(5500,4000))]
    
    #R11=[((5000,5000),(15000,5000)),((15000,5000),(10000,15000)),((10000,15000),(5000,5000))]
    #R12=[((12000,8000),(20000,10000)),((20000,10000),(18000,20000)),((18000,20000),(12000,8000))]
    
    #R11=[((5000,5000),(15000,5000)),((15000,5000),(10000,15000)),((10000,15000),(5000,5000))]
    #R12=[((8000,7000),(12000,8000)),((12000,8000),(10000,12000)),((10000,12000),(8000,7000))]
    
     #case 2 : have common line for both the regions
     
    # R11=[((5000,10000),(15000,10000)),((15000,10000),(18000,20000)),((18000,20000),(5000,10000))]
    #R12=[((15000,10000),(25000,10000)),((25000,10000),(18000,20000)),((18000,20000),(15000,10000))]
    
    #R11=[((5000,5000),(15000,5000)),((15000,5000),(10000,15000)),((10000,15000),(5000,5000))]
    #R12=[((12000,5000),(20000,5000)),((20000,5000),(18000,15000)),((18000,15000),(12000,5000))]
     
    #R11=[((8000,10000),(22000,10000)),((22000,10000),(15000,18000)),((15000,18000),(8000,10000))]
    #R12=[((8000,10000),(22000,10000)),((22000,10000),(15000,5000)),((15000,5000),(8000,10000))]
    
    
    R1=region.createRegionFromSegs(R11)
    R2=region.createRegionFromSegs(R12) 
    
    r=temporalAggregate.createIntervalRegionAndComputeTemporalAggregate(R1,R2);
    print"points with maximum duration,segments that are not part of cycles,cycles with maximum duration =",r
    
if __name__ == '__main__':
    
    createIntervalRegionUsingRandomRegion();
    createIntervalRegionUsingcreateRegionFromSegs();
    

    
