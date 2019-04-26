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


import collections
import pyspatiotemporalgeom.structureRegion as structureRegion
import pyspatiotemporalgeom.region as region
import os
from pyspatiotemporalgeom.utilities import regionInterpolator
from pyspatiotemporalgeom.utilities import hsegLibrary
from pyspatiotemporalgeom.utilities import triangleLibrary
from pyspatiotemporalgeom.utilities import mapLibrary

class cIntervalRegion:
    '''
    A **Component Interval Region** describes the movement of a moving region over a single time interval.  Thus, a CIR is defined as a pair of structural regions (the source and destination) respectively associated with a timestamp.  Structures from the source are mapped to structured in the destination in order to represent how the components move across the interval.  The region interpolator function is used to actually create the movement.
    '''

    def __init__( self ):
        ''' 
        Constructor.  Set up the class variables.
        
        self.sourceSR = None
        self.sourceTime = None
        self.destSR = None
        self.destTime = None
        
        You must set these to appropriate values before doing anything useful.

        sourceSR and destSR must be structural regions

        sourceTime and destTime must be integer timestamps

        .. warning::

            When adding component IDs to the componentMap, you should use the `mapComponent()`
            function rather than directly adding them.  This will do some necessary checks.

            For example, it will check that both component IDS exist in thier structural regions
            
            If a component from sourceSR maps to mulitple comonents in destSR, then you
            must map the ID of the source components to an iterable object containing 
            destination components.  Python dicts, by default, do not take
            duplicate keys, but will simply clobber the earlier entry.

            This is not an issue if you simply use the `mapComponent()` function
        '''
        self.sourceSR = None
        self.sourceTime = None
        self.destSR = None
        self.destTime = None
        self.componentMap = dict()

    def mapComponent( self, sourceComponentID, destComponentIDs ):
        '''
        Add components to the component mapping in order to represent movement across the interval.

        The function ensures that the component IDS exist in the source and dest region, then adds
        the pair to the mapping.

        **Input**:

        sourceComponentID:
            The ID of the component in the source structural region that will map to component[s] in the destination structural region

        destComponentIDs:
            An integer or an iterable of integers representing IDs of components in the destionation region that the source component will map to.
        
        **Returns**:

        True:
            if the IDs all exist in the respective source and destination structural regions

        False:
            otherwise
        '''
        # convert the dest ID to an iterable if it is only 1 ID
        if isinstance( destComponentIDs, int ):
            destComponentIDs = [ destComponentIDs ]

        # check that the IDS refer to an actual structure
        if not self.sourceSR.hasComponent( sourceComponentID ):
            return False

        if not self.destSR.hasComponent( destComponentIDs ):
            return False

        # put the IDs in the map
        if sourceComponentID not in self.componentMap:
            self.componentMap[ sourceComponentID ] = []
        self.componentMap[ sourceComponentID ].extend( destComponentIDs )
        
        return True

    def getMotionTriangles( self, returnSingleListOfAllTris = False ):
        '''
        Return a list of motion triangles indicating the movement implied by the mapping of structures

        NOTE: line and point mappings are not yet implemented
        
        **Input**:

        returnSingleListOfAllTris
            if set to ``True``, the function returns a single list of ALL motion triangles describing the motion of all structures in this interval region.

            If set to ``False`` (the default), the function will return the motion triangles such that the triangles for each component are in thier own list.  See the return type descripion
        
        **Returns**:
        
        If ``returnSingleListOfAllTris=True``
            A list of Triangles. Each triangle is a 3 tuple of 3D points: ((x1,y1,z1),(x2,y2,z2),(x3,y3,z3)).  Two points will always share a Z value (defining a segment in the plane) and will ALWAYS be the first 2 points in the triple (that is: ``z1 == z2``).
        
        If ``returnSingleListOfAllTris=True``
            A list of tuples where each tuple holds the ID of the component in the source region, the ID of the component in the destination region, and the triangles describing the motion of that component across the interval.

            [(sID1, dID1, [((x1,y1,z1),(x2,y2,z2),(x3,y3,z3)), ... ]), ... ,(sIDN, dIDN, triangleList)]

            where the first 2 ``Z`` values in each triangle are always equivalent (ie, they define a line segment in the ``X,Y`` plane).
        '''
        trisWithMappings = [] # a list of tuples (sourceID, destID, triList)
        # for each structure, build a region, and interpolate.
        for sItemID in self.sourceSR.getAllComponentIDs():
            sItemType, sItem = self.sourceSR.getComponentByID( sItemID )
            if sItemType == 'F' or sItemType == 'H':
                # we have a structure from the source.  make it a region
                regS = hsegLibrary.labelUniqueCycles( sItem )
                # now we have region for a source structure.  make a region for whatever it maps to
                # and make the tris
                for dItemID in self.componentMap[ sItemID ]:
                    dItemType, dItem = self.destSR.getComponentByID( dItemID )
                    if dItemType == 'F' or dItemType == 'H':
                        # we found a structure to map to.  get the tris
                        regD = hsegLibrary.labelUniqueCycles( dItem )
                        # finally, interpolate and get tris.
                        # we take the tris as they are, don't check for self intersections
                        # which means we only get 1 list back (the second in the tuple)
                        x, tris, x = regionInterpolator.interpolate( regS, regD, self.sourceTime, self.destTime, True )
                        trisWithMappings.append( (sItemID, dItemID, tris ) )
        
        if returnSingleListOfAllTris:
            allTris = []
            for item in trisWithMappings:

                allTris.extend( item[2] )
            return allTris
        # return the list of tuples containing a source component ID, a dest component ID, and the list of tris for that structure
        return trisWithMappings

    def __str__(self):
        theString = str( self.sourceTime ) + '\n' + str( self.sourceSR ) + '\n' + str(self.destTime) + '\n' + str( self.destSR )
        theString += 'Mapping:\n'
        theString += str( self.componentMap )
        return theString

    def printToFileFor3DVis( self, openFileObject ):
        '''
        print the component interval region to a file formatted for visualtization.
        
        data is printed one segment on each line.  Each segment is printed with 3D coordinates.
        
        **Input**:
        
        openFileObject:
            a file object that has been opened for writing.
        '''
        self.sourceSR.printToFileFor3DVis( openFileObject, self.sourceTime )
        self.destSR.printToFileFor3DVis( openFileObject, self.destTime )

    def getStructuralRegionAtTime( self, time ):
        '''
        Exctract the structural region defined by this component interval region at time ``time``.

        Call the interpolator, get the triangles, extract the region from those triangles

        **Input**:

        time:
            The time at which to extract the structural regions

        **Returns**:

        None:
            If the ``time`` is outside the bounds of this interval regions

        structural region:
            otherwise
        '''
        print '1'
        if time < self.sourceTime or time > self.destTime:
            return None
        print '2'
        if time == self.sourceTime:
            return self.sourceSR

        if time == self.destTime:
            return self.destSR
        print '3'
        # find out the percentage of how far along the time interval **time** lies
        multiplier = float(time-self.sourceTime) / (self.destTime - self.sourceTime)

        # step 1:  get the motion triangles, but maintain the IDs of the compnonets involved so we can rebuild the mappings
        componentTris = self.getMotionTriangles( )
        # step 2:  create a structural region to hold the result
        sr = structureRegion.structuralRegion()
        print 'componentTris', componentTris
        # step 3: go through the triangles for each moving component, extract the segs at time **time**, and add the structures
        for component in componentTris:
            segs = []
            for tri in component[2]:
                s1 = ((tri[0][0],tri[0][1]),(tri[2][0],tri[2][1]) )
                s2 = ((tri[1][0],tri[1][1]),(tri[2][0],tri[2][1]) ) 
                if tri[2][2] < tri[0][2]:
                    s1 = (s1[1], s1[0])
                    s2 = (s2[1], s2[0])
                p1x = (multiplier * (s1[1][0] - s1[0][0])) + s1[0][0]
                p1y = (multiplier * (s1[1][1] - s1[0][1])) + s1[0][1] 
                p2x = (multiplier * (s2[1][0] - s2[0][0])) + s2[0][0]
                p2y = (multiplier * (s2[1][1] - s2[0][1])) + s2[0][1] 
                segs.append( ((p1x,p1y),(p2x,p2y)) )
            # now we have the segs.  place them into the return SR
            # note, there will never be a line or point in the middle of an interval 
            if self.sourceSR.getComponentType(component[0]) != 'H':
                sr.addFace( segs, component[0] )
            elif self.sourceSR.getComponentType(component[0]) == 'H':
                sr.addHole( segs, self.sourceSR.getIDsForHolesInFace( component[0] ) , component[0] )
            print 'segs: ', segs 
        return sr         

