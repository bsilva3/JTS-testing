/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jts.io;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.regex.Pattern;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.Point;

/**
 *
 * @author Bruno Silva
 */
public class CorrReader {
    
    private File file;
    //used to split by spaces and new lines the coordinates in the correspondence file
    //by storing the pattern here we dont need to compile it every iteration of the loop
    private Pattern operatorPattern = Pattern.compile("[\\s\\r\\n]+");
    
    public CorrReader(File file){
        this.file = file;
    }
    
    public CorrReader(String fileName){
        this.file = new File(fileName);
    }
    //reads the coordinates from file and parses the into an array of Coordinates
    public Coordinate[] readAndGetPoints(){
        StringBuilder pointsInFile = new StringBuilder();
        try(BufferedReader br = new BufferedReader(new FileReader(this.file))) {
            for(String line; (line = br.readLine()) != null; ) {
                pointsInFile.append(line);
            }
        } catch (IOException ex) {
            Logger.getLogger(CorrReader.class.getName()).log(Level.SEVERE, null, ex);
        }
        return parseCorr(pointsInFile.toString());
    }
    
    private Coordinate[] parseCorr(String lines){
        List<Coordinate> coordinates = new ArrayList<>();
        String[] pointsFromFile = operatorPattern.split(lines);
        for (int i = 2; i <pointsFromFile.length; i+=2){
            //System.out.println(Double.parseDouble(pointsFromFile[i-1]) +", " + Double.parseDouble(pointsFromFile[i]));
            double x = Double.parseDouble(pointsFromFile[i-1]);
            double y = Double.parseDouble(pointsFromFile[i]);
            coordinates.add(new Coordinate(x, y));
        }
        Coordinate [] coords = new Coordinate[coordinates.size()];
        return coordinates.toArray(coords);
    }
    
    
}
