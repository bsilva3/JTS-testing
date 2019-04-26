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

# hseg is a 3 tuple, a tuple with 2 points, an above label, a below label
# ((dominatingPoint, submissivePoint), labelAbove, labelBelow)
# ( ((x1,y1),(x2,y2)) ,0,0)

'''
Fucntions that perform operations on lists of halfsegments.

A halfsegment has the following strucutre:

(((x1,y1),(x2,y2)),la,lb)

The coordinates are typically floating point values, and many functions will convert the values given 
to floating points.  la and lb are integers.  the side of the segment on which the interior of the region lies
will have a positive value.  The other side will be the side on which the region's exterior lies and will be a -1 (except in some special cases where a value of 0 is used.  Those cases are marked explicitly).

For every line segment ((x1,y1),(x2,y2)), there are 2 associated halfsegments: (((x1,y1),(x2,y2)),la,lb) and (((x2,y2),(x1,y1)),la,lb). The halfsegment with the lesser point occuring first is the **left** halfsegment, the other is the **right** halfsegment.  The term **brother** is sometimes used to indicate the left halfegment for a given right halfsegment, and vice versa.

A total ordering exists on halfsegments, see the halfsegment comparison function.



'''



def isLeft( hseg ):
        '''
        returns true if the input halfsegment is a left halfsegment, false otherwise

        A halfsegment has the structure: (((x1,y1),(x2,y2)),la,lb) where la,lb are ints
        '''
        return hseg[0][0]< hseg[0][1]


def collinear( L, R ):
        '''
        returns true if L and R are EXACTLY collinear.  Check the collinearity functions in segLibrary if a tolerance is allowed.
        '''
        x1 = L[0][0][0]
        y1 = L[0][0][1]
        x2 = L[0][1][0]
        y2 = L[0][1][1]
        x3 = R[0][0][0]
        y3 = R[0][0][1]
        x4 = R[0][1][0]
        y4 = R[0][1][1]

        denom = ((y4-y3)*(x2-x1)) - ((x4-x3)*(y2-y1))
        if denom == 0.0:
                return True
        return False


def slope( seg ):
        '''
        return the slope of a line segment.

        **input**:  A SEGMENT, not a halfsegment.

        **output**: a float
        '''
        if seg[0][0] ==seg[1][0]:
                return 0
        return ((seg[0][1]-seg[1][1]) / float( (seg[0][0]-seg[1][0])) )


def hsegComp( L, R ):
        '''
        Halfsegment comparison function.  Used to provide a total ordering on halfsegments

        **input**: two halfsegments

        **output**: True if L < R, False otherwise
        '''
        if L[0][0]< R[0][0]:
                return True;
        elif L[0][0] == R[0][0]:
                if not isLeft(L) and isLeft(R):
                        return True;
                elif isLeft(L) == isLeft(R):
                        if collinear(L, R):  #same dominating point and collinear
                                high1 =  L[0][1] if ( L[0][0] < L[0][1]) else L[0][0]
                                low1  =  L[0][1] if ( L[0][0] > L[0][1]) else L[0][0]
                                high2 =  R[0][1] if ( R[0][0] < R[0][1]) else R[0][0]
                                low2  =  R[0][1] if ( R[0][0] > R[0][1]) else R[0][0]
                
                        
                                xdif1 = high1[0] - low1[0];
                                xdif2 = high2[0] - low2[0];
                                ydif1 = high1[1] - low1[1];
                                ydif2 = high2[1] - low2[1];
                                
                                xdif1 = xdif1*-1 if (xdif1<0) else xdif1
                                xdif2 = xdif2*-1 if (xdif2<0) else xdif2
                                ydif1 = ydif1*-1 if (ydif1<0) else ydif1
                                ydif2 = ydif2*-1 if (ydif2<0) else ydif2
                        
                                return (( xdif1 < xdif2 ) or (ydif1<ydif2))
                        else: # smallest is that with smallest slope
                                if (L[0][0][0] == L[0][1][0]): #infinite going slope, definitely not smaller
                                        return False
                                elif (R[0][0][0] == R[0][1][0]): #inifinite going slope, definitely smaller
                                        return True
                                else:
                                        return slope( L[0]) < slope( R[0] )
                else:
                        return False;
        else:
                return False;
        

def hsegCompForSorted( L, R ):
        '''
        wrapper for halfsegment comparison function used for the sorted library.
        '''
        if L[0] == R[0]:
                return 0
        elif hsegComp( L, R ):
                return -1
        else:
                return 1
def hsegTriangulateStripCompForSorted( L, R ):
        '''
        comparison of halfsegments used in triangulating regions.

        this a special case of halfsegment comparisons.
        '''
        # if both vertical, use lowest Y vals
        lIsVert = L[0][0][0] == L[0][1][0]
        rIsVert = R[0][0][0] == R[0][1][0]
        if lIsVert and rIsVert:
                if L[0][0][1] < R[0][0][1] or ( L[0][0][1] == R[0][0][1] and  L[0][1][1] < R[0][1][1] ):
                        return -1
                return 1
        elif L[0][0][0] == R[0][0][0]: # dom point is same X, can use hsegs comp
                return hsegCompForSorted( L,R )
        else: # on seg is vertical and on the right
                # do a LHT test from the non vert to the unused point of the vert
                if lIsVert:
                        p1 = R[0][0]
                        p2 = R[0][1]
                        p3 = L[0][0]
                        if p3 == p1 or p3 == p2:
                                p3 = L[0][1]
                        return isLeftTurn( p1,p2,p3 )
                elif rIsVert:
                        p1 = L[0][0]
                        p2 = L[0][1]
                        p3 = R[0][0]
                        if p3 == p1 or p3 == p2:
                                p3 = R[0][1]
                        return isLeftTurn( p1,p2,p3 )   
        raise Exception( ' should not be hERERERERE!' )

def convertSegsToHsegs( segs ):
        '''
        convert a list of segments to a list of halfsegments.

        Labels are all set to 0.

        **input**: a list of segs in the usual structure

        **output**: a sorted list of halfsegments.
        '''
        hsegs = list(  )
        for s in segs:
                hsegs.append( ((s[0],s[1]),0,0) )
                hsegs.append( ((s[1],s[0]),0,0) )
        hsegs.sort( cmp = hsegCompForSorted )
        return hsegs

def doWeSwitchSides( currVal, currSeg, nextSeg ):
        '''
        When walking a cycle boundary and assigning labels to halfsegments, this function determines when
        we should switch the labeling of the hsegs (swith the LA and LB values).

        **input**:
        
        currVal: a bool indicating if we are currently labeling the interior of the region as ABOVE the current hseg

        currSeg:  The hseg that was labeled according to the currVal value

        nextSeg: The next hseg in cyclic order around a cycle

        **output**:

        a boolean value indicating if the nextSeg should have the interior of the region as ABOVE (true) or BELOW (False)
        '''
        #if both are left or right, keep the labelling
        # otherwise, switch it
        if isLeft( currSeg ) == isLeft( nextSeg ):
                return currVal
        return not currVal



def getOuterWalkPointSequence( hsegs ):
        '''
        given a list oh hsegs, get the liset of points, in cyclic order, that define the boundary of outer cycle of the leftmost face of the region.  

        This function is meant for regions with a single face.  If there are multiple faces, only the leftmost face is porcessed.

        **input**: a list of hsegs

        **output**: a list of points.
        '''
        poiList = []
        if len( hsegs ) < 6:
                return poiList
        # create a hash table for the seg portions mapped to their index
        indexLookup = dict()
        for i, h in enumerate( hsegs ):
                indexLookup[h[0]] = i
        firstHseg = hsegs[0]
        prevHseg = firstHseg
        currHseg = None
        while currHseg != firstHseg:
                poiList.append( prevHseg[0][0] )
                currHseg = getNextOuterCycleWalk( prevHseg, hsegs, indexLookup )
                prevHseg = currHseg
        return poiList

