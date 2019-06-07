from __future__ import print_function
import collections
#import structureRegion
import pyspatiotemporalgeom.structureRegion as structureRegion

#import componentMovingRegion
import pyspatiotemporalgeom.region as region
import os
#from utilities import regionInterpolator
from pyspatiotemporalgeom.utilities import regionInterpolator
from pyspatiotemporalgeom.utilities import hsegLibrary
from pyspatiotemporalgeom.utilities import triangleLibrary
from pyspatiotemporalgeom.utilities import mapLibrary
#from utilities import hsegLibrary
#from utilities import triangleLibrary
#from utilities import mapLibrary
import pyspatiotemporalgeom.componentMovingRegion as intervalRegion
from pyspatiotemporalgeom.componentMovingRegion import cIntervalRegion
import pyspatiotemporalgeom.intervalRegion as iintervalRegion
import sys
import re

import random

"""
    Parses a wkt string and returns a list of tuples with floats with line segments representing a geometry.
	
	Notes:
	Currently the function does not handle holes!
	Currently the function handles only POLYGON type geometries!
	
	Input: A wkt string.
	Output: A segment list.

"""
def wkt_to_segment_list(wkt):

    geom = []
    geometry_type = wkt.split(" (")[0]
    
    if geometry_type == "POLYGON":

        # 1. Parse the wkt string.

        coords_wkt = wkt.split("((")[1].split("))")[0].split(", ")

        for i in range(0, len(coords_wkt) - 1):
            coords_wkt[i] = coords_wkt[i].split(" ")
            # JD: Why add x to the wkt coordinates?
            geom.append((float(coords_wkt[i][0]), float(coords_wkt[i][1])))

        segmentList = []

        # 2. Remove duplicate points. Remove this?
        #geom = list(set(geom))

        # 3. Compute the segment list.

        for i in range(0, len(geom)):
            # Close the segment list.
            if (i == len(geom) - 1):
                segmentList.append((geom[i], geom[0]))
            else:
                segmentList.append((geom[i], geom[i+1]))

        return segmentList
    else:
        # Return None?
        return []

"""
# hseg is a 3 tuple, a tuple with 2 points, an above label, a below label
# ((dominatingPoint, submissivePoint), labelAbove, labelBelow)
# ( ((x1,y1),(x2,y2)) ,0,0)

A halfsegment has the following strucutre:

(((x1,y1),(x2,y2)),la,lb)
"""

"""
    To test the creation of a Component Interval Region with holes.
	Gives an error. This is also the case when using the original source code.
"""
def create_CIR_with_holes():
    sr1 = structureRegion.structuralRegion()
    sr1f1 = [((2,1),(4,1)),((4,1),(3,4)),((3,4),(2,1))]
    sr1h1 = [((4,2),(5,2)),((5,2),(5,3)),((5,3),(4,2))]

    sr1f1ID = sr1.addFace( sr1f1 )
    sr1h1ID = sr1.addHole( sr1h1, [sr1f1ID] )

    sr2 = structureRegion.structuralRegion()
    sr2f1 = [((2,1),(4,1)),((4,1),(3,4)),((3,4),(2,1))]
    sr2h1 = [((1,2),(2,2)),((2,2),(2,3)),((2,3),(1,2))]

    sr2f1ID = sr2.addFace( sr2f1 )
    sr2h1ID = sr2.addHole( sr2h1, [sr2f1ID] )

    t1 = 1000
    t2 = 2000

    cir = cIntervalRegion()
    cir.sourceSR = sr1
    cir.destSR = sr2
    cir.sourceTime = t1
    cir.destTime = t2
    cir.mapComponent( sr1f1ID, sr2f1ID ) 
    cir.mapComponent( sr1h1ID, sr2h1ID)

    return cir

"""
    Creates a Component Interval Region.
	This describes the movement of a moving region over a single time interval.
	
	Input:
		source_SL: 		The source segment list.
		dest_SL: 		The destination segment list.
		source_time:	The initial instant of the time interval.
		dest_time:		The final instant of the time interval.
		
		source_time and dest_time must be integer timestamps.
	
	Output:
		A Component Interval Region or None.
"""
def create_CIR(source_SL, dest_SL, source_time, dest_time):
    src_sr = structureRegion.structuralRegion()
    src_sr_id = src_sr.addFace( source_SL )

    dst_sr = structureRegion.structuralRegion()
    dst_sr_id = dst_sr.addFace( dest_SL )

    cir = intervalRegion.cIntervalRegion()

    cir.sourceSR = src_sr
    cir.destSR = dst_sr
    cir.sourceTime = int(source_time)
    cir.destTime = int(dest_time)

    if cir.mapComponent( src_sr_id, dst_sr_id ):
        return cir

    return None

"""
    Returns the WKT of a list of points.
	
	Input: A list of points: [(x0, y0), ..., (xn, yn)]
	Output: The wkt as a polygon: POLYGON((x0 y0, ..., xn yn, x0 y0))
"""
def points_list_to_wkt(points):
    wkt = 'POLYGON(('
    if points != None:
        n = len(points) - 1
        j = 0
        for point in points:
            wkt += str(point[0]) + ' ' + str(point[1]) + ', '
            j = j + 1

        # Close the polygon.
        wkt += str(points[0][0]) + ' ' + str(points[0][1]) + '))'

        return wkt

    # Return None instead?
    return 'POLYGON EMPTY'

"""
    Output for Octave.
"""
def points_list_to_octave(points):
    #print(len(points))
    wkt = '['
    if points != None:
        n = len(points) - 1
        j = 0
        for point in points:
            wkt += str(point[0]) + ', ' + str(point[1]) + '; '
            j = j + 1

        # Close the polygon.
        wkt += str(points[0][0]) + ', ' + str(points[0][1]) + ';];'

        return wkt

    # Return None instead?
    return '[]'