def computeTimeInstantsOfTopologicalChange( cir1, cir2 ):
    '''
    Find all time instants when a topological change occurs betweeen two input component interval regions.

    **Input**:

    ``cir1, cir2``
        Two component interval regions

    **Returns**:

        A sorted list of floats where each float is a time instant where the two input component interval regions experience a change in topology relative to each other.  For example, they were disjoint, and suddenly they meet.  These instants are discovered based on the intersections of motion triangles
    '''

    # for each item, build the motion triangles for all structures
    tris1 = cir1.getMotionTriangles( True )
    tris2 = cir2.getMotionTriangles( True )
#    thefile = open( '/tmp/alltris.txt','w')
#for t in tris1:
#        thestring = str( t[0][0] ) + ' ' +str( t[0][1] ) + ' ' +str( t[0][2] ) + ' ' +str( t[1][0] ) + ' ' +str( t[1][1] ) + ' ' +str( t[1][2] ) + '\n'
#        thefile.write( thestring )
#        thestring = str( t[0][0] ) + ' ' +str( t[0][1] ) + ' ' +str( t[0][2] ) + ' ' +str( t[2][0] ) + ' ' +str( t[2][1] ) + ' ' +str( t[2][2] ) + '\n'
#        thefile.write( thestring )
#        thestring = str( t[2][0] ) + ' ' +str( t[2][1] ) + ' ' +str( t[2][2] ) + ' ' +str( t[1][0] ) + ' ' +str( t[1][1] ) + ' ' +str( t[1][2] ) + '\n'
#        thefile.write( thestring )
#    thefile.write('E\n')
#    for t in tris2:
#        thestring = str( t[0][0] ) + ' ' +str( t[0][1] ) + ' ' +str( t[0][2] ) + ' ' +str( t[1][0] ) + ' ' +str( t[1][1] ) + ' ' +str( t[1][2] ) + '\n'
#        thefile.write( thestring )
#        thestring = str( t[0][0] ) + ' ' +str( t[0][1] ) + ' ' +str( t[0][2] ) + ' ' +str( t[2][0] ) + ' ' +str( t[2][1] ) + ' ' +str( t[2][2] ) + '\n'
#        thefile.write( thestring )
#        thestring = str( t[2][0] ) + ' ' +str( t[2][1] ) + ' ' +str( t[2][2] ) + ' ' +str( t[1][0] ) + ' ' +str( t[1][1] ) + ' ' +str( t[1][2] ) + '\n'
#        thefile.write( thestring )
#    thefile.close() 
    # now that we have all the tris, find the temporal points at which those motion tris intersect.
    zValSet = set()
    for t1 in tris1:
        for t2 in tris2:
            vals = triangleLibrary.triangle3DTriangle3DIntersectionPoint( t1, t2 )
            # extract jsut the z value (item [2] in the point tuples)
            zValSet |= set( [ x[2] for x in vals ] )
    # make sure the start and end times are in there.
    zValSet |= set( [cir1.sourceTime, cir2.sourceTime, cir1.destTime,cir2.destTime] )
    zList = list( zValSet )
    zList.sort()
    return zList

