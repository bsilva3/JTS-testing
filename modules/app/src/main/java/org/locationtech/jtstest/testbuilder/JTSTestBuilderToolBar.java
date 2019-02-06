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

import java.awt.Dimension;
import java.awt.Insets;
import java.awt.event.ActionEvent;

import javax.swing.Box;
import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JSpinner;
import javax.swing.JTextField;
import javax.swing.JToggleButton;
import javax.swing.JToolBar;
import javax.swing.SpinnerModel;
import javax.swing.SpinnerNumberModel;
import javax.swing.SwingConstants;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

public class JTSTestBuilderToolBar {


  JTSTestBuilderFrame tbFrame;

  JToolBar jToolBar1 = new JToolBar();
  JButton previousButton = new JButton();
  SpinnerModel sm;
  SpinnerModel sm2;
  JLabel labelForImageNumberPanel1 = new JLabel();
  JSpinner panel1ImageNumber;//image number on panel 1
  JLabel labelForImageNumberPanel2 = new JLabel();
  JSpinner panel2ImageNumber;//image number on panel 2
  JLabel totalImages = new JLabel();//a number with the total number of images in the directory (i.e. loaded to memory)
  JButton nextButton = new JButton();
  JButton newButton = new JButton();
  JButton copyButton = new JButton();
  JButton deleteButton = new JButton();
  JButton exchangeButton = new JButton();

  JButton oneToOneButton = new JButton();
  JButton zoomToFullExtentButton = new JButton();
  JButton zoomToInputButton = new JButton();
  JButton zoomToInputAButton = new JButton();
  JButton zoomToInputBButton = new JButton();
  JButton zoomToResultButton = new JButton();
  
  JToggleButton drawRectangleButton = new JToggleButton();
  JToggleButton drawPolygonButton = new JToggleButton();
  JToggleButton drawLineStringButton = new JToggleButton();
  JToggleButton drawPointButton = new JToggleButton();
  JToggleButton zoomButton = new JToggleButton();
  JToggleButton infoButton = new JToggleButton();
  JToggleButton panButton = new JToggleButton();
  JToggleButton btnEditVertex = new JToggleButton();
  JToggleButton btnShowHideGrid = new JToggleButton();
  JToggleButton extractComponentButton;
  ButtonGroup toolButtonGroup = new ButtonGroup();

  private final ImageIcon leftIcon = new ImageIcon(this.getClass().getResource("Left.png"));
  private final ImageIcon rightIcon = new ImageIcon(this.getClass().getResource("Right.png"));
  private final ImageIcon plusIcon = new ImageIcon(this.getClass().getResource("Plus.png"));
  private final ImageIcon copyCaseIcon = new ImageIcon(this.getClass().getResource("CopyCase.png"));
  private final ImageIcon deleteIcon = new ImageIcon(this.getClass().getResource("Delete.png"));
  private final ImageIcon zoomIcon = new ImageIcon(this.getClass().getResource("MagnifyCursor.gif"));
  private final ImageIcon drawRectangleIcon = new ImageIcon(this.getClass().getResource("DrawRectangle.png"));
  private final ImageIcon drawRectangleBIcon = new ImageIcon(this.getClass().getResource("DrawRectangleB.png"));
  private final ImageIcon drawPolygonIcon = new ImageIcon(this.getClass().getResource("DrawPolygon.png"));
  private final ImageIcon drawPolygonBIcon = new ImageIcon(this.getClass().getResource("DrawPolygonB.png"));
  private final ImageIcon drawLineStringIcon = new ImageIcon(this.getClass().getResource("DrawLineString.png"));
  private final ImageIcon drawLineStringBIcon = new ImageIcon(this.getClass().getResource("DrawLineStringB.png"));
  private final ImageIcon drawPointIcon = new ImageIcon(this.getClass().getResource("DrawPoint.png"));
  private final ImageIcon drawPointBIcon = new ImageIcon(this.getClass().getResource("DrawPointB.png"));
  private final ImageIcon infoIcon = new ImageIcon(this.getClass().getResource("Info.png"));
  private final ImageIcon zoomOneToOneIcon = new ImageIcon(this.getClass().getResource("ZoomOneToOne.png"));
  private final ImageIcon zoomToInputIcon = new ImageIcon(this.getClass().getResource("ZoomInput.png"));
  private final ImageIcon zoomToInputAIcon = new ImageIcon(this.getClass().getResource("ZoomInputA.png"));
  private final ImageIcon zoomToInputBIcon = new ImageIcon(this.getClass().getResource("ZoomInputB.png"));
  private final ImageIcon zoomToResultIcon = new ImageIcon(this.getClass().getResource("ZoomResult.png"));
  private final ImageIcon zoomToFullExtentIcon = new ImageIcon(this.getClass().getResource("ZoomAll.png"));
  private final ImageIcon selectIcon = new ImageIcon(this.getClass().getResource("Select.gif"));
  private final ImageIcon moveVertexIcon = new ImageIcon(this.getClass().getResource("MoveVertex.png"));
  private final ImageIcon panIcon = new ImageIcon(this.getClass().getResource("Hand.gif"));
  private final ImageIcon showHideGridIcon = new ImageIcon(this.getClass().getResource("gridIcon.png"));


