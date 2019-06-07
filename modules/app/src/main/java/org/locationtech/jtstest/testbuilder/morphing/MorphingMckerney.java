package org.locationtech.jtstest.testbuilder.morphing;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;
import jni_st_mesh.Main;
import static jni_st_mesh.MorphingMckerney.listSegmentToCoordinateList;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.Polygon;
import org.locationtech.jtstest.testbuilder.AppStrings;

/**
 *Given a source and a target, a begin and end time, a query time, and a morphing method, calls appropriate libraries to 
 * to perform the morphing operations using the provided input. This class acts as facade to call morphing methos from multiple
 * libraries
 */
public class MorphingMckerney {
    private String geometry1;
    private String geometry2;
    private double beginTime;
    private double endTime;
    private MorphingMethod morphingMethod;

    public MorphingMckerney(String geometry1, String geometry2, double beginTime, double endTime, MorphingMethod morphingMethod) {
        this.geometry1 = geometry1;
        this.geometry2 = geometry2;
        this.beginTime = beginTime;
        this.endTime = endTime;
        this.morphingMethod = morphingMethod;
    }
    
    
    /**
     * @param queryTime - must not be lower than beginTime and not higher than endTime
     * @return 
     */
    public String morphingMckerneyAtInstant (double queryTime){
        //String p1 = "POLYGON ((256.8359375 227.90468750000002, 266.11328125 215.69114583333334, 268.5546875 209.09583333333333, 267.578125 201.5234375, 268.798828125 196.39375, 274.90234375 191.50833333333333, 279.052734375 180.27187500000002, 278.3203125 171.47812499999998, 281.73828125 161.21875, 282.958984375 149.00520833333331, 278.80859375 143.38697916666666, 272.216796875 143.38697916666666, 265.13671875 153.64635416666667, 264.404296875 159.26458333333335, 260.498046875 163.17291666666665, 256.8359375 164.27213541666669, 253.173828125 165.37135416666666, 245.849609375 179.29479166666667, 231.4453125 205.92031250000002, 228.271484375 212.75989583333333, 216.30859375 243.04947916666666, 207.03125 273.33906249999995, 220.947265625 280.66718749999995, 228.515625 272.85052083333335, 238.525390625 265.76666666666665, 243.65234375 259.415625, 252.44140625 239.14114583333333, 256.8359375 227.90468750000002))";
        //String p2 = "POLYGON ((257.568359375 224.9734375, 261.962890625 221.06510416666669, 269.53125 206.653125, 268.798828125 198.83645833333333, 270.01953125 193.70677083333334, 276.611328125 188.3328125, 281.25 177.09635416666669, 279.296875 171.47812499999998, 283.69140625 158.77604166666669, 285.15625 145.82968749999998, 276.611328125 139.96718750000002, 273.681640625 140.94427083333335, 267.578125 151.20364583333333, 267.08984375 155.84479166666665, 263.18359375 160.24166666666667, 260.986328125 159.753125, 251.46484375 167.56979166666667, 243.1640625 188.57708333333335, 235.83984375 198.83645833333333, 225.09765625 217.40104166666669, 213.623046875 244.51510416666667, 207.03125 269.43072916666665, 220.458984375 276.75885416666665, 225.5859375 274.5604166666667, 228.759765625 268.69791666666663, 239.013671875 261.85833333333335, 244.384765625 255.26302083333334, 257.568359375 224.9734375))";
        //System.out.println(this.geometry1);
        //System.out.println(this.geometry2);
        List<Coordinate> coordinates = new ArrayList<>();
        StringBuilder output = new StringBuilder();
        String sep = System.getProperty("file.separator");
        //call python script
        ProcessBuilder pb = new ProcessBuilder("python","pyspatiotemporalgeom" + sep + "mckerney2.py", geometry1, geometry2, (int)beginTime+"", (int)endTime+"", (int)queryTime+"");
        try {
            Process p = pb.start();
            BufferedReader reader =  new BufferedReader(new InputStreamReader(p.getInputStream()));

            /*String line;
            while ((line = reader.readLine())!= null) {
                output.append(line).append("\n");
            }*/
            BufferedReader br = new BufferedReader(new FileReader("wkt.txt"));
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();
            List<String> lines = new ArrayList<>();
            while (line != null) {
                    sb.append(line);
                    lines.add(line);
                    sb.append(System.lineSeparator());
                    line = br.readLine();
                }
                String everything = sb.toString();
                String [] wktLine = lines.get(0).split(" = ");
                //for (String s : wktLine){//for each line
                    String s = wktLine[1].replace("[", "");
                    System.out.println("->"+s);
                    s = s.replace(";];", "");
                    String[] coordsList = s.split("; ");//get list of coordinates
                    for (String c : coordsList){
                        String[] point = c.split(", ");
                        //convert to coordinate
                        coordinates.add(new Coordinate(Double.parseDouble(point[0]), Double.parseDouble(point[1])));
                    }
                //}
        } catch (IOException ex) {
            Logger.getLogger(MorphingMckerney.class.getName()).log(Level.SEVERE, null, ex);
        }
        Coordinate[] coordinateArray = new Coordinate[coordinates.size()];
        coordinates.toArray(coordinateArray); // fill the array
        Polygon p = new GeometryFactory().createPolygon(coordinateArray);
        System.out.println(p.toText());
        return p.toText();
        //receive morphing result. It's a list of line segment format, so we must convert it to wkt
        //return parseMorphingResultInstant(output.toString());
    }
    