def computeMapsAtTimeInstants( zList, cir1, cir2 ):
    ''' 
    Compute a map overlay of the structural regions defined by ``cir1`` and ``cir2`` at each time in the zList

    **Input**:

    ``zList``
        A list of time values.  Sorted from earliest to latest

    ``cir1`` and ``cir2``
        component interval regions.  It is assumed they are **aligned** in the sense that they have equivalent source and destination times.

    **Output**:

    A list maps where each map is a tuple containing: the time instant,  a list of segments, above labels for the segments, below labels for the segments, and the label to label list dictionary:

    ``[(zval, segList, LAlist, LBList, label2DataDictionary, r1MapLabelToStructureIDDictionary,r2MapLabelToStructureIDDictionary, r1facetoHoleMappingUsingMapLabels, r2facetoHoleMappingUsingMapLabels ), ... ]``

    The maps are labeled with the following conventions:

    * interior face cycles have an even label
    * interior of hole cycles have an odd label
    * exterior label is -1
    * Labels for sturctural regions from ``cir1`` have positive labels (except for an exterior of -1), labels for sturctural regions from ``cir2`` have negative labels,
    
    Each seg will have a single above label (LA) and a single below labele (LB).  The  label2DataDictionary maps that LA or LB to the list of regin labels indicating the interiors of all cycles that lie above (LA) or below (LB) the line segment.  This labels were made according to the previos bullet point.  r1MapLabelToStructureIDDictionary maps those labels to the actual ID of the structure in the source structural region of CIR1.  likewise for r2MapLabelToStructureIDDictionary.
    '''
    if not isinstance(zList, collections.Iterable):
        zList = [ zList ]
        
    
    # step 2: extract the structural regions at those points in time
    structRegions1 = []
    structRegions2 = []
    
    # in the following, the IDs of each structure will be identical to what they were in 
    # the original interval regions.
    # This way, the mapping in the original component interval region still applies.
    for z in zList:
        r1 = cir1.getStructuralRegionAtTime( z )
        r2 = cir2.getStructuralRegionAtTime( z )
        structRegions1.append( (r1,z) )
        structRegions2.append( (r2,z) )
        print z
        print r1
        print r2
        print '^^^^^^^^^^^^'
    # step 3: intersect the components, and maintain the mappings.
    # for each pair of aligned structural regions, we will create a map with the following conventions:
    # interior face cycles have an even label
    # interior of hole cycles have an odd label
    # exterior label is -1
    # one region has positive labels, the other has negative labels.
    # we will compute a map overlay of all those cycles, then just pick out the pieces we need.
    allMaps = []
    for i in range( len( structRegions1 ) ):
        # get the first pair
        r1 = structRegions1[i][0]
        r2 = structRegions2[i][0]
        if r1 == None or r2 == None:
            continue
        # so, we just need to get each cycle, and label it appropiatly.
        r1LabeledSegs = []
        r2LabeledSegs = []
        r1MapLabel2ID = dict()
        r2MapLabel2ID = dict()
        r1ID2MapLabel = dict()
        r2ID2MapLabel = dict()

        # get labeled segs for r1
        currID = 2
        for fID in r1.F:
            print 'currID: ', currID, ': ', r1.F[ fID ]
            hsegs = hsegLibrary.labelUniqueCycles( r1.F[ fID ] )
            leftHsegs = [ h for h in hsegs if h[0][0] < h[0][1] ]
            leftHsegs = [ (h[0], currID, -1) if h[1] > 0 else (h[0], -1, currID) for h in leftHsegs ]
            r1LabeledSegs.extend( leftHsegs )
            r1MapLabel2ID[ currID ] = fID
            r1ID2MapLabel[ fID ] = currID
            currID +=2
        currID = 3
        for hID in r1.H:
            hsegs = hsegLibrary.labelUniqueCycles( r1.H[ hID ] )
            leftHsegs = [ h for h in hsegs if h[0][0] < h[0][1] ]
            leftHsegs = [ (h[0], currID, -1) if h[1] > 0 else (h[0], -1, currID) for h in leftHsegs ]
            r1LabeledSegs.extend( leftHsegs )
            r1MapLabel2ID[ currID ] = hID
            r1ID2MapLabel[ hID ] = currID
            currID +=2
        # get labeled segs for r2
        currID = -2
        for fID in r2.F:
            print 'currID: ', currID, ': ', r2.F[ fID ]
            hsegs = hsegLibrary.labelUniqueCycles( r2.F[ fID ] )
            leftHsegs = [ h for h in hsegs if h[0][0] < h[0][1] ]
            leftHsegs = [ (h[0], currID, -1) if h[1] > 0 else (h[0], -1, currID) for h in leftHsegs ]
            r2LabeledSegs.extend( leftHsegs )
            r2MapLabel2ID[ currID ] = fID
            r2ID2MapLabel[ fID ] = currID
            currID -=2
        currID = -3
        for hID in r2.H:
            hsegs = hsegLibrary.labelUniqueCycles( r2.H[ hID ] )
            leftHsegs = [ h for h in hsegs if h[0][0] < h[0][1] ]
            leftHsegs = [ (h[0], currID, -1) if h[1] > 0 else (h[0], -1, currID) for h in leftHsegs ]
            r2LabeledSegs.extend( leftHsegs )
            r2MapLabel2ID[ currID ] = hID
            r2ID2MapLabel[ hID ] = currID
            currID -=2
        # we need to convert the F2H dicts to map labels.  this makes things easier later on.
        r1MapLabelF2H = dict()
        r2MapLabelF2H = dict()
        for fID in r1.F2H:
            if r1ID2MapLabel[ fID ] not in r1MapLabelF2H:
                r1MapLabelF2H[ r1MapLabel2ID[ fID ] ] = []
            for hID in r1.F2H[fID]:
                r1MapLabelF2H[ r1ID2MapLabel[ fID ] ] = r1ID2MapLabel[ hID ]
        for fID in r2.F2H:
            if r2ID2MapLabel[ fID ] not in r2MapLabelF2H:
                r2MapLabelF2H[ r2ID2MapLabel[ fID ] ] = []
            for hID in r2.F2H[fID]:
                r2MapLabelF2H[ r2ID2MapLabel[ fID ] ] = r2ID2MapLabel[ hID ]
        # we now have all the segments to build a map.  put them together and go
        print 'results', zList[i]
        if len( r1LabeledSegs) > 0 or len( r2LabeledSegs ) == 0:
            
            allSegs = r1LabeledSegs + r2LabeledSegs
            print allSegs
            print '---'
            allC, allLa, allLb = zip(*allSegs )
            segs, la, lb = mapLibrary.breakSegsAndPreserveSegLabels( allC, allLa, allLb)
            rsegs, rla, rlb, index2labelDict = mapLibrary.createMapFromCycles( segs, la, lb )
            print zip( rsegs, rla, rlb )
            print index2labelDict
            allMaps.append( (zList[i], rsegs, rla, rlb, index2labelDict, r1MapLabel2ID, r2MapLabel2ID, r1MapLabelF2H, r2MapLabelF2H) )
        else:
            allMaps.append( (zList[i], [], [], [], dict(), dict(), dict(),dict(), dict() ) )
        print '#############'
    return allMaps