  public JTSTestBuilderToolBar(JTSTestBuilderFrame tbFrame) 
  {
    this.tbFrame = tbFrame;
  }

  public void clearToolButtons()
  {
    // this only works in JSE 1.6
    // In 1.5, need to add an invisible button and select it
    //toolButtonGroup.clearSelection();
  }
  
  public void unselectExtractComponentButton()
  {
    extractComponentButton.setSelected(false);
    toolButtonGroup.setSelected(extractComponentButton.getModel(), false);
  }
  
  public JToolBar getToolBar()
  {
    jToolBar1.setFloatable(false);

    /**--------------------------------------------------
     * Buttons
     * --------------------------------------------------
     */
      previousButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      previousButton.setMaximumSize(new Dimension(30, 30));
      previousButton.setMinimumSize(new Dimension(30, 30));
      previousButton.setPreferredSize(new Dimension(30, 30));
      previousButton.setToolTipText(AppStrings.TIP_PREV);
      previousButton.setHorizontalTextPosition(SwingConstants.CENTER);
      previousButton.setIcon(leftIcon);
      previousButton.setMargin(new Insets(0, 0, 0, 0));
      previousButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      previousButton.addActionListener(
          new java.awt.event.ActionListener() {
            public void actionPerformed(ActionEvent e) {
              boolean isZoom = 0 == (e.getModifiers() & ActionEvent.CTRL_MASK);
              tbFrame.moveToPreviousImage();
              updateImageNumbersInFields();
            }
          });
      sm = new SpinnerNumberModel(1, 1, AppImage.getInstance().getTotalNumberOfImages(), 1); //default value,lower bound,upper bound,increment by
      sm2 = new SpinnerNumberModel(1, 1, AppImage.getInstance().getTotalNumberOfImages(), 1); //default value,lower bound,upper bound,increment by
      panel1ImageNumber = new JSpinner(sm);
      panel1ImageNumber.setFont(new java.awt.Font("SansSerif", 0, 10));
      panel1ImageNumber.setMaximumSize(new Dimension(40, 20));
      panel1ImageNumber.setMinimumSize(new Dimension(40, 20));
      panel1ImageNumber.setPreferredSize(new Dimension(40, 20));
      
      panel1ImageNumber.addChangeListener(new ChangeListener() {
            @Override
            public void stateChanged(ChangeEvent e) {
                System.out.println("value changed: " + panel1ImageNumber.getValue());
            }
        });
      
      panel2ImageNumber = new JSpinner(sm2);
      panel2ImageNumber.setFont(new java.awt.Font("SansSerif", 0, 10));
      panel2ImageNumber.setMaximumSize(new Dimension(40, 20));
      panel2ImageNumber.setMinimumSize(new Dimension(40, 20));
      panel2ImageNumber.setPreferredSize(new Dimension(40, 20));
      panel2ImageNumber.addChangeListener(new ChangeListener() {
            @Override
            public void stateChanged(ChangeEvent e) {
                System.out.println("value changed: " + panel2ImageNumber.getValue());
            }
        });
      
      updateImageNumbersInFields();
      setTextForImageNumberLabels();
      
      nextButton.setMargin(new Insets(0, 0, 0, 0));
      nextButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      nextButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      nextButton.setMaximumSize(new Dimension(30, 30));
      nextButton.setMinimumSize(new Dimension(30, 30));
      nextButton.setPreferredSize(new Dimension(30, 30));
      nextButton.setToolTipText(AppStrings.TIP_NEXT);
      nextButton.setHorizontalTextPosition(SwingConstants.CENTER);
      nextButton.setIcon(rightIcon);
      nextButton.addActionListener(
          new java.awt.event.ActionListener() {
            public void actionPerformed(ActionEvent e) {
             boolean isZoom = 0 == (e.getModifiers() & ActionEvent.CTRL_MASK);
             tbFrame.moveToNextImage();
             updateImageNumbersInFields();
            }
          });
      
      newButton.setMargin(new Insets(0, 0, 0, 0));
      newButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      newButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      newButton.setMaximumSize(new Dimension(30, 30));
      newButton.setMinimumSize(new Dimension(30, 30));
      newButton.setPreferredSize(new Dimension(30, 30));
      newButton.setToolTipText(AppStrings.TIP_CASE_ADD_NEW);
      newButton.setHorizontalTextPosition(SwingConstants.CENTER);
      newButton.setIcon(plusIcon);
      newButton.addActionListener(
          new java.awt.event.ActionListener() {
            public void actionPerformed(ActionEvent e) {
              tbFrame.createNewCase();
            }
          });
      
      copyButton.setMargin(new Insets(0, 0, 0, 0));
      copyButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      copyButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      copyButton.setMaximumSize(new Dimension(30, 30));
      copyButton.setMinimumSize(new Dimension(30, 30));
      copyButton.setPreferredSize(new Dimension(30, 30));
      copyButton.setToolTipText(AppStrings.TIP_CASE_DUP);
      copyButton.setHorizontalTextPosition(SwingConstants.CENTER);
      copyButton.setIcon(copyCaseIcon);
      copyButton.addActionListener(
          new java.awt.event.ActionListener() {
            public void actionPerformed(ActionEvent e) {
              tbFrame.copyCase();
            }
          });
      
      deleteButton.setMargin(new Insets(0, 0, 0, 0));
      deleteButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      deleteButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      deleteButton.setMaximumSize(new Dimension(30, 30));
      deleteButton.setMinimumSize(new Dimension(30, 30));
      deleteButton.setPreferredSize(new Dimension(30, 30));
      deleteButton.setToolTipText(AppStrings.TIP_CASE_DELETE);
      deleteButton.setHorizontalTextPosition(SwingConstants.CENTER);
      deleteButton.setIcon(deleteIcon);
      deleteButton.addActionListener(
          new java.awt.event.ActionListener() {
            public void actionPerformed(ActionEvent e) {
              tbFrame.btnDeleteCase_actionPerformed(e);
            }
          });
           
      drawRectangleButton.setMargin(new Insets(0, 0, 0, 0));
      drawRectangleButton.setPreferredSize(new Dimension(30, 30));
      drawRectangleButton.setIcon(drawRectangleIcon);
      drawRectangleButton.setMinimumSize(new Dimension(30, 30));
      drawRectangleButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      drawRectangleButton.setSelected(true);
      drawRectangleButton.setToolTipText(AppStrings.TIP_DRAW_RECTANGLE);
      drawRectangleButton.setHorizontalTextPosition(SwingConstants.CENTER);
      drawRectangleButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      drawRectangleButton.setMaximumSize(new Dimension(30, 30));
      drawRectangleButton.addActionListener(
        new java.awt.event.ActionListener() {
          public void actionPerformed(ActionEvent e) {
            tbFrame.drawRectangleButton_actionPerformed(e);
          }
        });
      
      drawPolygonButton.setMargin(new Insets(0, 0, 0, 0));
      drawPolygonButton.setPreferredSize(new Dimension(30, 30));
      drawPolygonButton.setIcon(drawPolygonIcon);
      drawPolygonButton.setMinimumSize(new Dimension(30, 30));
      drawPolygonButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      drawPolygonButton.setSelected(true);
      drawPolygonButton.setToolTipText(AppStrings.TIP_DRAW_POLY);
      drawPolygonButton.setHorizontalTextPosition(SwingConstants.CENTER);
      drawPolygonButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      drawPolygonButton.setMaximumSize(new Dimension(30, 30));
      drawPolygonButton.addActionListener(
        new java.awt.event.ActionListener() {

          public void actionPerformed(ActionEvent e) {
            tbFrame.drawPolygonButton_actionPerformed(e);
          }
        });
      
      drawLineStringButton.setMargin(new Insets(0, 0, 0, 0));
      drawLineStringButton.setPreferredSize(new Dimension(30, 30));
      drawLineStringButton.setIcon(drawLineStringIcon);
      drawLineStringButton.setMinimumSize(new Dimension(30, 30));
      drawLineStringButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      drawLineStringButton.setSelected(true);
      drawLineStringButton.setToolTipText(AppStrings.TIP_DRAW_LINE);
      drawLineStringButton.setHorizontalTextPosition(SwingConstants.CENTER);
      drawLineStringButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      drawLineStringButton.setMaximumSize(new Dimension(30, 30));
      drawLineStringButton.addActionListener(
        new java.awt.event.ActionListener() {
          public void actionPerformed(ActionEvent e) {
            tbFrame.drawLineStringButton_actionPerformed(e);
          }
        });
      drawPointButton.setMargin(new Insets(0, 0, 0, 0));
      drawPointButton.setPreferredSize(new Dimension(30, 30));
      drawPointButton.setIcon(drawPointIcon);
      drawPointButton.setMinimumSize(new Dimension(30, 30));
      drawPointButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      drawPointButton.setSelected(true);
      drawPointButton.setToolTipText(AppStrings.TIP_DRAW_POINT);
      drawPointButton.setHorizontalTextPosition(SwingConstants.CENTER);
      drawPointButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      drawPointButton.setMaximumSize(new Dimension(30, 30));
      drawPointButton.addActionListener(
        new java.awt.event.ActionListener() {
          public void actionPerformed(ActionEvent e) {
            tbFrame.drawPointButton_actionPerformed(e);
          }
        });
      infoButton.setMargin(new Insets(0, 0, 0, 0));
      infoButton.setPreferredSize(new Dimension(30, 30));
      infoButton.setIcon(infoIcon);
      infoButton.setMinimumSize(new Dimension(30, 30));
      infoButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      infoButton.setSelected(false);
      infoButton.setToolTipText(AppStrings.TIP_INFO);
      infoButton.setHorizontalTextPosition(SwingConstants.CENTER);
      infoButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      infoButton.setMaximumSize(new Dimension(30, 30));
      infoButton.addActionListener(
        new java.awt.event.ActionListener() {
          public void actionPerformed(ActionEvent e) {
            tbFrame.infoButton_actionPerformed();
          }
        });
      zoomButton.setMaximumSize(new Dimension(30, 30));
      zoomButton.addActionListener(
        new java.awt.event.ActionListener() {

          public void actionPerformed(ActionEvent e) {
            tbFrame.zoomInButton_actionPerformed(e);
          }
        });
      zoomButton.setToolTipText(AppStrings.TIP_ZOOM);
      zoomButton.setHorizontalTextPosition(SwingConstants.CENTER);
      zoomButton.setFont(new java.awt.Font("Serif", 0, 10));
      zoomButton.setMinimumSize(new Dimension(30, 30));
      zoomButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      zoomButton.setPreferredSize(new Dimension(30, 30));
      zoomButton.setIcon(zoomIcon);
      zoomButton.setMargin(new Insets(0, 0, 0, 0));
      
      oneToOneButton.setMargin(new Insets(0, 0, 0, 0));
      oneToOneButton.setIcon(zoomOneToOneIcon);
      oneToOneButton.setPreferredSize(new Dimension(30, 30));
      oneToOneButton.setMinimumSize(new Dimension(30, 30));
      oneToOneButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      oneToOneButton.addActionListener(
        new java.awt.event.ActionListener() {

          public void actionPerformed(ActionEvent e) {
            tbFrame.oneToOneButton_actionPerformed(e);
          }
        });
      oneToOneButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      oneToOneButton.setToolTipText(AppStrings.TIP_ZOOM_1_1);
      oneToOneButton.setHorizontalTextPosition(SwingConstants.CENTER);
      oneToOneButton.setMaximumSize(new Dimension(30, 30));
      
      zoomToInputButton.setMargin(new Insets(0, 0, 0, 0));
      zoomToInputButton.setIcon(zoomToInputIcon);
      zoomToInputButton.setPreferredSize(new Dimension(30, 30));
      zoomToInputButton.setMaximumSize(new Dimension(30, 30));
      zoomToInputButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      zoomToInputButton.setMinimumSize(new Dimension(30, 30));
      zoomToInputButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      zoomToInputButton.setHorizontalTextPosition(SwingConstants.CENTER);
      zoomToInputButton.setToolTipText("Zoom To Input");
      zoomToInputButton.addActionListener(
        new java.awt.event.ActionListener() {

          public void actionPerformed(ActionEvent e) {
            tbFrame.zoomToInputButton_actionPerformed(e);
          }
        });

      zoomToInputAButton.setMargin(new Insets(0, 0, 0, 0));
      zoomToInputAButton.setIcon(zoomToInputAIcon);
      zoomToInputAButton.setPreferredSize(new Dimension(30, 30));
      zoomToInputAButton.setMaximumSize(new Dimension(30, 30));
      zoomToInputAButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      zoomToInputAButton.setMinimumSize(new Dimension(30, 30));
      zoomToInputAButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      zoomToInputAButton.setHorizontalTextPosition(SwingConstants.CENTER);
      zoomToInputAButton.setToolTipText(AppStrings.TIP_ZOOM_TO_A);
      zoomToInputAButton.addActionListener(
        new java.awt.event.ActionListener() {

          public void actionPerformed(ActionEvent e) {
            tbFrame.zoomToInputA_actionPerformed(e);
          }
        });
      
      zoomToInputBButton.setMargin(new Insets(0, 0, 0, 0));
      zoomToInputBButton.setIcon(zoomToInputBIcon);
      zoomToInputBButton.setPreferredSize(new Dimension(30, 30));
      zoomToInputBButton.setMaximumSize(new Dimension(30, 30));
      zoomToInputBButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      zoomToInputBButton.setMinimumSize(new Dimension(30, 30));
      zoomToInputBButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      zoomToInputBButton.setHorizontalTextPosition(SwingConstants.CENTER);
      zoomToInputBButton.setToolTipText(AppStrings.TIP_ZOOM_TO_B);
      zoomToInputBButton.addActionListener(
        new java.awt.event.ActionListener() {

          public void actionPerformed(ActionEvent e) {
            tbFrame.zoomToInputB_actionPerformed(e);
          }
        });
      zoomToInputButton.setMaximumSize(new Dimension(30, 30));
      
      zoomToResultButton.setMargin(new Insets(0, 0, 0, 0));
      zoomToResultButton.setIcon(zoomToResultIcon);
      zoomToResultButton.setPreferredSize(new Dimension(30, 30));
      zoomToResultButton.setMaximumSize(new Dimension(30, 30));
      zoomToResultButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      zoomToResultButton.setMinimumSize(new Dimension(30, 30));
      zoomToResultButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      zoomToResultButton.setHorizontalTextPosition(SwingConstants.CENTER);
      zoomToResultButton.setToolTipText(AppStrings.TIP_ZOOM_TO_RESULT);
      zoomToResultButton.addActionListener(
        new java.awt.event.ActionListener() {

          public void actionPerformed(ActionEvent e) {
            tbFrame.zoomToResult_actionPerformed(e);
          }
        });
      zoomToResultButton.setMaximumSize(new Dimension(30, 30));
      
      zoomToFullExtentButton.setMargin(new Insets(0, 0, 0, 0));
      zoomToFullExtentButton.setIcon(zoomToFullExtentIcon);
      zoomToFullExtentButton.setPreferredSize(new Dimension(30, 30));
      zoomToFullExtentButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      zoomToFullExtentButton.setMinimumSize(new Dimension(30, 30));
      zoomToFullExtentButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      zoomToFullExtentButton.setHorizontalTextPosition(SwingConstants.CENTER);
      zoomToFullExtentButton.setToolTipText(AppStrings.TIP_ZOOM_TO_FULL_EXTENT);
      zoomToFullExtentButton.addActionListener(
        new java.awt.event.ActionListener() {

          public void actionPerformed(ActionEvent e) {
            tbFrame.zoomToFullExtentButton_actionPerformed(e);
          }
        });
      zoomToFullExtentButton.setMaximumSize(new Dimension(30, 30));
      
      panButton.addActionListener(
        new java.awt.event.ActionListener() {

          public void actionPerformed(ActionEvent e) {
            tbFrame.panButton_actionPerformed(e);
          }
        });
      panButton.setMaximumSize(new Dimension(30, 30));
      panButton.setFont(new java.awt.Font("SansSerif", 0, 10));
      panButton.setHorizontalTextPosition(SwingConstants.CENTER);
      panButton.setToolTipText(AppStrings.TIP_PAN);
      panButton.setVerticalTextPosition(SwingConstants.BOTTOM);
      panButton.setMinimumSize(new Dimension(30, 30));
      panButton.setIcon(panIcon);
      panButton.setPreferredSize(new Dimension(30, 30));
      panButton.setMargin(new Insets(0, 0, 0, 0));
      
      btnEditVertex.setMaximumSize(new Dimension(30, 30));
      btnEditVertex.setMinimumSize(new Dimension(30, 30));
      btnEditVertex.setToolTipText(AppStrings.TIP_MOVE_VERTEX);
      btnEditVertex.setIcon(moveVertexIcon);
      btnEditVertex.setMargin(new Insets(0, 0, 0, 0));
      btnEditVertex.setMnemonic('0');
      btnEditVertex.addActionListener(new java.awt.event.ActionListener() {
        public void actionPerformed(ActionEvent e) {
          tbFrame.btnEditVertex_actionPerformed(e);
        }
      });
      
      btnShowHideGrid.setMaximumSize(new Dimension(30, 30));
      btnShowHideGrid.setMinimumSize(new Dimension(30, 30));
      btnShowHideGrid.setToolTipText(AppStrings.TIP_MOVE_VERTEX);
      btnShowHideGrid.setIcon(showHideGridIcon);
      btnShowHideGrid.setMargin(new Insets(0, 0, 0, 0));
      btnShowHideGrid.setMnemonic('0');
      btnShowHideGrid.addActionListener(new java.awt.event.ActionListener() {
        public void actionPerformed(ActionEvent e) {
          tbFrame.btnShowHideGrid_actionPerformed(e);
        }
      });

      extractComponentButton = createToggleButton(AppStrings.TIP_EXTRACT_COMPONENTS,
          new ImageIcon(this.getClass().getResource("ExtractComponent.png")), 
          new java.awt.event.ActionListener() {
            public void actionPerformed(ActionEvent e)
            {
              tbFrame.actionExtractComponentButton();
            }
          });

      JToggleButton deleteVertexButton = createToggleButton(AppStrings.TIP_DELETE_VERTEX_COMPONENT,
          new ImageIcon(this.getClass().getResource("DeleteVertex.png")), 
          new java.awt.event.ActionListener() {
            public void actionPerformed(ActionEvent e)
            {
              tbFrame.actionDeleteVertexButton();
            }
          });

      toolButtonGroup.add(drawRectangleButton);
      toolButtonGroup.add(drawPolygonButton);
      toolButtonGroup.add(drawLineStringButton);
      toolButtonGroup.add(drawPointButton);
      toolButtonGroup.add(panButton);
      toolButtonGroup.add(zoomButton);
      toolButtonGroup.add(btnEditVertex);
      toolButtonGroup.add(deleteVertexButton);
      toolButtonGroup.add(btnShowHideGrid);
      toolButtonGroup.add(infoButton);
      toolButtonGroup.add(extractComponentButton);


      jToolBar1.add(newButton, null);
      jToolBar1.add(copyButton, null);
      jToolBar1.add(previousButton, null);
      jToolBar1.add(labelForImageNumberPanel1, null);
      jToolBar1.add(panel1ImageNumber, null);
      jToolBar1.add(labelForImageNumberPanel2, null);
      jToolBar1.add(panel2ImageNumber, null);
      jToolBar1.add(totalImages, null);
      jToolBar1.add(nextButton, null);
      
      jToolBar1.add(Box.createHorizontalStrut(8), null);
      jToolBar1.add(deleteButton, null);
      
      jToolBar1.add(Box.createHorizontalStrut(8), null);
      jToolBar1.add(exchangeButton, null);
      
      jToolBar1.add(Box.createHorizontalStrut(8), null);
      
      jToolBar1.add(oneToOneButton, null);
      jToolBar1.add(zoomToInputAButton, null);
      jToolBar1.add(zoomToInputBButton, null);
      jToolBar1.add(zoomToInputButton, null);
      jToolBar1.add(zoomToResultButton, null);
      jToolBar1.add(zoomToFullExtentButton, null);
      
      jToolBar1.add(Box.createHorizontalStrut(28), null);
      
      jToolBar1.add(zoomButton, null);
      // remove in favour of using Zoom tool
      //jToolBar1.add(panButton, null);
      jToolBar1.add(infoButton, null);
      jToolBar1.add(extractComponentButton, null);
      
      jToolBar1.add(Box.createHorizontalStrut(28), null);
      
      jToolBar1.add(drawRectangleButton, null);
      jToolBar1.add(drawPolygonButton, null);
      jToolBar1.add(drawLineStringButton, null);
      jToolBar1.add(drawPointButton, null);
      jToolBar1.add(btnEditVertex, null);
      jToolBar1.add(deleteVertexButton, null);
      jToolBar1.add(btnShowHideGrid, null);
      
      //start with previous button deactivated because we begin with the first image and there is no image to go back to
      disablePreviousBtn();
      
      return jToolBar1;
  }
  
