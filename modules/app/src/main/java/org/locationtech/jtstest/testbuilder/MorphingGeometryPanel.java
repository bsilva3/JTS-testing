package org.locationtech.jtstest.testbuilder;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Shape;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageIO;
import javax.swing.JComponent;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.Timer;
import javax.swing.filechooser.FileNameExtensionFilter;
import org.geotools.geometry.jts.LiteShape;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.MultiPolygon;
import org.locationtech.jts.geom.Point;
import org.locationtech.jts.geom.Polygon;

/**
 *
 * @author Bruno Silva
 */
public class MorphingGeometryPanel extends JPanel{
    private int currentGeometryNumber = 0;
    private int nGeometries = 0;
    private MultiPolygon multiPolygon = null;
    private List<MultiPolygon> multiPolygonList;
    private List<Polygon> polygonList;
    Timer timer = null;

    //for a multipolygon, each polygon in a certain instant
    public MorphingGeometryPanel(MultiPolygon m_polygon) 
    {
        multiPolygon = m_polygon;
        nGeometries = multiPolygon.getNumGeometries();
        super.setBackground(Color.white);

        timer = new Timer(10, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                repaint();
            }
        });

        timer.start();
        
    }
     
     //for a list of mesh of triangules or list of polygons
     public MorphingGeometryPanel(List<?> geometryList){
        if(geometryList.get(0) instanceof MultiPolygon){
            multiPolygonList = (List<MultiPolygon>) geometryList;
            //System.out.println("-->multiPolygon");
            nGeometries = multiPolygonList.size();
        }
        else if(geometryList.get(0) instanceof Polygon){
            polygonList = (List<Polygon>) geometryList;
            //System.out.println("-->Polygon");
            nGeometries = polygonList.size();
        }
        
        super.setBackground(Color.white);

        timer = new Timer(10, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                repaint();
            }
        });

        timer.start();
    }
    
    public void changeToMultiPolygonList(List<MultiPolygon> mpList){
        timer.stop();
        this.multiPolygonList = mpList;
        nGeometries = multiPolygonList.size();
        this.polygonList = null;
        currentGeometryNumber = 0;

        timer.restart();
    }
    
    public void changeToPolygonList(List<Polygon> pList){
        timer.stop();
        this.multiPolygonList = null;
        this.polygonList = pList;
        nGeometries = polygonList.size();
        currentGeometryNumber = 0;

        timer.restart();
    }
    
    public void pause(){
        if(timer.isRunning()){
            timer.stop();
        }
    }
    
    //start the animation from the current selected geometry number (or frame)
    public void play(){
        if(!timer.isRunning()){
            timer.start();
        }
    }
    
    public void playFromGeometry(int n){
        this.currentGeometryNumber = n;
        if(!timer.isRunning()){
            timer.start();
        }
    }

    public void paintAtInstant(int n){
        //if animation is running stop it
        pause();
        this.currentGeometryNumber = n;
        //System.out.println(currentGeometryNumber);
        repaint();
    }
    @Override
    public Dimension getPreferredSize() {
        return new Dimension(400, 400);
    }

    @Override
    protected void paintComponent(Graphics g) 
    {
        super.paintComponent(g);
        
        //draw geometry 
        Graphics2D gr = (Graphics2D) g.create();
        gr.setColor(Color.blue);

        MultiPolygon mGeometry = null;
        Polygon pGeometry = null;
        
        AffineTransform at = new AffineTransform();
        //at.translate(100, 400);
        //at.scale(20, -20);
        double panelHeight = this.getHeight();
        double panelWidth = this.getWidth();
        if (multiPolygonList != null && currentGeometryNumber < multiPolygonList.size()){
            //System.out.println("--> geo paint: " + currentGeometryNumber);
            mGeometry = multiPolygonList.get(currentGeometryNumber);
            Point p = mGeometry.getCentroid();
            at.translate(panelWidth/2 - p.getX(), panelHeight/2 - p.getY());//place center of the geometry in the midle of the panel
            
            
            //mGeometry = AppCorrGeometries.getInstance().makePolygonFitComponent(mGeometry, this);
            currentGeometryNumber++;
            //to update the slider in the ui
            firePropertyChange(AppConstants.PROPERTY_CHANGED_NAME, currentGeometryNumber-1, currentGeometryNumber);
            
            LiteShape lt = new LiteShape(mGeometry, at, false);
            
            //check if this geometry is too big for the panel. If so, subtract to every coordinate the diferenc between
            //the size of the shape and the panel
            at = scaleShapeToFitScreen(lt, p);
            lt = new LiteShape(mGeometry, at, false);
            
            
            gr.draw(lt);

        }
        else if (polygonList != null && currentGeometryNumber < polygonList.size()){
            System.out.println("--> geo paint: " + currentGeometryNumber);
            pGeometry = polygonList.get(currentGeometryNumber);
            //pGeometry = AppCorrGeometries.getInstance().makePolygonFitComponent(pGeometry, this);
            Point p = pGeometry.getCentroid();
            at.translate(panelWidth/2 - p.getX(), panelHeight/2 - p.getY());//place center of the geometry in the midle of the panel
            
            currentGeometryNumber++;
            
            //to update the slider in the ui
            firePropertyChange(AppConstants.PROPERTY_CHANGED_NAME, currentGeometryNumber-1, currentGeometryNumber);
            
            //draw on the jpanel
            LiteShape lt = new LiteShape(pGeometry, at, false);
            at = scaleShapeToFitScreen(lt, p);
            lt = new LiteShape(pGeometry, at, false);

            gr.fill(lt);
            gr.draw(lt);
            
        }
        
        gr.dispose();

        if(currentGeometryNumber >= nGeometries) {
            timer.stop();
            //reset geom number
            currentGeometryNumber = 0;
            return;    	
        }
    }
    
    private AffineTransform scaleShapeToFitScreen(Shape s, Point centerPoint){
        AffineTransform at = new AffineTransform();
        double panelHeight = this.getHeight();
        double panelWidth = this.getWidth();
        int shapeWidth = s.getBounds().getSize().width;
        int shapeHeight = s.getBounds().getSize().height;
        double diferenceWidth = 0;
        double diferenceHeight = 0;
        
        //apply some scale to reduce the size of the shape, until it fits the screen
            /*double scaleDecr = 0.1
            while (diferenceWidth > 0 || diferenceHeight > 0){
                System.out.println("scale: "+scale);
                at = new AffineTransform();
                //translate to the center, considering the scale that is going to be applied
                at.translate( (panelWidth/2) - (p.getX()*(scale)), (panelHeight/2) - (p.getY()*(scale)));
                at.scale(scale, scale);
                //create new shape with the new scale
                lt = new LiteShape(mGeometry, at, false);
                shapeWidth = lt.getBounds().getSize().width;
                shapeHeight = lt.getBounds().getSize().height;
                diferenceWidth = shapeWidth-panelWidth;
                diferenceHeight = shapeHeight - panelHeight;
                scale = scale - scaleDecr;
                if (scale <= 0.1){
                    break;
                }
            }*/
        
        if (shapeWidth > panelWidth){
            diferenceWidth = shapeWidth-panelWidth;
        }
        if (shapeHeight > panelHeight){
            diferenceHeight = shapeHeight - panelHeight;
        }
        if (diferenceWidth > 0 || diferenceHeight > 0){
            //reduce scale of shape to fit the screen
            double scale = 0.7;
            //translate to the center, considering the scale that is going to be applied
            at.translate( (panelWidth/2) - (centerPoint.getX()*(scale)), (panelHeight/2) - (centerPoint.getY()*(scale)));
            at.scale(scale, scale);
            //create new shape with the new scale
        }
        return at;
    }
    
    public void saveAnimationToImages(){
        String saveDir = "animation_images";
        JFrame parentFrame = new JFrame();
        
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle(AppStrings.SAVE_SET_IMAGES_CHOOSER_DIALOG);
        fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        fileChooser.setAcceptAllFileFilterUsed(false);
        
        int userSelection = fileChooser.showSaveDialog(parentFrame);
        
        if (userSelection == JFileChooser.APPROVE_OPTION) {
            File fileToSave = fileChooser.getSelectedFile();
            //get selected dir, create new folder to save the images
            saveDir = fileToSave.getAbsolutePath() + File.separator + saveDir;
            new File(saveDir).mkdirs();

        }
        else {
            JOptionPane.showMessageDialog(new JFrame(),
                    AppStrings.NO_FILE_SELECTED_SET_IMAGE_SAVE, AppStrings.NO_FILE_SELECTED_ERROR, JOptionPane.ERROR_MESSAGE);
            return;
        }
        
        AffineTransform at = new AffineTransform();
        at.translate(100, 400);
        at.scale(20, -20);
        
        MultiPolygon mGeometry = null;
        Polygon pGeometry = null;
        if (multiPolygonList != null){
            for (int i = 0; i <multiPolygonList.size(); i++ ){
                BufferedImage bImg = new BufferedImage(this.getWidth(), this.getHeight(), BufferedImage.TYPE_INT_RGB);
                Graphics2D gr = bImg.createGraphics();
                
                gr.setColor(Color.blue);
                
                mGeometry = multiPolygonList.get(i);
                mGeometry = AppCorrGeometries.getInstance().makePolygonFitComponent(mGeometry, this);
                //gr.fill(new LiteShape(mGeometry, at, false));
                gr.draw(new LiteShape(mGeometry, at, false));   
                try {
                    ImageIO.write(bImg, "png" , new File(saveDir+ File.separator + i + ".png"));
                } catch (IOException ex) {
                    Logger.getLogger(MorphingGeometryPanel.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }
        else if (polygonList != null){
            for (int i = 0; i <polygonList.size(); i++ ){
                BufferedImage bImg = new BufferedImage(this.getWidth(), this.getHeight(), BufferedImage.TYPE_INT_RGB);
                Graphics2D gr = bImg.createGraphics();
                
                gr.setColor(Color.blue);
                
                pGeometry = polygonList.get(i);
                pGeometry = AppCorrGeometries.getInstance().makePolygonFitComponent(pGeometry, this);
                //gr.fill(new LiteShape(mGeometry, at, false));
                gr.draw(new LiteShape(pGeometry, at, false));
                try {
                    ImageIO.write(bImg, "png" , new File(saveDir+ File.separator + i + ".png"));
                } catch (IOException ex) {
                    Logger.getLogger(MorphingGeometryPanel.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }
    }
    
    public List<BufferedImage> generateImagesFromAnimation(int nFrames){
        List<BufferedImage> images = new ArrayList<>();
        
        AffineTransform at = new AffineTransform();
        at.translate(100, 400);
        at.scale(20, -20);
        
        Geometry geometry = null;
        MultiPolygon mGeometry = null;
        Polygon pGeometry = null;
        if (multiPolygon != null){
            for (int i = 0; i <multiPolygon.getNumGeometries(); i+=nFrames ){
                //System.out.println(i);
                BufferedImage bImg = new BufferedImage(500, 500, BufferedImage.TYPE_INT_RGB);
                Graphics2D gr = bImg.createGraphics();
                
                gr.setColor(Color.blue);
                
                geometry = multiPolygon.getGeometryN(i);
                gr.fill(new LiteShape(geometry, at, false));
                gr.draw(new LiteShape(geometry, at, false));    
                images.add(bImg);
            }
        }
        
        else if (multiPolygonList != null){
            for (int i = 0; i <multiPolygonList.size(); i++ ){
                BufferedImage bImg = new BufferedImage(this.getWidth(), this.getHeight(), BufferedImage.TYPE_INT_RGB);
                Graphics2D gr = bImg.createGraphics();
                
                gr.setColor(Color.blue);
                
                mGeometry = multiPolygonList.get(currentGeometryNumber);
                //gr.fill(new LiteShape(mGeometry, at, false));
                gr.draw(new LiteShape(mGeometry, at, false));         
                images.add(bImg);
            }
        }
        else if (polygonList != null){
            for (int i = 0; i <polygonList.size(); i++ ){
                BufferedImage bImg = new BufferedImage(this.getWidth(), this.getHeight(), BufferedImage.TYPE_INT_RGB);
                Graphics2D gr = bImg.createGraphics();
                
                gr.setColor(Color.blue);
                
                pGeometry = polygonList.get(currentGeometryNumber);
                //gr.fill(new LiteShape(mGeometry, at, false));
                gr.draw(new LiteShape(mGeometry, at, false));         
                images.add(bImg);
            }
        }
        return images;
    }
    
    //for every polygon in a multipolygon, changes the coordinates of the polygon to fit the screen
    private MultiPolygon resizeMultiPolygonToFitComponent(MultiPolygon multiPol, double diferenceWidth, double diferentHeight){
        Polygon[] pol = new Polygon[multiPol.getNumGeometries()];
        for (int i = 0; i <  multiPol.getNumGeometries(); i++){
            Polygon p = (Polygon) multiPol.getGeometryN(i);
            Coordinate[] polyCoords = p.getCoordinates();
            Coordinate[] resizedCoords = new Coordinate[polyCoords.length];
            //resize coordinates of this polygon
            for (int j = 0; j < polyCoords.length ; j++){
                Coordinate c = new Coordinate(polyCoords[j].getX()-(diferenceWidth*2), polyCoords[j].getY()-(diferentHeight*2));
                resizedCoords[j] = c;
            }
            //add the resized coordinates and make a new polygon
            pol[i] = new GeometryFactory().createPolygon(resizedCoords);
        }
        //create new multipolygon from the polygons with resized coordinates
        return new GeometryFactory().createMultiPolygon(pol);
    }
}
