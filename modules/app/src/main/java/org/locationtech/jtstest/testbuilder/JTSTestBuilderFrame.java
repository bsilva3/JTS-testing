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

import java.awt.AWTEvent;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.MouseInfo;
import java.awt.Rectangle;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.WindowEvent;
import java.awt.event.WindowStateListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;
import javax.swing.border.BevelBorder;
import javax.swing.border.Border;
import javax.swing.border.EmptyBorder;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.filechooser.FileNameExtensionFilter;

import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.util.LinearComponentExtracter;
import org.locationtech.jts.io.ParseException;
import org.locationtech.jts.util.Assert;
import org.locationtech.jtstest.clean.CleanDuplicatePoints;
import org.locationtech.jtstest.testbuilder.controller.JTSTestBuilderController;
import org.locationtech.jtstest.testbuilder.controller.ResultController;
import org.locationtech.jtstest.testbuilder.event.SpatialFunctionPanelEvent;
import org.locationtech.jtstest.testbuilder.event.SpatialFunctionPanelListener;
import org.locationtech.jtstest.testbuilder.model.DisplayParameters;
import org.locationtech.jtstest.testbuilder.model.GeometryEvent;
import org.locationtech.jtstest.testbuilder.model.HtmlWriter;
import org.locationtech.jtstest.testbuilder.model.JavaTestWriter;
import org.locationtech.jtstest.testbuilder.model.TestBuilderModel;
import org.locationtech.jtstest.testbuilder.model.TestCaseEdit;
import org.locationtech.jtstest.testbuilder.model.XMLTestWriter;
import org.locationtech.jtstest.testbuilder.ui.ImageUtil;
import org.locationtech.jtstest.testbuilder.ui.SwingUtil;
import org.locationtech.jtstest.testbuilder.ui.dnd.FileDrop;
import org.locationtech.jtstest.testbuilder.ui.tools.DeleteVertexTool;
import org.locationtech.jtstest.testbuilder.ui.tools.EditVertexTool;
import org.locationtech.jtstest.testbuilder.ui.tools.ExtractComponentTool;
import org.locationtech.jtstest.testbuilder.ui.tools.InfoTool;
import org.locationtech.jtstest.testbuilder.ui.tools.LineStringTool;
import org.locationtech.jtstest.testbuilder.ui.tools.PanTool;
import org.locationtech.jtstest.testbuilder.ui.tools.PointTool;
import org.locationtech.jtstest.testbuilder.ui.tools.RectangleTool;
import org.locationtech.jtstest.testbuilder.ui.tools.StreamPolygonTool;
import org.locationtech.jtstest.testbuilder.ui.tools.ZoomTool;
import org.locationtech.jtstest.testrunner.GuiUtil;
import org.locationtech.jtstest.util.FileUtil;
import org.locationtech.jtstest.util.StringUtil;


/**
 * The main frame for the JTS Test Builder.
 * 
 * @version 1.7
 */
public class JTSTestBuilderFrame extends JFrame 
{
    
  private static JTSTestBuilderFrame singleton = null;
  private ResultController resultController = new ResultController(this);
  private JTSTestBuilderMenuBar tbMenuBar = new JTSTestBuilderMenuBar(this);
  private JTSTestBuilderToolBar tbToolBar = new JTSTestBuilderToolBar(this);
  //---------------------------------------------
  JPanel contentPane;
  BorderLayout borderLayout1 = new BorderLayout();
  Border border4;
  JSplitPane jSplitPane1 = new JSplitPane();
  JPanel jPanel1 = new JPanel();
  BorderLayout borderLayout2 = new BorderLayout();
  TestCasePanel testCasePanel = new TestCasePanel();
  //this will be the 2nd panel, on the right
  TestCasePanel testCasePanel2 = new TestCasePanel(true);
  JPanel jPanel2 = new JPanel();
  JTabbedPane inputTabbedPane = new JTabbedPane();
  BorderLayout borderLayout3 = new BorderLayout();
  JPanel testPanel = new JPanel();
  WKTPanel wktPanel = new WKTPanel(this);
  InspectorPanel inspectPanel = new InspectorPanel();
  TestListPanel testListPanel = new TestListPanel(this);
  //LayerListPanel layerListPanel = new LayerListPanel();
  LayerListPanel layerListPanel = new LayerListPanel();
  GridBagLayout gridBagLayout2 = new GridBagLayout();
  GridLayout gridLayout1 = new GridLayout();
  ResultWKTPanel resultWKTPanel = new ResultWKTPanel();
  ResultValuePanel resultValuePanel = new ResultValuePanel();
  StatsPanel statsPanel = new StatsPanel();
  InfoPanel logPanel = new InfoPanel();
  //
  JTabbedPane tabbedPane = new JTabbedPane();
  MorphingGeometryOptionsPanel morphingPanel = new MorphingGeometryOptionsPanel();
  ChartsPanel chartsPanel = new ChartsPanel();
  
  private ZoomTool zoomTool;
  private final ImageIcon appIcon = new ImageIcon(this.getClass().getResource("app-icon.gif"));

  private JFileChooser fileChooser = new JFileChooser();
  private JFileChooser pngFileChooser;
  private JFileChooser fileAndDirectoryChooser = new JFileChooser();
  private JFileChooser directoryChooser = new JFileChooser();
  
  TestBuilderModel tbModel;
  TestBuilderModel tbModel2;
  
