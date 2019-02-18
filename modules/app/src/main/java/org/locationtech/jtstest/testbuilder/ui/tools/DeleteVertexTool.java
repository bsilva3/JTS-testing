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

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.Envelope;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jtstest.testbuilder.AppCorrGeometries;
import org.locationtech.jtstest.testbuilder.GeometryEditPanel;
import org.locationtech.jtstest.testbuilder.JTSTestBuilderFrame;
import org.locationtech.jtstest.testbuilder.geom.GeometryBoxDeleter;


/**
 * Deletes vertices within a selection box from a geometry component
 * @version 1.7
 */
public class DeleteVertexTool extends BoxBandTool {
  private static DeleteVertexTool singleton = null;

  public static DeleteVertexTool getInstance() {
    if (singleton == null)
      singleton = new DeleteVertexTool();
    return singleton;
  }

  private DeleteVertexTool() {
    super();
  }

  protected void gestureFinished() 
  {      
    Envelope env = getBox().getEnvelopeInternal();
    Geometry g = geomModel().getGeometry();
    Geometry edit = GeometryBoxDeleter.delete(g, env);
    
    //get list of removed coordinates
    List<Coordinate> removedCoords = getRemovedCoords(g.getCoordinates(), edit.getCoordinates());
    
    GeometryEditPanel editPanel = getClickedPanel();
    Coordinate[] removedCoordsOtherPanel = AppCorrGeometries.getInstance().deleteListOfPointsInBothCorrGeometries(removedCoords, editPanel.isSecondPanel());
    
    //update the geometry in the interacted panel with the removed coords
    editPanel.getGeomModel().setGeometry(edit);
    
    //draw the other geometry in the other panel with the corresponding coordinates now deleted
    GeometryFactory fact = new GeometryFactory();
    Geometry otherPanelGeomAfterDeletion = fact.createPolygon(removedCoordsOtherPanel);
    JTSTestBuilderFrame.getOtherGeometryEditPanel(editPanel).getGeomModel().setGeometry(otherPanelGeomAfterDeletion);
    //JTSTestBuilderFrame.instance().reloadBothPanels();
  }
  
    //returns a list of coordinates removed by the user
    private List<Coordinate> getRemovedCoords(Coordinate[] coordsBeforeDelete, Coordinate[] coordsAfterDelete){
        List<Coordinate> coordsBeforeDeleteLinked = new LinkedList<>(Arrays.asList(coordsBeforeDelete));
        List<Coordinate> coordsAfterDeleteLinked = new LinkedList<>(Arrays.asList(coordsAfterDelete));
        //return the diference between the 2 lists, i.e., the removed coordinates
        coordsBeforeDeleteLinked.removeAll(coordsAfterDeleteLinked);
        return coordsBeforeDeleteLinked;
    }


}
