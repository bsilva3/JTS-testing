import collections
import structureRegion

import componentMovingRegion
import pyspatiotemporalgeom.region as region
import os
from utilities import regionInterpolator
from utilities import hsegLibrary
from utilities import triangleLibrary
from utilities import mapLibrary
import pyspatiotemporalgeom.componentMovingRegion as intervalRegion
from pyspatiotemporalgeom.componentMovingRegion import cIntervalRegion
import sys
import re
#import imp
#structureRegion = imp.load_source('structureRegion', "pyspatiotemporalgeom\\structureRegion.py")
#intervalRegion = imp.load_source('intervalRegion', "pyspatiotemporalgeom\\componentMovingRegion.py")

#def t():
#    print(sys.path)

"""
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
interReg1 = intervalRegion.cIntervalRegion()
interReg1.sourceSR = sr1
interReg1.destSR = sr2
interReg1.sourceTime = t1
interReg1.destTime = t2
interReg1.mapComponent( sr1f1ID, sr2f1ID ) 
#interReg1.mapComponent( sr1h1, sr2h1)
print interReg1, '---'
interReg2 = intervalRegion.cIntervalRegion()
interReg2.sourceSR = sr3
interReg2.destSR = sr4
interReg2.sourceTime = t1
interReg2.destTime = t2
interReg2.mapComponent( sr3f1ID, sr4f1ID )

print(interReg1.getStructuralRegionAtTime(11))
"""

def wktToSegmentList(wkt):
   #parses a WKT string and returns a list of tuples with floats with line segments representing a geometry
    geom = []
    geometry_type = wkt.split(" (")[0]
    if geometry_type == "POLYGON":
        #get all the coordinates inside. Does not take into account holes!
        coords_wkt = wkt.split("((")[1].split("))")[0].split(", ")
        for coord in coords_wkt:
            coord = coord.split(" ")
            geom.append((float(coord[0]), float(coord[1]) ))

        segmentList = []
        for i in range(0, len(geom)):
            if (i == len(geom)-1):
                segmentList.append((geom[i], geom[0]))#close the geometry
            else:
                segmentList.append( (geom[i], geom[i+1]))
        return segmentList

if len(sys.argv) != 6: #counting the name of the file as an argument
    print "Usage: python mckerney.py <wkt source geom> <wkt target geom> <begin time> <end time> <query time>"
    sys.exit(0)

#geom1 = wktToSegmentList(sys.argv[1])
#geom2 = wktToSegmentList(sys.argv[2])
sr1 = structureRegion.structuralRegion()
geom1 = [((2,1),(4,1)),((4,1),(3,4)),((3,4),(2,1))]
sr1f1ID = sr1.addFace( geom1 )
sr2 = structureRegion.structuralRegion()
geom2 = [((4,2),(5,2)),((5,2),(5,3)),((5,3),(4,2))]
sr2f1ID = sr2.addFace( geom2 )

interReg1 = intervalRegion.cIntervalRegion()
interReg1.sourceSR = sr1
interReg1.destSR = sr2
interReg1.sourceTime = int(sys.argv[3])
interReg1.destTime = int(sys.argv[4])
interReg1.mapComponent( sr1f1ID, sr2f1ID )
queryTime = int(sys.argv[5])
print(interReg1.getStructuralRegionAtTime(1500))