  private TestCaseTextDialog testCaseTextDlg = new TestCaseTextDialog(this,
      "", true);
  private GeometryInspectorDialog geomInspectorDlg = new GeometryInspectorDialog(this);
  /*
  private LoadTestCasesDialog loadTestCasesDlg = new LoadTestCasesDialog(this,
      "Load Test Cases", true);
*/
  
  
  /**
   *  Construct the frame
   */
  public JTSTestBuilderFrame() {
    try {
        Assert.isTrue(singleton == null);
        singleton = this;
        enableEvents(AWTEvent.WINDOW_EVENT_MASK);
        setIconImage(appIcon.getImage());
        AppCorrGeometries.getInstance().setFrame(this);
        jbInit();
        //#setRollover was introduced in Java 1.4 and is not present in 1.3.1. [Jon Aquino]
        //jToolBar1.setRollover(true);
   //     initList(tcList);
        //loadEditList(testpp);
  //      testCasePanel.setModel(tbModel);

            
        
        testCasePanel.spatialFunctionPanel.addSpatialFunctionPanelListener(
            new SpatialFunctionPanelListener() {
              public void functionExecuted(SpatialFunctionPanelEvent e) {
                  resultController.spatialFunctionPanel_functionExecuted(e);
              }
            });

        testCasePanel2.spatialFunctionPanel.addSpatialFunctionPanelListener(
            new SpatialFunctionPanelListener() {
              public void functionExecuted(SpatialFunctionPanelEvent e) {
                  resultController.spatialFunctionPanel2_functionExecuted(e);
              }
            });

        testCasePanel.scalarFunctionPanel.addSpatialFunctionPanelListener(
            new SpatialFunctionPanelListener() {
              public void functionExecuted(SpatialFunctionPanelEvent e) {
                  resultController.scalarFunctionPanel_functionExecuted(e);
              }
            });

        testCasePanel2.scalarFunctionPanel.addSpatialFunctionPanelListener(
            new SpatialFunctionPanelListener() {
              public void functionExecuted(SpatialFunctionPanelEvent e) {
                  resultController.scalarFunctionPanel2_functionExecuted(e);
              }
            });

        testCasePanel.editCtlPanel.btnSetPrecisionModel.addActionListener(
            new java.awt.event.ActionListener() {
              public void actionPerformed(ActionEvent e) {
                precisionModelMenuItem_actionPerformed(e);
              }
            });

        testCasePanel2.editCtlPanel.btnSetPrecisionModel.addActionListener(
            new java.awt.event.ActionListener() {
              public void actionPerformed(ActionEvent e) {
                precisionModelMenuItem2_actionPerformed(e);
              }
            });
        //testCasePanel.editCtlPanel.cbMagnifyTopo.addActionListener(
        testCasePanel.cbMagnifyTopo.addActionListener(
            new java.awt.event.ActionListener() {
              public void actionPerformed(ActionEvent e) {
                revealTopo_actionPerformed();
              }
            });

        testCasePanel2.cbMagnifyTopo.addActionListener(
            new java.awt.event.ActionListener() {
              public void actionPerformed(ActionEvent e) {
                revealTopo2_actionPerformed();
              }
            });
        //testCasePanel.editCtlPanel.stretchDist
        testCasePanel.spStretchDist
        .addChangeListener(new javax.swing.event.ChangeListener() {
          public void stateChanged(javax.swing.event.ChangeEvent e) {
            revealTopo_actionPerformed();
          }
        });

        testCasePanel2.spStretchDist
        .addChangeListener(new javax.swing.event.ChangeListener() {
          public void stateChanged(javax.swing.event.ChangeEvent e) {
            revealTopo2_actionPerformed();
          }
        });
        //zoom factor is changed here!
        zoomTool = new ZoomTool(2, AppCursors.ZOOM);
        showGeomsTab();
        initFileDrop(testCasePanel);
        testCasePanel.getGeometryEditPanel().setCurrentTool(RectangleTool.getInstance());
        testCasePanel2.getGeometryEditPanel().setCurrentTool(RectangleTool.getInstance());
      }
      catch (Exception e) {
        e.printStackTrace();
      }
  }

  private void initFileDrop(Component comp) {
    new FileDrop(comp, new FileDrop.Listener() {
      public void filesDropped(java.io.File[] files) {
        try {
          openXmlFilesAndDirectories(files);
        } catch (Exception ex) {
          SwingUtil.reportException(null, ex);
        }
      }
    });
  }
  private void initFileChoosers() {
    if (pngFileChooser == null) {
      pngFileChooser = new JFileChooser();
      pngFileChooser.addChoosableFileFilter(SwingUtil.PNG_FILE_FILTER);
      pngFileChooser.setDialogTitle("Save PNG");
      pngFileChooser.setSelectedFile(new File("geoms.png"));
    }
  }
  
    public static JTSTestBuilderFrame instance() {
        if (singleton == null) {
          new JTSTestBuilderFrame();
        }
        return singleton;
    }

    public static GeometryEditPanel getGeometryEditPanel()
    {
        return instance().getTestCasePanel().getGeometryEditPanel();
    }
    
    public static GeometryEditPanel getGeometryEditPanel2()
    {
        return instance().getTestCasePanel2().getGeometryEditPanel();
    }
    
    public static GeometryEditPanel getGeometryEditPanelMouseIsIn(){
        if (isMouseWithinComponent(instance().getTestCasePanel2())){
            return instance().getTestCasePanel2().getGeometryEditPanel();
        }
        else{
            return instance().getTestCasePanel().getGeometryEditPanel();
        }
    }
    
    public static GeometryEditPanel getOtherGeometryEditPanel(GeometryEditPanel editPanel){
        if (editPanel.equals(instance().getTestCasePanel().getGeometryEditPanel())){
            return instance().getTestCasePanel2().getGeometryEditPanel();
        }
        return instance().getTestCasePanel().getGeometryEditPanel();
    }
    