  public void setFocusGeometry(int index)
  {
    drawRectangleButton.setIcon(index == 0 ? drawRectangleIcon : drawRectangleBIcon);
    drawPolygonButton.setIcon(index == 0 ? drawPolygonIcon : drawPolygonBIcon);
    drawLineStringButton.setIcon(index == 0 ? drawLineStringIcon : drawLineStringBIcon);
    drawPointButton.setIcon(index == 0 ? drawPointIcon : drawPointBIcon);
  }
  
  private static JToggleButton createToggleButton(String toolTipText, 
      ImageIcon icon, 
      java.awt.event.ActionListener actionListener)
  {
    JToggleButton btn = new JToggleButton();
    btn.setMargin(new Insets(0, 0, 0, 0));
    btn.setPreferredSize(new Dimension(30, 30));
    btn.setIcon(icon);
    btn.setMinimumSize(new Dimension(30, 30));
    btn.setVerticalTextPosition(SwingConstants.BOTTOM);
    btn.setSelected(false);
    btn.setToolTipText(toolTipText);
    btn.setHorizontalTextPosition(SwingConstants.CENTER);
    btn.setFont(new java.awt.Font("SansSerif", 0, 10));
    btn.setMaximumSize(new Dimension(30, 30));
    btn.addActionListener(actionListener);
    return btn;
  }
  