def intersection( cir1, cir2 ):
    '''
    computes the intersection of two component interval regions

    .. warning:: 

        Intersection assumes that cir1 and cir2 are temporally aligned. That is, they have the same start and end times.

        If this is not the case, you must align them using ``def computeTimeInstantsOfTopologicalChange()`` and then create the aligned interval regions.


    **Input**:

    cir1:
        a component interval region

    cir2:
        a component interval region

    **Returns**:

    A list of component interval regions sorted by time (earliest to latest)
    '''

    if cir1.sourceTime != cir2.sourceTime or cir1.destTime != cir2.destTime:
        return []

    # step 1: find all time stamps when a topological change occurs between line segments of the input regions.
    zList = computeTimeInstantsOfTopologicalChange( cir1, cir2 )
    
    print 'zlist:'
    print zList

    # step 2: for each point of topological change, compute the map overlay at that time
    # according to the following function.
    allMaps = computeMapsAtTimeInstants( zList, cir1, cir2 ) 

    for item in allMaps:
        for x in item:
            print x
        print '*-------------------------'

    # the last bit is to extract the faces that we need.
    # and build up the component interval regions.
    resultFaces = [] # each entry is a dict faceID->cycleID->list of individual face cycles (a list of segs)
    resultHoles = [] # each entry is a dict holeID->cycleID->list of individual hole cycles (a list of segs) 
    resultLines = [] # each entry is a dict lineID->simpleLineID->list of individual simple lines(a list of segs)
    resultPoints = []# each entry is a dict poiID-> list of individual points
    resultCIRs = []  # the CIRs resulting from the intersections
    for i in range( len( allMaps ) ):
        print '---> Map:', i, ':'
        for c in allMaps[i]:
            print c
        print '<<<<*' 
        
        faceCycles = collections.defaultdict( list )
        holeCycles = collections.defaultdict( list )
        lineSegs = collections.defaultdict( list )

        point2StructsContainingPoint = collections.defaultdict( set )
        point2LabelsOnThePoint = collections.defaultdict( set )
        map1 = allMaps[i]
        map1Index2LabelDict = map1[4]
        if len( map1[1] ) == 0:
            # no intersection at this time interval
            continue
        # we have a map at two consective time instants.
        # find the labels where two faces and no holes overlap.
        # allMaps[i] structure:
        # (zval, segList, LAlist, LBList, label2DataDictionary, r1MapLabelToStructureIDDictionary,r2MapLabelToStructureIDDictionary )
        
        # for each segment in map1, find the labels of the structures we want to keep, and add the segs to those structures.
        # also, create map of point->structures containing point
        # and a map of point->labels on the point
        for i in xrange( len( map1[1] ) ):
            seg = map1[1][i]

            # record what labels lie on each point
            point2LabelsOnThePoint[ seg[0] ] |= map1Index2LabelDict[map1[2][i]]  | map1Index2LabelDict[ map1[3][i]]
            point2LabelsOnThePoint[ seg[1] ] |= map1Index2LabelDict[map1[2][i]] | map1Index2LabelDict[map1[3][i]] 

            # compute the labels of pairs of intersecting faces and holes.
            # put each seg in a set with strucutres carrying the same label
            faceCycSet, holeCycSet, lineCycSet = relevantCyclesForIntersection( map1Index2LabelDict[ map1[2][i] ], map1[7], map1Index2LabelDict[ map1[3][i]], map1[8] )
            print 'faceCycSet', faceCycSet
            print 'above:', map1Index2LabelDict[ map1[2][i] ]
            print 'below:', map1Index2LabelDict[ map1[3][i]]
            # record the seg in its appropriate structures
            for f in faceCycSet:
                point2StructsContainingPoint[ seg[0] ] |= set( [f] )
                point2StructsContainingPoint[ seg[1] ] |= set( [f] )
                faceCycles[f].append( seg )
            for h in holeCycSet:
                point2StructsContainingPoint[ seg[0] ] |= set( [h] )
                point2StructsContainingPoint[ seg[1] ] |= set( [h] )
                holeCycles[h].append( seg )
            for l in lineCycSet:
                point2StructsContainingPoint[ seg[0] ] |= set( [l] )
                point2StructsContainingPoint[ seg[1] ] |= set( [l] )
                lineSegs[l].append( seg )

        # now, the segments are organized based on thier labels 
        # we need to extract the actual structures. 
        # remember, 2 simple regions can intersect resulting in 
        # multiple output regions

        print 'faceCycles', faceCycles
        print 'holeCycles', holeCycles
        print 'lineSegs', lineSegs

        # we now have a bunch of structures organized by label.  But, a label may map to multiple faces.  We need to get all 
        # faces and simple lines individually.
        individualFaceCycles = dict()
        for fID in faceCycles:
            individualFaceCycles[fID] = dict()
            # for the segs associated with a particular label, 
            # get all the cycles present in those segs.  Basically,
            # the intersection of two faces can result in multiple simple regions.
            # we need to get them all
            hsegs = hsegLibrary.labelUniqueCycles( faceCycles[ fID ] )
            for h in hsegs:
                if h[0][0] < h[0][1]:
                    # collect left segs, get the cycleID of the hseg
                    hseglabel = h[1]*h[2]*-1
                    if hseglabel not in individualFaceCycles[fID]:
                        individualFaceCycles[fID][hseglabel] =[]
                    individualFaceCycles[fID][hseglabel].append( h[0] )
        
        individualHoleCycles = dict()
        # with holes, we may have multiple hole cycles with the same label.
        for hID in holeCycles:
            individualHoleCycles[hID] = dict()
            hsegs = hsegLibrary.labelUniqueCycles( holeCycles[ hID ] )
            for h in hsegs:
                if h[0][0] < h[0][1]:
                    # collect left segs, get the cycleID of the hseg
                    hseglabel = h[1]*h[2]*-1
                    if hseglabel not in individualHoleCycles[hID]:
                        individualHoleCycles[hID][hseglabel] =[]
                    individualHoleCycles[hID][hseglabel].append( h[0] )
        #again, the segs with the same label may contain disjoint simple lines.  
        #need to find all connected structures.
        individualSimpleLines = dict() 
        simpleLineID = 2
        for lID in lineSegs:
            individualSimpleLines[lID] = collections.defaultdict(list)
            # idea is to map end points to the segs that contain them.  
            # then grab a line, find lines that share the end point, and build them up.
            point2segDict = collections.defaultdict(set)
            processedPointSet = set()
            segSet = set( lineSegs[ lID ] )
            # create a dictionary of points to segs that contain the point
            for seg in segSet:
                for p in seg:
                    point2segDict[p] |= set([seg])
            # now go through the segs.  use a queue! or stack
            pointsToProcess = collections.deque()
            while len( segSet ) > 0:
                seg = segSet.pop()
                # check if we have processed the points yet, put them in the queue if
                # we haven't
                for p in seg:
                    if p not in processedPointSet:
                        processedPointSet |= set([p])
                        pointsToProcess.append( p )
                while len( pointsToProcess ) > 0:
                    # grab a point, add its segs to the list
                    p = pointsToProcess.pop()
                    individualSimpleLines[lID][simpleLineID].extend(  point2SegDict[p] )
                    # update the points to process
                    for s2 in point2SegDict[p]:
                        # we are processing this seg, so remove it from 
                        # the set to be processed
                        segSet -= set([s2])
                        # add the end points of the seg to be processed
                        for p2 in s2:
                            if p2 not in processedPointSet:
                                processedPointSet |= set([p2])
                                pointsToProcess.append( p2 )
                    # at the end of the loop, we have grabbed a point, appended all
                    # segs containing that point to the simple line, and taken
                    # the end points of all those segs and put them in a list
                    # to be processed.
                #one simple line has been processed, so increment the ID.
                simpleLineID += 1
                
        # finally, find all intersection points in the map that were not involved above.
        # we need points where 2 faces meet, or where 2 faces and a hole meet.
        individualPoints = collections.defaultdict( list )
        for p in point2LabelsOnThePoint:
            # we have a point, and the list of labels on that point.  
            #first find all intersecting face labels
            posFaces= [ l for l in point2LabelsOnThePoint[ p ] if l > 0 and l%2 == 0]
            negFaces= [ l for l in point2LabelsOnThePoint[ p ] if l < -1 and l%2 == 0]
            posHoles= [ l for l in point2LabelsOnThePoint[ p ] if l > 0 and l%2 != 0]
            negHoles= [ l for l in point2LabelsOnThePoint[ p ] if l < -1 and l%2 != 0]
            # get all face combos
            faceCombos = []
            for l1 in posFaces:
                for l2 in negFaces:
                    faceCombos.append(  (l1,l2) )
            # get all hole combos
            holeCombos = []
            for l1 in faceCombos:
                for l2 in posHoles:
                    holeCombos.append( (l1[0], l1[1], l2) )
            for l1 in faceCombos:
                for l2 in negHoles:
                    holeCombos.append( (l1[0], l1[1], l2) )
            # now we know the labels of relevant structures that contain this point.
            # if such a structure is not in the point2StructsContainingPoint[p] set
            # then we know it is a meet at point situation.
            for l in faceCombos+holeCombos:
                if l not in point2StructsContainingPoint[p]:
                    # we found 2 faces that meet at a point!
                    individualPoints[l].append( p )
        
        print 'Individual face cycles:\n', individualFaceCycles
        print 'Individual hole cycles:\n', individualHoleCycles
        print 'Individual line segs:\n', individualSimpleLines
        print 'Individual points:\n', individualPoints
    
        # record the lists:
        resultFaces.append( individualFaceCycles )  
        resultHoles.append( individualHoleCycles )
        resultLines.append( individualSimpleLines )
        resultPoints.append( individualPoints )

    for i in range( len( zList ) ):
        print zList[i]
        print 'face:', resultFaces[i]
        print 'hole:', resultHoles[i]
        print 'line:', resultLines[i]
        print 'point:', resultPoints[i]
    for i in range( len( zList )-1 ):
        sr1 = structureRegion.structuralRegion()
        sr2 = structureRegion.structuralRegion()
        cir = cIntervalRegion()
        cir.sourceTime = zList[i]
        cir.destTime = zList[i+1]
        cir.sourceSR = sr1
        cir.destSR = sr2
        # build each structural region.
        # get faces, lines, points with same labels, and map them
        faceS = resultFaces[i]
        holeS = resultHoles[i]
        lineS = resultLines[i]
        pointS = resultPoints[i]
        faceD = resultFaces[i+1]
        holeD = resultHoles[i+1]
        lineD = resultLines[i+1]
        pointD = resultPoints[i+1]
        assignFacesToFacesLinesPoints( cir, faceS, faceD, lineD, pointD)
        assignHolesToHolesLinesPoints( cir, holeS, holeD, lineD, pointD)
        assignLinesPointsToFaces( cir, lineS, pointS, faceD)
        assignLinesPointsToHoles( cir, lineS, pointS, holeD)
        resultCIRs.append( cir )
    return resultCIRs