    public static boolean isMouseWithinComponent(Component c)
    {
        java.awt.Point mousePos = new java.awt.Point(MouseInfo.getPointerInfo().getLocation());
        Rectangle bounds = c.getBounds();
        bounds.setLocation(c.getLocationOnScreen());
        return bounds.contains(mousePos);
    }
  
    public TestBuilderModel getModel()
    {
      return tbModel;
    }

    public TestBuilderModel getModel2()
    {
      return tbModel2;
    }

    public void setModel(TestBuilderModel model, TestBuilderModel model2)
    {
      tbModel = model;
      tbModel2 = model2;
      testCasePanel.setModel(tbModel);
      testCasePanel2.setModel(tbModel2);
      wktPanel.setModel(model);
      inspectPanel.setModel(model);
      resultWKTPanel.setModel(model);
      resultValuePanel.setModel(model);
      statsPanel.setModel(model);

      model.getGeometryEditModel().addGeometryListener(
          new org.locationtech.jtstest.testbuilder.model.GeometryListener() {
            public void geometryChanged(GeometryEvent e) {
              model_geometryChanged(e);
            }
          });
      model2.getGeometryEditModel().addGeometryListener(
          new org.locationtech.jtstest.testbuilder.model.GeometryListener() {
            public void geometryChanged(GeometryEvent e) {
              model2_geometryChanged(e);
            }
          });

      testListPanel.populateList();
      //layerListPanel.init(getModel().getLayers());
      layerListPanel.populateList();
      updateTestCaseView();
      updatePrecisionModelDescription();
    }

    public static void reportException(Exception e) {
          SwingUtil.reportException(instance(), e);
    }

    public void setCurrentTestCase(TestCaseEdit testCase) {
      tbModel.cases().setCurrent(testCase);
      tbModel2.cases().setCurrent(testCase);
      updateTestCaseView();
      JTSTestBuilderController.zoomToInput();
    }

    public TestCasePanel getTestCasePanel() {
      return testCasePanel;
    }
    public TestCasePanel getTestCasePanel2() {
      return testCasePanel2;
    }

    public ResultWKTPanel getResultWKTPanel() {
      return resultWKTPanel;
    }

    public ResultValuePanel getResultValuePanel() {
      return resultValuePanel;
    }

    /**
     *  File | Exit action performed
     */
    public void jMenuFileExit_actionPerformed(ActionEvent e) {
      System.exit(0);
    }

    /**
     *  Help | About action performed
     */
    public void jMenuHelpAbout_actionPerformed(ActionEvent e) {
      JTSTestBuilder_AboutBox dlg = new JTSTestBuilder_AboutBox(this);
      java.awt.Dimension dlgSize = dlg.getPreferredSize();
      java.awt.Dimension frmSize = getSize();
      java.awt.Point loc = getLocation();
      dlg.setLocation((frmSize.width - dlgSize.width) / 2 + loc.x, (frmSize.height
           - dlgSize.height) / 2 + loc.y);
      dlg.setModal(true);
      dlg.setVisible(true);
    }

    public void showTab(String name)
    {
      inputTabbedPane.setSelectedIndex(inputTabbedPane.indexOfTab(name));
    }

    public void showGeomsTab()
    {
      showTab(AppStrings.TAB_LABEL_INPUT);
    }

    public void showResultWKTTab()
    {
      showTab(AppStrings.TAB_LABEL_RESULT);
    }
    public void showResultValueTab()
    {
      showTab(AppStrings.TAB_LABEL_VALUE);
    }

    public void showInfoTab()
    {
      showTab(AppStrings.TAB_LABEL_LOG);
    }

    public void openXmlFilesAndDirectories(File[] files) throws Exception {
      if (files.length == 1) {
        fileChooser.setSelectedFile(files[0]);
      }
      tbModel.openXmlFilesAndDirectories(files);
      reportProblemsParsingXmlTestFile(tbModel.getParsingProblems());
      updateTestCaseView();
      testListPanel.populateList();
      updatePrecisionModelDescription();
      JTSTestBuilderController.zoomToInput();
    }

    /**
     *  Overridden so we can exit when window is closed
     */
    protected void processWindowEvent(WindowEvent e) {
      super.processWindowEvent(e);
      if (e.getID() == WindowEvent.WINDOW_CLOSING) {
        jMenuFileExit_actionPerformed(null);
      }
    }

    void model_geometryChanged(GeometryEvent e) {
      //testCasePanel.relatePanel.clearResults();
      JTSTestBuilderController.geometryViewChanged();
      updateWktPanel();
    }
    void model2_geometryChanged(GeometryEvent e) {
      //testCasePanel.relatePanel.clearResults();
      JTSTestBuilderController.geometryViewChanged2();
      updateWktPanel();
    }

    void createNewCase() {
      tbModel.cases().createNew();
      tbModel2.cases().createNew();
      showGeomsTab();
      updateTestCases();
    }

    /*void moveToPrevCase(boolean isZoom) {
      tbModel2.cases().prevCase();
      updateTestCaseView();
      if (isZoom) JTSTestBuilderController.zoomToInput();
    }*/

    void moveToNextImage(){
        boolean lastImage = AppImage.getInstance().loadNextImage();
        this.reloadBothPanels();
        if (lastImage){
            tbToolBar.disableNextBtn();
        }
        if (!tbToolBar.isPreviousBtnActivated()){
            tbToolBar.enablePreviousBtn();
        }
    }

    void moveToPreviousImage(){
        boolean firstImage = AppImage.getInstance().loadPreviousImage();
        this.reloadBothPanels();
        if (firstImage){
            tbToolBar.disablePreviousBtn();
        }
        if (!tbToolBar.isNextBtnActivated()){
            tbToolBar.enableNextBtn();
        }
    }

