from __future__ import print_function

import collections
import pyspatiotemporalgeom.structureRegion as structureRegion
import pyspatiotemporalgeom.region as region
import os

from pyspatiotemporalgeom.utilities import regionInterpolator
from pyspatiotemporalgeom.utilities import hsegLibrary
from pyspatiotemporalgeom.utilities import triangleLibrary
from pyspatiotemporalgeom.utilities import mapLibrary

import pyspatiotemporalgeom.componentMovingRegion as intervalRegion

from pyspatiotemporalgeom.componentMovingRegion import cIntervalRegion

import pyspatiotemporalgeom.intervalRegion as iintervalRegion
import sys
import re

from geomet import wkt
import json

import random

"""

	How to use this script in the command line:

	python mckenney_final.py 1000 2000 "POLYGON ((949 781, 926 812, 891.6666656434536 796.66666620969772, 857.3333312869072 781.33333241939545, 823 766, 804 736, 807 689, 810 642, 833.6666673719883 612.99999913573265, 857.33333474397659 583.9999982714653, 881 555, 892 572, 909 576, 914 583, 922 580, 928 597, 920 640, 946 640, 968 647.5, 990 655, 949 781))" "POLYGON ((972 774, 955 806, 922 817, 905 816, 850 782, 822 755, 812 697, 812 656, 835 582, 848 565, 863 562, 876 576, 893 576, 899 583, 909 579, 917 592, 916 637, 962 632, 968 638, 990 640, 972 774))" 1000 2000 100

	python "D:\work\jni\mckenney_final.py" 1000 2000 100 "POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10))" "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))" 1000 2000 >> d:\wkt_1.txt
	
	Tested in windows.
	
	This script uses code taken from the pyspatiotemporalgeom examples source code.
	
	Tentative :)
	Parsing functions: wkt -> pyspatiotemporalgeom -> wkt.
	
	Bruno Silva and Jose Duarte
	
"""

"""

    Parses a wkt string and returns a list of tuples with line segments representing a geometry.
	
	Notes:
	Currently the function does not handle holes!
	Currently the function handles only POLYGON type geometries!
	
	Input: A wkt string.
	Output: A segment list.
	
	WKT Examples:
	
	POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10), (20 30, 35 35, 30 20, 20 30))
	POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))
	
	MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))
	MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)), ((20 35, 10 30, 10 10, 30 5, 45 20, 20 35), (30 20, 20 15, 20 25, 30 20)))
	
"""

#script params if at instant:
## begin time, end time, source geo, target geo, query time
#script params if at period:
## begin time, end time, source geo, target geo, query time begin, query time end, num samples

def wkt_to_segment_list(_wkt):

    segment_list = []

    geom_json = wkt.loads(_wkt)
    #geom_json = wkt.loads('POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10), (20 30, 35 35, 30 20, 20 30))')
    #wkt.dumps(geom_json, decimals=6)
    #print(geom_json)

    geometry_type = geom_json['type']
    if geometry_type != "Polygon":
         print('Only Polygon is supported.')
         return []

    coordinates = geom_json['coordinates']
    #print(coordinates)

    for i in range(0, len(coordinates)):
        values = coordinates[i]
        #print(values)
        # Face.
        if i == 0:

            for j in range(0, len(values) - 1):
                # Close the segment list.
                if (j == len(values) - 2):
                    segment_list.append((tuple(values[j]), tuple(values[0])))
                else:
                    segment_list.append((tuple(values[j]), tuple(values[j+1])))

        # Holes.
        else:
            """
            for j in range(0, len(values) - 1):
                # Close the segment list.
                if (j == len(values) - 2):
                    segment_list.append((tuple(values[j]), tuple(values[0])))
                else:
                    segment_list.append((tuple(values[j]), tuple(values[j+1])))
            """
            
    #print(segment_list)
    return segment_list

