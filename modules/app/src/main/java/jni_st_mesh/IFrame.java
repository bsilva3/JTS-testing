package jni_st_mesh;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.geom.AffineTransform;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JPanel;
import javax.swing.Timer;
import org.geotools.geometry.jts.LiteShape;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryCollection;
import org.locationtech.jts.geom.MultiPolygon;
import org.locationtech.jts.geom.Polygon;
import org.locationtech.jts.geom.Polygonal;

public class IFrame extends JPanel 
{

    private static final long serialVersionUID = 1L;

    private int geom = 0;
    private int N = 0;
    private MultiPolygon multiPolygon = null;
    private List<MultiPolygon> multiPolygonList;
    Timer timer = null;

    public IFrame(MultiPolygon m_polygon) 
    {
        
        multiPolygon = m_polygon;
        N = multiPolygon.getNumGeometries();

        super.setBackground(Color.white);

        timer = new Timer(16, new ActionListener() {
        @Override
        public void actionPerformed(ActionEvent e) {
            repaint();
        }
        });

        timer.start();
    }
    
     public IFrame(List<MultiPolygon> mPolygonList){
        
        multiPolygonList = mPolygonList;
        N = multiPolygonList.size();

        super.setBackground(Color.white);

        timer = new Timer(10, new ActionListener() {
        @Override
        public void actionPerformed(ActionEvent e) {
            repaint();
        }
        });

        timer.start();
    }

    @Override
    public Dimension getPreferredSize() {
        return new Dimension(800, 600);
    }

    @Override
    protected void paintComponent(Graphics g) 
    {
        super.paintComponent(g);

        Geometry geometry = null;
        MultiPolygon mGeometry = null;
        if (multiPolygon != null){
            geometry = multiPolygon.getGeometryN(geom);
            geom++;
        }
        else if (!multiPolygonList.isEmpty() && multiPolygonList != null){
            mGeometry = multiPolygonList.get(geom);
            geom++;
        }
        Graphics2D gr = (Graphics2D) g.create();

        AffineTransform at = new AffineTransform();
        at.translate(100, 400);
        at.scale(20, -20);

        gr.setColor(Color.blue);
        
        if (geometry != null){
            gr.fill(new LiteShape(geometry, at, false));
            gr.draw(new LiteShape(geometry, at, false));     
        }
        else if (mGeometry != null){
            //gr.fill(new LiteShape(mGeometry, at, false));
            gr.draw(new LiteShape(mGeometry, at, false));     
        }
        gr.dispose();

        if(geom >= N) {
            timer.stop();
            return;    	
        }
    }
}