/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder.ui.style;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics2D;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jtstest.testbuilder.AppImage;
import org.locationtech.jtstest.testbuilder.ui.Viewport;
import org.locationtech.jtstest.testbuilder.ui.render.GeometryPainter;

/**
 *
 * @author Bruno Silva
 */
public class CostumBasicStyle extends BasicStyle{
    private Color lineColor;
    private Color fillColor;

    public CostumBasicStyle(Color lineColor) {
      this.lineColor = lineColor;
      this.fillColor = new Color(255, 200, 200, 150);//transparent
    }

    public CostumBasicStyle() {

    }

    public void paint(Geometry geom, Viewport viewport, Graphics2D g)
    {
        //g.translate(0, viewport.getLowerLeftCornerInModel().getY());
        //g.drawImage(AppImage.getBackgroundImage(), 0, 0, AppImage.getImageWidthInPanel(), AppImage.getImageHeightInPanel(), null);
        //g.drawImage(AppImage.getBackgroundImage(), 0, 0, AppImage.getImageWidthInPanel(), AppImage.getImageHeightInPanel(), null);
        GeometryPainter.paintCostum(geom, viewport, g, lineColor, fillColor);
        /*AppImage.keepAspectRatioAndDrawImage(g, new Dimension((int) Math.round(viewport.getWidthInView()), 
                (int) Math.round(viewport.getWidthInView())));*/
        
    }

    public Color getLineColor() {
      return lineColor;
    }

    public Color getFillColor() {
      return fillColor;
    }

}
