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
import java.awt.geom.*;
import java.awt.event.MouseEvent;

import javax.swing.SwingUtilities;

import org.locationtech.jts.awt.GeometryCollectionShape;
import org.locationtech.jts.geom.*;
import org.locationtech.jtstest.testbuilder.AppCorrGeometries;
import org.locationtech.jtstest.testbuilder.AppCursors;
import org.locationtech.jtstest.testbuilder.GeometryEditPanel;
import org.locationtech.jtstest.testbuilder.IconLoader;
import org.locationtech.jtstest.testbuilder.JTSTestBuilderFrame;
import org.locationtech.jtstest.testbuilder.geom.*;
import org.locationtech.jtstest.testbuilder.model.GeometryEditModel;


/**
 * @version 1.7
 */
public class EditVertexTool 
extends IndicatorTool 
{
  private static EditVertexTool instance = null;

  //Point2D currentIndicatorLoc = null;
  Coordinate currentVertexLoc = null;
  
  private Coordinate selectedVertexLocation = null;
  private Coordinate[] adjVertices = null;

  public static EditVertexTool getInstance() {
    if (instance == null)
      instance = new EditVertexTool();
    return instance;
  }

  private EditVertexTool() {
    super(AppCursors.EDIT_VERTEX);
  }

  public void mousePressed(MouseEvent e) {
  	currentVertexLoc = null;
    if (SwingUtilities.isRightMouseButton(e))
      return;
    
    // initiate moving a vertex
    Coordinate mousePtModel = toModelCoordinate(e.getPoint());
    double tolModel = getModelSnapTolerance();
    GeometryEditPanel editPanel = getClickedPanel();
    selectedVertexLocation = editPanel.getGeomModel().locateVertexPt(mousePtModel, tolModel);
    if (selectedVertexLocation != null) {
      adjVertices = geomModel().findAdjacentVertices(selectedVertexLocation);
      currentVertexLoc = selectedVertexLocation;
      //indicate that there is a coordinate that is being edited, that may or may not be from the corr geometry
      AppCorrGeometries.getInstance().savePointIfExistInCorrGeometry(selectedVertexLocation, editPanel.isSecondPanel());
      redrawIndicator();
    }
  }

  public void mouseReleased(MouseEvent e) {
    if (SwingUtilities.isRightMouseButton(e))
      return;
    
    clearIndicator();
    // finish the move of the vertex
    if (selectedVertexLocation != null) {
      Coordinate newLoc = toModelSnapped(e.getPoint());
      GeometryEditPanel editPanel = getClickedPanel();
      editPanel.getGeomModel().moveVertex(selectedVertexLocation, newLoc);
      //update the coordinates if the moved vertex belonged to a corr Geometry
      AppCorrGeometries.getInstance().editPointIfExistInCorrGeometry(newLoc.getX(), newLoc.getY(), editPanel.isSecondPanel());
    }
  }

  public void mouseDragged(MouseEvent e) {
  	currentVertexLoc = toModelSnapped(e.getPoint());
    if (selectedVertexLocation != null)
      redrawIndicator();
  }

  public void mouseClicked(MouseEvent e) {
    if (! SwingUtilities.isRightMouseButton(e))
      return;
    GeometryEditPanel editPanelMouseIn = JTSTestBuilderFrame.getGeometryEditPanelMouseIsIn();
    GeometryEditModel geoModel = editPanelMouseIn.getGeomModel();
    Coordinate mousePtModel = toModelCoordinate(e.getPoint());
    double tolModel = getModelSnapTolerance();

    boolean isMove = ! e.isControlDown();
    if (isMove) { //insert vertex
        GeometryLocation geomLoc = geoModel.locateNonVertexPoint(mousePtModel, tolModel);
        if (geomLoc != null) {
            //add the coordinate in to the list and get the corresponding coordinate to draw in the other panel
            Coordinate correspondingCoord = AppCorrGeometries.getInstance().addPointToCorrGeometries(geomLoc, editPanelMouseIn.isSecondPanel());
            geoModel.setGeometry(geomLoc.insert());
            if(correspondingCoord != null){
                GeometryEditPanel editPanelMouseNotIn = JTSTestBuilderFrame.getOtherGeometryEditPanel(editPanelMouseIn);
                GeometryLocation geomLocOtherPanel = editPanelMouseNotIn.getGeomModel().locateNonVertexPoint(correspondingCoord, 0);
                editPanelMouseNotIn.getGeomModel().setGeometry(AppCorrGeometries.getInstance().getPanelCorrGeometry(editPanelMouseNotIn.isSecondPanel()));
            }
        }
    }
    else {  // is a delete
      GeometryLocation geomLoc = geoModel.locateVertex(mousePtModel, tolModel);
      //System.out.println("Testing: delete vertex at " + geomLoc);
      if (geomLoc != null) {
          AppCorrGeometries.getInstance().deletePointInBothCorrGeometries(geomLoc.getCoordinate());
          geoModel.setGeometry(geomLoc.delete());
      }
    }
  }

  protected Shape getShape() 
  {
  	GeometryCollectionShape ind = new GeometryCollectionShape();
  	Point2D currentIndicatorLoc = toView(currentVertexLoc);
  	ind.add(getIndicatorCircle(currentIndicatorLoc));
  	if (adjVertices != null) {
            for (int i = 0; i < adjVertices.length; i++) {
                GeneralPath line = new GeneralPath();
                line.moveTo((float) currentIndicatorLoc.getX(), (float) currentIndicatorLoc.getY());
                Point2D pt = toView(adjVertices[i]);
                line.lineTo((float) pt.getX(), (float) pt.getY());
                ind.add(line);
            }
  	}
  	return ind;
  	
//    return getIndicatorCircle(currentIndicatorLoc);
  }

  private static final double IND_CIRCLE_RADIUS = 10.0;

  protected Shape getIndicatorCircle(Point2D p) {
    return new Ellipse2D.Double(p.getX() - (IND_CIRCLE_RADIUS / 2), p.getY()
        - (IND_CIRCLE_RADIUS / 2), IND_CIRCLE_RADIUS, IND_CIRCLE_RADIUS);
  }

}
