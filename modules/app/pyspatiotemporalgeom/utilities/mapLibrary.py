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

from utilities import segLibrary



def breakSegsAndPreserveSegLabels( segs, la, lb ):
    '''
    `segs` is a list of segments that defines cycles. It is of the usual format: [((x1,y1),(x2,y2)), ... , ((xn,yn),(xm,ym))] 

    `la` and `lb` are lists of **integers**, are parallel to `segs`, and carry label infromation for the area *above* (la) and *below* (lb) its associated seg.
    
    #. Each cycle is assumed to be a well-formed, simple cycle. 
    #. Each cyle is assumed to carry a **unique label**.
    #. Segments can be in ANY order in `segs`, just as long as the list is parallel to `la` and `lb`
    #. `la` and `lb` are parallel to `segs`.  If the interior of the cycle lies above the segment, then `la` will have the cycle's labeland `lb` will have a value of `0`.  Vice versa if the interior of the cycle lies below the segment.  Note that a cycle may correspond to a *hole geometry* within a region, in which case the cycle will be labeled such that the cycle label lies on the *exterior* of the cycle.
    #. Segments from one cycle can intersect segments from another cycle, but indeividual cycles are simple (non-self intersecting)

    The basic idea is to label a bunch of cycles using, for instance `hsegLibrary.labelUniqueCycles()`, then just append them all to a segment list and label lists, and call this function.

    Note that duplicate segments are maintained with their original labels.  Therefore, this function can be used to break segments intersecting segments between cycles, then simply retrieve the individual cycles by label number.

    **Input:**

    #. `segs`: a list of segments.  It is assumed that the segments form simple cycles.  Each simple cycle is well formed.  Segments from different cycles can intersect.
    #. `la`: a list of labels indicating if the interior of a cycle lies above the corresponding segment.  `la` is parallel to `lb` and `segs`
    #. `lb`: same as `la`, but indicates if the interior of a cycle lies below the corresponding segment.

    **Output:**

    #. a list of segments.  No two segments in the list will intersect in thier interiors.  The only exception is that overlapping segments from the input will be duplicated.  One instance of the overlapping seg will exist for each cycle that contains the seg.
    #. a list of above labels
    #. a list of below labels

    '''


    # step 0.  make sure the segs have least point first
    
    segs = [ s if s[0] < s[1] else (s[1],s[0]) for s in segs]

    # step 1.  Sort the segs.  Make sure we keep the labels associated with the appropriate segs.
    zippedInput = zip( segs,la,lb)
    zippedInput.sort( )
    segs, la, lb = zip(*zippedInput)
    #print 'input segs appended and sorted\n', segs,'\n',la,'\n',lb

    # step 2.  Compute the intersection points between segs
    intersectPois = segLibrary.calcIntersectionPoints( segs )
    #print 'pois\n', intersectPois

    # step 3. Build the resulting segments
    #right now, the construct segs function handles labels a little weird because segLibrary.calcIntersectionPoints
    # was implemented in too specific a manner.  Until we fix that, we need to replace the colinear labels with
    # their original values 
    newIntersectPois = []
    for poi in intersectPois:
        newIntersectPois.append( (poi[0], (poi[1][0], poi[1][1]), la[ poi[0] ], lb[ poi[0] ]  ) )
    #print 'new Pois\n', newIntersectPois
    

    segs, la, lb = segLibrary.constructSegsWithLabels( newIntersectPois, segs, la, lb )
    #x = segLibrary.constructSegs( newIntersectPois, segs )
    #labeledSegs = zip( segs, la, lb)
    #labeledSegs.sort()
    #segs, la, lb = zip( *labeledSegs) 
    
    return segs, la, lb

