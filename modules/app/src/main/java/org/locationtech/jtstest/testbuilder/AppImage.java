/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder;

import java.awt.Dimension;
import java.awt.Graphics;
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
    
    //keeps the 1:1 aspect ration of the image and draws it
    public static void keepAspectRatioAndDrawImage(Graphics g, int panelWidth, int panelHeight){
        Dimension windowDimension = new Dimension(panelWidth, panelHeight);
      
        Dimension d = getScaledDimension(new Dimension((int) AppImage.getBackgroundImage().getWidth(null), 
        (int) AppImage.getBackgroundImage().getHeight(null)), windowDimension );
      
        g.drawImage(AppImage.getBackgroundImage(), 0, 0, d.width, d.height, null);
    }
  
    private static Dimension getScaledDimension(Dimension imageSize, Dimension boundary) {
        double widthRatio = boundary.getWidth() / imageSize.getWidth();
        double heightRatio = boundary.getHeight() / imageSize.getHeight();
        double ratio = Math.min(widthRatio, heightRatio);

        return new Dimension((int) (imageSize.width * ratio), (int) (imageSize.height * ratio));
    }
    
    
    
}
