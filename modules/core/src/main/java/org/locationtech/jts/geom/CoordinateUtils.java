/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jts.geom;

/**
 *
 * @author Bruno Silva
 */
public class CoordinateUtils extends Coordinate{
    
    public CoordinateUtils (double x, double y){
        super(x, y);
    }
    
    //used to transform this point from the original image to the size of the window the image is in
    public Coordinate transform (double originalWidth, double originalHeight, double panelWidth, double panelHeight){
        double transformedX = getCoordinateConversion(this.getX(), originalWidth, panelWidth);
        double transformedY = getCoordinateConversion(originalHeight - this.getY(), originalHeight, panelHeight);
        return new Coordinate(transformedX, transformedY);
    }
    
    public void transformCoords (double originalWidth, double originalHeight, double panelWidth, double panelHeight){
        this.setX(getCoordinateConversion(this.getX(), originalWidth, panelWidth));
        this.setY(getCoordinateConversion(originalHeight - this.getY(), originalHeight, panelHeight));
    }
    
    private double getCoordinateConversion(double c, double original, double panel){
        return (c/original) * panel;
    }
    
    public void translate(Coordinate coord){
        this.x+=coord.getX();
        this.y+=coord.getY();
    }
    
}
