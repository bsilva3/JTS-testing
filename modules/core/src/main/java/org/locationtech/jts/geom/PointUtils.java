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

/*
    utility methods for points
*/
public class PointUtils extends Point{
    
    
    public PointUtils(CoordinateSequence coordinates, GeometryFactory factory) {
        super(coordinates, factory);
        init(coordinates);
    }
    
    //used to transform this point from the original image to the size of the window the image is in
    public Point transform (double originalWidth, double originalHeight, double panelWidth, double panelHeight){
        double transformedX = getCoordinateConversion(this.getX(), originalWidth, panelWidth);
        double transformedY = getCoordinateConversion(this.getY(), originalHeight, panelHeight);
        return new GeometryFactory().createPoint(new Coordinate(transformedX, transformedY));
    }
    
    private double getCoordinateConversion(double c, double original, double panel){
        return (c/original) * panel;
    }

    @Override
    public String toString() {
        return "x: " + this.getX() +"y: "+ this.getY();
    }
    
    
}