def getNextOuterCycleWalk( searchHseg, hsegs, indexLookupDict ):
        '''
        get the next hseg in cyclic order from searchHseg along the outer cycle of a region structure.

        **input**

        searchHseg: the hseg from which the next hseg in cyclic order will be computed

        hsegs:  an hseg list (typically a well formed region, but not required)

        indexLookupDict:  A dictionary that maps segs to the index of thier equivalent hseg in the *hsegs* list

        **output**: a hseg
        '''
        return hsegs[ getNextOuterCycleWalkIndex( searchHseg, hsegs, indexLookupDict ) ]


def getNextOuterCycleWalkIndex( searchHseg, hsegs, indexLookupDict ):
        '''
        identical to *getNextOuterCycleWalk*, except the index of the hseg in the hsegs list is returned instead of the actual hseg.
        '''
        #find the brother
        index = indexLookupDict[(searchHseg[0][1],searchHseg[0][0])]
        domPoi = searchHseg[0][1]
        if index < 0:
                raise Exception( 'did not find hseg: getNextOuterCycleWalk' )
        # now rotate counter clockwise
        if index < len( hsegs)-1 and domPoi == hsegs[index+1][0][0]:
                return index+1
        else: #need to jump back to first seg aound this point
                while index > 0 and domPoi == hsegs[index-1][0][0]:
                        index -= 1
                if  domPoi != hsegs[index][0][0]:
                        print ((searchHseg[0][1],searchHseg[0][0]), searchHseg[1], searchHseg[2])
                        raise Exception(' did not find CCW walk seg: getNextOuterCycleWalk' )
                return index

def getConnectedCycleMappingConcav( hsegs ):
        ''' Assumes that assignCycleLabelsForConcavityMapping is already called
        Create a list such that the position at a cycle's index will have the cycle
        it is connected to
        Notes:
        
        * Exactly 1 cycle will be the outer cycle for the entire region
        * The first hseg will have the cycle number for the outer cycle as its above label
          (In this implementation the first cycle number is always 2 )
        * Each cycle will map to exactly 1 other cycle
        
        Once we have the list, make lists of segs for each connected cycle chain
        remove the connected cycle chain from the hsegs list.
        return the map list, the smaller hsegs list, and the connected cycle segment lists, and a dict mapping a point to all cycles connected at that point
        
        '''
        # get the ordering in which cycles appear
        cycSet = set()
        orderedCycList = []
        maxL = -1
        for h in hsegs:
                l = h[1] * h[2] * -1
                if isLeft( h ) and h[1] != -h[2] and l not in cycSet:
                        if l > maxL:
                                maxL = l
                        orderedCycList.append( l )
                        cycSet = cycSet | set( [l] )

        mapList = [None]*(maxL+1)
        for i in range( len( mapList ) ):
                mapList[i] = set()
        outerLabel = hsegs[0][1]*hsegs[0][2]*-1
        i = 0
        j = i
        fullSet = set()
        pointToLabelDict = dict()
        while j < len( hsegs ):
                # find last j with same dom point as i
                #start = i
                currSet = set()
                j = i+1
                while j < len( hsegs) and hsegs[i][0][0] == hsegs[j][0][0]:
                        li = hsegs[i][1]
                        lj = hsegs[j][1]
                        if hsegs[i][1] != -hsegs[i][2]:
                                li = hsegs[i][1]*hsegs[i][2] *-1
                        if hsegs[j][1] != -hsegs[j][2]:
                                lj = hsegs[j][1]*hsegs[j][2] *-1
                        if li != lj : # and li != outerLabel and lj != outerLabel:
                                currSet |= set([lj, li])
                        j+=1
                #end = j
                if j != i+1: # there were more than 2 segs at this dome point
                        for item in currSet:
                                mapList[item] |= currSet-set([item])
                                # also record the point at which we first saw this label
                                if item not in fullSet and 2 in currSet:
                                        fullSet |= set([item])
                                        pointToLabelDict[ hsegs[i][0][0] ] = item
                                
                i=j
        for item in mapList:
                item -= set( [outerLabel] )
        # now we have the maps. need to build up the complete sets.
        #connectedLabels = set()
        for i in range( 3, len( mapList ) ):
                if len(mapList[i] ) > 0:
                        fullSet = set()
                        mergeListSets( i, mapList, fullSet )
                        mapList[i] = fullSet
        # finally, copy the map list to all cycles involved
        for i in range( 3, len( mapList ) ):
                if len(mapList[i] ) > 0:
                        for c in mapList[i]:
                                if c != i:
                                        mapList[c] = set( mapList[i] )
        # update the poi to cycle dict to have the maplist
        finalPoiToLablesDict = dict()
        for k,v in pointToLabelDict.iteritems():
                finalPoiToLablesDict[k] = set([v]) | mapList[v]

        # now we need to build up the lists
        cycleSegLists = []
        for i in range( len( mapList ) ):
                cycleSegLists.append( [] )

        newHsegs = [ h for h in hsegs if h[1] == 2 or h[2] == 2 ]
        for h in hsegs:
                if h[1] == 2 or h[2] == 2 or h[1] == -h[2]:
                        continue
                else:
                        l = h[1]*h[2]*-1
                        cycleSegLists[l].append( h )
                        
        return mapList, newHsegs, cycleSegLists, finalPoiToLablesDict
                                
                
def mergeListSets( currCycle, meetingSets, fullSet ):
        '''
        a helper function to merge cycle lists.
        '''
        if len( meetingSets[currCycle] ) == 0:
                return
        fullSet |= meetingSets[currCycle]
        setCopy = set(meetingSets[currCycle])
        meetingSets[currCycle] = set()
        for c in setCopy:
                mergeListSets( c, meetingSets, fullSet )        
        
        

def assignCycleLabelsForConcavityMapping( hsegs ):
        '''
        first we need to relabel everything for our new mapping scheme
        assume connectors have both negative labels, segs have a pos an nevg
        labelling described in getIndexOfNextOuterCycleWalkSkipProcessed function
        '''

        newHsegs = [None]*len( hsegs) 
        for i,h in enumerate( hsegs ):
                if h[1]*h[2]*-1 > 0: # seg
                        la = 0
                        lb = 1
                        if h[1] > 0:
                                la = 1
                                lb = 0
                else: # connector
                        la = -1
                        lb = -1
                newHsegs[i] = (h[0], la, lb )
        hsegs = newHsegs
        #create a lookup for hseg indexes
        indexLookup = dict()
        for i, h in enumerate( hsegs ):
                indexLookup[h[0]] = i
        # a tricky bit in this cycle walk is when to stop.
        # once a seg is processed, we will not get back to it.
        # we can't stop when we reach the start vertex since many cycles may start
        # at the same vertex.  
        # we must compute the stop hseg when we start a walk.
        #   if firsthseg is a conn, stop hseg is the brother of the conn
        #   else, stop hseg is brother of greatest unprocessed hseg at that dom point

        # seg labels are reset, we now need to label everything based on an outer cycle walk
        cycleCount = 1
        for i in range( len ( hsegs ) ):
                h = hsegs[i]
                if isLeft( h ) and ( h[1]*h[2] *-1 <= 0 ): #find an unprocessed hseg that starts a cycle
                        cycleCount += 1
                        firstHseg = h
                        firstIndex = i
                        currHseg = h
                        currIndex = i
                        stopHseg = getStopHsegForOuterCycleWalkSkipProcessed( firstIndex, firstHseg, hsegs )
                        while True:
                                #process the current hseg and its brother
                                #find brother. 
                                bIndex = indexLookup[ (currHseg[0][1],currHseg[0][0])  ]
                                if bIndex < 0:
                                        raise Exception( 'did not find brother: assignCyclesForConcavityMapping')
                                if currHseg[1]*currHseg[2] == 0: # its a seg
                                        if currHseg[1] > 0:
                                                hsegs[currIndex] = ( currHseg[0], cycleCount, -1 )
                                                hsegs[bIndex]    = ( (currHseg[0][1],currHseg[0][0]), cycleCount, -1 )
                                        else:
                                                hsegs[currIndex] = ( currHseg[0], -1, cycleCount )
                                                hsegs[bIndex]    = ( (currHseg[0][1],currHseg[0][0]),-1, cycleCount )
                                else: # its a conn
                                        #don't relabel brother if its a connector
                                        hsegs[currIndex] = ( currHseg[0], cycleCount, -cycleCount )
                                        #hsegs[bIndex]    = ( (currHseg[0][1],currHseg[0][0]), cycleCount, -cycleCount )
                                # now that we have processed it, check if we have processed the last of the cycle
                        
                                if currHseg[0] == stopHseg[0]:
                                        break
                                # find the next unprocessed hseg CCW walk
                                currIndex = getIndexOfNextOuterCycleWalkSkipProcessed( currHseg, hsegs, indexLookup )
                                if currIndex == None: #error check
                                        raise Exception( 'assignLabelsForConcavityMapping: error: did not find next hseg' )
                                currHseg = hsegs[currIndex]
        
        # we have now labeled all hsegs
        return hsegs
                

