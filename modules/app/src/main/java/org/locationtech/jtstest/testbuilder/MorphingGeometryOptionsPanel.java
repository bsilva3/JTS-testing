package org.locationtech.jtstest.testbuilder;

import java.awt.GridBagConstraints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.SpinnerNumberModel;
import jni_st_mesh.Main;
import jni_st_mesh.TriangulationMethod;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.MultiPolygon;
import org.locationtech.jts.geom.Polygon;
import org.locationtech.jts.io.ParseException;
import org.locationtech.jts.io.WKTReader;
import org.locationtech.jtstest.testbuilder.morphing.Morphing;
import org.locationtech.jtstest.testbuilder.morphing.MorphingMethod;

/**
 *
 * @author Bruno Silva
 */
public class MorphingGeometryOptionsPanel extends javax.swing.JPanel {
     
    /**
     * Creates new form MorphingGeometryOptionsPanel
     */
    
    private String mesh1 = "MULTIPOLYGON (((924 618.5, 925.0000000596046 604.9166668355465, 928 597, 924 618.5)), ((925.0000000596046 604.9166668355465, 926.0000001192093 591.333333671093, 928 597, 925.0000000596046 604.9166668355465)), ((924.0000000596046 585.6666668355465, 926.0000001192093 591.333333671093, 925.0000000596046 604.9166668355465, 924.0000000596046 585.6666668355465)), ((914 583, 922 580, 924.0000000596046 585.6666668355465, 914 583)), ((924 618.5, 924.0000000298023 602.0833334177732, 925.0000000596046 604.9166668355465, 924 618.5)), ((924.0000000298023 602.0833334177732, 924.0000000596046 585.6666668355465, 925.0000000596046 604.9166668355465, 924.0000000298023 602.0833334177732)), ((913.3454177996489 583.9879156479267, 914 583, 924.0000000596046 585.6666668355465, 913.3454177996489 583.9879156479267)), ((909 576, 914 583, 913.3454177996489 583.9879156479267, 909 576)), ((946 640, 990 655, 963.6666669249535 647.5, 946 640)), ((937.3333338499069 640, 946 640, 959.3333334624767 647.5, 937.3333338499069 640)), ((928.6666669249535 640, 937.3333338499069 640, 959.3333334624767 647.5, 928.6666669249535 640)), ((913.3454177996489 583.9879156479267, 924.0000000298023 602.0833334177732, 893.1999313191997 574.3000686808003, 913.3454177996489 583.9879156479267)), ((959.3333334624767 647.5, 963.6666669249535 647.5, 990 655, 959.3333334624767 647.5)), ((946 640, 963.6666669249535 647.5, 959.3333334624767 647.5, 946 640)), ((909 576, 913.3454177996489 583.9879156479267, 893.1999313191997 574.3000686808003, 909 576)), ((955 647.5, 959.3333334624767 647.5, 949 781, 955 647.5)), ((928.6666669249535 640, 959.3333334624767 647.5, 955 647.5, 928.6666669249535 640)), ((920 640, 928.6666669249535 640, 955 647.5, 920 640)), ((810 642, 881 555, 886.5 563.5, 810 642)), ((892 572, 909 576, 893.1999313191997 574.3000686808003, 892 572)), ((886.5 563.5, 892 572, 893.1999313191997 574.3000686808003, 886.5 563.5)), ((804 736, 810 642, 955 647.5, 804 736)), ((823 766, 949 781, 926 812, 823 766)), ((949 781, 959.3333334624767 647.5, 990 655, 949 781)), ((810 642, 886.5 563.5, 893.1999313191997 574.3000686808003, 810 642)), ((823 766, 955 647.5, 949 781, 823 766)), ((804 736, 955 647.5, 823 766, 804 736)), ((810 642, 893.1999313191997 574.3000686808003, 920 640, 810 642)), ((810 642, 920 640, 955 647.5, 810 642)), ((893.1999313191997 574.3000686808003, 924.0000000298023 602.0833334177732, 920 640, 893.1999313191997 574.3000686808003)), ((913.3454177996489 583.9879156479267, 924.0000000596046 585.6666668355465, 924.0000000298023 602.0833334177732, 913.3454177996489 583.9879156479267)), ((920 640, 924.0000000298023 602.0833334177732, 924 618.5, 920 640)))";
    private String mesh2 = "MULTIPOLYGON (((926 812, 949 781, 964.346 816.418, 926 812)), ((823 766, 926 812, 834.664 878.198, 823 766)), ((804 736, 823 766, 787.52 767.454, 804 736)), ((810 642, 804 736, 725.596 683.804, 810 642)), ((881 555, 810 642, 770.158 537.014, 881 555)), ((886.5 563.5, 881 555, 891.111 554.487, 886.5 563.5)), ((892 572, 886.5 563.5, 896.611 562.987, 892 572)), ((909 576, 892 572, 903.964 559.278, 909 576)), ((914 583, 909 576, 917.562 575.17, 914 583)), ((922 580, 914 583, 915.402 574.572, 922 580)), ((924.0000000596046 585.6666668355465, 922 580, 927.9073335093856 581.1013333661556, 924.0000000596046 585.6666668355465)), ((926.0000001192093 591.333333671093, 924.0000000596046 585.6666668355465, 929.9073335689902 586.7680002017021, 926.0000001192093 591.333333671093)), ((928 597, 926.0000001192093 591.333333671093, 931.9073331004381 592.4346669387818, 928 597)), ((924 618.5, 928 597, 944.619 611.214, 924 618.5)), ((920 640, 924 618.5, 940.619 632.714, 920 640)), ((928.6666669249535 640, 920 640, 924.3333334624767 632.4946664429903, 928.6666669249535 640)), ((937.3333338499069 640, 928.6666669249535 640, 933.0000003874302 632.4946664429903, 937.3333338499069 640)), ((946 640, 937.3333338499069 640, 941.6666669249535 632.4946671140194, 946 640)), ((990 655, 946 640, 980.99 609.396, 990 655)), ((949 781, 990 655, 1078.616 753.506, 949 781)))";
    