    public void reloadBothPanels(){
        getTestCasePanel().getGeometryEditPanel().cleanAndDrawGeometry();
        getTestCasePanel2().getGeometryEditPanel().cleanAndDrawGeometry();
        getTestCasePanel().getGeometryEditPanel().forceRepaint();
        getTestCasePanel2().getGeometryEditPanel().forceRepaint();
    }
    
    //select the image i in the list of images and selects the image i+1 for the panel 2.
    void movePanel1ToImage(int i){
        boolean imageChanged = AppImage.getInstance().imageExistForPanel1(i);
        if (imageChanged){
            this.reloadBothPanels();
            if (AppImage.getInstance().isLastImageForPanel1()){
                tbToolBar.disableNextBtn();
            }
            else{
                tbToolBar.enableNextBtn();
            }
            if (AppImage.getInstance().isFirstImageForPanel1()){
                tbToolBar.disablePreviousBtn();
            }
            else{
                tbToolBar.enablePreviousBtn();
            }
        }
    }
    
    //select the image i in the list of images and selects the image i+1 for the panel 2.
    void movePanel2ToImage(int i){
        boolean imageChanged = AppImage.getInstance().imageExistForPanel2(i);
        if (imageChanged){
            this.reloadBothPanels();
            if (AppImage.getInstance().isLastImageForPanel2()){
                tbToolBar.disableNextBtn();
            }
            else{
                tbToolBar.enableNextBtn();
            }
            if (AppImage.getInstance().isFirstImageForPanel2()){
                tbToolBar.disablePreviousBtn();
            }
            else{
                tbToolBar.enablePreviousBtn();
            }
        }
    }

    /*void moveToNextCase(boolean isZoom) {
      tbModel.cases().nextCase();
      tbModel2.cases().nextCase();
      updateTestCaseView();
      if (isZoom) JTSTestBuilderController.zoomToInput();
    }*/

    void copyCase() {
      tbModel.cases().copyCase();
      tbModel2.cases().copyCase();
      updateTestCases();
    }
    TestCaseEdit currentCase() {
      return tbModel.cases().getCurrentCase();
    }
    TestCaseEdit currentCase2() {
      return tbModel2.cases().getCurrentCase();
    }
    public void updateTestCases()
    {
      testListPanel.populateList();    
      updateTestCaseView();
    }

    public void copyResultToTest() 
    {
      Object currResult = tbModel.getResult();
      if (! (currResult instanceof Geometry))
        return;
      tbModel.addCase(new Geometry[] { (Geometry) currResult, null }, 
                  "Result of " + tbModel.getOpName());
      updateTestCaseView();
      testListPanel.populateList();  
    }

    public void actionExchangeGeoms() {
      currentCase().exchange();
      testCasePanel.setTestCase(currentCase());
      currentCase2().exchange();
      testCasePanel2.setTestCase(currentCase2());
    }

    void btnDeleteCase_actionPerformed(ActionEvent e) {
      tbModel.cases().deleteCase();
      tbModel2.cases().deleteCase();
      updateTestCaseView();
      testListPanel.populateList();
    }

    /*
    void menuLoadTestCases_actionPerformed(ActionEvent e) {
      try {
        loadTestCasesDlg.show();
        TestCaseList tcl = loadTestCasesDlg.getList();
        loadTestCaseList(tcl, new PrecisionModel());
        refreshNavBar();
      }
      catch (Exception x) {
        reportException(this, x);
      }
    }

    void loadTestCaseList(TestCaseList tcl, PrecisionModel precisionModel) throws Exception {
      tbModel.setPrecisionModel(precisionModel);
      if (tcl != null) {
        loadEditList(tcl);
      }
      testListPanel.populateList();
    }
  */

    void menuExchangeGeom_actionPerformed(ActionEvent e) {
      currentCase().exchange();
      testCasePanel.setTestCase(currentCase());
    }

    void menuViewText_actionPerformed(ActionEvent e) {
      testCaseTextDlg.setTestCase(currentCase());
      testCaseTextDlg.setVisible(true);
    }

    public void actionInspectGeometry() {
      int geomIndex = tbModel.getGeometryEditModel().getGeomIndex();
      String tag = geomIndex == 0 ? AppStrings.GEOM_LABEL_A : AppStrings.GEOM_LABEL_B;
      Geometry geometry = currentCase().getGeometry(geomIndex);
      inspectPanel.setGeometry( tag, geometry, geomIndex);
      showTab(AppStrings.TAB_LABEL_INSPECT);
      /*
      geomInspectorDlg.setGeometry(
          geomIndex == 0 ? AppStrings.GEOM_LABEL_A : AppStrings.GEOM_LABEL_B,
          tbModel.getCurrentTestCaseEdit().getGeometry(geomIndex));
          */
      //geomInspectorDlg.setVisible(true);
    }

    public void actionInspectGeometryDialog() {
      int geomIndex = tbModel.getGeometryEditModel().getGeomIndex();
      String tag = geomIndex == 0 ? AppStrings.GEOM_LABEL_A : AppStrings.GEOM_LABEL_B;
      Geometry geometry = currentCase().getGeometry(geomIndex);
      geomInspectorDlg.setGeometry(tag, geometry);
      geomInspectorDlg.setVisible(true);
    }
    
