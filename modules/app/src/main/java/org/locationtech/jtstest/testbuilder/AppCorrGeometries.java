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
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.CoordinateUtils;
import org.locationtech.jtstest.testbuilder.model.GeometryEditModel;
import org.locationtech.jtstest.util.io.CorrToGeometryUtils;

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
    
    private Map<BufferedImage, Coordinate> images = new HashMap<>();
    
    private static final int IMAGE_HEIGHT = 10;
    
    private static final int IMAGE_WIDTH = 10;
    
    private static final int MAX_POINTS_STORED = 2;
    
    private JTSTestBuilderFrame frame;
    
    private int editIndex = -1;
    
    //flag to indicate if user manually edited, added, or deleted a point from on of the geometries
    //any changed made to one of the geometries will be equally made in the other geometry
    private boolean isCorrGeometryEdited = false;
    
    private static AppCorrGeometries instance;
    
    private AppCorrGeometries() {}
    
    public static AppCorrGeometries getInstance(){
        if(instance == null){
            instance = new AppCorrGeometries();
        }
        return instance;
    }
    
    public List<Coordinate> getListOfCoords(GeometryEditPanel editPanel){
        if (isCorrGeometryEdited){
            if (editPanel.isSecondPanel()){
                return this.corrGeometry2;
            }
            return this.corrGeometry1;
        }
        else{
            CorrToGeometryUtils corrToGeomUtils = new CorrToGeometryUtils(AppImage.getInstance().getCurrentCorrFile());
            //call this just to make sure that the variables with the image dimensions in the panel are not null or zero
            return correctCoordinates(corrToGeomUtils.getCoordsFromFile(editPanel.isSecondPanel()), editPanel);
        }
    }
    
    private List<Coordinate> correctCoordinates(Coordinate[] coord, GeometryEditPanel editPanel){
        AppImage appImage = AppImage.getInstance();
        Point2D viewOrigin = editPanel.getViewport().toView(new Coordinate(0, 0));
        double vOriginX = viewOrigin.getX();
        double currImageHeight = appImage.getImageHeightInPanel(editPanel.isSecondPanel());
        double currImageWidth = appImage.getImageWidthInPanel(editPanel.isSecondPanel());
        List<Coordinate> transformedCoords = new ArrayList<>();
        CoordinateUtils coordUtils;
        for (Coordinate c : coord){
            coordUtils = new CoordinateUtils(c.getX(), c.getY() );
            
            coordUtils.transformCoords(appImage.getCurrentImageWidth(editPanel.isSecondPanel()), 
                    appImage.getCurrentImageHeight(editPanel.isSecondPanel()), currImageWidth, currImageHeight);
            
            //add the diference of the top of the panel and the image 
            coordUtils.translate(new CoordinateUtils(vOriginX, (editPanel.getSize().getHeight() - currImageHeight) - 
                    (editPanel.getSize().getHeight() - currImageHeight) ));
            
            transformedCoords.add(coordUtils);
        }
        return transformedCoords;
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
    public void higlightCorrespondingPointInPanel(List<Coordinate> coords, boolean isSecondPanel){
        for (Coordinate coord : coords){
            Coordinate c = getCorrespondingCoordinate(coord.x, coord.y, isSecondPanel);
            if (c != null || drawnPoints.size() < MAX_POINTS_STORED){
                if (drawnPoints.contains(c)){
                    //this point is already marked
                    continue;
                }
                drawnPoints.add(c);
            }
        }
        //editPanel.setPointsDrawn(true);
        GeometryEditPanel editPanel;
        if(isSecondPanel){
            //we want to mark on the other panel
            editPanel = JTSTestBuilderFrame.getGeometryEditPanel();
        }
        else{
            editPanel = JTSTestBuilderFrame.getGeometryEditPanel2();
        }
        drawPoints(editPanel);
    }
    
    //draws a red dot on all points in the list in the panel
    //(this function is called on the render manager of the panel to be drawn the dots after a 
    //"force repaint" happens, because this method is asynchronous and this way the dots are not deleted.
    public void drawPoints(GeometryEditPanel editPanel){
        Graphics2D g2 = (Graphics2D) editPanel.getGraphics();
        g2.setStroke(new BasicStroke(6));
        g2.setColor(Color.red);
        Point2D point;
        BufferedImage bi;
        //draw the images to cover the red points previously drawn
        for (Map.Entry<BufferedImage, Coordinate> image : images.entrySet()){
            try{
                Point2D p = editPanel.getViewport().toView(image.getValue());
                g2.drawImage(image.getKey(), (int)p.getX()-IMAGE_WIDTH/2, (int)p.getY()-IMAGE_HEIGHT/2, IMAGE_WIDTH, IMAGE_HEIGHT, null);
            } catch (java.awt.image.RasterFormatException e) {}
                        
        }
        images.clear();
        //get the images cropped from the panel
        for (Coordinate c : drawnPoints){
            if (c!= null){
                point = editPanel.getViewport().toView(c);
                BufferedImage originalImage = (BufferedImage) editPanel.getRenderMgr().getImage();
                try{ 
                    bi = originalImage.getSubimage((int)point.getX()-IMAGE_WIDTH/2, (int)point.getY()-IMAGE_HEIGHT/2, IMAGE_WIDTH, IMAGE_HEIGHT);
                    this.images.put(bi, c);
                } catch (java.awt.image.RasterFormatException e) {}
                g2.drawLine((int)point.getX(), (int)point.getY(), (int)point.getX(), (int)point.getY());
            }
        }
        drawnPoints.clear();        
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
            this.isCorrGeometryEdited = true;
            Coordinate newC = new Coordinate(newX, newY);
            if (isSecondPanel){
                this.corrGeometry2.set(editIndex, newC);
            }
            else{
                this.corrGeometry1.set(editIndex, newC);
            }
            //there is no longer a point edited 
            editIndex = -1;
            frame.reloadBothPanels();
        }
    }
    
    //given a coordinate, if it is exists on one of the corr geometries, it is deleted from both geometries
    public void deletePointInBothCorrGeometries(Coordinate c){
        if ( this.corrGeometry1.contains(c)){
            this.isCorrGeometryEdited = true;
            int index = corrGeometry1.indexOf(c);
            corrGeometry2.remove(index);
            corrGeometry1.remove(index);
            frame.reloadBothPanels();
        }
        else if ( this.corrGeometry2.contains(c)){
            this.isCorrGeometryEdited = true;
            int index = corrGeometry2.indexOf(c);
            corrGeometry2.remove(index);
            corrGeometry1.remove(index);
            frame.reloadBothPanels();
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
    
    public void setFrame(JTSTestBuilderFrame frame){
        this.frame = frame;
    }
    
}
