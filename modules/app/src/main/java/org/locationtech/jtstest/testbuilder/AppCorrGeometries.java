/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.EventQueue;
import java.awt.Graphics2D;
import java.awt.geom.Point2D;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import org.apache.commons.lang3.ArrayUtils;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.CoordinateUtils;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.LineSegment;
import org.locationtech.jts.geom.MultiPolygon;
import org.locationtech.jtstest.testbuilder.geom.GeometryLocation;
import org.locationtech.jtstest.util.io.CorrToGeometryUtils;
import org.locationtech.jts.operation.distance.DistanceOp;
import org.locationtech.jts.geom.Point;
import org.locationtech.jts.geom.Polygon;
import org.locationtech.jts.io.ParseException;
import org.locationtech.jts.io.WKTReader;
import org.locationtech.jtstest.testbuilder.model.GeometryEditModel;
import org.locationtech.jtstest.testbuilder.model.GeometryType;

/**
 *
 * @author Bruno Silva
 */
//stores the List of Coordinates taken from the corr files.
//the coordinates in the geometries read from the corr files (corr geometry) are modified if the user add/removes/ moves them
//one List of Coordinates is from the right panel, and the other is from the left one
public class AppCorrGeometries {
    
    //these lists of coordinates are set when the geometries are drawn from the first time 
    //(after reading the coordinates from the file)
    private List<Coordinate> corrGeometry1;
    
    private List<Coordinate> corrGeometry2;
    
    //stores the original coordinates read from the corr file
    private List<Coordinate> originalCorrGeometry1;
    
    private List<Coordinate> originalCorrGeometry2;
    
    //stores the coordinates of a morphed geometry
    private List<Coordinate> morphingGeometry;
    
    private boolean showMorphingGeometry = false;
    
    private List<Coordinate> drawnPoints = new ArrayList<>();
    
    private Map<BufferedImage, Coordinate> images = new HashMap<>();
    
    private static final int IMAGE_HEIGHT = 10;
    
    private static final int IMAGE_WIDTH = 10;
    
    private static final int MAX_POINTS_STORED = 2;
    
    private JTSTestBuilderFrame frame;
    
    private int editIndex = -1;
    
    //flag to indicate if user manually edited, added, or deleted a point from on of the geometries
    //any changed made to one of the geometries will be equally made in the other geometry in the other panel
    private boolean isCorrGeometryEdited = false;
    
    private static AppCorrGeometries instance;
    
    private AppCorrGeometries() {}
    
    public static AppCorrGeometries getInstance(){
        if(instance == null){
            instance = new AppCorrGeometries();
        }
        return instance;
    }
    
    //returns the coordinates of a geometry in one panel.
    //if the coordinates were edited, returns the array of coordinates with the edited points
    public List<Coordinate> getCordsFromFileOrEdited(GeometryEditPanel editPanel){
        if (isCorrGeometryEdited){
            if (editPanel.isSecondPanel()){
                return this.corrGeometry2;
            }
            return this.corrGeometry1;
        }
        else{
            CorrToGeometryUtils corrToGeomUtils = new CorrToGeometryUtils(AppImage.getInstance().getCurrentCorrFile());
            List<Coordinate> corrsFromFile = corrToGeomUtils.getCoordsFromFile(editPanel.isSecondPanel());
            
            if (editPanel.isSecondPanel()){
                //store the coordinates read from file WITHOUT any correction to fit the screen
                this.originalCorrGeometry2 = corrsFromFile;
                //store the coordinates changed to fit the screen, inside the panel
                this.corrGeometry2 = correctCoordinates(corrsFromFile, editPanel);
                return corrGeometry2;
            }
            else{
                this.originalCorrGeometry1 = corrsFromFile;
                this.corrGeometry1 = correctCoordinates(corrsFromFile, editPanel);
                return corrGeometry1;
            }
        }
    }
    
