/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import javax.swing.JLabel;
import javax.swing.JSlider;
import javax.swing.JWindow;
import javax.swing.SpinnerModel;
import javax.swing.SpinnerNumberModel;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import jni_st_mesh.Main;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.axis.NumberTickUnit;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.category.DefaultCategoryDataset;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

/**
 *
 * @author Bruno Silva
 */
public class MorphingGeometryOptionsPanel extends javax.swing.JPanel {
     
    /**
     * Creates new form MorphingGeometryOptionsPanel
     */
    public MorphingGeometryOptionsPanel() {
        initComponents();

        this.playBtn.setText(AppStrings.START_MORPHING_BTN_STRING);
        this.timeLabel.setText(AppStrings.INSTANT_LABEL_STRING);
        this.metricLabel.setText(AppStrings.STATISTIC_LABEL_STRING);
        this.meshOrPolygonLabel.setText(AppStrings.GEOMETRY_TYPE_LABEL_STRING);
        this.timeOrInstantLabel.setText(AppStrings.TIME_LABEL_STRING);
        
        this.initialTimeSpinner.setModel(new SpinnerNumberModel(1000, 1000, 2000, 10));//set default, min max and increment value
        this.endTimeSpinner.setModel(new SpinnerNumberModel(2000, 1000, 2000, 10));//set default, min max and increment value
        this.remove(endTimeSpinner); //initially hidden
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
        this.methodSelectionComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.METHOD_SELECTION_STRINGS));
        this.meshOrPolygonComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.MESH_OR_POLY_STRINGS));
        this.metricsComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.METRICS_STRINGS));
        
        methodSelectionComboBox.addActionListener (new ActionListener () {
            public void actionPerformed(ActionEvent e) {
                //if user wants to get the morphing at an instant, hide the spinner for the end time
                if(methodSelectionComboBox.getSelectedItem().toString().equals(AppStrings.AT_INSTANT_METHOD_STRING)){
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
        methodSelectionComboBox = new javax.swing.JComboBox<>();
        meshOrPolygonComboBox = new javax.swing.JComboBox<>();
        initialTimeSpinner = new javax.swing.JSpinner();
        endTimeSpinner = new javax.swing.JSpinner();
        meshOrPolygonLabel = new javax.swing.JLabel();
        timeOrInstantLabel = new javax.swing.JLabel();
        metricLabel = new javax.swing.JLabel();
        metricsComboBox = new javax.swing.JComboBox<>();

        setFocusTraversalPolicyProvider(true);
        setLayout(new java.awt.GridBagLayout());

        playBtn.setText("Play");
        playBtn.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                playBtnActionPerformed(evt);
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

        methodSelectionComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 4;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 10);
        add(methodSelectionComboBox, gridBagConstraints);

        meshOrPolygonComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 4;
        gridBagConstraints.gridy = 3;
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
        gridBagConstraints.gridy = 3;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 0);
        add(meshOrPolygonLabel, gridBagConstraints);

        timeOrInstantLabel.setText("jLabel2");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 0);
        add(timeOrInstantLabel, gridBagConstraints);

        metricLabel.setText("jLabel3");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 0);
        add(metricLabel, gridBagConstraints);

        metricsComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 4;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(0, 10, 0, 10);
        add(metricsComboBox, gridBagConstraints);
    }// </editor-fold>//GEN-END:initComponents

    /** Calls the c++ library that, given a time interval, a previous geometry and a target geometry,
    * predict the morphing of the geometry in a given time having these two geometries as a reference.
    */
    private void playBtnActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_playBtnActionPerformed
        // get wkt of the corr geometries in both panels.
        //index 0 has the wkt of the corr geometry in panel 1 and index 1 has the wkt of the corr geometry in panel 2
        String[] wkts = AppCorrGeometries.getInstance().getWKTextFromGeometriesInPanels();
        /*System.out.println("wkt 1st geometry: "+wkts[0]);
        System.out.println("wkt 2nd geometry: "+wkts[1]);*/
        
        String[] result = new String[1];
        
        //load c++ libraries
        System.loadLibrary(AppStrings.DLL_LIBRARY);
        Main m = new Main();
        
        //find which method to call:
        String selectedMethod = this.methodSelectionComboBox.getSelectedItem().toString();
        String selectedType = this.meshOrPolygonComboBox.getSelectedItem().toString();
        boolean duringPeriod = false;
        
        if (selectedMethod.equals(AppStrings.AT_INSTANT_METHOD_STRING)){
            duringPeriod = false;
            if(selectedType.equals(AppStrings.POLY_STRING)){
                result[0] = m.at_instant_poly(1000.0, 2000.0, "POLYGON((0 0, 0 8, 2 8, 2 2, 4 2, 4 8, 6 8, 6 0))", "POLYGON((6 8, 6 0, 4 0, 4 6, 2 6, 2 0, 0 0, 0 8))", 
                        Double.parseDouble(initialTimeSpinner.getValue().toString()));
            }
            else if(selectedType.equals(AppStrings.MESH_STRING)){
                result[0] = m.at_instant_mesh_2(1000.0, 2000.0, "POLYGON((0 0, 0 8, 2 8, 2 2, 4 2, 4 8, 6 8, 6 0))", "POLYGON((6 8, 6 0, 4 0, 4 6, 2 6, 2 0, 0 0, 0 8))", 
                        Double.parseDouble(initialTimeSpinner.getValue().toString()));
            }
            
        }
        else if (selectedMethod.equals(AppStrings.DURING_PERIOD_METHOD_STRING)){
            duringPeriod = true;
            if(selectedType.equals(AppStrings.POLY_STRING)){
                result[0] = m.during_period_poly(1000.0, 2000.0, "POLYGON((0 0, 0 8, 2 8, 2 2, 4 2, 4 8, 6 8, 6 0))", "POLYGON((6 8, 6 0, 4 0, 4 6, 2 6, 2 0, 0 0, 0 8))", 1000.0, 2000.0, 1000);
            }
            else if(selectedType.equals(AppStrings.MESH_STRING)){
                result = m.during_period_mesh_2(1000.0, 2000.0, "POLYGON((0 0, 0 8, 2 8, 2 2, 4 2, 4 8, 6 8, 6 0))", "POLYGON((6 8, 6 0, 4 0, 4 6, 2 6, 2 0, 0 0, 0 8))", 1000.0, 2000.0, 1000);
            }
        }
        Map<String, Double> d = m.quality_measures_2("POLYGON((0 0, 0 8, 2 8, 2 2, 4 2, 4 8, 6 8, 6 0))");
        if(d != null){
            Iterator<Entry<String, Double>> it = d.entrySet().iterator();

            while (it.hasNext()) 
            {
                Map.Entry<String, Double> pair = (Map.Entry<String, Double>) it.next();

                System.out.println(pair.getKey() + ": " + pair.getValue());
                //it.remove();
            }
        }

        //System.out.println("result --> "+Arrays.toString(result));
        
        if (!result.equals(AppStrings.MORPHING_ERR_STRING)){
            //morphing was succesfull
            //add the wkt with result in the text area
            resultTextArea.setText(Arrays.toString(result));
            //for now, draw the result of the morphing geometry in the left panel (1st panel)
            AppCorrGeometries.getInstance().drawAndShowMorphingGeometry(result, duringPeriod);
            
            //enable the show morphing geometry in panel checkbox and check it
            showMorphedGeometryCheckBox.setEnabled(true);
            showMorphedGeometryCheckBox.setState(true);
        }
        
    }//GEN-LAST:event_playBtnActionPerformed

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JSpinner endTimeSpinner;
    private javax.swing.Box.Filler filler2;
    private javax.swing.JSpinner initialTimeSpinner;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JComboBox<String> meshOrPolygonComboBox;
    private javax.swing.JLabel meshOrPolygonLabel;
    private javax.swing.JComboBox<String> methodSelectionComboBox;
    private javax.swing.JLabel metricLabel;
    private javax.swing.JComboBox<String> metricsComboBox;
    private javax.swing.JButton playBtn;
    private javax.swing.JLabel resultLabel;
    private javax.swing.JTextArea resultTextArea;
    private java.awt.Checkbox showMorphedGeometryCheckBox;
    private javax.swing.JLabel timeLabel;
    private javax.swing.JLabel timeOrInstantLabel;
    // End of variables declaration//GEN-END:variables
}