def assignLinesPointsToHoles( intervalReg, lineS, pointS, holeD ):
    '''
    given a component interval region that is set up with source and destination objects, 
    map the lines and points in a source structural region to holes in the destination region
    this is used with  set operations

    At the moment, we map a line/point to every hole that shares its label.  This needs to be addressed in the future.

    **Input**:

    intervalReg
        An interval region with source and destination objects already created

    lineS:
        A 2 level dictionary of mapIDs->simpleLineID->listOfSegments.  simpleLineID is just a temporary identifier.  listOfSegments is a list of line segments that form a cycle.  lineS pertains to the source structural region in an interval region

    pointS:
        a Dictionary that maps mapIDs->listOfPoints.  listOfPoints is a list of simple points that carry the mapID.
   
    holeD:
        A 2 level dictionary of mapIDs->cycleID->listOfSegments.  cycleID is just a temporary identifier.  listOfSegments is a list of line segments that form a cycle.  holeD pertains to the destination structural region in an interval region

    '''
    # map any line segments to holes in the dest that share the ID
    for label in lineS:
        lineDict = lineS[ label ]
        if label in holeD:
            destCycleDict = holeD[ label ]
            for lineID in lineDict:
                for destC in destCycleDict:
                    sr1LID = intervalReg.sourceSR.addLine( lineDict[lineID] )
                    sr2FID = intervalReg.destSR.addHole( destCycleDict[ destC ] )
                    intervalReg.mapComponent( sr1LID, sr2FID )
    # do the same thing with points
    for label in pointS:
        poiList = pointS[ label ]
        if label in holeD:
            destCycleDict = holeD[ label ]
            for p in poiLis:
                for destC in destCycleDict:
                    sr1PID = intervalReg.sourceSR.addPoint( p )
                    sr2FID = intervalReg.destSR.addHole( destCycleDict[ destC ] )
        


