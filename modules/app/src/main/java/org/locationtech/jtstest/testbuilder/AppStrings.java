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

import jni_st_mesh.ChartType;
import org.locationtech.jtstest.testbuilder.morphing.MorphingMethod;
import jni_st_mesh.Ststistics;
import jni_st_mesh.TriangulationMethod;

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
    
    public static final String MORPHING_BTN_STRING = "Morph Geometry";
    
    //names of the methods in the c++ library
    public static final String AT_INSTANT_METHOD_STRING = "At instant";
    public static final String DURING_PERIOD_METHOD_STRING = "During period";
    
    public static final String MESH_STRING = "Mesh";
    public static final String POLY_STRING = "Polygon";
    public static final String AREA_STRING = "Area";
    public static final String QUALITY_METRICS_STRING = "Quality Metrics";
    
    //for the name of the rows on the quality metrics table
    public static final String QUALITY_METRICS_TABLE_STRING = "Metric";
    public static final String QUALITY_METRICS_RESULTS_STRING = "Result";
    
    //colinear threshold label
    public static final String COLINEAR_THRESHOLD_STRING = "Colinear Threshold: ";
    
    public static final String TRIANGULATION_LABEL_STRING = "Triangulation method: ";
    
    public static final String VERTICE_ORIENTATION_LABEL_STRING = "Vertice Orientation: ";
    
    public static final String METHOD_SELECTION_LABEL_STRING = "Morphing Method Selection: ";
    public static final String NUM_SAMPLES_LABEL = "Number of Samples ";
    
    public static final String STARTER_GEOM_LABEL = "Source: ";
    
    public static final String END_GEOM_LABEL = "Target: ";
    
    //vertice orientation
    public static final String CLOCK_WISE_STRING = "clock wise (cw)";
    public static final String COUNTER_CLOCK_WISE_STRING = "counter-clock wise (ccw)";
    
    //options for the combo box for the selection of the method to call in the c++ library
    public static final String[] INSTANT_OR_PERIOD_STRINGS = {AT_INSTANT_METHOD_STRING, DURING_PERIOD_METHOD_STRING};
    public static final String[] MESH_OR_POLY_STRINGS = {POLY_STRING, MESH_STRING};
    public static final String[] METRICS_STRINGS = {Ststistics.AREA_EVOLUTION.toString(), Ststistics.ROTATION_ANGLES.toString(),
                                Ststistics.COLLINEAR_POINTS_BY_METHOD.toString(), Ststistics.QUALITY_MEASURES.toString()};
    public static final String[] TRIANGULATION_METHOD_STRINGS = {TriangulationMethod.COMPATIBLE.toString(), TriangulationMethod.EQUILATERAL.toString()};
    public static final String[] VERTICE_ORIENTATION_STRINGS = {CLOCK_WISE_STRING, COUNTER_CLOCK_WISE_STRING};
    
    public static final String[] CHART_TYPE_STRINGS = {ChartType.BAR_CHART.getValue(), ChartType.LINE_CHART.getValue(), ChartType.TABLE.getValue()};
    
    public static final String[] MORPHING_METHODS = {MorphingMethod.NORMAL_METHOD.toString(), MorphingMethod.MCKERNEY_METHOD.toString()};
    
    public static final String CHART_TYPE_LABEL_STRING = "Chart type:";
    
    public static final String INSTANT_LABEL_STRING = "Instant";
    
    public static final String BEGIN_END_LABEL_STRING = "Begin and End Time";
    
    public static final String GEOMETRY_TYPE_LABEL_STRING = "Geometry type:";
    
    public static final String TIME_LABEL_STRING = "Instant or Interval:";
    
    public static final String STATISTIC_LABEL_STRING = "Statistics:";
    
    public static final String PLAY_STRING = "Play";
    
    public static final String PAUSE_STRING = "Pause";
    
    public static final String SAVE_CURRENT_GEOMETRY_STRING = "Save current geometry as image";
    
    public static final String SHOW_STATISTIC_STRING = "Show statistic";
    
    public static final String SAVE_ANIMATION_STRING = "Save Animation as images";
    
    public static final String SAVE_CURRENT_STATISTICS_STRING = "Save shown statistics as image";
    
    public static final String EXPORT_QUALITY_MEASURES_STRING = "Export quality measures";
    
    public static final String MORPHING_PANEL_TITLE = "Morphing Animation and Statistics";
    
    //the message error that shows if a morphing operation fails
    public static final String MORPHING_ERR_STRING = "ERR";
    //the name of the java library with the C++ methods for the morphing of a geometry
    public static final String DLL_LIBRARY = "java_mesh";
    
    public static final String SAVE_SET_IMAGES_CHOOSER_DIALOG = "Select directory and name of the folder to save images";
    
    public static final String NO_FILE_SELECTED_ERROR = "No folder selected";
    
    public static final String NO_FILE_SELECTED_SET_IMAGE_SAVE = "Please, select a directory and folder name to save the images.";
    
    
}
