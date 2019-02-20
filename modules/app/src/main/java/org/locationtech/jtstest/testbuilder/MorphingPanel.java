/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.JWindow;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

/**
 *
 * @author Bruno Silva
 */
public class MorphingPanel extends JPanel{
    
    private JPanel optionsPanel;
    private JButton playBtn;
    private JSlider timeSlider;
    
    private JWindow toolTip = new JWindow();
    private JLabel toolTipLabel = new JLabel("", SwingConstants.CENTER);
    private Dimension size = new Dimension(30, 20);
    private int prevValue = -1;
    
    public MorphingPanel (){
        setLayout(new BorderLayout() );
        
        //initialize options panel
        optionsPanel = new JPanel();
        //https://docs.oracle.com/javase/tutorial/uiswing/layout/gridbag.html
        optionsPanel.setLayout(new GridBagLayout());
        
        GridBagConstraints c = new GridBagConstraints();
        c.anchor = GridBagConstraints.PAGE_START;
        c.ipady = 5;
        playBtn = new JButton("Play");
        optionsPanel.add(playBtn, c);
        
        timeSlider = new JSlider(JSlider.HORIZONTAL, 1000, 2000, 1000);
        //labels for slider:
        timeSlider.setMajorTickSpacing(200);
        timeSlider.setMinorTickSpacing(100);
        timeSlider.setPaintTicks(true);
        timeSlider.setPaintLabels(true);
        
        //set up slider tooltip elements
        toolTipLabel.setOpaque(false);
        toolTipLabel.setBackground(UIManager.getColor("ToolTip.background"));
        toolTipLabel.setBorder(UIManager.getBorder("ToolTip.border"));
        toolTip.add(toolTipLabel);
        toolTip.setSize(size);
        
        //listeners to show a tooltip for the slider
        
        timeSlider.addMouseMotionListener(new MouseMotionListener(){
            @Override
            public void mouseDragged(MouseEvent e) {
                updateToolTip(e);
            }

            @Override
            public void mouseMoved(MouseEvent e) {
                updateToolTip(e);
            }
            
        });
        timeSlider.addMouseListener(new MouseListener(){
            @Override
            public void mouseClicked(MouseEvent e) { }

            @Override
            public void mousePressed(MouseEvent e) {
                toolTip.setVisible(true);
            }

            @Override
            public void mouseReleased(MouseEvent e) {}

            @Override
            public void mouseEntered(MouseEvent e) {
                toolTip.setVisible(true);
            }

            @Override
            public void mouseExited(MouseEvent e) {
                toolTip.setVisible(false);
            }
        });
        
        c.anchor = GridBagConstraints.PAGE_END;
        optionsPanel.add(timeSlider, c);
        
        this.add(optionsPanel, BorderLayout.EAST);
 
    }
    
    public void updateToolTip(MouseEvent me) {
        JSlider slider = (JSlider) me.getComponent();
        int intValue = (int) slider.getValue();
        if (prevValue != intValue) {
            toolTipLabel.setText(String.format("%03d", slider.getValue()));
            Point pt = me.getPoint();
            pt.y = -size.height;
            SwingUtilities.convertPointToScreen(pt, me.getComponent());
            pt.translate(-size.width / 2, 0);
            toolTip.setLocation(pt);
        }
        prevValue = intValue;
    }
    
}