    void menuLoadCorrFilesFolder_actionPerformed(ActionEvent e) {
      try {
        fileChooser.removeChoosableFileFilter(SwingUtil.JAVA_FILE_FILTER);
        FileNameExtensionFilter filter = new FileNameExtensionFilter("wkt, corr", "corr", "wkt");
        fileChooser.addChoosableFileFilter(filter);
        fileChooser.addChoosableFileFilter(SwingUtil.XML_FILE_FILTER);
        fileChooser.setDialogTitle("Open Folder with Corr File(s)");
        fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        fileChooser.setMultiSelectionEnabled(false);
        if (JFileChooser.APPROVE_OPTION == fileChooser.showOpenDialog(this)) {
          File[] files = fileChooser.getSelectedFile().listFiles();
          if (files.length == 0) {
              //no files in directory!
            JOptionPane.showMessageDialog(this, "The indicated folder is empty!\n No files were loaded.", "Warning", JOptionPane.WARNING_MESSAGE);
            return;
          }
          AppImage.getInstance().setAndLoadCorrDirFiles(fileChooser.getSelectedFile());
          this.reloadBothPanels();
        }
      }
      catch (Exception x) {
        SwingUtil.reportException(this, x);
      }
    }

    void menuLoadXmlTestFile_actionPerformed(ActionEvent e) {
      try {
        fileChooser.removeChoosableFileFilter(SwingUtil.JAVA_FILE_FILTER);
        fileChooser.addChoosableFileFilter(SwingUtil.XML_FILE_FILTER);
        fileChooser.setDialogTitle("Open XML Test File(s)");
        fileChooser.setMultiSelectionEnabled(true);
        if (JFileChooser.APPROVE_OPTION == fileChooser.showOpenDialog(this)) {
          File[] files = fileChooser.getSelectedFiles();
          if (files.length == 0) {
            files = new File[]{fileChooser.getSelectedFile()};
          }
          openXmlFilesAndDirectories(files);
        }
      }
      catch (Exception x) {
        SwingUtil.reportException(this, x);
      }
    }

    void menuSaveAsXml_actionPerformed(ActionEvent e) {
      try {
        fileChooser.removeChoosableFileFilter(SwingUtil.JAVA_FILE_FILTER);
        fileChooser.addChoosableFileFilter(SwingUtil.XML_FILE_FILTER);
        fileChooser.setDialogTitle("Save XML Test File");
        if (JFileChooser.APPROVE_OPTION == fileChooser.showSaveDialog(this)) {
          File file = fileChooser.getSelectedFile();
          if (! SwingUtil.confirmOverwrite(this, file)) return;
          FileUtil.setContents(fileChooser.getSelectedFile().getPath(), 
                          XMLTestWriter.getRunXml(tbModel.getTestCaseList(), tbModel.getPrecisionModel()) );
        }
      }
      catch (Exception x) {
        SwingUtil.reportException(this, x);
      }
    }

    public String getRunXml() 
    {
          return XMLTestWriter.getRunXml(tbModel.getTestCaseList(), tbModel.getPrecisionModel());
    }

    void menuSaveAsJava_actionPerformed(ActionEvent e) {
      try {
        fileChooser.removeChoosableFileFilter(SwingUtil.XML_FILE_FILTER);
        fileChooser.addChoosableFileFilter(SwingUtil.JAVA_FILE_FILTER);
        fileChooser.setDialogTitle("Save Java File");
        if (JFileChooser.APPROVE_OPTION == fileChooser.showSaveDialog(this)) {
          File file = fileChooser.getSelectedFile();
          if (! SwingUtil.confirmOverwrite(this, file)) return;
          String className = fileChooser.getSelectedFile().getName();
          int extensionIndex = className.lastIndexOf(".");
          if (extensionIndex > 0) {
            className = className.substring(0, extensionIndex);
          }
          ;
          FileUtil.setContents(fileChooser.getSelectedFile().getPath(), JavaTestWriter.getRunJava(className, tbModel));
        }
      }
      catch (Exception x) {
        SwingUtil.reportException(this, x);
      }
    }

    void menuSaveAsHtml_actionPerformed(ActionEvent e) {
      try {
        directoryChooser.setDialogTitle("Select Folder In Which To Save HTML and GIF Files");
        if (JFileChooser.APPROVE_OPTION == directoryChooser.showSaveDialog(this)) {
          int choice = JOptionPane.showConfirmDialog(this,
              "Would you like the spatial function images "
               + "to show the A and B geometries?", "Confirmation",
              JOptionPane.YES_NO_CANCEL_OPTION);
          final HtmlWriter writer = new HtmlWriter();
          switch (choice) {
            case JOptionPane.CANCEL_OPTION:
              return;
            case JOptionPane.YES_OPTION:
              writer.setShowingABwithSpatialFunction(true);
              break;
            case JOptionPane.NO_OPTION:
              writer.setShowingABwithSpatialFunction(false);
              break;
          }
          final File directory = directoryChooser.getSelectedFile();
          Assert.isTrue(directory.exists());
          //        BusyDialog.setOwner(this);
          //        BusyDialog busyDialog = new BusyDialog();
          //        writer.setBusyDialog(busyDialog);
          //        try {
          //          busyDialog.execute("Saving .html and .gif files", new BusyDialog.Executable() {
          //            public void execute() throws Exception {
          writer.write(directory, tbModel.getTestCaseList(), tbModel.getPrecisionModel());
          //            }
          //          });
          //        }
          //        catch (Exception e2) {
          //          System.out.println(busyDialog.getStackTrace());
          //          throw e2;
          //        }
        }
      }
      catch (Exception x) {
        SwingUtil.reportException(this, x);
      }
    }

    void menuSaveAsPNG_actionPerformed(ActionEvent e) {
      initFileChoosers();
      try {
        String fullFileName = SwingUtil.chooseFilenameWithConfirm(this, pngFileChooser);  
        if (fullFileName == null) return;
          ImageUtil.writeImage(testCasePanel.getGeometryEditPanel(), 
              fullFileName,
              ImageUtil.IMAGE_FORMAT_NAME_PNG);
      }
      catch (Exception x) {
        SwingUtil.reportException(this, x);
      }
    }

