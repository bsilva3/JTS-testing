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
    public Coordinate[] readAndGetPoints(boolean secondCoordinates){
        StringBuilder pointsInFile = new StringBuilder();
        try(BufferedReader br = new BufferedReader(new FileReader(this.file))) {
            for(String line; (line = br.readLine()) != null; ) {
                pointsInFile.append(line);
            }
        } catch (IOException ex) {
            Logger.getLogger(CorrReader.class.getName()).log(Level.SEVERE, null, ex);
        }
        return parseCorr(pointsInFile.toString(), secondCoordinates);        
    }
    
    // converts a string of coordinates into an array of Coordinates
    //if secondCoordinates is false, only the first set of coordinates is considered
    // if true, the second and the first set of coordinates are considered
    private Coordinate[] parseCorr(String lines, boolean secondCoordinates){
        //the string has the following format: x_value y_value x_value y_value
        List<Coordinate> coordinates = new ArrayList<>();
        String[] pointsFromFile = operatorPattern.split(lines);
        int startingCoord = 1;
        //to get only the first set of coordinates, iterate every 2 values, but start from the second value.
        // to get the second set of coordinates, do the same, but start from the 4th value
        if (secondCoordinates){
            startingCoord = 3;
        }
        for (int i = startingCoord; i <pointsFromFile.length; i+=4){
            double x = Double.parseDouble(pointsFromFile[i-1]);
            double y = Double.parseDouble(pointsFromFile[i]);
            //System.out.println(x+", "+y);
            coordinates.add(new Coordinate(x, y));
        }
        Coordinate [] coords = new Coordinate[coordinates.size()];
        //System.out.println(coordinates);
        return coordinates.toArray(coords);
    }
    
    
}
