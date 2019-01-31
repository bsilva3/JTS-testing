/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.geom.Point2D;
import java.util.ArrayList;
import java.util.List;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jtstest.testbuilder.model.GeometryEditModel;

/**
 *
 * @author Bruno Silva
 */
//stores the List of Coordinates taken from the corr files.
//one List of Coordinates is from the right panel, and the other is from the left
public class AppCorrGeometries {
    
    private List<Coordinate> corrGeometry1;
    
    private List<Coordinate> corrGeometry2;
    
    private List<Coordinate> drawnPoints = new ArrayList<>();
    
    private int editIndex = -1;
    
    private static AppCorrGeometries instance;
    
    private AppCorrGeometries() {}
    
    public static AppCorrGeometries getInstance(){
        if(instance == null){
            instance = new AppCorrGeometries();
        }
        return instance;
    }
    
    //returns the index of the coordinates in the array or -1 if it doesnt exist. The corresponding coordenate in the other geometry
    //on the other panel will be on the other list in the same index
    public int getCordIndex(double x, double y, boolean isSecondPanel){
        List<Coordinate> listToSearch;
        if(isSecondPanel){
            listToSearch = corrGeometry2;
        }
        else{
            listToSearch = corrGeometry1;
        }
        for (int i = 0; i < listToSearch.size(); i++){
            if (x == listToSearch.get(i).x && y == listToSearch.get(i).y){
                return i;
            }
        }
        //does not exist
        return -1;
    }
    
    //returns the matching coordinates of the other list of coordinates.
    //They have the same indexes in both lists
    public Coordinate getCorrespondingCoordinate(double x, double y, boolean isSecondPanel){
        List<Coordinate> correspondingCoordinates;
        if (isSecondPanel){
            //we want the other list of coordinates!
            correspondingCoordinates = corrGeometry1;
        }
        else{
            correspondingCoordinates = corrGeometry2;
        }
        int index = getCordIndex(x, y, isSecondPanel);
        if (index == -1){
            //not found
            return null;
        }
        return correspondingCoordinates.get(index);
    }
    
    //returns the matching coordinates of the other list of coordinates.
    //They have the same indexes in both lists
    public Coordinate getCorrespondingCoordinate(int index, boolean isSecondPanel){
        List<Coordinate> correspondingCoordinates;
        if (isSecondPanel){
            //we want the other list of coordinates!
            correspondingCoordinates = corrGeometry1;
        }
        else{
            correspondingCoordinates = corrGeometry2;
        }
        if (index == -1){
            //not found
            return null;
        }
        return correspondingCoordinates.get(index);
    }
    
    //store the point(s) the cursor is in. call a method to higlight the point in the panel
    //that the cursor IS NOT IN
    public void higlightCorrespondingPointInPanel(double x, double y, boolean isSecondPanel){
        Coordinate c = getCorrespondingCoordinate(x, y, isSecondPanel);
        if (c != null){
            if (drawnPoints.contains(c)){
                //this point is already marked
                return;
            }
            drawnPoints.add(c);
            GeometryEditPanel editPanel;
            if(isSecondPanel){
                //we want to mark on the other panel
                editPanel = JTSTestBuilderFrame.getGeometryEditPanel();
            }
            else{
                editPanel = JTSTestBuilderFrame.getGeometryEditPanel2();
            }
            editPanel.setPointsDrawn(true);
            drawPoints(editPanel);
        }
    }
    
    //call force repaint on the panel that has a highlited point. This will delete the higlited red points
    public void deleteMarkedPoints(boolean isSecondPanel){
        GeometryEditPanel editPanel;
        
        if (isSecondPanel){
            editPanel=JTSTestBuilderFrame.getGeometryEditPanel();
        }
        else{
            editPanel=JTSTestBuilderFrame.getGeometryEditPanel2();
        }
        if(editPanel.isPointsDrawn()){
            editPanel.forceRepaint();
            editPanel.setPointsDrawn(false);
            drawnPoints.clear();
        }
        
    }
    
    //draws a red dot on all points in the list in the panel
    //(this function is called on the render manager of the panel to be drawn the dots after a 
    //"force repaint" happens, because this method is asynchronous and this way the dots are not deleted.
    public void drawPoints(GeometryEditPanel editPanel){
        if(editPanel.isPointsDrawn()){
            for (Coordinate c : drawnPoints){
                Graphics2D g2 = (Graphics2D) editPanel.getGraphics();
                g2.setColor(Color.red);
                g2.setStroke(new BasicStroke(7));
                Point2D point = editPanel.getViewport().toView(c);
                g2.drawLine((int)point.getX(), (int)point.getY(), (int)point.getX(), (int)point.getY());
            }
            
        }
    }
    
    public void savePointIfExistInCorrGeometry(double x, double y, boolean isSecondPanel){
        int index = getCordIndex(x, y, isSecondPanel);
        if (index > -1){
            editIndex = index;
        }
    }
    
    //if a point from the corr geometry is moved, update the moved coordinate in the index
    //of the array with the edited corrGeometry
    public void editPointIfExistInCorrGeometry(double newX, double newY, boolean isSecondPanel){
        if (editIndex > -1){
            Coordinate newC = new Coordinate(newX, newY);
            if (isSecondPanel){
                this.corrGeometry2.set(editIndex, newC);
            }
            else{
                this.corrGeometry1.set(editIndex, newC);
            }
            //there is no longer a point edited 
            editIndex = -1;
        }
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
