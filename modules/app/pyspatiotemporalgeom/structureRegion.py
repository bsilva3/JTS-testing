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


import pyspatiotemporalgeom.utilities.segLibrary as segLibrary
import pyspatiotemporalgeom.utilities.hsegLibrary as hsegLibrary
from pyspatiotemporalgeom.utilities import mapLibrary

''' A structural region is a region representation in which a region is defined as a collection of **simple regions**, **simple lines** and **simple points**.

Simple Region:
    A region defined by a minimal cycle.

Simple Line:
    A line without branches or loops

Simple Point:
    A single point (x,y)

A structural region cotnains 4 sets:

#. A set **F** of minimal cycles representing *faces*
#. A set **H** of minimal cycles representing *holes*
#. A set **L** of simple lines
#. A set **P** of simple points
#. A dictionary that maps a face a set containing the holes that affect that face.

When used as a basis for Component Moving Regions, the lines and points have importance, otherwise they can be ignored.

A structural region represents the components that define a complex region.  The complex region defined by a structural region is computed as follows:

#. For each face, compute the difference of the face and the union of holes that the face maps to in the dictionary.
#. Compute the union of the resulting regions form step 1


.. warning::

    A structural region contains an integer that is used to provide a unique ID to each component added to it.
    If parallelization is added, the management of this integer will need to be in a critical section or incremented
    through an atomic operation, or race
    conditions will occur.

'''

import pyspatiotemporalgeom.utilities.hsegLibrary as hsegLibrary

