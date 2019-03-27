/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.util.io;

import java.io.File;
import java.util.Arrays;
import java.util.List;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.Polygon;
import org.locationtech.jts.io.CorrReader;

/**
 *
 * @author Bruno Silva
 */
public class CorrToGeometryUtils {
    
    private CorrReader corrReader;
    
    public CorrToGeometryUtils (File corrFile){
        this.corrReader = new CorrReader(corrFile);
    }
    
    public CorrToGeometryUtils (String corrFile){
        this.corrReader = new CorrReader(new File(corrFile));
    }
    
    public List<Coordinate> getCoordsFromFile(boolean secondSetCoordinates){
        return Arrays.asList(corrReader.readAndGetPoints(secondSetCoordinates));
    }
    
    /*
    //the coordinates read from the file are not closed, and a polygon cannot be formed. 
    //this method copies the first coordinate into the last position in the array
    public Coordinate[] closeCoordinates(Coordinate[] coord){
        Coordinate[] closedCoords = new Coordinate[coord.length + 1];
        closedCoords = coord;
        closedCoords[closedCoords.length-1] = closedCoords[0];
        return closedCoords;
    }*/
    
}
