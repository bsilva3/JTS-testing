package jni_st_mesh;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.Polygon;

/**
 *
 * @author Bruno Silva
 */
public class MorphingMckerney {
    
    
    
    public static void main(String[] args){
        
        String p1 = "POLYGON ((256.8359375 227.90468750000002, 266.11328125 215.69114583333334, 268.5546875 209.09583333333333, 267.578125 201.5234375, 268.798828125 196.39375, 274.90234375 191.50833333333333, 279.052734375 180.27187500000002, 278.3203125 171.47812499999998, 281.73828125 161.21875, 282.958984375 149.00520833333331, 278.80859375 143.38697916666666, 272.216796875 143.38697916666666, 265.13671875 153.64635416666667, 264.404296875 159.26458333333335, 260.498046875 163.17291666666665, 256.8359375 164.27213541666669, 253.173828125 165.37135416666666, 245.849609375 179.29479166666667, 231.4453125 205.92031250000002, 228.271484375 212.75989583333333, 216.30859375 243.04947916666666, 207.03125 273.33906249999995, 220.947265625 280.66718749999995, 228.515625 272.85052083333335, 238.525390625 265.76666666666665, 243.65234375 259.415625, 252.44140625 239.14114583333333, 256.8359375 227.90468750000002))";
        String p2 = "POLYGON ((257.568359375 224.9734375, 261.962890625 221.06510416666669, 269.53125 206.653125, 268.798828125 198.83645833333333, 270.01953125 193.70677083333334, 276.611328125 188.3328125, 281.25 177.09635416666669, 279.296875 171.47812499999998, 283.69140625 158.77604166666669, 285.15625 145.82968749999998, 276.611328125 139.96718750000002, 273.681640625 140.94427083333335, 267.578125 151.20364583333333, 267.08984375 155.84479166666665, 263.18359375 160.24166666666667, 260.986328125 159.753125, 251.46484375 167.56979166666667, 243.1640625 188.57708333333335, 235.83984375 198.83645833333333, 225.09765625 217.40104166666669, 213.623046875 244.51510416666667, 207.03125 269.43072916666665, 220.458984375 276.75885416666665, 225.5859375 274.5604166666667, 228.759765625 268.69791666666663, 239.013671875 261.85833333333335, 244.384765625 255.26302083333334, 257.568359375 224.9734375))";
        
        String p3 = "POLYGON ((1052 987, 1090 1037, 1100 1064, 1096 1095, 1101 1116, 1126 1136, 1143 1182, 1140 1218, 1154 1260, 1159 1310, 1142 1333, 1115 1333, 1086 1291, 1083 1268, 1067 1252, 1052 1247.5, 1037 1243, 1007 1186, 948 1077, 935 1049, 886 925, 848 801, 905 771, 936 803, 977 832, 998 858, 1034 941, 1052 987))";
        String p4 = "POLYGON ((1055 999, 1073 1015, 1104 1074, 1101 1106, 1106 1127, 1133 1149, 1152 1195, 1144 1218, 1162 1270, 1168 1323, 1133 1347, 1121 1343, 1096 1301, 1094 1282, 1078 1264, 1069 1266, 1030 1234, 996 1148, 966 1106, 922 1030, 875 919, 848 817, 903 787, 924 796, 937 820, 979 848, 1001 875, 1055 999))";
        String beginTime = "1000";
        String endTime = "2000";
        String queryTime = "1500";
        StringBuilder output = new StringBuilder();
        String sep = System.getProperty("file.separator");
        ProcessBuilder pb = new ProcessBuilder("python","pyspatiotemporalgeom" + sep + "mckerney.py", p3, p4, beginTime, endTime, queryTime);
        try {
            Process p = pb.start();
            BufferedReader reader =  new BufferedReader(new InputStreamReader(p.getInputStream()));

            String line;
            while ((line = reader.readLine())!= null) {
                output.append(line).append("\n");
            }
        } catch (IOException ex) {
            Logger.getLogger(MorphingMckerney.class.getName()).log(Level.SEVERE, null, ex);
        }
        System.out.println(output.toString());
        //receive morphing result. It's a list of line segment format, so we must convert it to wkt
        String result = output.toString();
        String coords;
        try{
            coords = result.split("segs:  ")[1];
            String wkt = listSegmentToWKTConversor(coords);
            System.out.println(wkt);
        } catch(ArrayIndexOutOfBoundsException ex){
            Logger.getLogger(MorphingMckerney.class.getName()).log(Level.SEVERE, null, ex);
            System.exit(0);
        }
        
    }
    
    /**
     * Converts the representation of a geometry from a list of line segments to a list of coordinates with ordered points.
     * The mckerney library does not always returns the list of line segment ordered with the connections of lines, and this
     * method makes sure all points are coorectly interconected so that the geometry is properly drawn.
     * Only works for polygons
     * @param listSegment - string with the list of segments of a geometry
     * @return 
     */
    public static Coordinate[] listSegmentToCoordinateList(String listSegment){
        listSegment = listSegment.split("\\[")[1].split("\\]")[0];
        String[] listOfSegments = listSegment.split(", ");
    
        Map<Coordinate, Coordinate> coords = new HashMap<>();
        for (int i = 3; i < listOfSegments.length; i+=4){
            //split to remove parenthesis and then get each number of the coordinate
            String xCoordPoint1 = listOfSegments[i-3].split("[\\)\\(]+")[1];
            String yCoordPoint1 = listOfSegments[i-2].split("[\\)\\(]+")[0];
            
            String xCoordPoint2 = listOfSegments[i-1].split("[\\)\\(]+")[1];
            String yCoordPoint2 = listOfSegments[i].split("[\\)\\(]+")[0];
            
            Coordinate c1 = new Coordinate(Double.parseDouble(xCoordPoint1), Double.parseDouble(yCoordPoint1));
            Coordinate c2 = new Coordinate(Double.parseDouble(xCoordPoint2), Double.parseDouble(yCoordPoint2));
            //do not add colinear points
            if (c1.equals2D(c2)){
                continue;
            }
            coords.put(c1 , c2);
        }
        Coordinate[] coordsOrdered = new Coordinate[coords.size()+1];
        coordsOrdered[0] = coords.keySet().stream().findFirst().get();
        int nPointsProcessed = 1;
        while (nPointsProcessed < coords.size()){
            Coordinate c = coordsOrdered[nPointsProcessed-1];
            coordsOrdered[nPointsProcessed] = coords.get(c);
            nPointsProcessed++;
        }
        //close polygon:
        coordsOrdered[coords.size()] = coordsOrdered[0];
        return coordsOrdered;
    }
    
    public static String listSegmentToWKTConversor(String listSegment){
        Coordinate[] coordsOrdered = listSegmentToCoordinateList(listSegment);
        Polygon p = new GeometryFactory().createPolygon(coordsOrdered);
        return p.toText();
    }
}