def wkt_to_geometry_segment_lists(_wkt):

    # A list with faces.
    # A dictionary that uses the face_id as a key and an entry in the dict is a list of holes on a face with face_id x.

    faces_segment_list = []
    holes_segment_list = {}

    geom_json = wkt.loads(_wkt)
    geometry_type = geom_json['type']

    if geometry_type == "Polygon":

        coordinates = geom_json['coordinates']

        face_id = 0

        for i in range(0, len(coordinates)):
            values = coordinates[i]

            # Face.
            if i == 0:

                face_segment_list = []

                if len(coordinates) > 1:
                    holes_segment_list[face_id] = []

                for j in range(0, len(values) - 1):
                    # Close the segment list.
                    if (j == len(values) - 2):
                        face_segment_list.append((tuple(values[j]), tuple(values[0])))
                    else:
                        face_segment_list.append((tuple(values[j]), tuple(values[j+1])))

                faces_segment_list.append(face_segment_list)

            # Holes.
            else:
                hole_segment_list = []

                for j in range(0, len(values) - 1):
                    # Close the segment list.
                    if (j == len(values) - 2):
                        hole_segment_list.append((tuple(values[j]), tuple(values[0])))
                    else:
                        hole_segment_list.append((tuple(values[j]), tuple(values[j+1])))

                holes_segment_list[face_id].append(hole_segment_list)

        face_id = face_id + 1

    elif geometry_type == "MultiPolygon":

        polygons = geom_json['coordinates']
        face_id = 0

        for polygon in polygons:
            for i in range(0, len(polygon)):
                values = polygon[i]

                # Face.
                if i == 0:

                    face_segment_list = []

                    if len(polygon) > 1:
                        holes_segment_list[face_id] = []

                    for j in range(0, len(values) - 1):
                        # Close the segment list.
                        if (j == len(values) - 2):
                            face_segment_list.append((tuple(values[j]), tuple(values[0])))
                        else:
                            face_segment_list.append((tuple(values[j]), tuple(values[j+1])))

                    faces_segment_list.append(face_segment_list)

                # Holes.
                else:
                    hole_segment_list = []

                    for j in range(0, len(values) - 1):
                        # Close the segment list.
                        if (j == len(values) - 2):
                            hole_segment_list.append((tuple(values[j]), tuple(values[0])))
                        else:
                            hole_segment_list.append((tuple(values[j]), tuple(values[j+1])))

                    holes_segment_list[face_id].append(hole_segment_list)

            face_id = face_id + 1

    else:

        print('Only Polygon and MultiPolygon are supported.')
        return []        

    return faces_segment_list, holes_segment_list

