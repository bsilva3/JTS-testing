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

    public CostumBasicStyle(Color lineColor) {
      this.lineColor = lineColor;
      this.fillColor = new Color(255, 200, 200, 0);//transparent
    }

    public CostumBasicStyle() {
    }

    public void paint(Geometry geom, Viewport viewport, Graphics2D g)
    {
        GeometryPainter.paintCostum(geom, viewport, g, lineColor, fillColor);
    }

    public Color getLineColor() {
      return lineColor;
    }

    public Color getFillColor() {
      return fillColor;
    }

}
