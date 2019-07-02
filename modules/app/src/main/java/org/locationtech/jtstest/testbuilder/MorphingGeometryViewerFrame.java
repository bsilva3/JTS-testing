package org.locationtech.jtstest.testbuilder;

import java.awt.BorderLayout;
import java.awt.GridBagConstraints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.DefaultBoundedRangeModel;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.SpinnerNumberModel;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import jni_st_mesh.CSVUtils;
import jni_st_mesh.ChartMaker;
import jni_st_mesh.ChartType;
import jni_st_mesh.Main;
import jni_st_mesh.Metrics;
import jni_st_mesh.ScreenImage;
import jni_st_mesh.Ststistics;
import jni_st_mesh.TriangulationMethod;
import org.jfree.chart.ChartPanel;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.MultiPolygon;
import org.locationtech.jts.geom.Polygon;
import org.locationtech.jts.io.ParseException;
import org.locationtech.jts.io.WKTReader;
import org.locationtech.jtstest.testbuilder.morphing.MorphingMethod;

/**
 *This frame shows an animation of a geometry throught a period of time. It is possible to pause and play the animation
 * as well as manually animate the geometry, see charts with quality metrics and save the geometry
 */
public class MorphingGeometryViewerFrame extends javax.swing.JFrame {
    
    private MorphingGeometryPanel morphingGeoPanel;
    private boolean userChangedSlider = true;
    private String[] wktGeometry;
    private boolean isPolygon;
    private int beginTime = 1000; //<----- temporary
    private int endTime = 2000; //<-----
    private int numSamples;
    HashMap<String, Double> statistics;
    
    private ChartMaker chartMaker;
    
    private MorphingMethod morphingMethod;
    
    private MultiPolygon mp;
    private MultiPolygon[] multiPolyList;
    private Polygon[] polyList;
    
    private MorphingGeometryViewerFrame(String[] wktGeometry, boolean isPolygon, MorphingMethod morphingMethod, int numSamples) {
        this.wktGeometry = wktGeometry;
        this.isPolygon = isPolygon;
        this.morphingMethod = morphingMethod;
        this.numSamples = numSamples;
        chartMaker = new ChartMaker();
        initComponents();
    }
    
    /**
     *
     * @param wktGeometry - array with wkt as string with the geometry on the first panel and the wkt of the geometry
     * in the second panel
     * @param isPolygon
     * @param morphingMethod
     * @param numSamples
     * @param mp - the result of the morphing of the geometries as a multipolygon, each polygon in an instant
     */
    public MorphingGeometryViewerFrame(String[] wktGeometry, boolean isPolygon, MorphingMethod morphingMethod,
            int numSamples, MultiPolygon mp) {
        this(wktGeometry, isPolygon, morphingMethod, numSamples);
        this.morphingGeoPanel = new MorphingGeometryPanel(mp);
        this.mp = mp;
        startComponents();
        initMorphingPanel();
        if (isPolygon)
            showStatisticsInChart(metricsComboBox.getSelectedItem().toString(), chartTypeComboBox.getSelectedItem().toString());
    }
    
    /**
     * @param wktGeometry - array with wkt as string with the geometry on the first panel and the wkt of the geometry
     * in the second panel
     * @param geometryList - the result of the morphing of the geometries as a list of multipolygon, or polygon
     * each multipolygon being a mesh of triangles in an instant or a polygon in each instant of time
     */
    public MorphingGeometryViewerFrame(String[] wktGeometry, boolean isPolygon, MorphingMethod morphingMethod, 
            int numSamples, Polygon[] geometryList) {
        this(wktGeometry, isPolygon, morphingMethod, numSamples);
        this.morphingGeoPanel = new MorphingGeometryPanel(geometryList);
        this.polyList = geometryList;
        startComponents();
        initMorphingPanel();
        //start by showing the area evolution chart
        if (isPolygon)
            showStatisticsInChart(metricsComboBox.getSelectedItem().toString(), chartTypeComboBox.getSelectedItem().toString());
    }
    