def getStopHsegForOuterCycleWalkSkipProcessed( startIndex, startHseg, hsegs ):
        '''
        helper function for building well-formed regions from possibly non-well-formed input
        '''
        # greatest hseg around point will always be unprocessed (hseg order)
        
        # if its a conn, just get the brother
        if startHseg[1]*startHseg[2] != 0:
                return ((startHseg[0][1], startHseg[0][0]), startHseg[1], startHseg[2] )
        # otherwise, find largest around the dom point, and get the brother
        dom = startHseg[0][0]
        index = startIndex
        #index += 1
        while index+1 < len( hsegs) and dom == hsegs[index+1][0][0]:# and hsegs[index][1]*hsegs[index][2]*-1 > 0:
                index+=1
        #error checking
        if index == startIndex or hsegs[index][1]*hsegs[index][2]*-1 >0:
                print 'start: ', startHseg
                print'  found: ', hsegs[index]
                print 'start index, foundindex: ', startIndex, index
                raise Exception( 'error finding stop hseg.' )
        return (( hsegs[index][0][1], hsegs[index][0][0]), hsegs[index][1], hsegs[index][2] )

def getIndexOfNextOuterCycleWalkSkipProcessed( searchHseg, hsegs, indexLookupDict ):
        '''
        this walk will assume the following labelling scheme
        after processed la*lb*-1 will be positive, with -1 being the exterior label
        processed connectors will have 1,-1
        processed segs will have x, -1 where x>1
        
        connectors:                      segs:
        processed:   x,-x          x, -1 : x>1  (-1 is exterior)
        unprocessed: -1,-1         1,0          (0 is exterior)
        '''
        index = indexLookupDict[(searchHseg[0][1],searchHseg[0][0])]
        domPoi = searchHseg[0][1]
        if index < 0:
                raise Exception( 'did not find hseg: getNextOuterCycleWalk' )
        # now rotate counter clockwise.  Skip any segs with a label val above the threshold.
        # segs with a label above the threshold are already used
        origIndex = index
        index+=1
        while index < len( hsegs) and domPoi == hsegs[index][0][0] and hsegs[index][1]*hsegs[index][2]*-1 > 0:
                index += 1
        if index < len(hsegs) and domPoi == hsegs[index][0][0] and hsegs[index][1]*hsegs[index][2]*-1 <= 0: # foun an unprocessed hseg.   if not, got to jump back
                return index
        else:
                # got to jump back around the dom point.  Find firstseg, then go from there
                index = origIndex
                while index > 0 and domPoi == hsegs[index-1][0][0]:
                        index -= 1
                #minIndex = index
                #no go foraward to find an unprocessed
                while index < len( hsegs)-1 and domPoi == hsegs[index][0][0] and hsegs[index][1]*hsegs[index][2]*-1 >= 1:
                        index += 1
                if index < len( hsegs ) and domPoi == hsegs[index][0][0] and hsegs[index][1]*hsegs[index][2]*-1 <= 0: #if we found an unprocessed return it.  
                        return index
                else:  #else, we went all around and didn't find an unprocessed.  this means we finished the cycle
                        raise Exception( 'EROROROROROROROR, should not be here i think' )
        
def labelUniqueCycles( segs, onlyReturnOuterCycle = False ):
        '''
        will do interior walks around cycles.  
        
        Each cycle will get a unique label.
        
        Label numbers will not necessarily start at 2, and may skip numbers
        
        Will also remove sticks!!!  a full service solution!
        
        Cycles will have unique labels, but holes in particular will have labelling flipped.  
        
        Use: def switchLabelsForCorrectCycleLabelling( hsegs ): to finalize labels

        This function is used to create well-formed regions from possibly non-wellformed input.

        **input**: 

        segs: a list of segs.

        onlyReturnOuterCycle:  if you want a simple region, set this to true!

        **output**: a hseg list representing a well formed region. Agian, call def switchLabelsForCorrectCycleLabelling( hsegs ): to finalize labels!!!  Everything is labeled as an outercycle after this call.
        '''
        #remove dups from segs
        nonDupSegs = []
        for s in segs:
                if s[0] < s[1]:
                        nonDupSegs.append( s )
                else:
                        nonDupSegs.append( (s[1],s[0]) )
        seenSegSet = set( nonDupSegs )  
        segs = list(seenSegSet )
        #convert segs to hsegs
        hsegs = []
        for s in segs:
                hsegs.append( ((s[0],s[1]),-1,-1) )
                hsegs.append( ((s[1],s[0]),-1,-1) )
        hsegs.sort( cmp = hsegCompForSorted )
        # create a hash table for the seg portions mapped to their index
        indexLookup = dict()
        for i, h in enumerate( hsegs ):
                indexLookup[h[0]] = i

        # visit unprocessed segs in hseg order.  Each unprocessed will start a new cycle
        currLabel = 1
        nestedLabel = 2
        for i, h in enumerate( hsegs ):
                if (h[1] == -1 and h[2] == -1) and isLeft( h ): #unprocessed, left
                        #nestedLabel = currLabel+1
                        # interior walk the cycle
                        visitedPoiSet = set()
                        seenSegSet = set()
                        visitedHsegStack = deque()
                        completeVisitedHistoryStack = deque()
                        currIndex = i
                        startIndex = i
                        firstTimeThrough = True
                        currLabel = nestedLabel
                        nestedLabel += 1
                        labellingAbove = True
                        startHseg = hsegs[ startIndex ]
                        while True:
                                currHseg = hsegs[ currIndex ]
                                #check if this is a stick seg.  If so, just label it as invalid and move on
                                if (currHseg[0][1], currHseg[0][0]) in seenSegSet:
                                        # we have walked its brother.  this is a stick. label it as such
                                        hsegs[ currIndex ] = (currHseg[0],0, 0)
                                        brotherIndex =  indexLookup[ (currHseg[0][1],currHseg[0][0]) ]
                                        brother = hsegs[ brotherIndex ]
                                        brother = (brother[0], 0, 0)
                                        hsegs[ brotherIndex ] = brother
                                        #If this happens to be the brother of the startHseg, we need to unvisit the 
                                        # walked cycle. (since we walked the exterior and may have walked mutliple stick-connected cycles)
                                        if brother[0] == hsegs[startIndex][0]:
                                                for itemHseg in completeVisitedHistoryStack:
                                                        if itemHseg[1] != 0:
                                                                itemIndex = indexLookup[itemHseg[0]]
                                                                brotherIndex = indexLookup[ (itemHseg[0][1], itemHseg[0][0]) ]
                                                                hsegs[ itemIndex ] = (itemHseg[0],-1,-1)
                                                                hsegs[ brotherIndex ] = ((itemHseg[0][1], itemHseg[0][0]), -1, -1)
                                                break
                                # check if we have reached a processed seg (happpnes if we started on a stick)
                                elif (currHseg[1] > 0 or currHseg[2] > 0) and currIndex != startIndex: # we have to process first seg twice
                                        # we must have started on a stick, and followed it to get here. 
                                        # mark everything we followed as such
                                        visitedHsegStack.appendleft( startHseg )                                        
                                        for itemHseg in visitedHsegStack:
                                                itemIndex = indexLookup[itemHseg[0]]
                                                brotherIndex = indexLookup[ (itemHseg[0][1], itemHseg[0][0]) ]
                                                hsegs[ itemIndex ] = (itemHseg[0],0,0)
                                                hsegs[ brotherIndex ] = ((itemHseg[0][1], itemHseg[0][0]), 0, 0)
                                        break
                                # final case we have an unprocessed, non-stick seg.
                                # label it appropriately
                                else:
                                        #label the current hseg and its brother
                                        la = currLabel
                                        lb = -1
                                        if not labellingAbove:
                                                lb = currLabel
                                                la = -1
                                
                                        hsegs[ currIndex ] = (currHseg[0],la, lb)
                                        brotherIndex =  indexLookup[ (currHseg[0][1],currHseg[0][0]) ]
                                        brother = hsegs[ brotherIndex ]
                                        brother = (brother[0], la, lb)
                                        hsegs[ brotherIndex ] = brother
                        
                                        # if we have closed a loop, pop and fix
                                        if currHseg[0][0] in visitedPoiSet:
                                                stopPoi = currHseg[0][0]
                                                
                                                
                                                while True:
                                                        #debug statment.  We are about to pop a stack.  if it is empty, this prog
                                                        # will crash.  So, preemptively printout the current region. current seg,
                                                
                                                        # end of debug statement
                                                        # pop it, updateLabels
                                                        #print currHseg
                                                        poppedHseg = visitedHsegStack.popleft()
                                                        
                                                        poppedIndex = indexLookup[poppedHseg[0]]
                                                        poppedIndexBrother = indexLookup[  (poppedHseg[0][1], poppedHseg[0][0] ) ]
                                                        if      hsegs[ poppedIndex ][1] > 0:
                                                                hsegs[ poppedIndex ] = (poppedHseg[0],nestedLabel, -1)
                                                                hsegs[ poppedIndexBrother ] = ( (poppedHseg[0][1], poppedHseg[0][0]), nestedLabel, -1)
                                                        elif    hsegs[ poppedIndex ][2] > 0:
                                                                hsegs[ poppedIndex ] = (poppedHseg[0],-1, nestedLabel)
                                                                hsegs[ poppedIndexBrother ] = ( (poppedHseg[0][1], poppedHseg[0][0]), -1, nestedLabel)
                                                        if poppedHseg[0][0] == stopPoi:
                                                                break
                                                nestedLabel += 1
                                                
                                # update visited stacks and get the next seg
                                if firstTimeThrough:
                                        firstTimeThrough = False
                                else:
                                        # if not first time through, record point and seg, check stopping condition
                                        visitedPoiSet |= set( [currHseg[0][0]] )
                                        visitedHsegStack.appendleft( currHseg )
                                        completeVisitedHistoryStack.appendleft( currHseg )
                                        if currIndex == startIndex:
                                                # if we get here, we finished a cycle
                                                # if we only want the outer cycle, we can jsut return it here
                                                if onlyReturnOuterCycle:
                                                        hsegs = [ h for h in hsegs if h[1] != h[2] ]
                                                        return hsegs    
                                                break
                                        
                                seenSegSet |= set( [(currHseg[0])] )

                                # get next hseg
                                prevIndex = currIndex
                                currIndex = getNextInnerCycleWalkIndex( currHseg, hsegs, indexLookup )
                                # check if we are switching label above
                                if isLeft( hsegs[prevIndex] ) != isLeft( hsegs[currIndex] ):
                                        labellingAbove = not labellingAbove
                
        hsegs = [ h for h in hsegs if h[1] != h[2] ]
        return hsegs