    public MorphingGeometryOptionsPanel() {
        initComponents();

        //set text for labels
        this.playBtn.setText(AppStrings.START_MORPHING_BTN_STRING);
        this.timeLabel.setText(AppStrings.INSTANT_LABEL_STRING);
        this.meshOrPolygonLabel.setText(AppStrings.GEOMETRY_TYPE_LABEL_STRING);
        this.timeOrInstantLabel.setText(AppStrings.TIME_LABEL_STRING);
        this.colinearThresholdLabel.setText(AppStrings.COLINEAR_THRESHOLD_STRING);
        this.triangulationLabel.setText(AppStrings.TRIANGULATION_LABEL_STRING);
        this.orientationLabel.setText(AppStrings.VERTICE_ORIENTATION_LABEL_STRING);
        this.methodSelection.setText(AppStrings.METHOD_SELECTION_LABEL_STRING);
        
        this.initialTimeSpinner.setModel(new SpinnerNumberModel(1000, 1000, 2000, 10));//set default, min max and increment value
        this.endTimeSpinner.setModel(new SpinnerNumberModel(2000, 1000, 2000, 10));//set default, min max and increment value
        this.remove(endTimeSpinner); //initially hidden
        
        this.colinearThresholdSpinner.setModel(new SpinnerNumberModel(0.5, 0, 1, 0.1));
        
        //start the showMorphedGeometry in panel checkbox deactivated
        showMorphedGeometryCheckBox.setEnabled(false);
        //add listener for checkbox (to show or hide the result of the morphing of the geometry in the panel)
        showMorphedGeometryCheckBox.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {
                if(e.getStateChange() == ItemEvent.SELECTED) {//checkbox has been selected
                    //show in the panel the result of the morphing
                    AppCorrGeometries.getInstance().showMorphingGeometryInPanel();
                } else {//checkbox has been deselected
                    //remove from the panel the result of the morphing and show the normal geometry
                    AppCorrGeometries.getInstance().hideMorphingGeometryInPanel();
                };
            }
        });
        
        //set the text for the combo boxes
        this.instantOrPeriodComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.INSTANT_OR_PERIOD_STRINGS));
        this.meshOrPolygonComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.MESH_OR_POLY_STRINGS));
        this.triangulationMethodComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.TRIANGULATION_METHOD_STRINGS));
        this.verticeOrientationComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.VERTICE_ORIENTATION_STRINGS));
        this.methodSelectionComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.MORPHING_METHODS));
        this.instantOrPeriodComboBox.addActionListener (new ActionListener () {
            public void actionPerformed(ActionEvent e) {
                //if user wants to get the morphing at an instant, hide the spinner for the end time
                if(instantOrPeriodComboBox.getSelectedItem().toString().equals(AppStrings.AT_INSTANT_METHOD_STRING)){
                    timeLabel.setText(AppStrings.INSTANT_LABEL_STRING);
                    remove(endTimeSpinner);
                }
                else{
                    //if user wants the morphing for period of time show the end time spinner in order for him to select the end period
                    timeLabel.setText(AppStrings.DURING_PERIOD_METHOD_STRING);
                    //add the spinner for end period
                    GridBagConstraints gridBagConstraints = new java.awt.GridBagConstraints();
                    gridBagConstraints.gridx = 2;
                    gridBagConstraints.gridy = 1;
                    gridBagConstraints.weightx = 1.0;
                    gridBagConstraints.weighty = 1.0;
                    add(endTimeSpinner, gridBagConstraints);
                }
            }
        });
    }
    
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {
        java.awt.GridBagConstraints gridBagConstraints;

        playBtn = new javax.swing.JButton();
        timeLabel = new javax.swing.JLabel();
        filler2 = new javax.swing.Box.Filler(new java.awt.Dimension(0, 20), new java.awt.Dimension(0, 20), new java.awt.Dimension(32767, 20));
        resultLabel = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        resultTextArea = new javax.swing.JTextArea();
        showMorphedGeometryCheckBox = new java.awt.Checkbox();
        instantOrPeriodComboBox = new javax.swing.JComboBox<>();
        meshOrPolygonComboBox = new javax.swing.JComboBox<>();
        initialTimeSpinner = new javax.swing.JSpinner();
        endTimeSpinner = new javax.swing.JSpinner();
        meshOrPolygonLabel = new javax.swing.JLabel();
        timeOrInstantLabel = new javax.swing.JLabel();
        triangulationMethodComboBox = new javax.swing.JComboBox<>();
        colinearThresholdLabel = new javax.swing.JLabel();
        colinearThresholdSpinner = new javax.swing.JSpinner();
        verticeOrientationComboBox = new javax.swing.JComboBox<>();
        orientationLabel = new javax.swing.JLabel();
        triangulationLabel = new javax.swing.JLabel();
        methodSelection = new javax.swing.JLabel();
        methodSelectionComboBox = new javax.swing.JComboBox<>();

        setFocusTraversalPolicyProvider(true);
        setLayout(new java.awt.GridBagLayout());

        playBtn.setText("Play");
        playBtn.addInputMethodListener(new java.awt.event.InputMethodListener() {
            public void caretPositionChanged(java.awt.event.InputMethodEvent evt) {
                playBtnCaretPositionChanged(evt);
            }
            public void inputMethodTextChanged(java.awt.event.InputMethodEvent evt) {
            }
        });
        playBtn.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                startMorphing(evt);
            }
        });
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.gridy = 6;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        add(playBtn, gridBagConstraints);

        timeLabel.setText("time");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 0, 0, 10);
        add(timeLabel, gridBagConstraints);
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 2;
        gridBagConstraints.gridy = 1;
        add(filler2, gridBagConstraints);

        resultLabel.setText("result");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 0, 0, 10);
        add(resultLabel, gridBagConstraints);

        resultTextArea.setColumns(40);
        resultTextArea.setRows(10);
        resultTextArea.setTabSize(4);
        resultTextArea.setToolTipText("");
        resultTextArea.setWrapStyleWord(true);
        resultTextArea.setCursor(new java.awt.Cursor(java.awt.Cursor.TEXT_CURSOR));
        jScrollPane1.setViewportView(resultTextArea);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.gridy = 3;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.gridheight = 3;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        gridBagConstraints.weightx = 4.0;
        gridBagConstraints.weighty = 2.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 0, 9, 0);
        add(jScrollPane1, gridBagConstraints);

        showMorphedGeometryCheckBox.setLabel("show Morphing Geometry");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 6;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 0, 0, 10);
        add(showMorphedGeometryCheckBox, gridBagConstraints);

        instantOrPeriodComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 4;
        gridBagConstraints.gridy = 3;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 10);
        add(instantOrPeriodComboBox, gridBagConstraints);

        meshOrPolygonComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 4;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 10);
        add(meshOrPolygonComboBox, gridBagConstraints);
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        add(initialTimeSpinner, gridBagConstraints);
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 2;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        add(endTimeSpinner, gridBagConstraints);

        meshOrPolygonLabel.setText("jLabel1");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 0);
        add(meshOrPolygonLabel, gridBagConstraints);

        timeOrInstantLabel.setText("jLabel2");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 3;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 0);
        add(timeOrInstantLabel, gridBagConstraints);

        triangulationMethodComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 6;
        gridBagConstraints.gridy = 3;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 10);
        add(triangulationMethodComboBox, gridBagConstraints);

        colinearThresholdLabel.setText("jLabel1");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 4;
        gridBagConstraints.gridy = 5;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 0);
        add(colinearThresholdLabel, gridBagConstraints);
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 5;
        gridBagConstraints.gridy = 5;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        add(colinearThresholdSpinner, gridBagConstraints);

        verticeOrientationComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 6;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 10);
        add(verticeOrientationComboBox, gridBagConstraints);

        orientationLabel.setText("jLabel1");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 5;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 0);
        add(orientationLabel, gridBagConstraints);

        triangulationLabel.setText("jLabel2");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 5;
        gridBagConstraints.gridy = 3;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 0);
        add(triangulationLabel, gridBagConstraints);

        methodSelection.setText("jLabel1");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        add(methodSelection, gridBagConstraints);

        methodSelectionComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 5;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        add(methodSelectionComboBox, gridBagConstraints);
    }// </editor-fold>//GEN-END:initComponents

    /** Calls the c++ library that, given a time interval, a previous geometry and a target geometry,
    * predict the morphing of the geometry in a given time having these two geometries as a reference.
    */
    private void startMorphing(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_startMorphing
        // get wkt of the corr geometries in both panels.
        String[] wkts;//first element is source, second is target geometry
        wkts = AppCorrGeometries.getInstance().getWKTextFromGeometriesInPanels();
        /*System.out.println("wkt 1st geometry: "+wkts[0]);
        System.out.println("wkt 2nd geometry: "+wkts[1]);*/
                
        String[] result = new String[1];
        
        //load c++ libraries
        System.loadLibrary(AppStrings.DLL_LIBRARY);
        Main m = new Main();
        
        //find which method to call:
        String selectedTime = this.instantOrPeriodComboBox.getSelectedItem().toString();
        String selectedGeomType = this.meshOrPolygonComboBox.getSelectedItem().toString();
        boolean duringPeriod = false;
        boolean isPolygon = false;
        //"POLYGON((0 0, 0 8, 2 8, 2 2, 4 2, 4 8, 6 8, 6 0))", "POLYGON((6 8, 6 0, 4 0, 4 6, 2 6, 2 0, 0 0, 0 8))"
        
        //obtain user inserted data from combo boxes and other fields
        int triangulationMethod;
        if ( triangulationMethodComboBox.getSelectedItem().toString().equals(TriangulationMethod.COMPATIBLE.toString()) ){
            triangulationMethod = TriangulationMethod.COMPATIBLE.get_value();
        }
        else{
            triangulationMethod = TriangulationMethod.EQUILATERAL.get_value();
        }
        
        boolean cw;
        cw = verticeOrientationComboBox.getSelectedItem().toString().equals(AppStrings.CLOCK_WISE_STRING);
        
        double initialTime = Double.parseDouble(initialTimeSpinner.getValue().toString());
        double threshold = Double.parseDouble(colinearThresholdSpinner.getValue().toString());
        MorphingMethod morphingMethod = MorphingMethod.valueOf(this.methodSelectionComboBox.getSelectedItem().toString());

        //TEMPORARY begin and end time values
        Morphing morphing = new Morphing(wkts[0], wkts[1], 1000.0, 2000.0, morphingMethod);

        //send the data as input to the corresponding c++ function
        if (selectedTime.equals(AppStrings.AT_INSTANT_METHOD_STRING)){
            duringPeriod = false;
            //polygon, at instant
            if(selectedGeomType.equals(AppStrings.POLY_STRING)){
                isPolygon = true;
                if (morphingMethod.equals(MorphingMethod.NORMAL_METHOD)){
                    result[0] = morphing.morphingAtInstantPoly(initialTime, triangulationMethod, cw, threshold);
                }
                else if (morphingMethod.equals(MorphingMethod.MCKERNEY_METHOD)){
                    result[0] = morphing.morphingMckerney(initialTime);
                }
            }
            //mesh, at instant
            else if(selectedGeomType.equals(AppStrings.MESH_STRING)){
                isPolygon = false;
                if (morphingMethod.equals(MorphingMethod.NORMAL_METHOD)){
                    result[0] = morphing.morphingAtInstantMesh(initialTime, triangulationMethod, cw, threshold);
                }
            }
            
        }
        else if (selectedTime.equals(AppStrings.DURING_PERIOD_METHOD_STRING)){
            duringPeriod = true;
            
            double endTime = Double.parseDouble(endTimeSpinner.getValue().toString());
            if(selectedGeomType.equals(AppStrings.POLY_STRING)){
                //polygon, during period
                isPolygon = true;
                result = m.during_period_poly(1000.0, 2000.0, wkts[0], wkts[1], initialTime, endTime, 1000, triangulationMethod, cw, threshold);
            }
            else if(selectedGeomType.equals(AppStrings.MESH_STRING)){
                //mesh, during period
                isPolygon = false;
                result = m.during_period_mesh(1000.0, 2000.0, wkts[0], wkts[1], initialTime, endTime, 1000, triangulationMethod, cw, threshold);
            }
        }

        //System.out.println("result --> "+result.length);
        
        String res = Arrays.toString(result);
        if (!res.contains(AppStrings.MORPHING_ERR_STRING)){
            //morphing was succesfull
            //add the wkt with result in the text area
            //resultTextArea.setText(res);
            //draw the result of the morphing geometry in the left panel (1st panel) if is at instant
            // open new window with animation of morphing if is 2nd 
            drawAndShowMorphingGeometry(result, duringPeriod, isPolygon, morphingMethod);
            
            //enable the show morphing geometry in panel checkbox and check it
            showMorphedGeometryCheckBox.setEnabled(true);
            showMorphedGeometryCheckBox.setState(true);
        }
        else{
            //open error dialog box
            JOptionPane.showMessageDialog(new JFrame(), "An error occurred during morphing operation.",
            "Error on Morphing", JOptionPane.ERROR_MESSAGE);
        }
    }//GEN-LAST:event_startMorphing

    private void playBtnCaretPositionChanged(java.awt.event.InputMethodEvent evt) {//GEN-FIRST:event_playBtnCaretPositionChanged
        // TODO add your handling code here:
    }//GEN-LAST:event_playBtnCaretPositionChanged

    //draw in the left panel (1st panel) the result of the morphing of a geometry
    public void drawAndShowMorphingGeometry(String[] wktGeometry, boolean duringPeriod, boolean isPolygon, MorphingMethod morphingMethod){
        WKTReader reader = new WKTReader();

        //set of geometries for each instant, showed in a new window
        if (duringPeriod){
            //several polygons for a certain interval of time

            if(wktGeometry.length == 1){
                //a multipolygon, each polygon representing one instant
                MultiPolygon mPolygon = null;

                try {
                    //array has length 1, with the multipolygon
                    mPolygon = (MultiPolygon) reader.read(wktGeometry[0]);        
                }catch(Exception e) {   }

                AppCorrGeometries.getInstance().animation(wktGeometry, mPolygon, isPolygon, morphingMethod);
            }
            else{
                
                if(isPolygon){
                    //a list of polygons, each representing one instant of time
                    List<Polygon> pList = new ArrayList<>();
                    for (String wkt : wktGeometry){
                        try { 
                            Polygon p = (Polygon) reader.read(wkt);
                            pList.add(p);
                        } catch (ParseException ex) {
                            Logger.getLogger(AppCorrGeometries.class.getName()).log(Level.SEVERE, null, ex);
                        }

                    }
                    AppCorrGeometries.getInstance().animation(wktGeometry, pList, isPolygon, morphingMethod);
                }
                else{
                    //a list of multipolygons, each multypoligon representing a mesh of triangules in a period of time
                    List<MultiPolygon> mpList = new ArrayList<>();
                    for (String wkt : wktGeometry){
                        try { 
                            MultiPolygon mp = (MultiPolygon) reader.read(wkt);
                            mpList.add(mp);
                        } catch (ParseException ex) {
                            Logger.getLogger(AppCorrGeometries.class.getName()).log(Level.SEVERE, null, ex);
                        }

                    }
                    AppCorrGeometries.getInstance().animation(wktGeometry, mpList, isPolygon, morphingMethod);
                }
            }
        }
        //at instant
        else {
            //one polygon or a multipolygon of triangules for one instant
            if (isPolygon){
                //a polygon
                 Polygon polygon = null;
                try {
                    polygon = (Polygon) reader.read(wktGeometry[0]);
                    System.out.println("wkt -> "+wktGeometry[0]);
                    AppCorrGeometries.getInstance().showMorphingGeometryInPanel(polygon);
                } catch (ParseException ex) {
                    Logger.getLogger(AppCorrGeometries.class.getName()).log(Level.SEVERE, null, ex);
                }           
            }
            else{
                //a multipolygon, with meshes of triangules
                MultiPolygon multiPolygon = null;
                try {
                    multiPolygon = (MultiPolygon) reader.read(wktGeometry[0]);
                    System.out.println("wkt -> "+wktGeometry[0]);
                    AppCorrGeometries.getInstance().showMorphingGeometryInPanel(multiPolygon);
                } catch (ParseException ex) {
                    Logger.getLogger(AppCorrGeometries.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }
    }
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JLabel colinearThresholdLabel;
    private javax.swing.JSpinner colinearThresholdSpinner;
    private javax.swing.JSpinner endTimeSpinner;
    private javax.swing.Box.Filler filler2;
    private javax.swing.JSpinner initialTimeSpinner;
    private javax.swing.JComboBox<String> instantOrPeriodComboBox;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JComboBox<String> meshOrPolygonComboBox;
    private javax.swing.JLabel meshOrPolygonLabel;
    private javax.swing.JLabel methodSelection;
    private javax.swing.JComboBox<String> methodSelectionComboBox;
    private javax.swing.JLabel orientationLabel;
    private javax.swing.JButton playBtn;
    private javax.swing.JLabel resultLabel;
    private javax.swing.JTextArea resultTextArea;
    private java.awt.Checkbox showMorphedGeometryCheckBox;
    private javax.swing.JLabel timeLabel;
    private javax.swing.JLabel timeOrInstantLabel;
    private javax.swing.JLabel triangulationLabel;
    private javax.swing.JComboBox<String> triangulationMethodComboBox;
    private javax.swing.JComboBox<String> verticeOrientationComboBox;
    // End of variables declaration//GEN-END:variables
}
