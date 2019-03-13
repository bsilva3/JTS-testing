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

package org.locationtech.jtstest.testbuilder;

public class AppStrings {
    
    public static final String LABEL_TEST_CASE = "Case";
    
    public static final String GEOM_LABEL_A = "A";
    public static final String GEOM_LABEL_B = "B";
    
    public static final String TAB_LABEL_LOG = "Log";
    public static final String TAB_LABEL_VALUE = "Value";
    static final String TAB_LABEL_RESULT = "Result";
    static final String TAB_LABEL_INSPECT = "Inspect";
    static final String TAB_LABEL_INPUT = "Input";
    static final String TAB_LABEL_LAYERS = "Layers";
    static final String TAB_LABEL_STATS = "Stats";
    static final String TAB_LABEL_CASES = "Cases";
    
    public static final String TIP_TEXT_ENTRY = "Enter WKT, WKB GeoJSON, or GML, or drag-n-drop a WKT, WKB, GeoJSON, GML or SHP file";
    public static final String TIP_WKT_PANEL_LOAD_GEOMETRY = "Load geometries";
    public static final String TIP_INSPECT_GEOMETRY = "Inspect Geometry";
    
    static final String TIP_EXTRACT_COMPONENTS = "Extract Components to Case";
    
    static final String TIP_DELETE_VERTEX_COMPONENT = "Delete Vertices or Components";
    
    static final String TIP_MOVE_VERTEX = "<html>Move/Add/Delete Vertex<br><br>Move = Left-Btn<br>Add = Right-Btn<br>Delete = Ctl-Right-Btn</html>";
    
    static final String TIP_PAN = "Pan";
    static final String TIP_ZOOM_TO_FULL_EXTENT = "Zoom To Full Extent";
    static final String TIP_ZOOM_TO_RESULT = "Zoom To Result";
    static final String TIP_ZOOM_TO_B = "Zoom To B";
    static final String TIP_ZOOM_TO_A = "Zoom To A";
    static final String TIP_ZOOM_1_1 = "Zoom 1:1";
    static final String TIP_ZOOM = "<html>Zoom In/Out | Pan<br><br>Zoom In = Left-Btn<br>Zoom Extent = Left-Drag<br>Zoom Out = Right-Btn<br>Pan = Right-Drag | Ctl-Drag</html>";
    
    static final String TIP_INFO = "Show Info on Geometry, Segment, or Point";
    
    static final String TIP_DRAW_RECTANGLE = "Draw Rectangle";
    static final String TIP_DRAW_POINT = "Draw Point";
    static final String TIP_DRAW_LINE = "<html>Draw LineString<br><br>Add Pt = Left-Click<br>Stream = Left-Drag</html>";
    static final String TIP_DRAW_POLY = "<html>Draw Polygon<br><br>Add Pt = Left-Click<br>Stream = Left-Drag</html>";
    
    
    static final String TIP_EXCHANGE_A_B = "Exchange A & B";
    
    static final String TIP_CASE_DELETE = "Delete Case";
    static final String TIP_CASE_DUP = "Duplicate Case";
    static final String TIP_CASE_ADD_NEW = "Add New Case";
    
    static final String TIP_NEXT = "<html>Next Case<br><br>No Zoom = Ctl-Click</html>";
    static final String TIP_PREV = "<html>Previous Case<br><br>No Zoom = Ctl-Click</html>";
    
    static final String TIP_PASTE_DATA = "Paste from WKT, WKB, or GML";
    
    static final String TIP_COPY_DATA = "Copy as WKT (Ctl-click for formatted)";
    
    public static final String MORPHING_PANE_TOOLTIP = "Morphing for the geometries shown above";
    
    
    public static final String START_MORPHING_BTN_STRING = "Start Morphing";
    
    //names of the methods in the c++ library
    public static final String AT_INSTANT_METHOD_STRING = "At instant";
    public static final String DURING_PERIOD_METHOD_STRING = "During period";
    
    public static final String MESH_STRING = "Mesh";
    public static final String POLY_STRING = "Polygon";
    public static final String AREA_STRING = "Area";
    
    //options for the combo box for the selection of the method to call in the c++ library
    public static final String[] METHOD_SELECTION_STRINGS = {AT_INSTANT_METHOD_STRING, DURING_PERIOD_METHOD_STRING};
    public static final String[] MESH_OR_POLY_STRINGS = {POLY_STRING, MESH_STRING};
    public static final String[] METRICS_STRINGS = {AREA_STRING};
    
    public static final String INSTANT_LABEL_STRING = "Instant";
    
    public static final String BEGIN_END_LABEL_STRING = "Begin and End Time";
    
    public static final String GEOMETRY_TYPE_LABEL_STRING = "Geometry type:";
    
    public static final String TIME_LABEL_STRING = "Instant or Interval:";
    
    public static final String STATISTIC_LABEL_STRING = "Statistics:";
    
    public static final String PLAY_STRING = "Play";
    
    public static final String PAUSE_STRING = "Pause";
    
    public static final String SAVE_AS_IMAGE_STRING = "Save as image";
    
    public static final String MORPHING_PANEL_TITLE = "Morphing Animation and Statistics";
    
    //the message error that shows if a morphing operation fails
    public static final String MORPHING_ERR_STRING = "ERR";
    //the name of the java library with the C++ methods for the morphing of a geometry
    public static final String DLL_LIBRARY = "java_mesh";
    
}