def switchLabelsForCorrectCycleLabelling( hsegs ):
        '''
        Assumes all cycles have a unique label. Labels can start at any number and can skip  numbers.
        
        Use labelUniqueCycles() to guarantee that cycles have unique label numbers.
        
        Assumes that cycles are labeled consistently, but possibly with the exterior on the incorrect side.
        
        This function will flip labels for all cycles that need it.
        
        Approach: find the first seg in each cycle.  Do a point in polygon test for the midpoint of that seg.
        
        this will tell us if it is a hole or outer cycle.  then flip labels accordingly
        
        **input**: hsegs: a list of hsegs indicating a well-formed region, but with hole labels labeled as outer cycles.

        **output**: a well formed region with appropriate labels.
        '''
        # make sure seg labels start at 2 and don't skip
        oldIndexToNewIndexDict = dict()
        counter = 2
        for h in hsegs:
                label = h[1]*h[2]*-1
                if label not in oldIndexToNewIndexDict:
                        oldIndexToNewIndexDict[label] = counter
                        counter += 1
        oldIndexToNewIndexDict[-1] = -1
        hsegs = [(h[0], oldIndexToNewIndexDict[h[1]], oldIndexToNewIndexDict[h[2]]) for h in hsegs]
        # now labels are correct
        #maxLabeledHseg = max( hsegs, key=lambda h: h[1]*h[2]*-1 )
        maxLabel = counter-1 # maxLabeledHseg[1]*maxLabeledHseg[2]*-1
        counts = [0]*(maxLabel+1)
        cycleSeg = [None]*(maxLabel+1)
        #cyclePoint = [None]*(maxLabel+1)
        seenSet = set()
        for h in hsegs:
                num = h[1]*h[2]*-1
                if num not in seenSet:
                        seenSet |= set([num])
                        cycleSeg[num] = h
        #               cyclePoint[num] = ( (h[0][0][0]+h[0][1][0])/float(2),  (h[0][0][1]+h[0][1][1])/float(2))
        # now we have the points.  Do the point in polygon test. shoot a ray down
        # only test against segs that are not in the current cycle
        start = 2
        end = maxLabel+1
        for h in hsegs:
                if isLeft( h ) and h[0][0][0] != h[0][1][0]: #only look at left, non vertical segs
                        for i in range( start, end ):
                                if h[0] == cycleSeg[i]: #don't test the seg we go tthe point from
                                        continue
                                #elif h[0][0][0] >= cyclePoint[maxLabel][0]: # got past the cycle point 
                                        break
                                elif h[0][1][0] <= cycleSeg[i][0][0][0]:# hseg does not reach any more cyc points
                                        break
                                elif h[0][0][0] > cycleSeg[i][0][0][0]: # hseg is past current check point
                                        start+=1
                                        continue
                                elif h[0][0] == cycleSeg[i][0][0]: # share a dom point, use cycSeg sub point in LHTtest
                                        if isLeftTurn( h[0][0], h[0][1], cycleSeg[i][0][1]) == 1:
                                                counts[i]+=1
                                else:#elif h[0][1][0] > cyclePoint[i][0]: # hsegs spans the point in the x direction. and has different dom point
                                        # we checked that h[0][0][0] is <= to cycPoi X val and that h[0][1][0] > cycPoi X val
                                        # now check if h[0][0], h[0][1], cycPoi is a left hand turn.  if so, h is belowthe poi,
                                        # h is not vertical, and h spans the poi in the X direction
                                        if isLeftTurn( h[0][0], h[0][1], cycleSeg[i][0][0] ) == 1:
                                                counts[i] += 1
        # now we now how many segs lie below each cycle.  odd counts mean a hole.  even counts mean an outer cycle
        holeLabelSet = set( [ i for i,c in enumerate(counts) if c %2 == 1 ] )
        outercycleLabelSet =  set( [ i for i,c in enumerate(counts) if c %2 == 0 ] )
        for i,h in enumerate( hsegs ):
                label = h[1]*h[2]*-1
                if  label in holeLabelSet and cycleSeg[label][1] > 0:
                        hsegs[i] = (h[0], h[2], h[1] )
                elif label in outercycleLabelSet and cycleSeg[label][2] > 0:
                        hsegs[i] = (h[0], h[2], h[1] )
        return hsegs