def assignLinesPointsToFaces( intervalReg, lineS, pointS, faceD ):
    '''
    given a component interval region that is set up with source and destination objects, 
    map the lines and points in a source structural region to faces in the destination region
    this is used with  set operations

    At the moment, we map a line/point to every face that shares its label.  This needs to be addressed in the future.

    **Input**:

    intervalReg
        An interval region with source and destination objects already created

    lineS:
        A 2 level dictionary of mapIDs->simpleLineID->listOfSegments.  simpleLineID is just a temporary identifier.  listOfSegments is a list of line segments that form a cycle.  lineS pertains to the source structural region in an interval region

    pointS:
        a Dictionary that maps mapIDs->listOfPoints.  listOfPoints is a list of simple points that carry the mapID.
   
        faceD:
            A 2 level dictionary of mapIDs->cycleID->listOfSegments.  cycleID is just a temporary identifier.  listOfSegments is a list of line segments that form a cycle.  faceD pertains to the destination structural region in an interval region

    '''
    # map any line segments to faces in the dest that share the ID
    for label in lineS:
        lineDict = lineS[ label ]
        if label in faceD:
            destCycleDict = faceD[ label ]
            for lineID in lineDict:
                for destC in destCycleDict:
                    sr1LID = intervalReg.sourceSR.addLine( lineDict[lineID] )
                    sr2FID = intervalReg.destSR.addFace( destCycleDict[ destC ] )
                    intervalReg.mapComponent( sr1LID, sr2FID )
    # do the same thing with points
    for label in pointS:
        poiList = pointS[ label ]
        if label in faceD:
            destCycleDict = faceD[ label ]
            for p in poiList:
                for destC in destCycleDict:
                    sr1PID = intervalReg.sourceSR.addPoint( p )
                    sr2FID = intervalReg.destSR.addFace( destCycleDict[ destC ] )
        



def assignHolesToHolesLinesPoints( intervalReg, holeS, holeD, lineD, pointD ):
    '''
    given a component interval region that is set up with source and destination objects, 
    map the holes in a source structural region  resulting from a hole list resulting from a 
    set operation to holes, points, lines,
    in the destination structural region of the interval region

    At the moment, we map a hole to every other structure that shares its label.  This needs to be addressed in the future.

    **Input**:

    intervalReg
        An interval region with source and destination objects already created

    holeS:
        A 2 level dictionary of mapIDs->cycleID->listOfSegments.  cycleID is just a temporary identifier.  listOfSegments is a list of line segments that form a cycle.  holeS pertains to the source structural region in an interval region

    holeD:
        Identical to holeS, but for the destination structural region in the interval regions

    lineD: 
        Identical to holeD, but the list of segments defines a connected simple line.

    pointD:
        a Dictionary that maps mapIDs->listOfPoints.  listOfPoints is a list of simple points that carry the mapID.
    '''
    # right now, we just map every instance of an identical label to every other instance of that label
    for label in holeS:
        cycleDict = holeS[ label ]
        # map this face to everything in Dest with same label
        if label in holeD:
            destCycleDict = holeD[ label ]
            # we now have a list of face cycles and a list of dest face cycles. 
            # map them all
            for sourceC in cycleDict:
                for destC in destCycleDict:
                    sr1HID = intervalReg.sourceSR.addHole( cycleDict[sourceC] )
                    sr2HID = intervalReg.destSR.addHole( destCycleDict[ destC ] )
                    intervalReg.mapComponent( sr1HID, sr2HID )
        # now do lines
        if label in lineD:
            destCycleDict = lineD[ label ]
            # we now have a list of face cycles and a list of dest face cycles. 
            # map them all
            for sourceC in cycleDict:
                for destC in destCycleDict:
                    sr1HID = intervalReg.sourceSR.addHole( cycleDict[sourceC] )
                    sr2LID = intervalReg.destSR.addLine( destCycleDict[ destC ] )
                    intervalReg.mapComponent( sr1HID, sr2LID )
        # now do points
        # point dict is different, it is not a 2 level dict
        if label in pointD:
            destPointList = pointD[ label ]
            # we now have a list of face cycles and a list of dest face cycles. 
            # map them all
            for sourceC in cycleDict:
                for destP in destPointList:
                    sr1HID = intervalReg.sourceSR.addHole( cycleDict[sourceC] )
                    sr2PID = intervalReg.destSR.addPoint( destP )
                    intervalReg.mapComponent( sr1HID, sr2PID )
        