    //corrects the coordinates in the corr file according to the size of the viewport
    private List<Coordinate> correctCoordinates(List<Coordinate> coord, GeometryEditPanel editPanel){
        AppImage appImage = AppImage.getInstance();

        double currImageHeightInPanel = appImage.getImageHeightInPanel(editPanel.isSecondPanel());
        double currImageWidthInPanel = appImage.getImageWidthInPanel(editPanel.isSecondPanel());
        List<Coordinate> transformedCoords = new ArrayList<>();
        CoordinateUtils coordUtils;
        for (Coordinate c : coord){
            coordUtils = new CoordinateUtils(c.getX(), c.getY() );
            
            coordUtils.transformCoords(appImage.getCurrentImageWidth(editPanel.isSecondPanel()), 
                    appImage.getCurrentImageHeight(editPanel.isSecondPanel()), currImageWidthInPanel, currImageHeightInPanel);
            
            //add the diference of the top of the panel and the image 
            /*coordUtils.translate(new CoordinateUtils(0, -(editPanel.getSize().getHeight() - currImageHeightInPanel) - 
                    (editPanel.getSize().getHeight() - currImageHeightInPanel) ));*/
            
            coordUtils.translate(new CoordinateUtils(0, -(editPanel.getSize().getHeight() - currImageHeightInPanel)));
            
            transformedCoords.add(coordUtils);
        }
        return transformedCoords;
    }
    
    public Polygon makePolygonFitComponent(Polygon pol, JComponent comp){
        Coordinate[] transformedCoords = correctCoordinates(pol.getCoordinates(), comp);
        return new GeometryFactory().createPolygon(transformedCoords);
    }
    
    /**
     * Transform the coordinates of a geometry to fit inside a JPanel
     * @param coord - the list of coordinates to transform
     * @param comp - the Java swing component
     * @return list of coordinates transformed to fits the Java swing component
     */
    public Coordinate[] correctCoordinates(Coordinate[] coord, JComponent comp){
        
        Coordinate[] transformedCoords = new Coordinate[coord.length];
        CoordinateUtils coordUtils;
        
        //first pass to see maximum x and y coordinates
        double maxX = 0;
        double maxY = 0;
        for (Coordinate c : coord){
            if (c.x > maxX){
                maxX = c.x;
            }
            if (c.y > maxY){
                maxY = c.y;
            }
        }
        int i = 0;
        for (Coordinate c : coord){
            coordUtils = new CoordinateUtils(c.getX(), c.getY() );
            
            coordUtils.transformCoords(maxX+200, maxY+200, comp.getWidth(), comp.getHeight());
            transformedCoords[i] = coordUtils;
            i++;
        }
        return transformedCoords;
    }
    
    //returns the index of the coordinates in the array or -1 if it doesnt exist. The corresponding coordenate in the other geometry
    //on the other panel will be on the other list in the same index
    public int getCordIndex(Coordinate c, boolean isSecondPanel){
        List<Coordinate> listToSearch;
        if(isSecondPanel){
            listToSearch = corrGeometry2;
        }
        else{
            listToSearch = corrGeometry1;
        }
        for (int i = 0; i < listToSearch.size(); i++){
            if (c.equals(listToSearch.get(i))){
                return i;
            }
        }
        //does not exist
        return -1;
    }
    