    public String parseMorphingResultInstant(String result){
        String coords;
        System.out.println("result _> "+result);
        /*try{
            String[] resultSplit = result.split("F: 1: ");
            coords = resultSplit[1].split(";")[0];
            if (resultSplit.length > 1){
                coords = resultSplit[1];
            }
            else{
                coords = resultSplit[0];
            }
            if (!coords.contains("[((")){
                resultSplit = result.split("segs:  ");
                coords = resultSplit[1];
            }
            System.out.println("coords: "+coords+"<--");
            return listSegmentToWKT(coords);
            //System.out.println(wkt);
        } catch(ArrayIndexOutOfBoundsException ex){
            Logger.getLogger(MorphingMckerney.class.getName()).log(Level.SEVERE, null, ex);
            return null;
        }*/
        String coord = null;
        //String[] resultSplit = result.split("result");
        String[] resultSplit = result.split("segs:  ");
        coord = resultSplit[1];
        System.out.println("-> "+ coord);
        return listSegmentToWKT(coord);
        //System.out.println(wkt);
    }
    
    /**
     * @param queryTimeBegin
     * @param queryTimeEnd 
     * @return 
     */
    public String[] morphingMckerneyDuringPeriod (double queryTimeBegin, double queryTimeEnd){
        //String p1 = "POLYGON ((256.8359375 227.90468750000002, 266.11328125 215.69114583333334, 268.5546875 209.09583333333333, 267.578125 201.5234375, 268.798828125 196.39375, 274.90234375 191.50833333333333, 279.052734375 180.27187500000002, 278.3203125 171.47812499999998, 281.73828125 161.21875, 282.958984375 149.00520833333331, 278.80859375 143.38697916666666, 272.216796875 143.38697916666666, 265.13671875 153.64635416666667, 264.404296875 159.26458333333335, 260.498046875 163.17291666666665, 256.8359375 164.27213541666669, 253.173828125 165.37135416666666, 245.849609375 179.29479166666667, 231.4453125 205.92031250000002, 228.271484375 212.75989583333333, 216.30859375 243.04947916666666, 207.03125 273.33906249999995, 220.947265625 280.66718749999995, 228.515625 272.85052083333335, 238.525390625 265.76666666666665, 243.65234375 259.415625, 252.44140625 239.14114583333333, 256.8359375 227.90468750000002))";
        //String p2 = "POLYGON ((257.568359375 224.9734375, 261.962890625 221.06510416666669, 269.53125 206.653125, 268.798828125 198.83645833333333, 270.01953125 193.70677083333334, 276.611328125 188.3328125, 281.25 177.09635416666669, 279.296875 171.47812499999998, 283.69140625 158.77604166666669, 285.15625 145.82968749999998, 276.611328125 139.96718750000002, 273.681640625 140.94427083333335, 267.578125 151.20364583333333, 267.08984375 155.84479166666665, 263.18359375 160.24166666666667, 260.986328125 159.753125, 251.46484375 167.56979166666667, 243.1640625 188.57708333333335, 235.83984375 198.83645833333333, 225.09765625 217.40104166666669, 213.623046875 244.51510416666667, 207.03125 269.43072916666665, 220.458984375 276.75885416666665, 225.5859375 274.5604166666667, 228.759765625 268.69791666666663, 239.013671875 261.85833333333335, 244.384765625 255.26302083333334, 257.568359375 224.9734375))";
        //System.out.println(this.geometry1);
        //System.out.println(this.geometry2);
        List<String> wkts = new ArrayList<>();
        StringBuilder output = new StringBuilder();
        String sep = System.getProperty("file.separator");
        //call python script
        ProcessBuilder pb = new ProcessBuilder("python","pyspatiotemporalgeom" + sep + "mckerney2.py", geometry1, geometry2, (int)beginTime+"", (int)endTime+"", (int)queryTimeBegin+"", (int)queryTimeEnd+"");
        try {
            Process p = pb.start();
            BufferedReader reader =  new BufferedReader(new InputStreamReader(p.getInputStream()));

            String line;
            while ((line = reader.readLine())!= null) {
                output.append(line).append("\n");
            }
            //System.out.println("output -> "+output);
            BufferedReader br = new BufferedReader(new FileReader("wkt.txt"));
            StringBuilder sb = new StringBuilder();
            line = br.readLine();
            List<String> lines = new ArrayList<>();
            while (line != null) {
                    sb.append(line);
                    lines.add(line);
                    sb.append(System.lineSeparator());
                    line = br.readLine();
                }
            
            for (int i = 0; i < lines.size(); i++){
                List<Coordinate> coordinates = new ArrayList<>();
                List<Coordinate> coordinatesEX = new ArrayList<>();
                String [] wktLine = lines.get(i).split(" = ");
                String s = wktLine[1].replace("[", "");
                System.out.println("->"+s);
                s = s.replace(";];", "");
                String[] coordsList = s.split("; ");//get list of coordinates
                for (String c : coordsList){
                    String[] point = c.split(", ");
                    //convert to coordinate
                    coordinates.add(new Coordinate(Double.parseDouble(point[0]), Double.parseDouble(point[1])));
                }
                //remove collinear points
                /*for (int j = 0; j < coordinates.size()-2; j++){
                    double p1x = coordinates.get(j).x;
                    double p1y = coordinates.get(j).y;

                    double p2x = coordinates.get(j+1).x;
                    double p2y = coordinates.get(j+1).y;

                    double p3x = coordinates.get(j+2).x;
                    double p3y = coordinates.get(j+2).y;
                    
                    if (p2x - p1x != 0 && p3x - p1x != 0){
                        double s1 = (p2y - p1y) / (p2x - p1x);
                        double s2 = (p3y - p1y) / (p3x - p1x);
                        if (s1!= s2){
                            coordinatesEX.add(coordinates.get(j+1));
                        }
                    }
                    else if (!(p2x - p1x == 0 && p3x - p1x == 0)){
                        coordinatesEX.add(coordinates.get(j+1));
                    }
                    
                }*/
                //convert to polygon and then wkt
                Coordinate[] coordinateArray = new Coordinate[coordinates.size()];
                coordinates.toArray(coordinateArray); // fill the array
                coordinateArray[coordinateArray.length-1] = coordinateArray[0];
                Polygon pol = new GeometryFactory().createPolygon(coordinateArray);
                System.out.println(pol.toText());
                wkts.add(pol.toText());
            }
        } catch (IOException ex) {
            Logger.getLogger(MorphingMckerney.class.getName()).log(Level.SEVERE, null, ex);
        }
        //receive morphing result. It's a list of line segment format, so we must convert it to wkt
        String[] wktsArray = new String[wkts.size()];
        wkts.toArray(wktsArray); // fill the array
        return wktsArray;
    }
    
    
    public String[] parseMorphingResultPeriod(String result){
       // System.out.println("-->"+result);
       
        List<String> coords = new ArrayList<>();
        try{
            String[] resultSplit = result.split("result");
            for (int i = 1; i < resultSplit.length; i+=2){
                //System.out.println("iterBegin\n"+resultSplit[i]+"\niterEnd");
                coords.add(resultSplit[i]);
            }
            String[] coordsList = new String[coords.size()];
            for (int i = 0; i < coords.size(); i++){
                coordsList[i] = listSegmentToWKT(coords.get(i));
            }
            /*for (String s : coordsList){
                 System.out.println(s);
            }*/
            return coordsList;
            //System.out.println(wkt);
        } catch(ArrayIndexOutOfBoundsException ex){
            Logger.getLogger(MorphingMckerney.class.getName()).log(Level.SEVERE, null, ex);
            return null;
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
        System.out.println("list of segments: "+ Arrays.toString(listOfSegments));
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
            /*if (c1.equals2D(c2)){
                continue;
            }*/
            coords.put(c1 , c2);
        }
        Coordinate[] coordsOrdered = new Coordinate[coords.size()+1];
        coordsOrdered[0] = coords.keySet().stream().findFirst().get();
        int nPointsProcessed = 1;
        while (nPointsProcessed < coords.size()){
            Coordinate c = coordsOrdered[nPointsProcessed-1];
            System.out.println("point: "+c);
            coordsOrdered[nPointsProcessed] = coords.get(c);
            nPointsProcessed++;
        }
        //close polygon:
        coordsOrdered[coords.size()] = coordsOrdered[0];
        return coordsOrdered;
        /*//List<Coordinate> segments = new ArrayList<>();
        Set<Coordinate> coordinates = new LinkedHashSet<>();
        //ou usar List e manter os repetidos..
        for (int i = 1; i < listOfSegments.length; i+=2){
            String x = listOfSegments[i-1].split("[\\)\\(]+")[1];
            String y = listOfSegments[i].split("[\\)\\(]+")[0];
            
            Coordinate c1 = new Coordinate(Double.parseDouble(x), Double.parseDouble(y));
            coordinates.add(c1);
        }
        
        Coordinate[] coordsList = new Coordinate[coordinates.size()+1];//account that we have to close the polygon
        coordsList = coordinates.toArray(coordsList);
        //close polygon:
        coordsList[coordsList.length-1]=coordsList[0];
        return coordsList;*/
    }
    
    public String listSegmentToWKT(String listSegment){
        Coordinate[] coordsOrdered = listSegmentToCoordinateList(listSegment);
        Polygon p = new GeometryFactory().createPolygon(coordsOrdered);
        return p.toText();
    }
}
