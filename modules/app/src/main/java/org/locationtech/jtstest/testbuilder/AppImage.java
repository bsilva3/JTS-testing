/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder;

import java.awt.Dimension;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageIO;

/**
 *
 * @author Bruno Silva
 */
public class AppImage {
    private int currentImageWidthInPanel;
    
    private int currentImageHeightInPanel;
    
    private List<Image> images = new ArrayList<>();
    
    private int selectedImageIndex = 0;
    
    private static AppImage instance;
    
    private AppImage() {}
    
    public static AppImage getInstance(){
        if(instance == null){
            instance = new AppImage();
        }
        return instance;
    }
    
    public void loadImages(File[] files){
        for (File file : files){
            try {
                BufferedImage b = ImageIO.read(file);
                images.add(b);
            } catch (IOException ex) {
                Logger.getLogger(AppImage.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
    
    //load next Image in the list
    public void loadNextImage(){
        if(selectedImageIndex == images.size()-1){
            //already on last image, return to first image
            selectedImageIndex = 0;
        }
        else{
            selectedImageIndex++;
        }
    }
    
    //load previous image in the list
    public void loadPreviousImage(){
        if(selectedImageIndex == 0){
            //already on first image, go to last image
            selectedImageIndex = images.size()-1;
        }
        else{
            selectedImageIndex--;
        }
    }

    public Image getCurrentlySelectedImage(){
        return images.get(selectedImageIndex);
    }
    
    public int getCurrentImageWidth() {
        return getCurrentlySelectedImage().getWidth(null);
    }


    public int getCurrentImageHeight() {
        return getCurrentlySelectedImage().getHeight(null);
    }

    
    //resizes a dimension to fit a boundary dimension, while maintaining the aspect ratio
    public Dimension resizeImageDimension(Dimension windowDimension){
        //Dimension windowDimension = new Dimension(panelWidth, panelHeight);
      
        Dimension d = getScaledDimension(new Dimension((int) getCurrentImageWidth(), 
        (int) getCurrentImageHeight()), windowDimension );
        setImageHeightInPanel((int) Math.round(d.height));
        setImageWidthInPanel((int) Math.round(d.width));
        return d;
    }
       
     //keeps the 1:1 aspect ration of the image and draws it
    public void keepAspectRatioAndDrawImage(Graphics2D g, Dimension panelDim){
        Dimension d = resizeImageDimension(panelDim);
        g.drawImage(getCurrentlySelectedImage(), 0, 0, d.width, d.height, null);
    }
      
    private Dimension getScaledDimension(Dimension imageSize, Dimension boundary) {
        double widthRatio = boundary.getWidth() / imageSize.getWidth();
        double heightRatio = boundary.getHeight() / imageSize.getHeight();
        double ratio = Math.min(widthRatio, heightRatio);

        return new Dimension((int) (imageSize.width * ratio), (int) (imageSize.height * ratio));
    }

    public int getImageWidthInPanel() {
        return currentImageWidthInPanel;
    }

    public void setImageWidthInPanel(int imageWidthInPanel) {
        this.currentImageWidthInPanel = imageWidthInPanel;
    }

    public int getImageHeightInPanel() {
        return currentImageHeightInPanel;
    }

    public void setImageHeightInPanel(int imageHeightInPanel) {
        this.currentImageHeightInPanel = imageHeightInPanel;
    }

   
    
    
    
}