    //returns the matching coordinates of the other list of coordinates.
    //They have the same indexes in both lists
    public Coordinate getCorrespondingCoordinate(Coordinate c, boolean isSecondPanel){
        List<Coordinate> correspondingCoordinates;
        if (isSecondPanel){
            //we want the other list of coordinates!
            correspondingCoordinates = corrGeometry1;
        }
        else{
            correspondingCoordinates = corrGeometry2;
        }
        int index = getCordIndex(c, isSecondPanel);
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
    public void higlightCorrespondingPointInPanel(Collection<Coordinate> coords, boolean isSecondPanel){
        for (Coordinate coord : coords){
            Coordinate c = getCorrespondingCoordinate(coord, isSecondPanel);
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
    
    //draws a red dot on all points in the list of edited points in the panel the user is not interacting
    //This function is called on the render manager of the panel to be drawn the dots, after a 
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
    
    //indicate that the user is editing a point (used when the user presses the mouse and is moving a point)
    public void savePointIfExistInCorrGeometry(Coordinate c, boolean isSecondPanel){
        int index = getCordIndex(c, isSecondPanel);
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
    
    // given a lista of coordinates removed by the user in one of the geometries in one panel, if they belong
    //to a corr geometry, delete that coordinate from both corr geometries
    public Coordinate[] deleteListOfPointsInBothCorrGeometries(List<Coordinate> coords, boolean isSecondPanel){
        List<Coordinate> interactedPanel;
        List<Coordinate> otherPanel;
        if (isSecondPanel){
            interactedPanel = this.corrGeometry2;
            otherPanel = this.corrGeometry1;
        }
        else{
            interactedPanel = this.corrGeometry1;
            otherPanel = this.corrGeometry2;
        }
        
        for(Coordinate c : coords){
            if (interactedPanel.contains(c)){
                //remove, this point was deleted
                int index = this.getCordIndex(c, isSecondPanel);
                interactedPanel.remove(index);
                otherPanel.remove(index);
            }
        }
        return otherPanel.toArray(new Coordinate[otherPanel.size()]);
    }
    
    //given a new coordinate for a panel, add that coordinate to the list (between the 2 points)
    //and find a corresponding coordinate to add in the other panel. Returns this corresponding coordinate
    public Coordinate addPointToCorrGeometries(GeometryLocation loc, boolean isSecondPanel){
        List<Coordinate> interactedPanelCoords;
        List<Coordinate> otherPanelCoords;
        Coordinate newCoordinate = loc.getCoordinate();
        List<Coordinate> nearbyCoords = loc.get2CoordsInSegment();//size 2
        if (isSecondPanel){
            interactedPanelCoords = corrGeometry2;
            otherPanelCoords = corrGeometry1;
        }
        else{
            interactedPanelCoords = corrGeometry1;
            otherPanelCoords = corrGeometry2;
        }
        //add coordinate in both panels, but first, find the points closest to the new point in a line segment
        int index1 = this.getCordIndex(nearbyCoords.get(0), isSecondPanel);
        int index2 = this.getCordIndex(nearbyCoords.get(1), isSecondPanel);
        if (index1 > -1 && index2 > -1){//they exist in the geometry
            int [] indexes = new int[]{index1, index2};
            List indexesList = Arrays.asList(ArrayUtils.toObject(indexes));
            //the new coordinate will now be on the position of the coordinate with the biggest index
            int indexForNewCoord = Integer.parseInt(Collections.max(indexesList).toString());
            int minIndex = Integer.parseInt(Collections.min(indexesList).toString());
            if (indexForNewCoord == interactedPanelCoords.size()-1 && minIndex == 0){
                //special case: simply add to the last position the new coordinate
                indexForNewCoord = interactedPanelCoords.size();
            }
            interactedPanelCoords.add(indexForNewCoord, newCoordinate);
            Coordinate newCoordinateOtherPanel = findPointInLine(interactedPanelCoords, otherPanelCoords, 
                    newCoordinate, indexForNewCoord, isSecondPanel);
            //add the new coordinate found in the respective line segment for the other geometry
            otherPanelCoords.add(indexForNewCoord, newCoordinateOtherPanel);
            return newCoordinateOtherPanel;
        }
        return null;
    }
    
    //find a point in the respective line segment on the other panel to add a point
    private Coordinate findPointInLine(List<Coordinate> referenceCoords, List<Coordinate> coordsToAddNewPoint,
            Coordinate newCoord, int newPointNumber, boolean isSecondPanel){
        Coordinate c1 = referenceCoords.get(newPointNumber-1);
        Coordinate c2 = referenceCoords.get(newPointNumber+1);
        double distanceC1_newCoord = c1.distance(newCoord);
        //total distance between the points that a coordinate was added between in the original panel
        double totalDistance = c1.distance(c2);
        double c1_newCoordRatio = (100.0*distanceC1_newCoord)/totalDistance;
        
        Coordinate c1Target = coordsToAddNewPoint.get(newPointNumber-1);
        Coordinate c2Target = coordsToAddNewPoint.get(newPointNumber);//point hasnt been added yet!
        
        LineSegment l = new LineSegment();
        l.setCoordinates(c1Target, c2Target);
        
        Coordinate aproxCoordOtherPanel;
        if(c1_newCoordRatio > 60){
            //the new point is closer do point c2
             LineSegment midLine = new LineSegment();
             midLine.setCoordinates(c2, l.midPoint());
             aproxCoordOtherPanel = midLine.midPoint();
        }
        else if(c1_newCoordRatio < 40){
            //the new point is closer do point c1
             LineSegment midLine = new LineSegment();
             midLine.setCoordinates(c1, l.midPoint());
             aproxCoordOtherPanel = midLine.midPoint();
        }
        else{
            //its more or less in the middle (40 to 60% closer to c1)
            aproxCoordOtherPanel = l.midPoint();
        }
        
        Point p = new GeometryFactory().createPoint(aproxCoordOtherPanel);
        
        Polygon corrGeometryInOtherPanel = getPanelCorrGeometry(!isSecondPanel);//get the other panel
        DistanceOp dOP = new DistanceOp(corrGeometryInOtherPanel, p);
        
        return dOP.nearestPoints()[0];
    }
    
    //returns the polygon read from the corr file in the panel
    public Polygon getPanelCorrGeometry(boolean isSecondPanel){
        GeometryFactory gf = new GeometryFactory();
        if (isSecondPanel){
            return gf.createPolygon(corrGeometry2.toArray(new Coordinate[corrGeometry2.size()]));   
        }
        else{
            return gf.createPolygon(corrGeometry1.toArray(new Coordinate[corrGeometry1.size()]));   
        }
    }
    
    //returns the polygon read from the corr file, with the original pixels in the file, without any change to fit the screen
    public Polygon getCorrGeometry(boolean isSecondPanel){
        GeometryFactory gf = new GeometryFactory();
        if (isSecondPanel){
            return gf.createPolygon(originalCorrGeometry2.toArray(new Coordinate[originalCorrGeometry2.size()]));   
        }
        else{
            return gf.createPolygon(originalCorrGeometry1.toArray(new Coordinate[originalCorrGeometry1.size()]));   
        }
    }
    
    //returns an array with the wkt of the corr geometries in both panels (with original coords from tht corr file, wihtout
    //correction to fit the screen
    //index 0 contains the wkt string of the corr geometry in the left (first) panel 
    //index 1 contains the wkt string of the corr geometry in the right (second) panel 
    public String[] getWKTextFromGeometriesInPanels(){
        //get geometry in the left panel
        Geometry g1 = getCorrGeometry(false);
        String wkt1 = GeometryEditModel.getText(g1, GeometryType.WELLKNOWNTEXT);
        
        //get geometry in the right panel
        Geometry g2 = getCorrGeometry(true);
        String wkt2 = GeometryEditModel.getText(g2, GeometryType.WELLKNOWNTEXT);
        
        return new String[] {wkt1, wkt2};
    }
    
    public Geometry WktToGeometry(String wkt){
        WKTReader reader = new WKTReader();
        Geometry g = null;
        try {
            g = reader.read(wkt);
        } catch (ParseException ex) {
            Logger.getLogger(AppCorrGeometries.class.getName()).log(Level.SEVERE, null, ex);
        }
        return g;
    }
    
    //draw in the left panel (1st panel) the result of the morphing of a geometry
    public void drawAndShowMorphingGeometry(String[] wktGeometry, boolean duringPeriod, boolean isPolygon){
        WKTReader reader = new WKTReader();

        //set of geometries for each instant, showed in a new window
        if (duringPeriod){
            //several polygons for a certain interval of time

            if(wktGeometry.length == 1){
                //a multipolygon, each polygon representing one instant
                MultiPolygon mPolygon = null;

                try {
                    //array has length 1, with the multipolygon
                    mPolygon = (MultiPolygon) reader.read(wktGeometry[0]);        			
                }catch(Exception e) {   }

                animation(wktGeometry, mPolygon);
            }
            else{
                
                if(isPolygon){
                    //a list of polygons, each representing one instant of time
                    List<Polygon> pList = new ArrayList<>();
                    for (String wkt : wktGeometry){
                        try { 
                            Polygon p = (Polygon) reader.read(wkt);
                            pList.add(p);
                        } catch (ParseException ex) {
                            Logger.getLogger(AppCorrGeometries.class.getName()).log(Level.SEVERE, null, ex);
                        }

                    }
                    animation(wktGeometry, pList);
                }
                else{
                    //a list of multipolygons, each multypoligon representing a mesh of triangules in a period of time
                    List<MultiPolygon> mpList = new ArrayList<>();
                    for (String wkt : wktGeometry){
                        try { 
                            MultiPolygon mp = (MultiPolygon) reader.read(wkt);
                            mpList.add(mp);
                        } catch (ParseException ex) {
                            Logger.getLogger(AppCorrGeometries.class.getName()).log(Level.SEVERE, null, ex);
                        }

                    }
                    animation(wktGeometry, mpList);
                }
            }
        }
        //at instant
        else {
            //one polygon or a multipolygon of triangules for one instant
            Geometry mGeometry = null;
            try {
                mGeometry = reader.read(wktGeometry[0]);
                //store this coordinates to be redrawn on the first panel when panel repaint occurs
                this.morphingGeometry = Arrays.asList(mGeometry.getCoordinates());
                morphingGeometry = this.correctCoordinates(morphingGeometry, JTSTestBuilderFrame.getGeometryEditPanel());
                showMorphingGeometryInPanel();
            } catch (ParseException ex) {
                Logger.getLogger(AppCorrGeometries.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
    
    public void animation(String[] wktGeometry, MultiPolygon multiPolygon) {
        MorphingGeometryViewerFrame mframe = new MorphingGeometryViewerFrame(wktGeometry, multiPolygon);
        openMorphingGeometryFrame(mframe);
    }
    
    public void animation(String[] wktGeometry, List<?> geomList) {
        MorphingGeometryViewerFrame mframe = new MorphingGeometryViewerFrame(wktGeometry, geomList);
        openMorphingGeometryFrame(mframe);
    }
    
    private void openMorphingGeometryFrame(MorphingGeometryViewerFrame frame){
        EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() 
            {
                try {
                    UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
                } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | UnsupportedLookAndFeelException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                //start frame to show the animation for the morphing geometry
                frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE); //dont close entire project on window close
                frame.pack();
                frame.validate();
                frame.setLocationRelativeTo(null);
                frame.setTitle(AppStrings.MORPHING_PANEL_TITLE);
                frame.setVisible(true);
            }
        });
    }
    
    public void showMorphingGeometryInPanel(){
        this.showMorphingGeometry = true;
        //draw on the 1st panel
        JTSTestBuilderFrame.getGeometryEditPanel().drawGeometry();
    }
    
    public void hideMorphingGeometryInPanel(){
        this.showMorphingGeometry = false;
        //draw back the normal geometry on the 1st panel
        JTSTestBuilderFrame.getGeometryEditPanel().drawGeometry();
    }
    
    public void clearCoords(){
        if(corrGeometry1 != null && corrGeometry2 != null){
            corrGeometry1.clear();
            corrGeometry2.clear();
        }
    }
    
    public List<Coordinate> getCorrGeometry1() {
        return corrGeometry1;
    }

    public void setCorrGeometry(List<Coordinate> corrGeometry, boolean isSecondPanel) {
        if (isSecondPanel){
         this.corrGeometry2 = corrGeometry;   
        }
        else{
         this.corrGeometry1 = corrGeometry;   
        }
    }

    public List<Coordinate> getCorrGeometry2() {
        return corrGeometry2;
    }
    
    public void setFrame(JTSTestBuilderFrame frame){
        this.frame = frame;
    }

    public JTSTestBuilderFrame getFrame() {
        return frame;
    }
    
    public void setGeometriesEdited(boolean b){
        this.isCorrGeometryEdited = b;
    }

    public boolean showMorphingGeometry() {
        return showMorphingGeometry;
    }

    public List<Coordinate> getMorphingGeometry() {
        return morphingGeometry;
    }
    
}
