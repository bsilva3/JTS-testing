package jni_st_mesh;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.geom.AffineTransform;
import javax.swing.JPanel;
import javax.swing.Timer;
import org.geotools.geometry.jts.LiteShape;
import org.locationtech.jts.geom.MultiPolygon;
import org.locationtech.jts.geom.Polygon;

public class IFrame extends JPanel 
{

    private static final long serialVersionUID = 1L;

    private int geom = 0;
    private int N = 0;
    private MultiPolygon col = null;
    Timer timer = null;

    public IFrame(MultiPolygon m_polygon) 
    {
        col = m_polygon;
        N = col.getNumGeometries();

        super.setBackground(Color.white);

        timer = new Timer(16, new ActionListener() {
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

        Polygon p = (Polygon) col.getGeometryN(geom);
        geom++;

        Graphics2D gr = (Graphics2D) g.create();

        AffineTransform at = new AffineTransform();
        at.translate(100, 400);
        at.scale(20, -20);

        gr.setColor(Color.blue);
        gr.fill(new LiteShape(p, at, false));
        gr.draw(new LiteShape(p, at, false));     

        gr.dispose();

        if(geom >= N) {
            timer.stop();
            return;    	
        }
    }
}