  private static JButton createButton(String toolTipText, 
      ImageIcon icon, 
      java.awt.event.ActionListener actionListener)
  {
    JButton btn = new JButton();
    btn.setMargin(new Insets(0, 0, 0, 0));
    btn.setPreferredSize(new Dimension(30, 30));
    btn.setIcon(icon);
    btn.setMinimumSize(new Dimension(30, 30));
    btn.setVerticalTextPosition(SwingConstants.BOTTOM);
    btn.setSelected(false);
    btn.setToolTipText(toolTipText);
    btn.setHorizontalTextPosition(SwingConstants.CENTER);
    btn.setFont(new java.awt.Font("SansSerif", 0, 10));
    btn.setMaximumSize(new Dimension(30, 30));
    btn.addActionListener(actionListener);
    return btn;
  }
  
    public boolean isNextBtnActivated(){
        return this.nextButton.isEnabled();
    }

    public boolean isPreviousBtnActivated(){
        return this.previousButton.isEnabled();
    }
    
    public void enableNextBtn(){
        nextButton.setEnabled(true);
    }

    public void disableNextBtn(){
        nextButton.setEnabled(false);
    }

    public void enablePreviousBtn(){
        previousButton.setEnabled(true);
    }

    public void disablePreviousBtn(){
        previousButton.setEnabled(false);
    }
    
    private int getNumberOfImagePanel1(){
        return AppImage.getInstance().getCurrentIndexImageForPanel1()+1;
    }
    
    private int getNumberOfImagePanel2(){
        return AppImage.getInstance().getCurrentIndexImageForPanel2()+1;
    }
    
    //updates the number of the currently shown images in each text field
    private void updateImageNumbersInFields(){
      panel1ImageNumber.setValue(getNumberOfImagePanel1());
      panel2ImageNumber.setValue(getNumberOfImagePanel2());
    }
    
    //set the text for the labels next to the spinners with the number of the images in the panel
    private void setTextForImageNumberLabels(){
        labelForImageNumberPanel1.setText("  left panel image nº: ");
        labelForImageNumberPanel2.setText(" right panel image nº: ");
        totalImages.setText(" "+AppImage.getInstance().getTotalNumberOfImages()+" images total  ");
    }
  
}