class structuralRegion:

    def __init__( self, RHS = None ):
        '''
        constructor.  Simply create the lists and dictionary
        
        Acts as a copy constructor if **RHS** is another sturctural region.
        Performs a deep copy
        '''
        if RHS == None:
            self.F = dict()
            self.H = dict()
            self.L = dict()
            self.P = dict()
            self.F2H = dict()
            self.nextOpenID = 1
        else: 
            self.F = dict( RHS.F )
            self.H = dict( RHS.H )
            self.L = dict( RHS.L )
            self.P = dict( RHS.P )
            self.F2H = dict( RHS.F2H)
            self.nextOpenID = RHS.nextOpenID

    def findUnusedID( self ):
        '''
        Increment the integer used to keep track of the next open strucutreID.

        This function will ensure that the next open ID is indeed open, and is not in use alredy.

        If you increment ``self.nextOpenID`` without this function, make sure you re-use an ID. For example, use ``self.hasComponent()`` to check if it is in use.
        
        **Returns**:

        an integer ID that is available for use.
        '''

        while self.hasComponent( self.nextOpenID): 
            self.nextOpenID += 1

        return self.nextOpenID

    
    def hasComponent( self, componentIDs ):
        '''
        check that a component ID is actually existing
        in the structural region
        
        **Input**: 

        componentIDs:
            a single integer or a list of integers.  Each integer is a componentID that will be checked for existence

        **Returns**:

        True:
            if all componentIDs are in the strutural region

        False:
            otherwise
        '''

        # convert the componentID to an iterable if it is only 1 ID
        if isinstance( componentIDs, int ):
            componentIDs = [ componentIDs ]
        
        for x in componentIDs:
            if not ( x in self.F or x in self.H or x in self.L or x in self.P ) :
                return False
        return True

    def getIDsForHolesInFace( self, theFaceID ):
        '''
        get a list of IDS of holes that are in a face

        **Input**: 

        theFaceID:
            The ID of the face that contains the desired holes

        **Returns**:
            
        A list of IDS (integers):
            The IDs of all holes in the specified face

        ``None``:
            if the ID is not a face ID.
        '''

        theType = self.getComponentType( theFaceID )
        if theType == None or theType != 'F':
            return None
        return self.F2H[ theFaceID ]

    def getComponentType( self, theID ):
        '''
        given a component ID, tell if it is a face, hole, line or point

        **Input**:

        theID
            the ID of the component who's type you want to know.

        **Returns**:
        
        Type identifer:
            A string consisiting of:

            * 'F' for face
            * 'H' for hole
            * 'L' for line
            * 'P' for point

        None:
            If the ID is not in use in the object
        '''
        if not self.hasComponent( theID ):
            return None

        if theID in self.F:
            return 'F'
        if theID in self.H:
            return 'H'
        if theID in self.L:
            return 'L'
        if theID in self.P:
            return 'P'
    
    def getComponentByID( self, theID ):
        '''
        Return a component with the given ID

        **Input**:

        theID
            the ID of the component you wish to get.

        **Returns**:
        
        A tuple containing an identifier indicating the type of component, and the component itself:

        Type identifer:
            A string consisiting of:

            * 'F' for face
            * 'H' for hole
            * 'L' for line
            * 'P' for point

        A list of segments, or a point:
            If the ID refers to a valid component, that component is returned.  IT will be a list of segments, or a single point

        None:
            If the ID is not in use in the object
        '''

        if not self.hasComponent( theID ):
            return None

        if theID in self.F:
            return ('F', self.F[theID] )
        if theID in self.H:
            return ('H', self.H[theID] )
        if theID in self.L:
            return ('L', self.L[theID] )
        if theID in self.P:
            return ('P', self.P[theID] )
        
    def getAllComponentIDs( self ):
        '''
        returns a list containig the IDs of all components currently in the object
        '''
        return self.F.keys() + self.H.keys() + self.L.keys() + self.P.keys()
        
        

    def addFace( self, theFace, manualIDOverride = None ):
        '''
        verify the face is a simple cycle.  If so, add it.
        returns the ID of the face
        
        **Input:**

        theFace:
            A list of segments forming a minimal cycle
        
        manualIDOverride:
            If you want to manually assign an ID to a structure, pass an integer in for this value.  
            
            .. warning::
    
                if you specify an ID that is in use, the function will return a -1
       
        **Returns:**
        
        * The index of the face once it is added to the 
        **F** list on success,
        
        * -1 if the face is not a minimal cycle

        * -1 if the manualIDOverride is specified and the ID is already in use
        '''
        if manualIDOverride != None and self.hasComponent( manualIDOverride ):
            return -1
        
        hsegs = hsegLibrary.labelUniqueCycles( theFace )

        # make sure theFace only contained 1 cycle.  If so, hsegs will
        # only have 2 labels: 1 interior label and a -1 for the exterior
        labelSet = set()

        # make a set of all the labels
        for h in hsegs:
            labelSet |= set( [ h[1], h[2] ] )

        # check for 2 labels
        if len( labelSet ) != 2:
            return( -1 )

        # the cycle is good, collect the segs
        theSegs = [ (h[0][0],h[0][1]) for h in hsegs if h[0][0] < h[0][1] ]

        # get the id for this object, and put it in its list
        if manualIDOverride != None:
            ID = manualIDOverride
        else:
            ID = self.findUnusedID()
        
        # put it in the faces dict
        self.F[ ID ] =  theSegs
        return( ID )


    def addHole(self, theHole, indexesOfFacesToWhichItBelongs, manualIDOverride = None ):
        '''
        verify the hole is a simple cycle.  If so add it.


        **Input:**

        theHole:
            A list of segments forming a minimal cycle
        
        indexesOfFacesToWhichItBelongs :
            A **list** of face indexes to which the hole should be associated.
       
       manualIDOverride:
            If you want to manually assign an ID to a structure, pass an integer in for this value.

            .. warning::

                if you specify an ID that is in use, the function will return a -1

        **Returns:**
        
        * The ID of the hole
        
        * -1 if the hole is not a minimal cycle or the hole is not assigned to a valid face

        * -1 if the manualIDOverride is specified and the ID is already in use 
        '''
        if manualIDOverride != None and self.hasComponent( manualIDOverride ):
            return -1
        if isinstance( indexesOfFacesToWhichItBelongs, int ):
            indexesOfFacesToWhichItBelongs = list( indexesOfFacesToWhichItBelongs )
        
        # first make sure this hole will actually refer to a face in the F list
        faceIDList = [ i for i in indexesOfFacesToWhichItBelongs if i in self.F ]
        faceIDList = list( set( faceIDList) )

        if len( faceIDList ) == 0:
            return -1

        hsegs = hsegLibrary.labelUniqueCycles( theHole )

        # make sure theFace only contained 1 cycle.  If so, hsegs will
        # only have 2 labels: 1 interior label and a -1 for the exterior
        labelSet = set()

        # make a set of all the labels
        for h in hsegs:
            labelSet |= set( [ h[1], h[2] ] )

        # check for 2 labels
        if len( labelSet ) != 2:
            return( -1 )

        # the cycle is good, collect the segs
        theSegs = [ (h[0][0],h[0][1]) for h in hsegs if h[0][0] < h[0][1] ]
        
        # get the id for this object, and put it in its list
        if manualIDOverride != None:
            ID = manualIDOverride
        else:
            ID = self.findUnusedID()

        # append the face to the faces list
        self.H[ID] = theSegs 

        #update the mapping
        for i in faceIDList:
            if i not in self.F2H:
                self.F2H[i] = []
            self.F2H[i].append( ID )
        return( ID )

    def addPoint( self, thePoint ):
        '''
        Add a point to the structural region.

        **Input**:

        thePoint:
            A tuple: `(x,y)`

        **Returns**:
            
        the integer ID of the point:
            if `thePoint` is a tuple that contains 2 items

        -1:
            otherwise
        '''
        # make sure its a point
        if not isinstance( thePoint, tuple ) or not len( thePoint) == 2:
            return -1

        for item in thePoint:
            if not( isinstance(item, int) or isinstance(item, float) ):
                return -1
        
        # get the id for this object, and put it in its list
        ID = self.findUnusedID()
        
        self.P[ID] = thePoint
        return ID
    

    def addLine( self, theLine ):
        '''
        Veify the line is simple (all end points up twice, except for 2), and add it if so
       
        **Input**:

        theLine:
            a list of line segments.  `[((x1,y1),(x2,y2)),...,((xn,yn),(xm,ym))]`

        **Returns**:
        
            The integer ID of the simple line: 
                on success. line is indeed a simple line.
            
            -1:
                if the line is not simple. Note, the function does not currently test for self-intersecting line segments.
        '''
            
        #approach:  the labelCycles function will remove any segs that are not involved in a cycle.  so, call that, and make sure 
        # no segs got removed!

        # make the segs left
        # remove dups
        # make a copy
        print theLine
        theLine = [s if s[0] < s[1] else (s[1], s[0]) for s in theLine]
        theLine = list( set( theLine ) )
        
        print theLine

        # check that exactly 2 end points are used once
        seenOncePointSet = set()
        for s in theLine:
            if s[0] not in seenOncePointSet:
                seenOncePointSet |= set( [ s[0] ] )
            else:
                seenOncePointSet -= set( [ s[0] ] ) 
            if s[1] not in seenOncePointSet:
                seenOncePointSet |= set( [ s[1] ] )
            else:
                seenOncePointSet -= set( [ s[1] ] ) 
        # at the end, there should be exactly 2 points in the seenOncePointSet
        if len(seenOncePointSet) != 2:
            return -1 
        print( seenOncePointSet )
        print theLine
        # check the line contains no cycles
        hsegs = hsegLibrary.labelUniqueCycles( theLine )
        print hsegs
        if  len(hsegs) > 0:
            return -1 

        # if we get here, its a simple line
        theLine.sort()


        # get the id for this object, and put it in its list
        ID = self.findUnusedID()
        
        self.L[ID] = theLine
        return ID

    def extractFace( self, faceID ):
        '''
        Compute the face imposed by a face cycle and its
        associated hole cycles (associated through the mapping).

        **Input**:

            faceIndex:
                The index (in the self.F list) of the face to extract.

        **Output**:
            A list of labeled segments.  The exterior of the face is identified
            by a label of `-1`.  The interior is identified by `faceIndex+2`

        '''
        extractedFace = []
        currHoleID = faceID + 1 
        f = self.F[ faceID ]
        #get the labeled segs for the face
        hsegs = hsegLibrary.labelUniqueCycles( f, True )
        allsegs = [ h for h in hsegs if h[0][0] < h[0][1]]
        allsegs = [ (h[0],-1, faceID) if h[1] < 0 else (h[0],faceID,-1) for h in allsegs]
        # now get the labeled segs for all the holes
        for j in self.F2H[faceID]:
            hsegs = hsegLibrary.labelUniqueCycles( self.H[j] )
            lsegs = [ h for h in hsegs if h[0][0] < h[0][1]]
            lsegs = [ (h[0],-1, currHoleID) if h[1] < 0 else (h[0],currHoleID,-1) for h in lsegs]
            allsegs.extend( lsegs )
            currHoleID += 1
        # Now we have all the appropriately labeled segments.  break them
        # and compute the map
        allC, allLa, allLb = zip(*allsegs )
        segs, la, lb = mapLibrary.breakSegsAndPreserveSegLabels( allC, allLa, allLb)
        rsegs, rla, rlb, index2labelDict = mapLibrary.createMapFromCycles( segs, la, lb )

        # keep segs that have a single label of 2 on one side
        for j in xrange( len( rsegs ) ):
            if index2labelDict[ rla[j] ] == set( [faceID] ):
                extractedFace.append( (rsegs[j], faceID, -1) )
            elif index2labelDict[ rlb[j] ] == set( [faceID] ): 
                extractedFace.append( (rsegs[j], -1, faceID) )
        return extractedFace

    def extractRegion(self):
        '''
        Returns the region imposed by the structural region.

        computed as the following:

        #. Compute to difference of each face with its mapped holes. (See extractFace())
        #. Compute the union for all geometries returned from the above line.

        **Input:**

        none

        **Returns:**

        a region represented as a  list of segments
        '''
        # we will use map construction to deal with this problem.
        # label all the cycles we need, then make a map out of it.
        #finally, only keep the segs we want
        extractedFaces = []
        for i in self.F:
            theExtractedFace = self.extractFace( i ) 
            extractedFaces.extend(  theExtractedFace )
        # at this point, all the faces are extracted.  Now we must union them
        # again, create a map.  then just keep segs that border the exterior
        allC, allLa, allLb = zip(*extractedFaces )
        segs, la, lb = mapLibrary.breakSegsAndPreserveSegLabels( allC, allLa, allLb)
        rsegs, rla, rlb, index2labelDict = mapLibrary.createMapFromCycles( segs, la, lb )
        # keep segs that border an exterior
        finalSegs = []
        for i in xrange( len( rsegs ) ):
            if index2labelDict[ rla[i] ] == set( [-1] ) or index2labelDict[ rlb[i] ] == set( [-1] ) :
                finalSegs.append( rsegs[i] )
        
        finalSegs.sort()
        return finalSegs

    def __str__(self):
        theString = 'F: '
        for f in self.F:
            theString += str( f ) + ': ' + str( self.F[f] ) +'\n'
        theString += 'H: '
        for h in self.H:
            theString += str( h ) + ': ' + str( self.H[h] ) +'\n' 
        theString += 'L: '
        for l in self.L:
            theString += str( l ) + ': ' + str( self.L[l] ) +'\n'  
        theString += 'P: '
        for p in self.P:
            theString += str( p ) + ': ' + str( self.P[p] ) +'\n'  
        theString += 'Map: '
        for i in self.F2H:
            theString += str(i) + '-> ['
            for j in self.F2H[i]:
                theString += str(j) + ' '
            theString += ']\n'
        return( theString )
    
    def printToFileFor3DVis( self, openFileObject, zval ):
        '''
        print the component interval region to a file formatted for visualtization.
        
        data is printed one segment on each line.  Each segment is printed with 3D coordinates.
        
        **Input**:
        
        openFileObject:
            a file object that has been opened for writing.
        
        zval:
            the value to use for the z coordinate, for 3D printing
        '''
        for f in self.F:
            for x in self.F[f]:
                openFileObject.write( str(x[0][0]) + ' '  + str(x[0][1]) + ' '   + str(zval) + ' '   + str(x[1][0]) + ' '   + str(x[1][1]) + ' '  + str(zval) +'\n' )
        for h in self.H:
            for x in self.H[h]:
                openFileObject.write( str(x[0][0]) + ' '  + str(x[0][1]) + ' '   + str(zval) + ' '   + str(x[1][0]) + ' '   + str(x[1][1]) + ' '  + str(zval) +'\n' )
        for l in self.L:
            for x in self.L[l]:
                openFileObject.write( str(x[0][0]) + ' '  + str(x[0][1]) + ' '   + str(zval) + ' '   + str(x[1][0]) + ' '   + str(x[1][1]) + ' '  + str(zval) +'\n' )
        for p in self.P:
            x = self.P[p]
            openFileObject.write( str(x[0])+ ' ' +str(x[1]) + ' '  + str(zval) + ' '  + str(x[0]+0.0001) + ' '  + str(x[1]+0.0001) + ' '   + str(zval) +'\n' )
    
if __name__ == '__main__':
    sr = structuralRegion()
    f1 = [((1,1),(3,1)),((3,1),(2,3)),((2,3),(1,1))]
    h1 = [((1,2),(4,2)),((4,2),(3,3)),((3,3),(1,2))]
    f2 = [((2,1),(4,3)),((2,1),(2,2)),((2,2),(4,3))]
    h2 = [((2.2,1.5),(4,1)),((2.2,1.5),(4,1.5)),((4,1),(4,1.5))]
    f1index = sr.addFace( f1 )
    f2index = sr.addFace( f2 )
    h1index = sr.addHole( h1,[f1index] )
    h2index = sr.addHole( h2,[f2index] )

    l1 = [((1,1),(3,1)),((3,1),(2,3)),((2,3),(1,1))]
    l2 = [((6,6),(7,7)),((7,7),(8,6))]
    sr.addLine( l1 )
    sr.addLine( l2 )
    
    p1 = 'adsf'
    p2 = (2,4.0)
    sr.addPoint( p1 )
    sr.addPoint( p2 )
    print sr
    print sr.extractRegion( )