def createMapFromCycles( segs, la, lb ):
    '''
    .. warning
        
        #. This function assumes that no two segments in `segs` intersect in thier interiors EXCEPT for pairs of segments that are equal.  That is, if two cycles share a portion of a boundary, those segs are dupicated for each cycle that shares a boundary; furthermore, each duplciate is labeled for its associated cycle

        #. The exterior label is `-1`

        #. `la` and `lb` are lists of *integers*

        To enforce point 1 above, simply use the `breakSegsAndPreserveSegLabels()` function.
    
    `segs` is a list of segments that defines cycles. It is of the usual format: [((x1,y1),(x2,y2)), ... , ((xn,yn),(xm,ym))] 

    `la` and `lb` are lists of **integers**, are parallel to `segs`, and carry label infromation for the area *above* (la) and *below* (lb) its associated seg.
    
    
    The purpose of this function is to create a map from a collection of individual cycles, so two cycles may overlap.  

    Because we are creating a map, the idea is to treat the input cycles as imposing a spatial partition on the embedding space.  This function will assign to each region in that partition the labels of all cycles that cover that region.  Thus, an area covered by 2 cycles will carry the labels of both of those cycles.

  
    It is assumed that input segments have correct labeling.
    
    **Input:**

    #. `segs` a list of segs in the format [ ((x1,y1),(x2,y2)), ... ,((xn,yn),(xm,ym))].  The segs form cycles.  **Segments cannot intersect each other, excet for overlapping segs where two cycles share a boundary**. 
    #. `la` a list of labels that is a parallel list to the segments (item 0 in la corresponds to item 0 in lb corresponds to item 0 in segs, etc).
    #. `lb` a list of labels that is a parallel list to the segments (item 0 in la corresponds to item 0 in lb corresponds to item 0 in segs, etc).
    
    `la` and `lb` are lists of integers.  It is assumed each cycle simply has a single integer as a label for this function
   
   **Returns:**

    #. A list of segs forming a map
    #. Parallel la and lb arrays with label IDs corresponding to the segs
    #. A dictionary to translate label indexes in the la and lb arrays to a set indicating all input labels for all input cycles that cover the corresponding region.

    .. warning::
        
        This function assumes that the **exterior** is labeled with `0`
    '''
    
    # steps 1-3 in creating the map occur in `breakSegsAndPreserveSegLabels( segs, la, lb ):`
    # step 4.  At this point, we have all the broken segs with their original labels.  The last part is to simply combine the labels.
    # this is done, basically, with a point in poly test for each segment.  the labels for a segment are adjusted based on the labels
    # of all segments that lie directly below it.
    # we will use a hash table to map ids of collections of labels to collections of labels
    index2LabelDict =dict()
    label2IndexDict = dict()
    labelSet = set( la+lb )
    nextIndex = max( labelSet ) + 1

    # put the exterior label with all interiors.  This just makes the computations a little easier
    for l in labelSet:
        labelWithExterior = frozenset([l])|frozenset([-1])
        index2LabelDict[l] = labelWithExterior
        label2IndexDict[labelWithExterior] = l
    
    #create label lists for returning (so we don't clobber the original lists)
    retLa = list( la )
    retLb = list( lb )

    #print nextIndex
    for i in range( len( segs) ):
        labelCountsDict = dict()
        aboveKnown = set()
        belowKnown = set()
        # print '***', segs[i],index2LabelDict[ la[i]],index2LabelDict[lb[i]]
        for j in range( len(segs ) ):
            adjustLabels = False
            if i == j:
                continue
            s = segs[i]
            r = segs[j]
            if abs(r[0][0]- r[1][0])<0.0000000001 : #skip verticals for R.
                continue
            
            # print '-', segs[j],index2LabelDict[ la[j]],index2LabelDict[lb[j]]
            if s == r:
                # s and r are identical, but have different indexes
                # merge the labels accordingly
                aboveKnown = aboveKnown | index2LabelDict[la[j]]
                belowKnown = belowKnown | index2LabelDict[lb[j]]
                adjustLabels = True
            
            elif s[0] == r[0]: # share a left end point
                if segLibrary.isLeftTurn( r[0], r[1], s[1] ) == 1:
                    # s is above r (they share a left end point)
                    # adjust S's labels accordingly
                    # the below label gets all the above labels from R
                    # the above label gets all the below labels from R that are not in the above labels of S
                    intAboveLabels = index2LabelDict[la[j]] - index2LabelDict[lb[j]]
                    intBelowLabels = index2LabelDict[lb[j]]- index2LabelDict[la[j]]
                    for label in intAboveLabels:
                        if label not in labelCountsDict:
                            labelCountsDict[label] = 0
                        labelCountsDict[label] += 1
                    for label in intBelowLabels:
                        if label not in labelCountsDict:
                            labelCountsDict[label] = 0
                        labelCountsDict[label] -= 1
                    adjustLabels = True     

            elif  r[0][0] <= s[0][0] and s[0][0] < r[1][0]: # r spans s's left point
                if segLibrary.isLeftTurn( r[0], r[1], s[0] ) == 1:
                    # s is above r.
                    #adjust S's labels accordingly
                    intAboveLabels = index2LabelDict[la[j]] - index2LabelDict[lb[j]]
                    intBelowLabels = index2LabelDict[lb[j]]- index2LabelDict[la[j]]
                    for label in intAboveLabels:
                        if label not in labelCountsDict:
                            labelCountsDict[label] = 0
                        labelCountsDict[label] += 1
                    for label in intBelowLabels:
                        if label not in labelCountsDict:
                            labelCountsDict[label] = 0
                        labelCountsDict[label] -= 1
                    adjustLabels = True     

        # now we have collected the openings and closings for all segs below this one
        closeLabelSet = index2LabelDict[lb[i]] - index2LabelDict[la[i]]
        # update closelabelset with known labels (from overlapping segs)
        closeLabelSet = closeLabelSet | ( belowKnown - aboveKnown)
        newLabelSet = set()
        for label in labelCountsDict:
            if labelCountsDict[label] > 0:
                #we found an interior that extends up to or over this seg
                newLabelSet = newLabelSet | set([label])
        # the new below set will be everything that was on the old below labels, plus everything in the new label set
        # don't forget known labels from overlapping segs
        newBelowSet =  frozenset( newLabelSet | belowKnown | index2LabelDict[lb[i]])
        # the new above set will be everything in the old above set, plus the things in the new label set - closed labels
        newAboveSet = frozenset( index2LabelDict[la[i]] | ( (aboveKnown|newLabelSet)-closeLabelSet) )
        
        # finally, update the dicttionaries and indexes.
        if newBelowSet in label2IndexDict:
            retLb[i] = label2IndexDict[ newBelowSet ]
        else:
            retLb[i] = nextIndex
            index2LabelDict[nextIndex] = newBelowSet
            label2IndexDict[newBelowSet] = nextIndex
            nextIndex += 1
        if newAboveSet in label2IndexDict:
            retLa[i] = label2IndexDict[ newAboveSet ]
        else:
            retLa[i] = nextIndex
            index2LabelDict[nextIndex] = newAboveSet
            label2IndexDict[newAboveSet] = nextIndex
            nextIndex += 1

    # remove the exterior label from all interiors
    for key in index2LabelDict:
        item =index2LabelDict[key]
        #print item
        if len(item) > 1:
            index2LabelDict[key] = item - frozenset([-1])
    # remove duplicates
    finalSegs = zip( segs, retLa, retLb)
    finalSegs = list( set( finalSegs) )
    segs, retLa, retLb = zip(*finalSegs )
    #print 'index2LabelDict\n', index2LabelDict
    #print 'label2IndexDict\n', label2IndexDict
    
    return segs, retLa, retLb, index2LabelDict