    void menuSaveScreenToClipboard_actionPerformed(ActionEvent e) {
      try {
          ImageUtil.saveImageToClipboard(testCasePanel.getGeometryEditPanel(), 
                          ImageUtil.IMAGE_FORMAT_NAME_PNG);
      }
      catch (Exception x) {
        SwingUtil.reportException(this, x);
      }
    }

    void drawRectangleButton_actionPerformed(ActionEvent e) {
      testCasePanel2.getGeometryEditPanel().setCurrentTool(RectangleTool.getInstance());
      testCasePanel.getGeometryEditPanel().setCurrentTool(RectangleTool.getInstance());
    }

    void drawPolygonButton_actionPerformed(ActionEvent e) {
      testCasePanel.getGeometryEditPanel().setCurrentTool(StreamPolygonTool.getInstance());
      testCasePanel2.getGeometryEditPanel().setCurrentTool(StreamPolygonTool.getInstance());
    }

    void drawLineStringButton_actionPerformed(ActionEvent e) {
      testCasePanel.getGeometryEditPanel().setCurrentTool(LineStringTool.getInstance());
      testCasePanel2.getGeometryEditPanel().setCurrentTool(LineStringTool.getInstance());
    }

    void drawPointButton_actionPerformed(ActionEvent e) {
      testCasePanel.getGeometryEditPanel().setCurrentTool(PointTool.getInstance());
      testCasePanel2.getGeometryEditPanel().setCurrentTool(PointTool.getInstance());
    }

    void infoButton_actionPerformed() {
      testCasePanel.getGeometryEditPanel().setCurrentTool(InfoTool.getInstance());
      testCasePanel2.getGeometryEditPanel().setCurrentTool(InfoTool.getInstance());
    }

    void actionExtractComponentButton() {
      testCasePanel.getGeometryEditPanel().setCurrentTool(ExtractComponentTool.getInstance());
      testCasePanel2.getGeometryEditPanel().setCurrentTool(ExtractComponentTool.getInstance());
    }

    void actionDeleteVertexButton() {
      testCasePanel.getGeometryEditPanel().setCurrentTool(DeleteVertexTool.getInstance());
      testCasePanel2.getGeometryEditPanel().setCurrentTool(DeleteVertexTool.getInstance());
    }

    void zoomInButton_actionPerformed(ActionEvent e) {
        testCasePanel2.getGeometryEditPanel().setCurrentTool(zoomTool);
        testCasePanel.getGeometryEditPanel().setCurrentTool(zoomTool);
    }

    void oneToOneButton_actionPerformed(ActionEvent e) {
        resetZoom();
    }

    void zoomToFullExtentButton_actionPerformed(ActionEvent e) {
      testCasePanel.getGeometryEditPanel().zoomToFullExtent();
    }

    void zoomToResult_actionPerformed(ActionEvent e) {
      testCasePanel.getGeometryEditPanel().zoomToResult();
    }

    void zoomToInputButton_actionPerformed(ActionEvent e) {
      testCasePanel.getGeometryEditPanel().zoomToInput();
    }

    void zoomToInputA_actionPerformed(ActionEvent e) {
      testCasePanel.getGeometryEditPanel().zoomToGeometry(0);
    }

    void zoomToInputB_actionPerformed(ActionEvent e) {
      testCasePanel.getGeometryEditPanel().zoomToGeometry(1);
      testCasePanel.getGeometryEditPanel().zoomToFullExtent();
    }

    void panButton_actionPerformed(ActionEvent e) {
      testCasePanel.getGeometryEditPanel().setCurrentTool(PanTool.getInstance());
      testCasePanel2.getGeometryEditPanel().setCurrentTool(PanTool.getInstance());
    }

    void deleteAllTestCasesMenuItem_actionPerformed(ActionEvent e) {
      tbModel.cases().init();
      tbModel2.cases().init();
      updateTestCaseView();
      testListPanel.populateList();
    }

    public void setShowingGrid(boolean showGrid) {
      testCasePanel.editPanel.setGridEnabled(showGrid);
      JTSTestBuilderController.geometryViewChanged();
    }

    void showVertexIndicesMenuItem_actionPerformed(ActionEvent e) {
  //    testCasePanel.editPanel.setShowVertexIndices(showVertexIndicesMenuItem.isSelected());
    }

    void menuLoadXmlTestFolder_actionPerformed(ActionEvent e) {
      try {
        directoryChooser.removeChoosableFileFilter(SwingUtil.JAVA_FILE_FILTER);
        directoryChooser.setDialogTitle("Open Folder(s) Containing XML Test Files");
        directoryChooser.setMultiSelectionEnabled(true);
        if (JFileChooser.APPROVE_OPTION == directoryChooser.showOpenDialog(this)) {
          File[] files = directoryChooser.getSelectedFiles();
          if (files.length == 0) {
            files = new File[]{fileChooser.getSelectedFile()};
          }
          openXmlFilesAndDirectories(files);
        }
      }
      catch (Exception x) {
        SwingUtil.reportException(this, x);
      }
    }

    void precisionModelMenuItem_actionPerformed(ActionEvent e) {
      try {
        PrecisionModelDialog precisionModelDialog = new PrecisionModelDialog(
            this, "Edit Precision Model", true);
        GuiUtil.center(precisionModelDialog, this);
        precisionModelDialog.setPrecisionModel(tbModel.getPrecisionModel());
        precisionModelDialog.setVisible(true);
        tbModel.changePrecisionModel(precisionModelDialog.getPrecisionModel());
        updatePrecisionModelDescription();
        updateGeometry();
      }
      catch (ParseException pe) {
        SwingUtil.reportException(this, pe);
      }
    }