    public MorphingGeometryViewerFrame(String[] wktGeometry, boolean isPolygon, MorphingMethod morphingMethod, 
            int numSamples, MultiPolygon[] geometryList) {
        this(wktGeometry, isPolygon, morphingMethod, numSamples);
        this.morphingGeoPanel = new MorphingGeometryPanel(geometryList);
        this.multiPolyList = geometryList;
        startComponents();
        initMorphingPanel();
        //start by showing the area evolution chart
        if (isPolygon)
            showStatisticsInChart(metricsComboBox.getSelectedItem().toString(), chartTypeComboBox.getSelectedItem().toString());
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

        chartPanel = new javax.swing.JPanel();
        morphingFormPanel = new javax.swing.JPanel();
        playBtn = new javax.swing.JButton();
        pauseBtn = new javax.swing.JButton();
        timeSlider = new javax.swing.JSlider();
        saveCurrentGeometryBtn = new javax.swing.JButton();
        minTimeLabel = new javax.swing.JLabel();
        maxTimeLabel = new javax.swing.JLabel();
        saveAnimationBtn = new javax.swing.JButton();
        chartTypeLabel = new javax.swing.JLabel();
        chartTypeComboBox = new javax.swing.JComboBox<>();
        metricsLabel = new javax.swing.JLabel();
        metricsComboBox = new javax.swing.JComboBox<>();
        triangulationLabel = new javax.swing.JLabel();
        triangulationComboBox = new javax.swing.JComboBox<>();
        exportBtn = new javax.swing.JButton();
        saveStatisticsBtn = new javax.swing.JButton();
        cwComboBox = new javax.swing.JComboBox<>();
        cwLabel = new javax.swing.JLabel();
        colinearThresholdLabel = new javax.swing.JLabel();
        colinearThresholdSpinner = new javax.swing.JSpinner();
        showStatisticsBtn = new javax.swing.JButton();
        jSeparator1 = new javax.swing.JSeparator();
        morphBtn = new javax.swing.JButton();
        geomTypeLabel = new javax.swing.JLabel();
        geomTypeComboBox = new javax.swing.JComboBox<>();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        getContentPane().setLayout(new java.awt.GridBagLayout());

        chartPanel.setLayout(new java.awt.BorderLayout());
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.gridwidth = 3;
        gridBagConstraints.gridheight = 9;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        gridBagConstraints.weightx = 30.0;
        gridBagConstraints.weighty = 5.0;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 15);
        getContentPane().add(chartPanel, gridBagConstraints);

        morphingFormPanel.setLayout(new java.awt.GridBagLayout());

        playBtn.setText("jButton1");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 2;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        morphingFormPanel.add(playBtn, gridBagConstraints);

        pauseBtn.setText("jButton2");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        morphingFormPanel.add(pauseBtn, gridBagConstraints);
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.gridy = 3;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        morphingFormPanel.add(timeSlider, gridBagConstraints);

        saveCurrentGeometryBtn.setText("jButton3");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        morphingFormPanel.add(saveCurrentGeometryBtn, gridBagConstraints);

        minTimeLabel.setText("jLabel3");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 3;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_END;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        morphingFormPanel.add(minTimeLabel, gridBagConstraints);

        maxTimeLabel.setText("jLabel4");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 3;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_START;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        morphingFormPanel.add(maxTimeLabel, gridBagConstraints);

        saveAnimationBtn.setText("jButton4");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 2;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        morphingFormPanel.add(saveAnimationBtn, gridBagConstraints);

        chartTypeLabel.setText("jLabel2");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 6;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_START;
        gridBagConstraints.insets = new java.awt.Insets(5, 10, 5, 0);
        morphingFormPanel.add(chartTypeLabel, gridBagConstraints);

        chartTypeComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 7;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_START;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(chartTypeComboBox, gridBagConstraints);

        metricsLabel.setText("jLabel1");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 6;
        gridBagConstraints.gridy = 2;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_START;
        gridBagConstraints.insets = new java.awt.Insets(5, 10, 5, 0);
        morphingFormPanel.add(metricsLabel, gridBagConstraints);

        metricsComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 7;
        gridBagConstraints.gridy = 2;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_START;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(metricsComboBox, gridBagConstraints);

        triangulationLabel.setText("jLabel3");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 2;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_START;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(triangulationLabel, gridBagConstraints);

        triangulationComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.gridy = 2;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_START;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(triangulationComboBox, gridBagConstraints);

        exportBtn.setText("jButton2");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 5;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.gridwidth = 3;
        gridBagConstraints.insets = new java.awt.Insets(5, 10, 5, 0);
        morphingFormPanel.add(exportBtn, gridBagConstraints);

        saveStatisticsBtn.setText("jButton1");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 8;
        gridBagConstraints.gridy = 4;
        gridBagConstraints.gridwidth = 3;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(saveStatisticsBtn, gridBagConstraints);

        cwComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_START;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(cwComboBox, gridBagConstraints);

        cwLabel.setText("jLabel4");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_START;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(cwLabel, gridBagConstraints);

        colinearThresholdLabel.setText("jLabel5");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 2;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_END;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(colinearThresholdLabel, gridBagConstraints);
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_START;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(colinearThresholdSpinner, gridBagConstraints);

        showStatisticsBtn.setText("jButton3");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 7;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.gridwidth = 4;
        morphingFormPanel.add(showStatisticsBtn, gridBagConstraints);
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 4;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.gridheight = 4;
        gridBagConstraints.fill = java.awt.GridBagConstraints.VERTICAL;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        morphingFormPanel.add(jSeparator1, gridBagConstraints);

        morphBtn.setText("jButton1");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        morphingFormPanel.add(morphBtn, gridBagConstraints);

        geomTypeLabel.setText("jLabel1");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 2;
        gridBagConstraints.gridy = 2;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.LINE_END;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(geomTypeLabel, gridBagConstraints);

        geomTypeComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.gridy = 2;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(5, 0, 5, 0);
        morphingFormPanel.add(geomTypeComboBox, gridBagConstraints);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 5;
        gridBagConstraints.gridwidth = 3;
        gridBagConstraints.gridheight = 4;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        getContentPane().add(morphingFormPanel, gridBagConstraints);