"""

    To test the creation of a CIR with holes.
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
    src_sr_id = src_sr.addFace(source_SL)

    dst_sr = structureRegion.structuralRegion()
    dst_sr_id = dst_sr.addFace(dest_SL)

    cir = intervalRegion.cIntervalRegion()

    cir.sourceSR = src_sr
    cir.destSR = dst_sr
    cir.sourceTime = int(source_time)
    cir.destTime = int(dest_time)

    if cir.mapComponent( src_sr_id, dst_sr_id ):
        return cir

    return None

def create_complex_CIR(source_faces_SLs, source_holes_SLs, target_faces_SLs, target_holes_SLs, source_time, dest_time):

    s_f_component_ids = []
    s_h_component_ids = []

    t_f_component_ids = []
    t_h_component_ids = []

    # Source Structural Region.

    source_SR = structureRegion.structuralRegion()

    for i in range(0, len(source_faces_SLs)):
    #for face_SL in source_faces_SLs:
        face_id = source_SR.addFace(source_faces_SLs[i])
        s_f_component_ids.append(face_id)

        if i in source_holes_SLs:
            holes_SLs = source_holes_SLs[i]

            for hole_SL in holes_SLs:
                hole_id = source_SR.addHole(hole_SL, [face_id])
                s_h_component_ids.append(hole_id)

    # Target Structural Region.

    target_SR = structureRegion.structuralRegion()

    for i in range(0, len(target_faces_SLs)):
    #for face_SL in target_faces_SLs:
        face_id = target_SR.addFace(target_faces_SLs[i])
        t_f_component_ids.append(face_id)

        if i in target_holes_SLs:
            holes_SLs = target_holes_SLs[i]

            for hole_SL in holes_SLs:
                hole_id = target_SR.addHole(hole_SL, [face_id])
                t_h_component_ids.append(hole_id)

    cir = intervalRegion.cIntervalRegion()

    cir.sourceSR = source_SR
    cir.destSR = target_SR
    cir.sourceTime = int(source_time)
    cir.destTime = int(dest_time)

    # Component mapping.

    for i in range(0, len(s_f_component_ids)):
        if not cir.mapComponent(s_f_component_ids[i], t_f_component_ids[i]):
            return None

    for i in range(0, len(s_h_component_ids)):
        if not cir.mapComponent(s_h_component_ids[i], t_h_component_ids[i]):
            return None

    #if cir.mapComponent( src_sr_id, dst_sr_id ):
    #    return cir

    return cir

"""

	Returns a string representation of the given list of points in the form:
		(x1 y1, ..., xn yn, x1 y1)
	
	Input: A list of points: [(x0, y0), ..., (xn, yn)]
	Output: (x1 y1, ..., xn yn, x1 y1)
	
	Notes:
	Used as an intermediate step in the computation of a wkt of a geometry.
	
"""
def points_list_to_intermediate_wkt(points):
    if points != None:
        _wkt = '('

        for point in points:
            _wkt += str(point[0]) + ' ' + str(point[1]) + ', '

        # Close the cycle.
        _wkt += str(points[0][0]) + ' ' + str(points[0][1]) + ')'

        return _wkt

    return None

"""

    Gets a region at the specified instant t.

	Input: 	A component interval region and an instant.
	Output: The structural region defined at instant t.

"""
def at(cir, t):

    # Exctract the structural region defined by cir at time t.
    return cir.getStructuralRegionAtTime(t)

"""
    Gets the wkt of a given structural region.