def assignFacesToFacesLinesPoints( intervalReg, faceS, faceD, lineD, pointD ):
    '''
    given a component interval region that is set up with source and destination objects, 
    map the faces in a source structural region  resulting from a face list resulting from a 
    set operation to faces, points, lines,
    in the destination structural region of the interval region

    At the moment, we map a face to every other structure that shares its label.  This needs to be addressed in the future.

    **Input**:

    intervalReg
        An interval region with source and destination objects already created

    faceS:
        A 2 level dictionary of mapIDs->cycleID->listOfSegments.  cycleID is just a temporary identifier.  listOfSegments is a list of line segments that form a cycle.  faceS pertains to the source structural region in an interval region

    faceD:
        Identical to faceS, but for the destination structural region in the interval regions

    lineD: 
        Identical to faceD, but the list of segments defines a connected simple line.

    pointD:
        a Dictionary that maps mapIDs->listOfPoints.  listOfPoints is a list of simple points that carry the mapID.
    '''
    # right now, we just map every instance of an identical label to every other instance of that label
    for label in faceS:
        cycleDict = faceS[ label ]
        # map this face to everything in Dest with same label
        if label in faceD:
            destCycleDict = faceD[ label ]
            # we now have a list of face cycles and a list of dest face cycles. 
            # map them all
            for sourceC in cycleDict:
                for destC in destCycleDict:
                    sr1FID = intervalReg.sourceSR.addFace( cycleDict[sourceC] )
                    sr2FID = intervalReg.destSR.addFace( destCycleDict[ destC ] )
                    intervalReg.mapComponent( sr1FID, sr2FID )
        # now do lines
        if label in lineD:
            destCycleDict = lineD[ label ]
            # we now have a list of face cycles and a list of dest face cycles. 
            # map them all
            for sourceC in cycleDict:
                for destC in destCycleDict:
                    sr1FID = intervalReg.sourceSR.addFace( cycleDict[sourceC] )
                    sr2LID = intervalReg.destSR.addLine( destCycleDict[ destC ] )
                    intervalReg.mapComponent( sr1FID, sr2LID )
        # now do points
        # point dict is different, it is not a 2 level dict
        if label in pointD:
            destPointList = pointD[ label ]
            # we now have a list of face cycles and a list of dest face cycles. 
            # map them all
            for sourceC in cycleDict:
                for destP in destPointList:
                    sr1FID = intervalReg.sourceSR.addFace( cycleDict[sourceC] )
                    sr2PID = intervalReg.destSR.addPoint( destP )
                    intervalReg.mapComponent( sr1FID, sr2PID )
        

