package org.locationtech.jtstest.testbuilder;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.geom.AffineTransform;
import java.util.List;
import javafx.beans.InvalidationListener;
import javafx.beans.Observable;
import javax.swing.JPanel;
import javax.swing.Timer;
import org.geotools.geometry.jts.LiteShape;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.MultiPolygon;

/**
 *
 * @author Bruno Silva
 */
public class MorphingGeometryPanel extends JPanel{
    private int currentGeometryNumber = 0;
    private int nGeometries = 0;
    private MultiPolygon multiPolygon = null;
    private List<MultiPolygon> multiPolygonList;
    Timer timer = null;

    //for a multipolygon, each polygon in a certain instant
    public MorphingGeometryPanel(MultiPolygon m_polygon) 
    {
        multiPolygon = m_polygon;
        nGeometries = multiPolygon.getNumGeometries();
        System.out.println(nGeometries);
        super.setBackground(Color.white);

        timer = new Timer(10, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                repaint();
            }
        });

        timer.start();
        
    }
    
    //for a list of mesh of triangules
     public MorphingGeometryPanel(List<MultiPolygon> mPolygonList){
        
        multiPolygonList = mPolygonList;
        nGeometries = multiPolygonList.size();

        super.setBackground(Color.white);

        timer = new Timer(10, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                repaint();
            }
        });

        timer.start();
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

        Geometry geometry = null;
        MultiPolygon mGeometry = null;
        if (multiPolygon != null){
            geometry = multiPolygon.getGeometryN(currentGeometryNumber);
            currentGeometryNumber++;
            firePropertyChange(AppConstants.PROPERTY_CHANGED_NAME, currentGeometryNumber-1, currentGeometryNumber);
        }
        else if (!multiPolygonList.isEmpty() && multiPolygonList != null){
            mGeometry = multiPolygonList.get(currentGeometryNumber);
            currentGeometryNumber++;
            firePropertyChange(AppConstants.PROPERTY_CHANGED_NAME, currentGeometryNumber-1, currentGeometryNumber);
        }
        
        //draw geometry and 
        Graphics2D gr = (Graphics2D) g.create();

        AffineTransform at = new AffineTransform();
        //at.translate(100, 400);
        
        at.translate(this.getWidth()/2, this.getHeight()/2);
        at.scale(20, -20);
        //at.scale(this.getWidth()/20, -this.getHeight()/20);

        gr.setColor(Color.blue);
        
        if (geometry != null){
            LiteShape lt = new LiteShape(geometry, at, false);
            //correct the position of the shape to be at center and update transform in shape
            //at.translate(-lt.getBounds().width/2, -lt.getBounds().height/2);
            //lt = new LiteShape(geometry, at, false);
            gr.fill(lt);
            gr.draw(lt);
            
        }
        else if (mGeometry != null){
            LiteShape lt = new LiteShape(mGeometry, at, false);
            //at.translate(-lt.getBounds().width/2, -lt.getBounds().height/2);
            //correct the position of the shape to be at center and update transform in shape
            //lt = new LiteShape(mGeometry, at, false);
            //gr.fill(new LiteShape(mGeometry, at, false));
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
}
