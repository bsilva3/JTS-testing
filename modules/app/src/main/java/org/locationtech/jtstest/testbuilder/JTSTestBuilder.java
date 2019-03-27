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
import java.awt.Toolkit;
import java.io.File;
import java.lang.reflect.InvocationTargetException;
import javax.swing.JFileChooser;

import javax.swing.UIManager;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.filechooser.FileSystemView;

import org.locationtech.jts.geom.*;
import org.locationtech.jtstest.command.*;
import org.locationtech.jtstest.function.*;
import org.locationtech.jtstest.geomfunction.GeometryFunctionRegistry;
import org.locationtech.jtstest.testbuilder.model.*;


/**
 * A Swing application which supports 
 * creating geometries and running JTS operations.
 * <p>
 * <b>Command Line Options</b>
 * <table border='1'>
 * <tr>
 * <td><tt>-geomfunc <i>{ &lt;classname&gt; }</i></tt> </td>
 * <td>Specifies classes whose <tt>public static<tt> methods will be loaded as geometry functions</td>
 * </tr>
 * </table>
 * 
 * @version 1.7
 */
public class JTSTestBuilder
{
  private static final String PROP_SWING_DEFAULTLAF = "swing.defaultlaf";

  private static final String OPT_GEOMFUNC = "geomfunc";
  
  private TestBuilderModel tbModel = new TestBuilderModel(false);
  
  private TestBuilderModel tbModel2 = new TestBuilderModel(true);
  
  boolean packFrame = false;
  
  public static JTSTestBuilder instance()
  {
  	return app;
  }
  
  public static TestBuilderModel model() { return instance().tbModel; }
  
  public static TestBuilderModel model2() { return instance().tbModel2; }

  private static GeometryFunctionRegistry funcRegistry = GeometryFunctionRegistry.createTestBuilderRegistry();
  private static CommandLine commandLine = createCmdLine();
  public static JTSTestBuilder app;
  
  private static CommandLine createCmdLine() {
    commandLine = new CommandLine('-');
    commandLine.addOptionSpec(new OptionSpec(OPT_GEOMFUNC, OptionSpec.NARGS_ONE_OR_MORE));
    return commandLine;
  }

  public static GeometryFunctionRegistry getFunctionRegistry()
  {
    return funcRegistry;
  }

  public static PrecisionModel getPrecisionModel() 
  { 
    return model().getPrecisionModel();
  }
  
  public static GeometryFactory getGeometryFactory() 
  { 
    return model().getGeometryFactory();
  }
  
   /**Construct the application*/
  public JTSTestBuilder() {
  }
  
  private void initFrame()
  {
    JTSTestBuilderFrame frame = new JTSTestBuilderFrame();
    frame.setModel(model(), model2());
    
    //Validate frames that have preset sizes
    //Pack frames that have useful preferred size info, e.g. from their layout
    /*if (packFrame) {
      frame.pack();
    } else {
      frame.validate();
    }*/
    frame.validate();
    //Center the window
    Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    Dimension frameSize = frame.getSize();
    if (frameSize.height > screenSize.height) {
      frameSize.height = screenSize.height;
    }
    if (frameSize.width > screenSize.width) {
      frameSize.width = screenSize.width;
    }
    frame.setLocation(
        (screenSize.width - frameSize.width) / 2,
        (screenSize.height - frameSize.height) / 2);
    frame.setVisible(true);
  }

  
  /**Main method*/
  public static void main(String[] args)
  {
    try {
        //file chooser window to select a directory of images
        /*JFileChooser jfc = new JFileChooser(FileSystemView.getFileSystemView().getHomeDirectory());
        jfc.setDialogTitle("Choose a directory with images to open: ");
           
        jfc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        jfc.setAcceptAllFileFilterUsed(false);
        FileNameExtensionFilter filter = new FileNameExtensionFilter("png, gif, jpg, bmp or tiff images", "png", "gif", "jpg", "bmp", "tiff");
        jfc.addChoosableFileFilter(filter);
        int returnValue = jfc.showOpenDialog(null);
        File selectedDirectory = null;
        if (returnValue == JFileChooser.APPROVE_OPTION) {
             selectedDirectory = jfc.getSelectedFile();
        }
        else{
            //no valid image selected, end the program
            return;
        }

        AppImage.getInstance().loadImages(selectedDirectory.listFiles());
        
        jfc.setDialogTitle("Choose a directory with the corr files to open: ");
           
        jfc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        jfc.setAcceptAllFileFilterUsed(false);
        filter = new FileNameExtensionFilter("corr", "wkt");
        jfc.addChoosableFileFilter(filter);
        returnValue = jfc.showOpenDialog(null);
        selectedDirectory = null;
        if (returnValue == JFileChooser.APPROVE_OPTION) {
             selectedDirectory = jfc.getSelectedFile();
        }
        else{
            //no valid corr files folder selected, end the program
            return;
        }
        AppImage.getInstance().setAndLoadCorrDirFiles(selectedDirectory);*/
        
        AppImage.getInstance().loadImages(new File("C:\\Users\\bjpsi\\Desktop\\Investigacao\\JTS-testing\\img\\").listFiles());
        AppImage.getInstance().setAndLoadCorrDirFiles(new File("C:\\Users\\bjpsi\\Desktop\\Investigacao\\JTS-testing\\ice1\\"));
    	
        readArgs(args);
    	//setLookAndFeel();
        try { 
            UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsLookAndFeel"); 
        } catch(Exception ignored){}
        app = new JTSTestBuilder();
        app.initFrame();
        //now that the frame has been initialized, draw the geometry
        //now called on the event "window resized"
        //JTSTestBuilderFrame.getGeometryEditPanel().drawGeometry();

      } catch (Exception e) {
        e.printStackTrace();
      }
  }

  /**
   * Sets the look and feel, using user-defined LAF if 
   * provided as a system property.
   * 
   * e.g. Metal: -Dswing.defaultlaf=javax.swing.plaf.metal.MetalLookAndFeel
   * 
   * @throws InterruptedException
   * @throws InvocationTargetException
   */
  private static void setLookAndFeel() throws InterruptedException, InvocationTargetException
  {
    /**
     * Invoke on Swing thread to pass Java security requirements
     */
    javax.swing.SwingUtilities.invokeAndWait(new Runnable() {
      public void run()
      {
        try {
          String laf = System.getProperty(PROP_SWING_DEFAULTLAF);
          if (laf == null) {
            laf = UIManager.getSystemLookAndFeelClassName();
          }
          javax.swing.UIManager.setLookAndFeel(laf);
        }
        catch (Exception e) {
          e.printStackTrace();
        }
      }
    });
  }

  private static void readArgs(String[] args) throws ParseException,
			ClassNotFoundException {
		commandLine.parse(args);

		if (commandLine.hasOption(OPT_GEOMFUNC)) {
			Option opt = commandLine.getOption(OPT_GEOMFUNC);
			for (int i = 0; i < opt.getNumArgs(); i++) {
				String geomFuncClassname = opt.getArg(i);
				try {
					funcRegistry.add(geomFuncClassname);
					System.out.println("Added Geometry Functions from: "
							+ geomFuncClassname);
				} catch (ClassNotFoundException ex) {
					System.out.println("Unable to load function class: "
							+ geomFuncClassname);
				}
			}
		}
	}

}