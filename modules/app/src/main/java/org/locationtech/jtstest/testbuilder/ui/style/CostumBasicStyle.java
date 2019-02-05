/*
 * this is a style with a transparent color as filling, and an image as background
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
    private boolean isSecondPanel;

    public CostumBasicStyle(Color lineColor, boolean isSecondPanel) {
      this.lineColor = lineColor;
      this.fillColor = new Color(255, 200, 200, 0);//transparent
      this.isSecondPanel = isSecondPanel;
    }

    public CostumBasicStyle() {
    }

    public void paint(Geometry geom, Viewport viewport, Graphics2D g)
    {
        GeometryPainter.paintCostum(geom, viewport, g, lineColor, fillColor, isSecondPanel);
    }

    public Color getLineColor() {
      return lineColor;
    }

    public Color getFillColor() {
      return fillColor;
    }

    public boolean isIsSecondPanel() {
        return isSecondPanel;
    }
    

}
