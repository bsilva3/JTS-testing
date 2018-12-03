/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder;

import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageIO;

/**
 *
 * @author Bruno Silva
 */
public class AppImage {
    private static Image backgroundImage;
    
    private static int imageWidth;
    
    private static int imageHeight;
    
    private static int imageWidthInPanel;
    
    private static int imageHeightInPanel;

    private static int oldImageHeightInPanel;
    
    private static int oldImageWidthInPanel;

    public static Image getBackgroundImage() {
        return backgroundImage;
    }

    public static void setBackgroundImage(Image backgroundImage) {
        AppImage.backgroundImage = backgroundImage;
    }
    
    public static void setBackgroundImageFile(File backgroundImageFile) {
        try {
            AppImage.backgroundImage = ImageIO.read(backgroundImageFile);
        } catch (IOException | NullPointerException ex) {
            Logger.getLogger(AppImage.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    public static int getImageWidth() {
        if (backgroundImage != null)
            return backgroundImage.getWidth(null);
        return 0;
    }

    public static void setImageWidth(int imageWidth) {
        AppImage.imageWidth = imageWidth;
    }

    public static int getImageHeight() {
        if (backgroundImage != null)
            return backgroundImage.getHeight(null);
        return 0;
    }

    public static void setImageHeight(int imageHeight) {
        AppImage.imageHeight = imageHeight;
    }
    
    //resizes a dimension to fit a boundary dimension, while maintaining the aspect ratio
    public static Dimension resizeImageDimension(int panelWidth, int panelHeight, double scale){
        Dimension windowDimension = new Dimension(panelWidth, panelHeight);
      
        Dimension d = getScaledDimension(new Dimension((int) AppImage.getBackgroundImage().getWidth(null), 
        (int) AppImage.getBackgroundImage().getHeight(null)), windowDimension );
        AppImage.setImageHeightInPanel((int) Math.round(d.height * scale));
        AppImage.setImageWidthInPanel((int) Math.round(d.width * scale));
        return d;
    }
    
    //keeps the 1:1 aspect ration of the image and draws it
    public static void keepAspectRatioAndDrawImage(Graphics g, int panelWidth, int panelHeight, 
            int cornerX, int cornerY, double scale){
        Dimension d = AppImage.resizeImageDimension(panelWidth, panelHeight, scale);
        Graphics2D g2 = (Graphics2D) g;
        //g2.scale(scale, scale);
        
        g2.drawImage(AppImage.getBackgroundImage(), -cornerX, -cornerY, d.width, d.height, null);
    }
  
    private static Dimension getScaledDimension(Dimension imageSize, Dimension boundary) {
        double widthRatio = boundary.getWidth() / imageSize.getWidth();
        double heightRatio = boundary.getHeight() / imageSize.getHeight();
        double ratio = Math.min(widthRatio, heightRatio);

        return new Dimension((int) (imageSize.width * ratio), (int) (imageSize.height * ratio));
    }

    public static int getImageWidthInPanel() {
        return imageWidthInPanel;
    }

    public static void setImageWidthInPanel(int imageWidthInPanel) {
        AppImage.imageWidthInPanel = imageWidthInPanel;
    }

    public static int getImageHeightInPanel() {
        return imageHeightInPanel;
    }

    public static void setImageHeightInPanel(int imageHeightInPanel) {
        AppImage.imageHeightInPanel = imageHeightInPanel;
    }

    public static int getOldImageHeightInPanel() {
        return oldImageHeightInPanel;
    }

    public static void setOldImageHeightInPanel(int oldImageHeightInPanel) {
        AppImage.oldImageHeightInPanel = oldImageHeightInPanel;
    }

    public static int getOldImageWidthInPanel() {
        return oldImageWidthInPanel;
    }

    public static void setOldImageWidthInPanel(int oldImageWidthInPanel) {
        AppImage.oldImageWidthInPanel = oldImageWidthInPanel;
    }
    
    
    
}