"""
    Gets a region at the specified instant. 

	Input: A component interval region and an instant.
	Output: A list with the dictionaries containing the wkt of the faces and the holes of a moving region at the given instant.
"""
def at(cir, t):
    faces_wkt = dict()
    holes_wkt = dict()

    # Exctracts the structural region defined by this component interval region at time t.
    region = cir.getStructuralRegionAtTime(t)

    # Iterate through the faces.
    for face_id in region.F:
        face = region.F[face_id]

        # Labeled segs for this face.
        hsegs = hsegLibrary.labelUniqueCycles(face, True)

        # List of points, in cyclic order, that define the boundary of the outer cycle of this face.
        face_outer_cycle_points = hsegLibrary.getOuterWalkPointSequence(hsegs);

        wkt = points_list_to_wkt(face_outer_cycle_points)
        #print(wkt)
        faces_wkt[face_id] = wkt

        # Regions has holes?
        if region.F2H != None:
            if face_id in region.F2H:
                for j in region.F2H[face_id]:
                    hsegs = hsegLibrary.labelUniqueCycles(region.H[j])
                    hole_outer_cycle_points = hsegLibrary.getOuterWalkPointSequence(hsegs);

                    wkt = points_list_to_wkt(hole_outer_cycle_points)
                    #print(wkt)
                    holes_wkt[face_id] = wkt

    return [faces_wkt, holes_wkt]

"""
    Gets a region at the specified instant. 

	Input: A moving region and an instant.
	Output: A list with the dictionaries containing a representation of the faces and the holes of a moving region at the given instant for display in octave.
"""
def at_for_octave(cir, t):
    faces_wkt = dict()
    holes_wkt = dict()

    region = cir.getStructuralRegionAtTime(t)

    # Iterate through the faces.
    for face_id in region.F:
        face = region.F[face_id]

        # Labeled segs for this face.
        hsegs = hsegLibrary.labelUniqueCycles(face, True)

        # List of points, in cyclic order, that define the boundary of the outer cycle of this face.
        face_outer_cycle_points = hsegLibrary.getOuterWalkPointSequence(hsegs);

        wkt = points_list_to_octave(face_outer_cycle_points)
        #print(wkt)
        faces_wkt[face_id] = wkt

        # Regions has holes?
        if region.F2H != None:
            if face_id in region.F2H:
                for j in region.F2H[face_id]:
                    hsegs = hsegLibrary.labelUniqueCycles(region.H[j])
                    hole_outer_cycle_points = hsegLibrary.getOuterWalkPointSequence(hsegs);

                    wkt = points_list_to_octave(hole_outer_cycle_points)
                    #print(wkt)
                    holes_wkt[face_id] = wkt

    return [faces_wkt, holes_wkt]

# Inputs.

geom1 = wkt_to_segment_list("POLYGON ((1052 987, 1090 1037, 1100 1064, 1096 1095, 1101 1116, 1126 1136, 1143 1182, 1140 1218, 1154 1260, 1159 1310, 1142 1333, 1115 1333, 1086 1291, 1083 1268, 1067 1252, 1052 1247.5, 1037 1243, 1007 1186, 948 1077, 935 1049, 886 925, 848 801, 905 771, 936 803, 977 832, 998 858, 1034 941, 1052 987))")
geom2 = wkt_to_segment_list("POLYGON ((1055 999, 1073 1015, 1104 1074, 1101 1106, 1106 1127, 1133 1149, 1152 1195, 1144 1218, 1162 1270, 1168 1323, 1133 1347, 1121 1343, 1096 1301, 1094 1282, 1078 1264, 1069 1266, 1030 1234, 996 1148, 966 1106, 922 1030, 875 919, 848 817, 903 787, 924 796, 937 820, 979 848, 1001 875, 1055 999))")
geom1 = wkt_to_segment_list(sys.argv[1])
geom2 = wkt_to_segment_list(sys.argv[2])

#geom1 = [((2,1),(4,1)),((4,1),(3,4)),((3,4),(2,1))]
#geom2 = [((4,2),(5,1)),((5,1),(5,3)),((5,3),(4,2))]

source_t = 1000
dest_t = 2000
source_t = int(sys.argv[3])
dest_t = int(sys.argv[4])
cir = create_CIR(geom1, geom2, source_t, dest_t)
#cir = create_CIR_with_holes()

"""
    Do work.
"""

#query_time_begin = 1500
#query_time_end = 2000
query_time_begin = int(sys.argv[5])
query_time_end = query_time_begin
if len(sys.argv) == 7:
    query_time_end = int(sys.argv[6])

print("end: "+str(query_time_end))
file = open("wkt.txt","w+")
#number_of_instants = 50
#number_of_instants = int(sys.argv[7])
counter = 0
t = query_time_begin
step = (query_time_end - query_time_begin) / 1000
while t <= query_time_end:
    #for t in range(query_time_begin, query_time_end + 1):
    # Get region at t.
    #faces_wkt, holes_wkt = at(cir, t)
    faces_wkt, holes_wkt = at_for_octave(cir, t)

    # Debug
    if faces_wkt != None:
        for face_wkt in faces_wkt:
            file.write('M' + str(counter) + ' = ' + faces_wkt[face_wkt])
            file.write('\n')
            counter = counter + 1
            #print(face_wkt)

    if holes_wkt != None:
        for hole_wkt in holes_wkt:
            file.write('M' + str(counter) + ' = ' + holes_wkt[hole_wkt])
            file.write('\n')
            counter = counter + 1
            #print(hole_wkt)

    t = t + step
    if step == 0:
        break #at instant

file.close()