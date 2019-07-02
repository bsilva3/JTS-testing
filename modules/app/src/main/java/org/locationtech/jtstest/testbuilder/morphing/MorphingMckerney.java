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
        String sep = System.getProperty("file.separator");
        //call python script
        ProcessBuilder pb = new ProcessBuilder("python","pyspatiotemporalgeom" + sep + "mckenney_final.py", beginTime+"", endTime+"", geometry1, geometry2, queryTime+"");
        String wkt = "";
        try {
            Process p = pb.start();
            BufferedReader reader =  new BufferedReader(new InputStreamReader(p.getInputStream()));
            //the output will be a wkt representing the geometry at the specified instant
            wkt = reader.readLine();
            //System.out.println(wkt);
            
        } catch (IOException ex) {
            Logger.getLogger(MorphingMckerney.class.getName()).log(Level.SEVERE, null, ex);
        }
        if (wkt != null && !wkt.isEmpty() && !wkt.contains("Error")){
            return wkt;
        }
        //System.out.println(p.toText());
        return null;
    }
    
    /**
     * Calls a python script and passes as input the time and geometries for the morphing operation using mckeeney algorithm.
     * @param queryTimeBegin
     * @param queryTimeEnd
     * @param numSamples
     * @return wkt list
     */
    public String[] morphingMckerneyDuringPeriod (double queryTimeBegin, double queryTimeEnd, int numSamples){
        List<String> wkts = new ArrayList<>();
        String sep = System.getProperty("file.separator");
        //call python script
        //parameters for during period are: begin time, end time, source geo, target geo, query time begin, query time end, num samples
        ProcessBuilder pb = new ProcessBuilder("python","pyspatiotemporalgeom" + sep + "mckenney_final.py", beginTime+"", endTime+"", geometry1, geometry2, queryTimeBegin+"", queryTimeEnd+"", numSamples+"");
        String line;
        try {
            Process p = pb.start();
            BufferedReader reader =  new BufferedReader(new InputStreamReader(p.getInputStream()));
            
            while ((line = reader.readLine())!= null) {
                //System.out.println(line);
                wkts.add(line);
            }
            
        } catch (IOException ex) {
            Logger.getLogger(MorphingMckerney.class.getName()).log(Level.SEVERE, null, ex);
        }
        String[] wkt = new String[wkts.size()];
        wkt = wkts.toArray(wkt);
        
        //receive morphing result. It's a list of line segment format, so we must convert it to wkt
        return wkt;
    }
    
}