"""
def structural_region_to_wkt(sregion):

    # Currently, only POLYGON is being considered.
    # In the future, MULTIPOLYGON will also be considered.
    geom_wkt = ''

    counter = 0

    # Iterate through the faces.
    for face_id in sregion.F:
        face = sregion.F[face_id]

        # Labeled segs for this face.
        hsegs = hsegLibrary.labelUniqueCycles(face, True)

        # List of points, in cyclic order, that define the boundary of the outer cycle of this face.
        face_outer_cycle_points = hsegLibrary.getOuterWalkPointSequence(hsegs)

        if counter > 0:
            geom_wkt += ', '

        # Add the intermediate wkt representation of the face with no holes.
        geom_wkt += '(' + points_list_to_intermediate_wkt(face_outer_cycle_points)

        counter = counter + 1

        #print(sregion.F2H)

        # Face has holes?
        if sregion.F2H != None:
            if face_id in sregion.F2H:
                #print("Has holes.")
                for j in sregion.F2H[face_id]:
                    hsegs = hsegLibrary.labelUniqueCycles(sregion.H[j])

                    hole_outer_cycle_points = hsegLibrary.getOuterWalkPointSequence(hsegs);

                    # Add the intermediate wkt representation of the face's hole(s).
                    geom_wkt += ', ' + points_list_to_intermediate_wkt(hole_outer_cycle_points)

        # Close the polygon wkt representation.
        geom_wkt += ')'

    # The geometry is a single polygon (1 face with >= 0 holes).
    if counter == 1:
        geom_wkt = 'POLYGON ' + geom_wkt
    # The geometry has >1 faces each with >= 0 holes.
    else:
        geom_wkt = 'MULTIPOLYGON (' + geom_wkt + ')'

    return geom_wkt

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Inputs.
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Geometries (shapes).

# New Interface
#s_faces_wkt = 'POLYGON ((2 1, 4 1, 3 4, 2 1), (4 2, 5 2, 5 3, 4 2))'
#t_faces_wkt = 'POLYGON ((2 1, 4 1, 3 4, 2 1), (1 2, 2 2, 2 3, 1 2))'

#s_faces_wkt = 'POLYGON ((3 3, 12 7, 4 10, 3 3), (4 6, 6 7, 5 8, 4 6), (7 6, 8 7, 7 8, 7 6))'
#t_faces_wkt = 'POLYGON ((17 4, 27 0, 20.5 12, 17 4), (19 5.5, 20 5, 20 7, 19 5.5), (22 4, 24 3, 24 4, 22 4))'


s_faces_wkt = 'MULTIPOLYGON (((3 3, 12 7, 4 10, 3 3), (4 6, 6 7, 5 8, 4 6), (7 6, 8 7, 7 8, 7 6)), ((7 2, 9 2, 7 4, 7 2)))'
t_faces_wkt = 'MULTIPOLYGON (((17 4, 27 0, 20.5 12, 17 4), (19 5.5, 20 5, 20 7, 19 5.5), (22 4, 24 3, 24 4, 22 4)), ((27 8, 29 8, 29 10, 27 8)))'
s_faces, s_holes = wkt_to_geometry_segment_lists(str(sys.argv[3]))
t_faces, t_holes = wkt_to_geometry_segment_lists(str(sys.argv[4]))

#script params if at instant:
## begin time, end time, source geo, target geo, query time
#script params if at period:
## begin time, end time, source geo, target geo, query time begin, query time end, num samples
# New Interface

#source_geom = wkt_to_segment_list(str(sys.argv[4]))
#target_geom = wkt_to_segment_list(str(sys.argv[5]))

# Validate the wkt parsing process output.

#if source_geom == [] or target_geom == []:
#    print("Error parsing wkt.")
#    quit()

# Input for the interpolation of the CIR.
query_time_begin = int(float(sys.argv[5]))
at_instant = True

n_samples = 1

#if there are 8 parameters, during period is selected,
#if there are 6 parameters, at instant is selected
if len(sys.argv) == 6:
	query_time_end = query_time_begin #at instant
elif len(sys.argv) == 8:
	query_time_end = int(float((sys.argv[6])))
	at_instant = False
	n_samples = int(sys.argv[7])
else:
	print("Error, invalid number of parameters")

# Number of samples to be taken.



# CIR interval.

source_t = int(float(sys.argv[1]))
target_t = int(float(sys.argv[2]))
# Create the CIR.

#cir = create_CIR(source_geom, target_geom, source_t, target_t)
#cir = create_CIR_with_holes()
cir = create_complex_CIR(s_faces, s_holes, t_faces, t_holes, source_t, target_t)

"""
region_at = at(complex_cir, query_time_begin)
if region_at != None:
    print(structural_region_to_wkt(region_at))
else:
    print("ERR_AT")

region_at = at(complex_cir, query_time_end)
if region_at != None:
    print(structural_region_to_wkt(region_at))
else:
    print("ERR_AT")

quit()
"""

"""
    Do work.
	Call at() to get a specified number of samples (aka, regions).
"""

n = (n_samples - 1)
dt = (query_time_end - query_time_begin)

if at_instant:
	#at instant

	# Get region at t.
	region_at = at(cir, query_time_begin)
	if region_at != None:
		print(structural_region_to_wkt(region_at))
	else:
		print("Error: Region is None!")
		quit()
else:
	#during period
	for i in range(0, n_samples):
		t = (float(i) / n) * dt + query_time_begin

		# Get region at t.
		region_at = at(cir, t)
		#region_at = at(complex_cir, t)

		# Debug.
		if region_at != None:
			print(structural_region_to_wkt(region_at))
		else:
			print("Error: Region is None!")
			quit()