        pack();
    }// </editor-fold>//GEN-END:initComponents
    
    private void initMorphingPanel(){
        //remove any previous panels
        getContentPane().remove(morphingGeoPanel);
        //add here the panel
        GridBagConstraints gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.gridwidth = 3;///<-------- increase or decrease the size of this acording to the number of columns the top buttons take
        gridBagConstraints.gridheight = 4;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.CENTER;
        gridBagConstraints.insets = new java.awt.Insets(5, 5, 0, 5);
        gridBagConstraints.weightx = 4.0; 
        gridBagConstraints.weighty = 10.0;
        try{
            getContentPane().add(morphingGeoPanel, gridBagConstraints);
        } catch (NullPointerException ex){ }
        
        //add listener for when a frame in the animation changes and update the slider with the value for the new frame
        this.morphingGeoPanel.addPropertyChangeListener(new PropertyChangeListener() {
            @Override
            public void propertyChange(PropertyChangeEvent e) {
                if (e.getPropertyName().equals(AppConstants.PROPERTY_CHANGED_NAME)) {
                    userChangedSlider = false;
                    int value = Integer.parseInt(e.getNewValue().toString());
                    //System.out.println("changed " + value);
                    timeSlider.setValue(convertValueToSliderValue(value));
                    userChangedSlider = true;
                }
            }
        });
    }
    
    /** Add text, values and listeners to the components of this panel.
     *
     */
    private void startComponents(){
        //initialize buttons
        this.playBtn.setText(AppStrings.PLAY_STRING);
        this.pauseBtn.setText(AppStrings.PAUSE_STRING);
        this.exportBtn.setText(AppStrings.EXPORT_QUALITY_MEASURES_STRING);
        this.saveStatisticsBtn.setText(AppStrings.SAVE_CURRENT_STATISTICS_STRING);
        this.saveCurrentGeometryBtn.setText(AppStrings.SAVE_CURRENT_GEOMETRY_STRING);
        this.saveAnimationBtn.setText(AppStrings.SAVE_ANIMATION_STRING);
        this.showStatisticsBtn.setText(AppStrings.SHOW_STATISTIC_STRING);
        this.morphBtn.setText(AppStrings.MORPHING_BTN_STRING);
        
        //initialize labels
        this.chartTypeLabel.setText(AppStrings.CHART_TYPE_LABEL_STRING);
        this.metricsLabel.setText(AppStrings.STATISTIC_LABEL_STRING);
        this.triangulationLabel.setText(AppStrings.TRIANGULATION_LABEL_STRING);
        this.cwLabel.setText(AppStrings.VERTICE_ORIENTATION_LABEL_STRING);
        this.colinearThresholdLabel.setText(AppStrings.COLINEAR_THRESHOLD_STRING);
        this.minTimeLabel.setText(beginTime+"");
        this.maxTimeLabel.setText(endTime+"");
        this.geomTypeLabel.setText(AppStrings.GEOMETRY_TYPE_LABEL_STRING);
        

        
        //initialize combo box
        this.metricsComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(Metrics.getStatStringList()));
        this.chartTypeComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(ChartType.getChartTypeList()));
        this.triangulationComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.TRIANGULATION_METHOD_STRINGS));
        this.cwComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.VERTICE_ORIENTATION_STRINGS));
        this.geomTypeComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(AppStrings.MESH_OR_POLY_STRINGS));
        
        //initialize spinner
        this.colinearThresholdSpinner.setModel(new SpinnerNumberModel(0.5, 0, 1, 0.1));
        
        metricsComboBox.addItemListener(new ItemListener(){
            @Override
            public void itemStateChanged(ItemEvent e) {
                if (e.getStateChange() == ItemEvent.SELECTED) {
                    // new statistic selected
                    //certain statistics should not be shown in chart, only in table.
                    //if such statistic is selected, disable the combo box to choose the chart type,
                    //and force the table to be selected
                    int statisticSelected = Ststistics.stringToInt(metricsComboBox.getSelectedItem().toString());
                    
                    //AFTER UPDATE THIS MAY NOT BE NECESSARY... TO BE DECIDED
                    /*if (statisticSelected > 2){
                        //statistics that can only be shown in tables
                        chartTypeComboBox.setSelectedItem(ChartType.TABLE.getValue());
                        chartTypeComboBox.setEnabled(false);
                    }
                    else{
                        //statistics that can be shown in any chart and table
                        //chartTypeComboBox.setSelectedIndex(0);
                        chartTypeComboBox.setEnabled(true);
                    }*/
                  }
            }
        });
        
        /*chartTypeComboBox.addItemListener(new ItemListener(){
            @Override
            public void itemStateChanged(ItemEvent e) {
                if (e.getStateChange() == ItemEvent.SELECTED) {
                    // new item selected
                    //call the appropriate function to show the corresponding chart/table
                    if (chartTypeComboBox.getSelectedItem().equals(ChartType.BAR_CHART)){
                        showStatisticsInChart(Ststistics.AREA_EVOLUTION.get_value());
                        exportBtn.setVisible(false);
                    }
                    else if(chartTypeComboBox.getSelectedItem().equals(ChartType.LINE_CHART)){
                        showQualityMetricsTable();
                        exportBtn.setVisible(true); //should only be visible on quality metrics, (for now)
                    }                    
                    else if(chartTypeComboBox.getSelectedItem().equals(ChartType.TABLE)){
                        showQualityMetricsTable();
                        exportBtn.setVisible(true); //should only be visible on quality metrics, (for now)
                    }
                  }
            }
        }); */
        
        morphBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                //obtain user inserted data from combo boxes and other fields
                int triangulationMethod;
                if ( triangulationComboBox.getSelectedItem().toString().equals(TriangulationMethod.COMPATIBLE.toString()) ){
                    triangulationMethod = TriangulationMethod.COMPATIBLE.get_value();
                }
                else{
                    triangulationMethod = TriangulationMethod.EQUILATERAL.get_value();
                }

                boolean cw;
                cw = cwComboBox.getSelectedItem().toString().equals(AppStrings.CLOCK_WISE_STRING);
                //selected type of geometry
                String selectedType = geomTypeComboBox.getSelectedItem().toString();
                //double initialTime = Double.parseDouble(initialTimeSpinner.getValue().toString());
                double threshold = Double.parseDouble(colinearThresholdSpinner.getValue().toString());
                //send the data as input to the corresponding c++ function
                //load c++ libraries
                System.loadLibrary(AppStrings.DLL_LIBRARY);
                Main m = new Main();

                String[] result = new String[1];
                if(selectedType.equals(AppStrings.POLY_STRING)){
                    //polygon, during period
                    result = m.during_period_poly(beginTime, endTime, wktGeometry[0], wktGeometry[1], beginTime, endTime, numSamples, triangulationMethod, cw, threshold, 0.0);
                }
                else if(selectedType.equals(AppStrings.MESH_STRING)){
                    //mesh, during period
                    result = m.during_period_mesh(beginTime, endTime, wktGeometry[0], wktGeometry[1], beginTime, endTime, numSamples, triangulationMethod, cw, threshold);
                }
                
                WKTReader reader = new WKTReader();
                String res = Arrays.toString(result);
                if (!res.contains(AppStrings.MORPHING_ERR_STRING)){
                    if(selectedType.equals(AppStrings.POLY_STRING)){
                        //a list of polygons, each representing one instant of time
                        Polygon[] pList = new Polygon[result.length];
                        for (int i = 0; i < result.length; i++){
                            try { 
                                Polygon p = (Polygon) reader.read(result[i]);
                                pList[i] = p;
                            } catch (ParseException ex) {
                                Logger.getLogger(AppCorrGeometries.class.getName()).log(Level.SEVERE, null, ex);
                            }
                        }
                        //System.out.println(pList.size());
                        morphingGeoPanel.changeToPolygonList(pList);
                    }
                    else{
                        //a list of multipolygons, each multypoligon representing a mesh of triangules in a period of time
                        MultiPolygon[] mpList = new MultiPolygon[result.length];
                        for (int i = 0; i < result.length; i++){
                            try { 
                                MultiPolygon mp = (MultiPolygon) reader.read(result[i]);
                                mpList[i] = mp;
                            } catch (ParseException ex) {
                                Logger.getLogger(AppCorrGeometries.class.getName()).log(Level.SEVERE, null, ex);
                            }

                        }
                        morphingGeoPanel.changeToMultiPolygonList(mpList);
                    }
                }
            }
        });
        
        playBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                morphingGeoPanel.play();
            }
        });
        
        pauseBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                morphingGeoPanel.pause();
            }
        });
        
        this.exportBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                
                //capture the panel with the chart and save as image
                if(statistics != null){
                    int status = CSVUtils.exportAndSaveToCSV(statistics);
                    if (status == 0){
                        //success
                        JOptionPane.showMessageDialog(new JFrame(), "File save succesfully");
                    }
                    else if (status == 1){
                        //error
                        JOptionPane.showMessageDialog(new JFrame(), "Error while saving file", "Error",
                        JOptionPane.ERROR_MESSAGE);
                    }
                }
            }
        });
        
        saveCurrentGeometryBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                
                //capture the panel with the current geometry displayed and save as image
                ScreenImage.printAndSaveAsImage(morphingGeoPanel);
            }
        });
        
        saveAnimationBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                //create images for every frame and save in user created folder;
                JDialog dialog = createWaitDialog();
                dialog.setVisible(true);
                morphingGeoPanel.saveAnimationToImages();
                dialog.setVisible(false);
                //get list of all images corresponding to every frame of the animation
                /*List<BufferedImage> imagesFromAnimation = morphingGeoPanel.generateImagesFromAnimation(10);
                GifSequenceWriter.createGIFAndSave(imagesFromAnimation);*/
            }
        });
        
        saveStatisticsBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                
                //capture the panel with the chart or table and save as image
                ScreenImage.printAndSaveAsImage(chartPanel);
            }
        });
        
        showStatisticsBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showStatisticsInChart(metricsComboBox.getSelectedItem().toString(), chartTypeComboBox.getSelectedItem().toString());
            }
        });
        int step = (endTime-beginTime)/numSamples;
        //the slider's range will be from the begin time to begin time + number of samples
        timeSlider.setModel(new DefaultBoundedRangeModel(beginTime, 1, beginTime, beginTime+numSamples));
        //timeSlider.setMinorTickSpacing(step);
        //timeSlider.setPaintTicks(true);
        //timeSlider.setPaintLabels(true);
        //timeSlider.setLabelTable(timeSlider.createStandardLabels(step));
        
        timeSlider.addChangeListener(new ChangeListener() {
            @Override
            public void stateChanged(ChangeEvent e) {
                if (userChangedSlider){
                    morphingGeoPanel.paintAtInstant(convertSliderValueToValue(timeSlider.getValue()));
                }
            }
        });
        
        
    }
    
    private void showStatisticsInChart(String statisticStr, String chart){
        //clear any other element in the panel that shows the charts
        chartPanel.removeAll();
        
        System.loadLibrary(AppStrings.DLL_LIBRARY);
        Main m = new Main();
        
        //call the method from the C++ library
        String headerLegend = "";
        String xAxisLegend = "";
        String yAxisLegend = "";
        boolean keysAreNumbers = false; //flag to check if sort by key is needed to display data in the charts
        String[] geometries;
        if (mp == null && multiPolyList == null && this.polyList.length > 0){
            geometries = new String[polyList.length];
            for (int i = 0; i < polyList.length; i++){
                geometries[i] = polyList[i].toText();
            }
        }
        else if (mp == null && polyList == null && this.multiPolyList.length > 0){
            geometries = new String[multiPolyList.length];
            for (int i = 0; i < multiPolyList.length; i++){
                geometries[i] = multiPolyList[i].toText();
            }
        }
        else{
            geometries = new String[mp.getNumGeometries()];
            for (int i = 0; i < mp.getNumGeometries(); i++){
                geometries[i] = mp.getGeometryN(i).toText();
            }
        }
        HashMap<String, Double> statisticValues = new HashMap<String, Double>();
        switch(statisticStr)
        {
            case "Area":
                for(int j = 0; j < geometries.length; j++)
                    statisticValues.put(String.valueOf(j), m.numerical_metric(geometries[j], Metrics.AREA.get_value()));
                
                headerLegend = "Evolution of the Area";
                xAxisLegend = "Observations";
                yAxisLegend = "Area (Dimensionless)";
                break;
            case "Perimeter":
                for(int j = 0; j < geometries.length; j++)
                    statisticValues.put(String.valueOf(j), m.numerical_metric(geometries[j], Metrics.PERIMETER.get_value()));
                
                headerLegend = "Evolution of the Perimeter";
                xAxisLegend = "Observations";
                yAxisLegend = "Perimeter (Dimensionless)";
                break;
            /*case "Hausdorff Distance":
                for(int j = 0; j < geometries.length; j++)
                    statisticValues.put(String.valueOf(j), m.compare_geometries(ref_geom_wkt, geometries[j], SimilarityMetrics.GEOMETRIC_SIMILARITY.get_value()));
                
                headerLegend = "Evolution of the Hausdorff Distance";
                xAxisLegend = "Observations";
                yAxisLegend = "Hausdorff Distance (Dimensionless)";
                break;
            case "Jaccard Index":
                for(int j = 0; j < geometries.length; j++)
                    statisticValues.put(String.valueOf(j), m.compare_geometries(ref_geom_wkt, geometries[j], SimilarityMetrics.JACCARD_INDEX.get_value()));
                
                headerLegend = "Evolution of the Jaccard Index";
                xAxisLegend = "Observations";
                yAxisLegend = "%";
                break;*/
        }
        
        /*for (Map.Entry<String, Double> entry : statistics.entrySet()) {
            String key = entry.getKey();
            double value = entry.getValue();
            System.out.println("stats -> "+key+", "+value);
        }*/
        //call apropriate function to create selected chart type
        ChartPanel cp = null;
        if (chart.equals(ChartType.BAR_CHART.getValue())){
            cp = chartMaker.createBarChart(statistics, headerLegend, xAxisLegend, yAxisLegend);
        }
        else if(chart.equals(ChartType.LINE_CHART.getValue())){
            cp = chartMaker.createLineChart(statistics, headerLegend, xAxisLegend, yAxisLegend);
        }
        else if (chart.equals(ChartType.TABLE.getValue())){
            JTable table = chartMaker.createJTable(statistics, xAxisLegend, yAxisLegend, keysAreNumbers);
            this.chartPanel.add(new JScrollPane(table), BorderLayout.CENTER);
            chartPanel.validate();
            return;
        }
        
        //add the panel to the frame
        this.chartPanel.add(cp, BorderLayout.CENTER);
        chartPanel.validate();
    }
    
    /**
     * Convert a value (representing a frame) to a Slider value (representing an instant in time),
     * used to control the frame of the animation.
     * The values in the slider represent an instant in time and the frame of animation start at 0, so this method makes
     * the apropriate conversion so that the frame value becomes a time value
     * @param v - the frame number shown in the animation
     * @return - the instant in time that the frame belongs to
     */
    private int convertValueToSliderValue(int v){
        return beginTime+v;
    }
    
    /**
     * Convert a Slider value (representing an instant in time) to a normal value (representing a frame),
     * used to control the frame of the animation.
     * The values in the slider represent an instant in time and the frame of animation start at 0, so this method makes
     * the apropriate conversion so that the time value becomes a frame value
     * @param v - the instant in time selected in the slider
     * @return - the frame number to be shown in the animation
     */
    private int convertSliderValueToValue(int v){
        return Math.abs(beginTime-v);
    }
    
    private JDialog createWaitDialog(){
        JDialog dialog = new JDialog();
        JLabel label = new JLabel("Please wait...");
        dialog.setLocationRelativeTo(null);
        dialog.setTitle("Please Wait...");
        dialog.add(label);
        dialog.pack();
        return dialog;
    }
        
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JPanel chartPanel;
    private javax.swing.JComboBox<String> chartTypeComboBox;
    private javax.swing.JLabel chartTypeLabel;
    private javax.swing.JLabel colinearThresholdLabel;
    private javax.swing.JSpinner colinearThresholdSpinner;
    private javax.swing.JComboBox<String> cwComboBox;
    private javax.swing.JLabel cwLabel;
    private javax.swing.JButton exportBtn;
    private javax.swing.JComboBox<String> geomTypeComboBox;
    private javax.swing.JLabel geomTypeLabel;
    private javax.swing.JSeparator jSeparator1;
    private javax.swing.JLabel maxTimeLabel;
    private javax.swing.JComboBox<String> metricsComboBox;
    private javax.swing.JLabel metricsLabel;
    private javax.swing.JLabel minTimeLabel;
    private javax.swing.JButton morphBtn;
    private javax.swing.JPanel morphingFormPanel;
    private javax.swing.JButton pauseBtn;
    private javax.swing.JButton playBtn;
    private javax.swing.JButton saveAnimationBtn;
    private javax.swing.JButton saveCurrentGeometryBtn;
    private javax.swing.JButton saveStatisticsBtn;
    private javax.swing.JButton showStatisticsBtn;
    private javax.swing.JSlider timeSlider;
    private javax.swing.JComboBox<String> triangulationComboBox;
    private javax.swing.JLabel triangulationLabel;
    // End of variables declaration//GEN-END:variables
}
