/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder;

import java.util.List;
import org.locationtech.jts.geom.Coordinate;

/**
 *
 * @author Bruno Silva
 */
//stores the List of Coordinates taken from the corr files.
//one List of Coordinates is from the right panel, and the other is from the left
public class AppCorrGeometries {
    
    private List<Coordinate> corrGeometry1;
    
    private List<Coordinate> corrGeometry2;
    
    private static AppCorrGeometries instance;
    
    private AppCorrGeometries() {}
    
    public static AppCorrGeometries getInstance(){
        if(instance == null){
            instance = new AppCorrGeometries();
        }
        return instance;
    }

    public List<Coordinate> getCorrGeometry1() {
        return corrGeometry1;
    }

    public void setCorrGeometry1(List<Coordinate> corrGeometry1) {
        this.corrGeometry1 = corrGeometry1;
    }

    public List<Coordinate> getCorrGeometry2() {
        return corrGeometry2;
    }

    public void setCorrGeometry2(List<Coordinate> corrGeometry2) {
        this.corrGeometry2 = corrGeometry2;
    }
    
    
    
}