def relevantCyclesForIntersection( LA, sr1MapLabelF2HDict, LB, sr2MapLabelF2HDict ):
    '''
    
    This function is called by ``def intersection( cir1, cir2 )``. 

    Given a list of labels that lie above and a list of labels that lie below the same segment in a **map**,
    this function returns a set containing tuples of labels where each tuple indicates 
    
    * a pair of map labels that corresond to Face IDS from the input structural regions used to build the map that intersect
    * OR, a pair of map labels and a hole label that corresponds to a hole ID in the input structural region

    essentially, we are identifying overlapping faces, and holes that overlap overlapping faces

    **Input**: 

    LA
        the labels that lie above a segment from a map created with ``computeMapsAtTimeInstants()``

    sr1MapLabelF2HDict
        A copy of the structural region's F2H mapping, except map labels are used instead of IDs from the structural labels.  ``computeMapsAtTimeInstants()`` provides this as a return value.

    LB, sr2MapLabelF2HDict
        correspond to LA and sr1MapLabelF2HDict, except the labels lie below the segment, and the dicitonanary applies to the second input structural region to ``computeMapsAtTimeInstants()``
    
    **Returns**:

    A set of tuples where each tuple indicates a pair of face labels.  The labels correspond to the intersection of two faces from the input structural regions to ``computeMapsAtTimeInstants()``.  Map lables are used as opposed to structure IDs in the structural regions.

    A set of tuples where each tuple is a triple; a face label, a face label, and a hole label.  This corresponds to a hole intersecting the intersection of two faces from the input structural regions passed to ``computeMapsAtTimeInstants()``.  Map labels are used, as opposed to structure IDs in the structural regions.
    '''
    aboveFaceSet = set()
    aboveHoleSet = set() 
    belowFaceSet = set()
    belowHoleSet = set() 
    laSet = set( LA ) - set( [-1] )
    lbSet = set( LB ) - set( [-1] ) 
    laposFace = [ l for l in laSet if l > 0 and l % 2 == 0]
    laposHole = [ l for l in laSet if l > 0 and l % 2 == 1]
    lanegFace = [ l for l in laSet if l < -1 and l % 2 == 0]
    lanegHole = [ l for l in laSet if l < -1 and l % 2 == 1]
    lbposFace = [ l for l in lbSet if l > 0 and l % 2 == 0]
    lbposHole = [ l for l in lbSet if l > 0 and l % 2 == 1]
    lbnegFace = [ l for l in lbSet if l < -1 and l % 2 == 0]
    lbnegHole = [ l for l in lbSet if l < -1 and l % 2 == 1]
    
    # For intersection, we want faces that have a pair of pos/neg face IDS
    # we want holes that have a pos/neg pair of face IDs and a holeID for one of the faces
    print laSet, lbSet,laposFace, lanegFace
    for PL in laposFace:
        for NL in lanegFace:
            aboveFaceSet |= set( [(PL,NL)] )
    
    # repeat for the below labels
    for PL in lbposFace:
        for NL in lbnegFace:
            belowFaceSet |= set( [(PL,NL)] )
    # remove any labels that do not close on this seg
    boundaryLabelsAbove = aboveFaceSet - belowFaceSet
    boundaryLabelsBelow = belowFaceSet - aboveFaceSet
    aboveFaceSet = boundaryLabelsAbove
    belowFaceSet = boundaryLabelsBelow
    # now, add the relevant hole sets
    for item in aboveFaceSet:
        # item 0 is positive
        if item[0] in sr1MapLabelF2HDict:
            for holeLabel in sr1MapLabelF2HDict[ item[0] ]: 
                if holeLabel in laposHole:
                    aboveHoleSet |= set( [(item[0], item[1], holeLabel)] )
        if item[1] in sr2MapLabelF2HDict:
            for holeLabel in sr2MapLabelF2HDict[ item[1] ]: 
                if holeLabel in lanegHole:
                    aboveHoleSet |= set( [(item[0], item[1], holeLabel)] )
    # now, add the relevant hole sets
    for item in belowFaceSet:
        # item 0 is positive (
        if item[0] in sr1MapLabelF2HDict:
            for holeLabel in sr1MapLabelF2HDict[ item[0] ]: 
                if holeLabel in lbposHole:
                    aboveHoleSet |= set( [(item[0], item[1], holeLabel)] )
        if item[1] in sr2MapLabelF2HDict:
            for holeLabel in sr2MapLabelF2HDict[ item[1] ]: 
                if holeLabel in lbnegHole:
                    aboveHoleSet |= set( [(item[0], item[1], holeLabel)] )

    #remove any hole labels that do not close on this seg
    boundaryLabelsAbove = aboveHoleSet - belowHoleSet
    boundaryLabelsBelow = belowHoleSet - aboveHoleSet
    aboveHoleSet = boundaryLabelsAbove
    belowHoleSet = boundaryLabelsBelow
    finalFaceSet = aboveFaceSet | belowFaceSet
    finalHoleSet = aboveHoleSet | belowHoleSet
    print 'finalFace set, final hole set', finalFaceSet, finalHoleSet
    #finally , this seg may be the meeting line between two faces.  get all combinations of above/below boudnary labels
    finalLineSet = set()
    for l1 in boundaryLabelsAbove:
        for l2 in boundaryLabelsBelow:
            finalLineSet |= set( [(l1, l2)] )
    
    return finalFaceSet, finalHoleSet, finalLineSet


if __name__ == '__main__':
    '''
    Create  two interval regions.  Compute their intersection
    '''

    # create 4 structural regions 
    sr1 = structureRegion.structuralRegion()
    sr1f1 = [((2,1),(4,1)),((4,1),(3,4)),((3,4),(2,1))]
    sr1h1 = [((4,2),(5,2)),((5,2),(5,3)),((5,3),(4,2))]
    sr1f1ID = sr1.addFace( sr1f1 )
    #sr1h1 = sr1.addHole( sr1h1, [sr1f1ID] )
    sr2 = structureRegion.structuralRegion()
    sr2f1 = [((2,1),(4,1)),((4,1),(3,4)),((3,4),(2,1))]
    sr2h1 = [((1,2),(2,2)),((2,2),(2,3)),((2,3),(1,2))]
    sr2f1ID = sr2.addFace( sr2f1 )
    #sr2h1 = sr2.addHole( sr2h1, [sr2f1ID] )
    sr3 = structureRegion.structuralRegion()
    sr3f1 = [((1,1),(2,1)),((2,1),(1,2)),((1,2),(1,1))]
    sr3f1ID =sr3.addFace( sr3f1 )
    sr4 = structureRegion.structuralRegion()
    sr4f1 = [((3,3),(4,3)),((4,3),(4,4)),((4,4),(3,3))]
    sr4f1ID =sr4.addFace( sr4f1 )

    t1 = 10
    t2 = 20

    # use the structural regions to create component interval regions
    interReg1 = cIntervalRegion()
    interReg1.sourceSR = sr1
    interReg1.destSR = sr2
    interReg1.sourceTime = t1
    interReg1.destTime = t2
    interReg1.mapComponent( sr1f1ID, sr2f1ID ) 
    #interReg1.mapComponent( sr1h1, sr2h1)
    print interReg1, '---'
    interReg2 = cIntervalRegion()
    interReg2.sourceSR = sr3
    interReg2.destSR = sr4
    interReg2.sourceTime = t1
    interReg2.destTime = t2
    interReg2.mapComponent( sr3f1ID, sr4f1ID ) 
    print interReg2 
    print 'Intersection:'
    result = intersection( interReg1, interReg2 )
    of = open( os.pathsep+'tmp' + os.pathsep +'of.txt', 'w')
    for c in result:
        print c
        print '++++++++++++++'
        c.printToFileFor3DVis(of)
    of.close()
    if1 = open( os.pathsep+'tmp' +os.pathsep + 'if1.txt','w')
    interReg1.printToFileFor3DVis( if1 )
    if1.close()
    if1 = open( os.pathsep + 'tmp' + os.pathsep + 'if2.txt','w')
    interReg2.printToFileFor3DVis( if1 )
    if1.close()
#    sr1h1 = [((),()),((),()),((),())]
#    sr1h1 = [((),()),((),()),((),())]
#    sr1h1 = [((),()),((),()),((),())]
#    sr1h1 = [((),()),((),()),((),())]
#    sr1h1 = [((),()),((),()),((),())]
#    sr1h1 = [((),()),((),()),((),())]
#    sr1h1 = [((),()),((),()),((),())]
#    sr1h1 = [((),()),((),()),((),())]
#    sr1h1 = [((),()),((),()),((),())]