def isLeftTurn( p1,p2,p3):
        '''
        Another left hand turn test.

        When traveling from point p1 to pont p2, do we take a left or right turn to travel on th point p3?

        **input**: 3 points, p1, p2, p3 in (x,y) format

        **output**: -1 if its a left turn, 0 if the points ar collinear, 1 if its a right turn.
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

def getNextInnerCycleWalkIndex( searchHseg, hsegs, indexLookupDict ):
        '''
        when traversing a cycle in cyclic order, find the next halfsegment by rotating the current segment through the INTERIOR of the cycle.

        This will find smaller cycles, but will interpret a well formed region correctly.

        **input**: 

        searchHseg.  The current hseg from which the next hseg in cyclic order is found

        hsegs: a hseg list forming a region

        indexLookupDict:  a hash table mapping segments to their corresponding halfsegment index in the hsegs list.

        **output**: the next hsed in cyclic order.
        '''
        #find the brother
        index = indexLookupDict[ (searchHseg[0][1],searchHseg[0][0]) ]
        domPoi = searchHseg[0][1]
        if index < 0:
                raise Exception( 'did not find hseg: getNextInnerCycleWalkIndex' )
        # now rotate clockwise
        if index > 0 and  domPoi == hsegs[index-1][0][0]:
                return index-1
        else: # need to jump to last seg around this point
                while  index < len( hsegs)-1 and domPoi == hsegs[index+1][0][0]:
                        index+=1
                if  domPoi != hsegs[index][0][0]:
                        print  ((searchHseg[0][1],searchHseg[0][0]), searchHseg[1], searchHseg[2])
                        raise Exception( ' did not find CW walk seg: getNextInnerCycleWalk' )
                return index
        
def extractAllLargeValidCycles( segs ):
        ''' 
        Extracts cycles from an input seg set.  
        
        segs shoule be a list of line segments. a segments is a tuple ((x1,y1),(x2,y2))

        This algorithm favors larger cycles, due to CCW rotations around hseg endpoints.
        
        will not return any cycles that touch another cycle from the interior
        
        Returns a valid region, correctly labeled.
        
        Each cycle get is own unique label

        '''
        #remove dups from segs
        seenSegSet = set()
        nonDupSegs = []
        for s in segs:
                if s in seenSegSet or (s[1],s[0]) in seenSegSet:
                        continue
                nonDupSegs.append( s )
                seenSegSet |= set([s])
        segs = nonDupSegs
        #convert segs to hsegs
        refHsegs = []
        for s in segs:
                refHsegs.append( ((s[0],s[1]), 0, 0 ) )
                refHsegs.append( ((s[1],s[0]), 0, 0 ) )
        refHsegs.sort( cmp = hsegCompForSorted )
        # create a hash table for the seg portions mapped to their index
        indexLookup = dict()
        for i, h in enumerate( refHsegs ):
                indexLookup[h[0]] = i

        # walk 1 cycle at a time
        # mark segs as being visited as we walk
        # invalids will have -1,-1 labels
        # when a seg is determined to be part of a cycle, mark all others that share a point
        # with it as invalid as well. and mark their brothers
        currCycle = 1
        meetCycle = 1
        index = 0
        extLabel = -1

        for origIndex,h in enumerate( refHsegs ):
                if isLeft( h ) and h[1]==0 and h[2] == 0:
                        currCycle = currCycle+1
                        if meetCycle+1 > currCycle:
                                currCycle = meetCycle+1
                        meetCycle = currCycle
                        origSeg = h[0]
                        # label the first seg
                        refHsegs[origIndex] = (h[0], currCycle, extLabel )
                        brotherIndex = indexLookup[(h[0][1], h[0][0])]
                        brother = refHsegs[brotherIndex]
                        refHsegs[brotherIndex] = (brother[0], currCycle, extLabel )

                        searchSeg = None
                        labellingAbove = False
                        index = origIndex
                        visitedPois = []
                        visitedIndexes = []
                        visitedPois.append( h[0][0] )
                        visitedIndexes.append( 0 )
                        while True: # origSeg != searchSeg :
                                searchSeg = (refHsegs[index][0][1], refHsegs[index][0][0] )

                                # find the index of the search seg
                                index = indexLookup[searchSeg]

                                #now we have the search seg, get the next CounterClockwise seg
                                #that has no labeling for the current cycle
                                found = False
                                tmpIndex = index
                                while  tmpIndex+1 < len( refHsegs ) and refHsegs[tmpIndex+1][0][0] == searchSeg[0] :
                                        tmpIndex = tmpIndex+1
                                        if  refHsegs[tmpIndex][1] == currCycle or  refHsegs[tmpIndex][2] == currCycle or refHsegs[tmpIndex][1] == 0 or  refHsegs[tmpIndex][2]==0:
                                                found  = True
                                                break                                           
                                if found:
                                        index = tmpIndex
                                else:
                                        # got to end seg around the point (max around the point), 
                                        #jump back to beginning around point and continue
                                        while index-1 >= 0 and refHsegs[index-1][0][0] == searchSeg[0]:
                                                index = index - 1
                                        while  index < len( refHsegs ) and refHsegs[index][0][0] == searchSeg[0] :
                                                if refHsegs[index][1] == currCycle or refHsegs[index][2] == currCycle or refHsegs[index][1] == 0 or  refHsegs[index][2]==0:
                                                        found = True
                                                        break #we found the next seg
                                                index = index+1
                                if not found:
                                        #only happens if we end on a stick that starts out of the very left most seg
                                        break
                                        print 'search seg: ', searchSeg, 'index ',index
                                        print '+++'
                                        for h in refHsegs:
                                                print h[0][0][0], h[0][0][1], h[0][1][0], h[0][1][1]
                                        print '------\n'
                                        for zz,h in enumerate(refHsegs):
                                                print zz, h[0][0][0], h[0][0][1], h[0][1][0], h[0][1][1], h[1], h[2]
                                        raise Exception( 'DID NOT FIND HSEG' )
                        
                                
                                # now we have the next seg in the cycle.  figure out if we switch labeling sides
                                # calcuate switch sides based on the previous hseg, not its brother used for searching
                                labellingAbove = doWeSwitchSides( labellingAbove, ((searchSeg[1], searchSeg[0]),0,0), refHsegs[index] )
                                if labellingAbove:
                                        la = extLabel
                                        lb = refHsegs[index][2]
                                        if lb >= 0:
                                                lb = currCycle
                                        refHsegs[index] = (refHsegs[index][0], la,lb)
                                # and the brother
                                        brotherIndex = indexLookup[(refHsegs[index][0][1], refHsegs[index][0][0])]
                                        la = extLabel
                                        lb = refHsegs[brotherIndex][2]
                                        if lb >= 0:
                                                lb = currCycle
                                        refHsegs[brotherIndex] = (refHsegs[brotherIndex][0], la,lb )
                                else:
                                        la =  refHsegs[index][1]
                                        lb = extLabel
                                        if la >= 0:
                                                la = currCycle # = (hsegs[index][0], extLabel, hsegs[index][2] )
                                        refHsegs[index] = (refHsegs[index][0], la, lb)# = (hsegs[index][0], extLabel, hsegs[index][2] )
                                # and the brother
                                        brotherIndex = indexLookup[(refHsegs[index][0][1], refHsegs[index][0][0])]
                                        la =  refHsegs[brotherIndex][1]
                                        lb = extLabel
                                        if la >= 0:
                                                la = currCycle # = (hsegs[index][0], extLabel, hsegs[index][2] )
                                        refHsegs[brotherIndex] = (refHsegs[brotherIndex][0], la, lb) # = (hsegs[index][0], extLabel, hsegs[index][2] )


                                #finally, mark all unmarked segs that share an endpoint with this seg, and their brothers, as visited
                                #by this cycle
                                #find start index and end index, then markem
                                endIndex = index
                                while  endIndex+1 < len( refHsegs ) and refHsegs[endIndex+1][0][0] == searchSeg[0]:

                                        endIndex = endIndex+1
                                startIndex = index
                                while startIndex-1 >= 0 and refHsegs[startIndex-1][0][0] == searchSeg[0] :
                                                # we have to jump to the largest seg around this point
                                        startIndex = startIndex - 1
                                for i in range( startIndex, endIndex+1):
                                        if refHsegs[i][1] == 0 and refHsegs[i][2] == 0:
                                                refHsegs[i] = (refHsegs[i][0], currCycle, currCycle)
                                                # and the brother
                                                brotherIndex = indexLookup[(refHsegs[i][0][1], refHsegs[i][0][0])]
                                                refHsegs[brotherIndex] = (refHsegs[brotherIndex][0], currCycle, currCycle )

                                # we have now labeled the seg, its time to loop again and get the next one
                                if refHsegs[index][0] == origSeg or (refHsegs[index][0][1], refHsegs[index][0][0] ) == origSeg:
                                #if origPoi == refHsegs[index][0][1]:
                                        break
                                # check if the submissivedom point has been visited in our cycle walk.  If it has,
                                # and its labelling is both sided current
                                # here we have the next seg.  Its dom point may have been visited before (we have just completed a cycle 
                                # at this segs dom point).  pop all segs back to this dom point, and relabel them
                                
                                if refHsegs[index][0][0] in visitedPois:
                                        stopPoi = refHsegs[index][0][0] 
                                        testPoi = None
                                        testIndex = None
                                        switchedALabel = False
                                        meetCycle = meetCycle+1
                                        while True:
                                                #prevPoi = testPoi
                                                testPoi = visitedPois.pop()
                                                #prevIndex = testIndex
                                                testIndex = visitedIndexes.pop()
                                                # relabel the prev segs to something new
                                                # relabel the cycle number to the new meetCycle number
                                                if refHsegs[testIndex][1] > 0:
                                                        switchedALabel = True
                                                        refHsegs[testIndex] = (refHsegs[testIndex][0], meetCycle, refHsegs[testIndex][2])
                                                        brotherIndex = indexLookup[(refHsegs[testIndex][0][1], refHsegs[testIndex][0][0])]
                                                        refHsegs[brotherIndex] = (refHsegs[brotherIndex][0], meetCycle, refHsegs[brotherIndex][2])
                                                elif  refHsegs[testIndex][2] > 0:
                                                        switchedALabel = True
                                                        refHsegs[testIndex] = (refHsegs[testIndex][0], refHsegs[testIndex][1], meetCycle )
                                                        brotherIndex = indexLookup[(refHsegs[testIndex][0][1], refHsegs[testIndex][0][0])]
                                                        refHsegs[brotherIndex] = (refHsegs[brotherIndex][0], refHsegs[brotherIndex][1], meetCycle )
                                                if testPoi == stopPoi:
                                                        break
                                        if not switchedALabel:
                                                meetCycle = meetCycle-1
                                        
                                # record the seg we have visited in the stack
                                visitedPois.append( refHsegs[index][0][0] )
                                visitedIndexes.append( index )
                        
        badRemoved = [r for r in refHsegs if r[1] !=r[2] ]      
        return badRemoved

def getListOfCycleLabels( hsegs ):
        '''
        get a list of all cycle labels used in a region.
        
        **input**: an hseg list representing a region

        **output**: a list if inegers
        '''
        aset = set([h[1] *h[2]*-1 for h in hsegs])
        cycList = list(aset)
        cycList.sort()
        return cycList


def getConnectedCycleMapping( hsegs ):
        '''
        returns a vector where the value V of the Ith Item indicates that cycle I
        either directly touches cycle V or touches a sequence of 1 or more cycles that 
        touch V.  Cycle V cill be the first cycle in hseg order that is touched by all other
        cycles whose value in the vector is V.

        ASSUMES that each cycle is labeled with a unique label.

        The basic idea is to find connected components (cycles that share points)
        '''
        # we will never have a loop of cycles
        # at a meet point, each label will show up twice!
        # holes won't touch from the inside

        # get the list of cycle labels
        cycSet = set()
        orderedCycList = []
        maxL = -1
        for h in hsegs:
                l = h[1] * h[2] * -1
                if isLeft( h ) and l not in cycSet: 
                        if l > maxL:
                                maxL = l
                        orderedCycList.append( l )
                        cycSet = cycSet | set( [l] )
        #now we have the cycles in the order that they appear
        #make a list:
        meetingSets = [None]*(maxL+1)
        for i in range( maxL+1 ):
                meetingSets[i]=set()
        # go through and make a set of cycs that share points
        i = 0
        while i < len(hsegs):
                j = i
                currStartCyc = hsegs[i][1]*hsegs[i][2] * -1
                while j+1 < len( hsegs ) and hsegs[i][0][0] == hsegs[j+1][0][0]:
                        j= j+1
                        l = hsegs[j][1]*hsegs[j][2]*-1
                        if l != currStartCyc:
                                meetingSets[currStartCyc] |= set( [l] )
                                meetingSets[l] |= set( [currStartCyc] )
                i = j+1
        #we now have a bunch of sets of cycles that meet.  we need to form the chains
        #get the first cycle in hseg order, and construct its chain.  remove its chain 
        #from the set list as we build it.
        cyleTofirstConnectedCycleMapList = [-1]*(maxL+1)
       
        #connectedLabels = set()
        for c in orderedCycList:
                if len(meetingSets[c] ) > 0:

                        mergeLists( c, meetingSets, cyleTofirstConnectedCycleMapList, c )

                        cyleTofirstConnectedCycleMapList[c] = -1

        return cyleTofirstConnectedCycleMapList
        


def mergeLists( currCycle, meetingSets, cyleTofirstConnectedCycleMapList, firstCycleInChain ):
        '''
        helper function identifying connected components in a region (cycles that meet at a point)
        '''
        if len( meetingSets[currCycle] ) == 0:
                return

        setCopy = set(meetingSets[currCycle])
        meetingSets[currCycle] = set()
        for c in setCopy:
                cyleTofirstConnectedCycleMapList[c] = firstCycleInChain 

                mergeLists( c, meetingSets, cyleTofirstConnectedCycleMapList, firstCycleInChain )
        


def relabelTouchingCyclesToFirstCycleNum( hsegs, cycleMapList ):
        ''' 
        relabel segments in touching cycles to have the same cycle label
        '''
        for i, h in enumerate( hsegs ):
                if cycleMapList[h[1]*h[2]*-1] > 0:
                        if h[1] > 0:
                                hsegs[i] = (h[0], cycleMapList[h[1]], h[2])
                        else:
                                hsegs[i] = (h[0], h[1], cycleMapList[h[2]])
        return hsegs


def addVerticalConnectorsPS( hsegs, highestCycleNum = None ):
        '''
        Adding vertical connectors (for use in regionInterpolator module)
        '''
        #debug check
        for h in hsegs:
                if h[0][0] == h[0][1]:
                        print '++++++ found bad: ', h
        # active list will be a sorted list
        #active list containts tuples: (index of hesg in hsegList, copy of hseg)
        if highestCycleNum == None:
                highestCycleNum = max( hsegs, key= lambda (h,la,lb): la)
        seenCycle = [False] * (highestCycleNum+1)
        connSet = set()
        holeLabelSet = set( )
        AL = []
        connectorList = []
        lastRemovedIndex = None
        for j,h in enumerate( hsegs ):
                cNum = h[1]*h[2]*-1
                if isLeft( h ):
                        # see if we need to connect linearly sep
                        # make sure x vals are different, otherwise we will jsut get a verti
                        if lastRemovedIndex != None and len( AL ) == 0 and hsegs[lastRemovedIndex][0][0][0] != h[0][0][0]:
                                connectorList.append( ( lastRemovedIndex, j, True ) )
                                connSet |= set( [ cNum, hsegs[j][1]*hsegs[j][2]*-1 ] )
                        #find where to insert it in the list
                        pos = 0
                        if len( AL ) > 0:
                                found = False
                                for i,g in enumerate( AL ):
                                        pos = i
                                        if hsegCmpForActiveList( h, g[0] ):
                                                found = True
                                                break
                                if not found:
                                        pos +=1
                        AL.insert( pos, (h,j) )
                        posBelow = None
                        if pos > 0:
                                posBelow = pos-1
                        posAbove = None
                        if pos < len( AL)-1:
                                posAbove = pos+1
                        # check below to see if this is a hole
                        if not seenCycle[ cNum ]:
                                seenCycle[ cNum ] = True
                                nonVertCount = 0
                                for i in range( pos ):
                                        if AL[i][0][0][0][0] != AL[i][0][0][1][0]: #not vertical
                                                nonVertCount+=1
                                if nonVertCount != 0 and nonVertCount %2 == 1:
                                        holeLabelSet |= set([cNum])
                        #if cycle is not connected, connect it
                                if cNum not in connSet:
                                        if posBelow != None:
                                                connectorList.append( (j, AL[posBelow][1], False ) )
                                                connSet |= set( [ cNum, AL[posBelow][0][1]*AL[posBelow][0][2]*-1 ] )
                                        elif posAbove != None:
                                                # must make sure there is nothing directly above this seg not in the AL
                                                # must check which seg, the one above in AL or
                                                # the one above with the same endpoint, is acutally closer
                                                # make sure to only walk up vertical segs.
                                                checkIndex = j+1
                                                while checkIndex < len( hsegs ) and h[0][0][0] == hsegs[ checkIndex ][0][0][0] and h[1]*h[2]*-1 == hsegs[ checkIndex ][1]*hsegs[ checkIndex ][2]*-1 and hsegs[ checkIndex ][0][0][0] == hsegs[ checkIndex ][0][1][0]:
                                                        checkIndex +=1
                                                # here check if above with same endpoint exists and is closer
                                                if h[0][0][0] == hsegs[ checkIndex ][0][0][0] and hsegs[ checkIndex ][0][0][1] <getYvalAtX(h[0][0][0], AL[posAbove][0][0]) :
                                                        connectorList.append( (checkIndex, AL[posAbove][1], False ) )
                                                else:
                                                        connectorList.append( (j, AL[posAbove][1], False ) )
                                                connSet |= set( [ cNum, AL[posAbove][0][1]*AL[posAbove][0][2]*-1 ] ) 
                else: #right hseg
                        #remove from activeList
                        lastRemovedIndex = j
                        tmpHseg = ((h[0][1],h[0][0]),h[1], h[2])
                        for i,r in enumerate( AL ):
                                if r[0] == tmpHseg:
                                        AL.pop(i)
                                        break
                        
        #relabel holes
        relabeledHsegs = [None]*len( hsegs )
        for i,h in enumerate( hsegs ):
                if h[1]*h[2]*-1 in holeLabelSet:
                        relabeledHsegs[i] = ( h[0], h[2], h[1] )
                else:
                        relabeledHsegs[i] = h
        hsegs = relabeledHsegs
        # we now have all the connector maps.  generate the connectors
        finalConns = []
        hsegsToRemoveSet = set([])
        segsToSplit = []
        for i,c in enumerate( connectorList ):
                if c[2]: # linear seperable cycles, always outer to outer
                        h = ((hsegs[c[0]][0][0],hsegs[c[1]][0][0]), -1, -1)
                        finalConns.append( h )
                        finalConns.append( ((h[0][1],h[0][0]),h[1],h[2] ) )
                else:
                        
                        y = getYvalAtX( hsegs[c[0]][0][0][0], hsegs[c[1]][0] )
                        s1 = hsegs[c[0]][0]
                        s2 = hsegs[c[1]][0]
                        #determine if the other seg is above or below the first seg
                        connLabel = -2
                        # create the connector
                        if s1[0][0] == s2[0][0]: #vertical dom points
                                finalConns.append( (( hsegs[c[0]][0][0], hsegs[c[1]][0][0]), connLabel, connLabel) )
                                finalConns.append( (( hsegs[c[1]][0][0], hsegs[c[0]][0][0]), connLabel, connLabel) )
                        elif s1[0][0] == s2[1][0]: # first seg in cycle is vertical with submissive point of other
                                finalConns.append( (( hsegs[c[0]][0][0], hsegs[c[1]][0][1]), connLabel, connLabel) )
                                finalConns.append( (( hsegs[c[1]][0][1], hsegs[c[0]][0][0]), connLabel, connLabel) )
                        else: #non vertical dom point
                                # might have multiple conns to the same seg, so we cannot split segs now.
                                # instead record the seg id of the seg split, and the split point, and generate at the end
                                splitPoi = ( hsegs[c[0]][0][0][0], y )
                                segsToSplit.append( (c[1], splitPoi ) )
                                #newSegsList.append( ( ( hsegs[c[1]][0][0], splitPoi), hsegs[c[1]][1], hsegs[c[1]][2] ) )
                                #newSegsList.append( ( ( splitPoi, hsegs[c[1]][0][0]), hsegs[c[1]][1], hsegs[c[1]][2] ) )
                                #newSegsList.append( ( ( splitPoi, hsegs[c[1]][0][1]), hsegs[c[1]][1], hsegs[c[1]][2] ) )
                                #newSegsList.append( ( ( hsegs[c[1]][0][1], splitPoi), hsegs[c[1]][1], hsegs[c[1]][2] ) )
                                finalConns.append( (( hsegs[c[0]][0][0],splitPoi), connLabel, connLabel) )
                                finalConns.append( (( splitPoi,hsegs[c[0]][0][0]), connLabel, connLabel) )
                                # invalidate split seg
                                hsegsToRemoveSet |= set( [hsegs[c[1]] ])
                                hsegsToRemoveSet |= set([ ( (hsegs[c[1]][0][1],hsegs[c[1]][0][0]), hsegs[c[1]][1], hsegs[c[1]][2] ) ] )
        # generate the split hsegs
        newSegsList = splitSegsOnIndexedPoints( hsegs, segsToSplit)
        

        # finally, remove invlids, merge in connectors
        hsegs = [ h for h in hsegs if h not in hsegsToRemoveSet ]
        newSegsList.sort( cmp = hsegCompForSorted )
        hsegs = mergeSortedHsegLists( hsegs, newSegsList )
        finalConns.sort( cmp = hsegCompForSorted )
        hsegs = mergeSortedHsegLists( hsegs, finalConns )
        return hsegs


def cmpForIndexedPoints( p1, p2):
        '''
        comparison function for indexed points.  stucture is (index, (x,y))
        '''
        if p1 == p2:
                return 0
        elif p1[0] < p2[0] or ( p1[0] == p2[0] and p1[1][0] < p2[1][0] ) or ( p1[0] == p2[0] and p1[1][0] < p2[1][0] and p1[1][1] < p2[1][1] ):
                return -1
        return 1


def splitSegsOnIndexedPoints( hsegs, indexedPoints ):
        '''
        break apart halfsegments at the points indicated in indexedPoints. Similar functions are in the segLibrary.

        In this case, we must break the hseg, and its brother, and maintain labels appropriately
        '''
        #define return list
        retHsegs = []
        # remove dups
        poiSet = set( indexedPoints )
        indexedPoints = [p for p in poiSet]
        
        #sort the indexed pois. first sort based on ID, then split point
        indexedPoints.sort( cmp = cmpForIndexedPoints )
        
        
        # now generate new segs
        # indexed point is tuple( index of seg to split, splitpoint)
        i = 0
        while i <  len( indexedPoints ) :
                ip = indexedPoints[i]
                h = hsegs[ip[0]]
                currSeg = ((h[0][0], ip[1]), h[1], h[2] )
                # ERROR.  might need to check for degenerate segs at each retHsegs.append.
                # shouldn't occur, but keep in mid
                retHsegs.append( currSeg )
                retHsegs.append( ((currSeg[0][1], currSeg[0][0]), currSeg[1], currSeg[2] ) )
                # if there are more intersections in this seg, keep on goin
                j = i
                while j+1 < len( indexedPoints ) and indexedPoints[j+1][0] == indexedPoints[i][0]:
                        # make the next portion of the seg
                        j += 1
                        currSeg = ((currSeg[0][1], indexedPoints[j][1]), currSeg[1], currSeg[2] )
                        retHsegs.append( currSeg )
                        retHsegs.append( ((currSeg[0][1], currSeg[0][0]), currSeg[1], currSeg[2] ) )
                        
                # make the last portion of the split seg
                currSeg = ((currSeg[0][1], h[0][1]), currSeg[1], currSeg[2]) 
                retHsegs.append( currSeg )
                retHsegs.append( ((currSeg[0][1], currSeg[0][0]), currSeg[1], currSeg[2] ) )
                i = j+1
        return retHsegs
        

def hsegCmpForActiveList( h1, h2 ):
        '''
        comparison function for hsegs in an active list.
        
        Used in PLANE SWEEP algorithms
        '''
        # first check for same dom point
        if h1[0][0] == h2[0][0]:
                return hsegComp( h1, h2 )
        y = getYvalAtX( h1[0][0][0], h2[0] )
        if h1[0][0][1] < y:
                return True
        return False


def getYvalAtX( x, seg):
        '''
        given a segment, and an x value that lies on the segment, return the y value on the segment at that x value.
        '''
        if x == seg[0][0]:
                return seg[0][1]
        elif x == seg[1][0]:
                return seg[1][1]

        x1 = seg[0][0]
        y1 = seg[0][1]
        x2 = seg[1][0]
        y2 = seg[1][1]
        y = ( (y2*x - y2*x1 - y1*x + y1*x1) / float((x2-x1))) + y1
        return y




def mergeSortedHsegLists( L1, L2 ):
        '''
        merge two sorted hseg lists into a single hseg list.
        '''
        retList = [None] * (len( L1 ) + len( L2 ) )
        i = 0
        j = 0
        k = 0
        L1Max = len( L1 )
        L2Max = len( L2 )
        while i < L1Max or j < L2Max:
                if i == L1Max:
                        retList[k] = L2[j]
                        j+=1
                elif j == L2Max:
                        retList[k] = L1[i]
                        i+=1
                elif hsegComp( L1[i], L2[j] ):
                        retList[k] = L1[i]
                        i+=1
                elif hsegComp( L2[j], L1[i] ):
                        retList[k] = L2[j]
                        j+=1
                else:
                        writeHsegListToFile( L1, 'debug_addVertsPS_L1.txt')
                        writeHsegListToFile( L2, 'debug_addVertsPS_L2.txt')
                        print 'error dups: ',  L1[i], L2[j]
                        raise Exception( 'found dup when merging' )
                k+=1
        return retList

def writeHsegListToFile( theRegion, theFileName ):
        ''' 
        write halfsegments to a file.

        1 hseg per line

        format: x1 y1 x2 y2 la lb
        ''' 
        theFileObject = open( theFileName, 'w')
        for h in theRegion:
                if isLeft( h ) or h[0][0] == h[0][1]:
                        s1 = str( h[0][0][0])+' '+str(h[0][0][1])+' '+str( h[0][1][0])+' '+str(h[0][1][1])+' '+ str(h[1])+' '+ str(h[2])  +' ' + '\n'
                        theFileObject.write( s1 )
        theFileObject.close()


def triangulate( hsegs ):
        '''
        polygon triangulator.  handles arbitrary polygons -- holes, nested holes, convex, etc
        
        pass it an ordered list of hsegs, get a bunch of triangles
        
        Not coded for maximum efficiency, but should be robust.
        
        **input**: hsegs --  an ordered list of hsegs.  for example, call region.createRegionFromSegs( ) on a bunch of segs
        
        **output**: A list of triangles.  a triangle is a tuple containing 3 points.
        triangles are not in a particular CW or CCW order
        '''
        #get split points, they will be all dom points, don't duplicate
        splitSet = set([h[0][0][0] for h in hsegs ])
        splitPois = [x for x in splitSet]
        splitPois.sort()

        numStrips = len(splitPois)-1
        stripSegs = [ list() for i in range(numStrips) ]  # the arrays of strips
        
        # grab a seg, put it each strip that it goes in
        # strip 1 will be at index 1, etc
        start = 0
        for h in hsegs:
                if (not isLeft( h )) or h[1] == -h[2]: #make sure we got a lefty and not a conn
                        continue
                for i in range( start, numStrips):
                        p = splitPois[i]
                        pnext = splitPois[i+1]
                        if h[0][0][0] == h[0][1][0] and (h[0][0][0] == p): #vertical on first or mid split
                                stripSegs[i].append( h )
                                if i > 0:
                                        stripSegs[i-1].append( h )
                                break
                        elif i == len(splitPois)-2 and h[0][0][0] == h[0][1][0] and (h[0][0][0] == pnext): #vertical on last split
                                stripSegs[i].append( h )
                                break
                        elif h[0][0][0] > p: # h is passed the split.  don't need to visit this split anymore
                                start += 1
                                continue
                        elif h[0][1][0] < p: # we have finished with this seg
                                break
                        elif h[0][0][0] == p and h[0][1][0] == pnext: # seg spans split exactly
                                stripSegs[i].append( h )
                                break
                        elif h[0][0][0] == p: # seg starts at left of this strip
                                newY = getYvalAtX( pnext, h[0] )
                                newH = ((h[0][0], (pnext,newY)), h[1], h[2] )
                                stripSegs[i].append( newH )
                                continue
                        elif h[0][1][0] == pnext: #seg ends at right of this strip
                                newY = getYvalAtX( p, h[0] )
                                newH = (((p,newY),h[0][1] ), h[1], h[2] )
                                stripSegs[i].append( newH )
                                break
                        else: # seg starts before and ends after this strip
                                newY1 = getYvalAtX( p, h[0] )
                                newY2 = getYvalAtX( pnext, h[0] )
                                newH = (((p,newY1), (pnext, newY2 )), h[1], h[2] )
                                stripSegs[i].append( newH )
                                continue

        # now we have all the splits, sort them and create triangles
        # All hsegs in lists are left.  Use the left hand turn test to compare them
        # can do all this in parallel
        for hsegList in stripSegs:
                hsegList.sort( cmp = hsegTriangulateStripCompForSorted )
        # each list is sorted.  now traverse up each list.  can do this in parallel
        # tris must be split up if parallelized
        tris = []
        for hsegList in stripSegs:
                if len(hsegList) == 0:
                        continue
                # boundary can't start on a vertical, must move to non vert
                start = 0
                while start < len( hsegList) and hsegList[start][0][0][0] == hsegList[start][0][1][0]: start += 1
                boundary = hsegList[start]
                for i in range( start, len(hsegList)):
                        h = hsegList[i]
                        if boundary[0] == h[0]:
                                boundary = h
                        elif h[0][0][0] == h[0][1][0]: #vertical seg
                                if h[0][0][0] == boundary[0][0][0] and boundary[1]>0: #vertical on left of strip
                                        if boundary[0][0] != h[0][0]:
                                                tris.append( (boundary[0][0], boundary[0][1], h[0][0]) )
                                                boundary = ((h[0][0], boundary[0][1]),boundary[1],boundary[2])
                                        tris.append( (boundary[0][0], boundary[0][1], h[0][1]) )
                                        boundary = ((h[0][1], boundary[0][1]),h[2],h[1])
                                elif  h[0][0][0] == boundary[0][1][0] and boundary[1]>0: #vertical seg on right of strip
                                        if boundary[0][1] != h[0][0]:
                                                tris.append( (boundary[0][0], boundary[0][1], h[0][0]) )
                                                boundary = ((boundary[0][0], h[0][0] ),boundary[1],boundary[2])
                                        tris.append( (boundary[0][0], boundary[0][1], h[0][1]) )
                                        boundary = ((boundary[0][0], h[0][1]),h[1],h[2])
                        elif boundary[1] > 0: #normal case.  segs form a trapezoid
                                if boundary[0][0] == h[0][0]: #segs share a point
                                        tris.append( (boundary[0][0], boundary[0][1], h[0][1] ) )
                                elif boundary[0][1] == h[0][1]: #segs share a point
                                        tris.append( (boundary[0][0], boundary[0][1], h[0][0] ) )
                                else: # trapezoid
                                        tris.append( (boundary[0][0], h[0][0], h[0][1] ) )
                                        tris.append( (boundary[0][0], boundary[0][1], h[0][1] ) )
                                boundary = h
                        else: # we are in an exterior portion, just update the boundary
                                boundary = h
        return tris
        