    void precisionModelMenuItem2_actionPerformed(ActionEvent e) {
      try {
        PrecisionModelDialog precisionModelDialog = new PrecisionModelDialog(
            this, "Edit Precision Model", true);
        GuiUtil.center(precisionModelDialog, this);
        precisionModelDialog.setPrecisionModel(tbModel2.getPrecisionModel());
        precisionModelDialog.setVisible(true);
        tbModel2.changePrecisionModel(precisionModelDialog.getPrecisionModel());
        updatePrecisionModelDescription();
        updateGeometry2();
      }
      catch (ParseException pe) {
        SwingUtil.reportException(this, pe);
      }
    }

    void revealTopo_actionPerformed() {
      DisplayParameters.setMagnifyingTopology(testCasePanel.cbMagnifyTopo.isSelected());
      DisplayParameters.setTopologyStretchSize(testCasePanel.getStretchSize());
      //tbModel.setMagnifyingTopology(testCasePanel.editCtlPanel.cbMagnifyTopo.isSelected());
      //tbModel.setTopologyStretchSize(testCasePanel.editCtlPanel.getStretchSize());
      JTSTestBuilderController.geometryViewChanged();
    }
    void revealTopo2_actionPerformed() {
      DisplayParameters.setMagnifyingTopology(testCasePanel2.cbMagnifyTopo.isSelected());
      DisplayParameters.setTopologyStretchSize(testCasePanel2.getStretchSize());
      //tbModel.setMagnifyingTopology(testCasePanel.editCtlPanel.cbMagnifyTopo.isSelected());
      //tbModel.setTopologyStretchSize(testCasePanel.editCtlPanel.getStretchSize());
      JTSTestBuilderController.geometryViewChanged2();
    }


    /**
     *  Component initialization
     */
    private void jbInit() throws Exception {
      fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
      fileChooser.setMultiSelectionEnabled(false);
      fileAndDirectoryChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
      fileAndDirectoryChooser.setMultiSelectionEnabled(true);
      directoryChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
      directoryChooser.setMultiSelectionEnabled(false);
      //Center the window
      Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();

      //---------------------------------------------------
      contentPane = (JPanel) this.getContentPane();
      border4 = BorderFactory.createBevelBorder(BevelBorder.LOWERED, Color.white,
          Color.white, new Color(93, 93, 93), new Color(134, 134, 134));
      contentPane.setLayout(borderLayout1);
      this.setSize(new Dimension(screenSize.width, screenSize.height));
      this.setTitle("JTS TestBuilder");
      //start JFrame maximized
      setExtendedState(java.awt.Frame.MAXIMIZED_BOTH);

      /*
      testCasePanel.editPanel.addGeometryListener(
        new com.vividsolutions.jtstest.testbuilder.model.GeometryListener() {

          public void geometryChanged(GeometryEvent e) {
            editPanel_geometryChanged(e);
          }
        });
  */    
    
    jSplitPane1.setOrientation(JSplitPane.VERTICAL_SPLIT);
    jSplitPane1.setPreferredSize(new Dimension(601, 690));
    //top panel (top half of window)
    jPanel1.setLayout(new GridLayout(1, 2));
    //jPanel1.setMinimumSize(new Dimension(431, 0));
    contentPane.setPreferredSize(new Dimension(601, 690));
    //panel with statistics and the buttons to swith statistics
    inputTabbedPane.setTabPlacement(JTabbedPane.LEFT);
    jPanel2.setLayout(borderLayout3);
    wktPanel.setMinimumSize(new Dimension(111, 0));
    wktPanel.setPreferredSize(new Dimension(600, 100));
    wktPanel.setToolTipText(AppStrings.TIP_TEXT_ENTRY);
    testPanel.setLayout(gridBagLayout2);
    gridLayout1.setRows(4);
    gridLayout1.setColumns(1);
    
    contentPane.add(jSplitPane1, BorderLayout.CENTER);
    jSplitPane1.add(jPanel1, JSplitPane.TOP);
    jPanel1.add(testCasePanel);
    jPanel1.add(testCasePanel2);
    
    //try to add tabbed pane with the jpanel2
    jSplitPane1.add(tabbedPane, JSplitPane.BOTTOM);
    
    //load the icons for the tabs
    ImageIcon wktPanelIcon = new ImageIcon(this.getClass().getResource("wkt_info_panel.png"));
    ImageIcon morphingIcon = new ImageIcon(this.getClass().getResource("morphing_icon.png"));
    tabbedPane.addTab("WKT Panel", wktPanelIcon, jPanel2, "WKT Panel and other related operations");

    tabbedPane.addTab("Morphing", morphingIcon, morphingPanel, "Morphing for the geometries shown above");
    
    tabbedPane.addTab("Charts", morphingIcon, chartsPanel, "Morphing for the geometries shown above");
    
    //previously, before the tabbed pane:
    //jSplitPane1.add(jPanel2, JSplitPane.BOTTOM);
    
    jPanel2.add(tbToolBar.getToolBar(), BorderLayout.NORTH);
    //jPanel2 contains the wkt panel results and other statistics (bottom)
    jPanel2.add(inputTabbedPane, BorderLayout.CENTER);
    jSplitPane1.setBorder(new EmptyBorder(2,2,2,2));
    jSplitPane1.setResizeWeight(0.5);
    inputTabbedPane.add(testListPanel, AppStrings.TAB_LABEL_CASES);
    inputTabbedPane.add(wktPanel,  AppStrings.TAB_LABEL_INPUT);
    inputTabbedPane.add(resultWKTPanel, AppStrings.TAB_LABEL_RESULT);
    inputTabbedPane.add(resultValuePanel, AppStrings.TAB_LABEL_VALUE);
    inputTabbedPane.add(inspectPanel,  AppStrings.TAB_LABEL_INSPECT);
    inputTabbedPane.add(statsPanel, AppStrings.TAB_LABEL_STATS);
    inputTabbedPane.add(logPanel, AppStrings.TAB_LABEL_LOG);
    inputTabbedPane.add(layerListPanel, AppStrings.TAB_LABEL_LAYERS);
    inputTabbedPane.setSelectedIndex(1);
    inputTabbedPane.addChangeListener(new ChangeListener() {
      public void stateChanged(ChangeEvent e)
      {
        updateStatsPanelIfVisible();
        }
    });
    
    jSplitPane1.setDividerLocation(500);
    this.setJMenuBar(tbMenuBar.getMenuBar());
    //contentPane.add(tbToolBar.getToolBar(), BorderLayout.NORTH);   
    
    
    }
  
  

