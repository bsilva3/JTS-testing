/*
 * Copyright (c) 2016 Vivid Solutions.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * and Eclipse Distribution License v. 1.0 which accompanies this distribution.
 * The Eclipse Public License is available at http://www.eclipse.org/legal/epl-v10.html
 * and the Eclipse Distribution License is available at
 *
 * http://www.eclipse.org/org/documents/edl-v10.php.
 */

package org.locationtech.jtstest.testbuilder.ui.tools;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.event.MouseWheelEvent;
import java.awt.geom.Point2D;

import org.locationtech.jts.awt.FontGlyphReader;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.PrecisionModel;
import org.locationtech.jtstest.*;
import org.locationtech.jtstest.testbuilder.AppConstants;
import org.locationtech.jtstest.testbuilder.GeometryEditPanel;
import org.locationtech.jtstest.testbuilder.JTSTestBuilder;
import org.locationtech.jtstest.testbuilder.JTSTestBuilderFrame;
import org.locationtech.jtstest.testbuilder.model.*;
import org.locationtech.jtstest.testbuilder.ui.Viewport;


public abstract class BasicTool implements Tool
{
  protected Cursor cursor = Cursor.getDefaultCursor();

  private PrecisionModel gridPM;
  private PrecisionModel gridPM2;

  private GeometryEditPanel panel;
  private GeometryEditPanel panel2;
  
  public BasicTool() {
    super();
  }

  public BasicTool(Cursor cursor) {
    super();
    this.cursor = cursor;
  }

  protected Graphics2D getGraphics2D() {
    Graphics2D g = (Graphics2D) getClickedPanel().getGraphics();
    if (g != null) {
      // guard against g == null
      g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
          RenderingHints.VALUE_ANTIALIAS_ON);
    }
    return g;
  }

  public void mouseClicked(MouseEvent e) {}
  public void mousePressed(MouseEvent e) {}
  public void mouseReleased(MouseEvent e) {}
  public void mouseEntered(MouseEvent e) {}
  public void mouseExited(MouseEvent e) {}
  public void mouseDragged(MouseEvent e)   {  }
  public void keyPressed(KeyEvent e)  { }
  public void keyReleased(KeyEvent e)  { }
  public void keyTyped(KeyEvent e)  {  }
  public void mouseMoved(MouseEvent e) {  }
  public void mouseWheelMoved(MouseWheelEvent e) {  }
  
  public Cursor getCursor()
  {
    return cursor;
  }

  /**
   * Called when tool is activated.
   * 
   * If subclasses override this method they must call <tt>super.activate()</tt>.
   */
    public void activate(GeometryEditPanel panel, boolean isSecondPanel) 
    {
        if (isSecondPanel){
            this.panel2 = panel;
            gridPM2 = getViewport2().getGridPrecisionModel();
            this.panel2.setCursor(getCursor());
            this.panel2.addMouseListener(this);
            this.panel2.addMouseMotionListener(this);
            this.panel2.addMouseWheelListener(this);
        }
        else{
            this.panel = panel;
            gridPM = getViewport().getGridPrecisionModel();
            this.panel.setCursor(getCursor());
            this.panel.addMouseListener(this);
            this.panel.addMouseMotionListener(this);
            this.panel.addMouseWheelListener(this);
        }
    }
 
    public void deactivate() 
    {
        this.panel.removeMouseListener(this);
        this.panel.removeMouseMotionListener(this);
        this.panel.removeMouseWheelListener(this);
        
        this.panel2.removeMouseListener(this);
        this.panel2.removeMouseMotionListener(this);
        this.panel2.removeMouseWheelListener(this);
    }

    protected GeometryEditPanel panel()
    {
      // this should probably be passed in during setup
      //return JTSTestBuilderFrame.instance().getTestCasePanel().getGeometryEditPanel();
      return panel;
    }

    protected GeometryEditPanel panel2()
    {
      // this should probably be passed in during setup
      //return JTSTestBuilderFrame.instance().getTestCasePanel().getGeometryEditPanel();
      return panel2;
    }
  
    protected GeometryEditModel geomModel()
    {
        return getClickedPanel().getGeomModel();
    }
  
    private Viewport getViewport()
    {

      return panel().getViewport();
    }

    private Viewport getViewport2()
    {

      return panel2().getViewport();
    }

    Point2D toView(Coordinate modePt)
    {
      return getClickedPanel().getViewport().toView(modePt);
    }

    double toView(double distance)
    {
      return getClickedPanel().getViewport().toView(distance);
    }

    Point2D toModel(java.awt.Point viewPt)
    {
      return getClickedPanel().getViewport().toModel(viewPt);
    }

    Coordinate toModelCoordinate(java.awt.Point viewPt)
    {
      return getClickedPanel().getViewport().toModelCoordinate(viewPt);
    }

    double toModel(double viewDist)
    {
      return viewDist / getClickedPanel().getViewport().getScale();
    }

    double getModelSnapTolerance()
    {
      return toModel(AppConstants.TOLERANCE_PIXELS);
    }

    protected Coordinate toModelSnapped(Point2D p)
    {
          return toModelSnappedIfCloseToViewGrid(p);  
    }

    protected Coordinate toModelSnappedToViewGrid(Point2D p)
    {
        GeometryEditPanel editPanel = getClickedPanel();
        Coordinate pModel = editPanel.getViewport().toModelCoordinate(p);
        if (editPanel.equals(this.panel)){
            gridPM.makePrecise(pModel);
        }
        else if(editPanel.equals(this.panel2)){
            gridPM2.makePrecise(pModel);
        }
        // snap to view grid
        return pModel;
    }

    protected Coordinate toModelSnappedIfCloseToViewGrid(Point2D p)
    {
        GeometryEditPanel editPanel = getClickedPanel();
        // snap to view grid if close to view grid point
        Coordinate pModel = editPanel.getViewport().toModelCoordinate(p);
        Coordinate pSnappedModel = new Coordinate(pModel);
        if (editPanel.equals(this.panel)){
            gridPM.makePrecise(pSnappedModel);
        }
        else if(editPanel.equals(this.panel2)){
            gridPM2.makePrecise(pSnappedModel);
        }
        
        double tol = getModelSnapTolerance();
        if (pModel.distance(pSnappedModel) <= tol)
                return pSnappedModel;
        return pModel;
    }
  
    protected double gridSize()
    {
      return getClickedPanel().getViewport().getGridSizeModel();
    }
  
  /*
  protected Coordinate toModelSnappedToDrawingGrid(Point2D p)
  {
    Point2D pt = panel().snapToGrid(getViewport().toModel(p));
    return new Coordinate(pt.getX(), pt.getY());
  }
  */
  
    public static GeometryEditPanel getClickedPanel(){
        return JTSTestBuilderFrame.getGeometryEditPanelMouseIsIn();
    }
}