    public JTSTestBuilderToolBar getToolbar()
    {
      return tbToolBar;
    }

    private void updateStatsPanelIfVisible()
    {
      int index = inputTabbedPane.getSelectedIndex();
      if (index < 0) return;
      if (inputTabbedPane.getComponent(index) == statsPanel) {
        statsPanel.refresh();         
      }   
    }

    private void updateGeometry() {
      testCasePanel.relatePanel.clearResults();
      testCasePanel.setTestCase(currentCase());
      updateWktPanel();
    }
    private void updateGeometry2() {
      testCasePanel2.relatePanel.clearResults();
      testCasePanel2.setTestCase(currentCase2());
      //updateWktPanel();
    }

    private void updateWktPanel() {
      try{
          Geometry g0 = tbModel.getGeometryEditModel().getGeometry(0);
          wktPanel.setText(g0, 0);
          Geometry g1 = tbModel2.getGeometryEditModel().getGeometry(0);
          wktPanel.setText(g1, 1);
      } catch (NullPointerException e) {}

    }

    private void updatePrecisionModelDescription() {
      testCasePanel.setPrecisionModelDescription(tbModel.getPrecisionModel().toString());
      testCasePanel2.setPrecisionModelDescription(tbModel2.getPrecisionModel().toString());
    }

    public void updateTestCaseView() {
      testCasePanel.setTestCase(currentCase());
      getTestCasePanel().setCurrentTestCaseIndex(tbModel.getCurrentCaseIndex() + 1);
      getTestCasePanel().setMaxTestCaseIndex(tbModel.getCasesSize());
      testCasePanel2.setTestCase(currentCase2());
      getTestCasePanel2().setCurrentTestCaseIndex(tbModel2.getCurrentCaseIndex() + 1);
      getTestCasePanel2().setMaxTestCaseIndex(tbModel2.getCasesSize());
      updateWktPanel();
      updateStatsPanelIfVisible();
    }

    public void displayInfo(Coordinate modelPt)
    {
        displayInfo(testCasePanel.getGeometryEditPanel().getInfo(modelPt));
    }
  
  public void displayInfo(String s)
  {
    displayInfo(s, true);
  }
  
  public void displayInfo(String s, boolean showTab)
  {
    logPanel.addInfo(s);
    if (showTab) showInfoTab();
  }
  
  private void reportProblemsParsingXmlTestFile(List parsingProblems) {
    if (parsingProblems.isEmpty()) {
      return;
    }
    for (Iterator i = parsingProblems.iterator(); i.hasNext(); ) {
      String problem = (String) i.next();
      System.out.println(problem);
    }
    JOptionPane.showMessageDialog(this, StringUtil.wrap(parsingProblems.size()
         + " problems occurred parsing the XML test file."
         + " The first problem was: " + parsingProblems.get(0), 80),
        "Error", JOptionPane.ERROR_MESSAGE);
  }

  void menuRemoveDuplicatePoints_actionPerformed(ActionEvent e) {
    CleanDuplicatePoints clean = new CleanDuplicatePoints();
    Geometry cleanGeom = clean.clean(tbModel.getGeometryEditModel().getGeometry(0));
    currentCase().setGeometry(0, cleanGeom);
    updateGeometry();
  }

  void menuChangeToLines_actionPerformed(ActionEvent e) {
    Geometry cleanGeom = LinearComponentExtracter.getGeometry(tbModel.getGeometryEditModel().getGeometry(0));
    currentCase().setGeometry(0, cleanGeom);
    updateGeometry();
  }

  void btnEditVertex_actionPerformed(ActionEvent e) {
    testCasePanel.getGeometryEditPanel().setCurrentTool(EditVertexTool.getInstance());
    testCasePanel2.getGeometryEditPanel().setCurrentTool(EditVertexTool.getInstance());
  }
  
  void btnShowHideGrid_actionPerformed(ActionEvent e) {
      //show or hide the grid
    getGeometryEditPanel().getGridRenderer().swithEnabled();
    //update ui
    getGeometryEditPanel().forceRepaint();
  }

  private Coordinate pickOffset(Geometry a, Geometry b) {
    if (a != null && ! a.isEmpty()) {
      return a.getCoordinates()[0];
    }
    if (b != null && ! b.isEmpty()) {
      return b.getCoordinates()[0];
    }
    return null;
  }
  
    public void resetZoom(){
        testCasePanel.getGeometryEditPanel().getViewport().zoomToInitialExtent();
        testCasePanel2.getGeometryEditPanel().getViewport().zoomToInitialExtent();
    }


}

