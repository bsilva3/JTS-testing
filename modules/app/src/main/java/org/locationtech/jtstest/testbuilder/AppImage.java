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
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.imageio.ImageIO;

/**
 *
 * @author Bruno Silva
 */
public class AppImage {
    private int currentImageWidthInPanel;
    
    private int currentImageHeightInPanel;
    
    private List<Image> images = new ArrayList<>();
    
    private List<File> corrFiles = new ArrayList<>();
    
    private int selectedImageIndexPanel1 = 0;
    private int selectedImageIndexPanel2 = 1;
    
    private File corrDir;
    
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
    
    public void setAndLoadCorrDirFiles(File corrDir){
        this.corrDir = corrDir;
        loadCorrFiles();
    }
    
    //select the correct corr files for the currently selected image on panel 1
    // it is assumed that the corr files have a <number>_<number>_<number> in the name, with the number
    //in the middle indicating the corresponding image (starting at 0)
    public void loadCorrFiles(){
        corrFiles.clear();
        Pattern pattern = Pattern.compile("\\d+_" + selectedImageIndexPanel1 + "_\\d+");
        File[] files = corrDir.listFiles();
        for (File corrFile : files){
            Matcher matcher = pattern.matcher(corrFile.getName());
            if (matcher.find()){
                //System.out.println(corrFile.getName());
                corrFiles.add(corrFile);
            }
        }
    }
    
    //load next Image in the list, unless it is the last image in the list 
    //return true if the image changed is the last one, false otherwise
    public boolean loadNextImage(){
        if(selectedImageIndexPanel1 < images.size()-1){
            selectedImageIndexPanel1++;
            selectedImageIndexPanel2++;
            loadCorrFiles();
        }
        return selectedImageIndexPanel1 != images.size()-1;
    }
    
    //load previous image in the list, unless the image in the first panel is the first one in the list
    //returns true if the image changed is the first image, false otherwise
    public boolean loadPreviousImage(){
        if(selectedImageIndexPanel1 > 0){
            selectedImageIndexPanel1--;
            selectedImageIndexPanel2--;
            loadCorrFiles();
        }
        return selectedImageIndexPanel1 != 0;
    }

    
    public Image getCurrentlySelectedImageForPanel(boolean isSecondPanel){
        if (isSecondPanel){
            return images.get(selectedImageIndexPanel2);
        }
        else{
            return images.get(selectedImageIndexPanel1);
        }
    }
    
    public int getCurrentImageWidth(boolean isSecondPanel) {
        return getCurrentlySelectedImageForPanel(isSecondPanel).getWidth(null);
    }


    public int getCurrentImageHeight(boolean isSecondPanel) {
        return getCurrentlySelectedImageForPanel(isSecondPanel).getHeight(null);
    }
    
     //keeps the 1:1 aspect ration of the image and draws it
    public void keepAspectRatioAndDrawImage(Graphics2D g, Dimension panelDim, boolean isSecondPanel){
        Dimension d = resizeImageDimension(panelDim, isSecondPanel);
        g.drawImage(getCurrentlySelectedImageForPanel(isSecondPanel), 0, 0, d.width, d.height, null);
    }
    
    //resizes a dimension to fit a boundary dimension, while maintaining the aspect ratio
    public Dimension resizeImageDimension(Dimension windowDimension, boolean isSecondPanel){
        //Dimension windowDimension = new Dimension(panelWidth, panelHeight);
        Image im = getCurrentlySelectedImageForPanel(isSecondPanel);
        Dimension d = getScaledDimension(new Dimension((int) im.getWidth(null), 
        (int) im.getHeight(null)), windowDimension );
        setImageHeightInPanel((int) Math.round(d.height));
        setImageWidthInPanel((int) Math.round(d.width));
        return d;
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

    public File getCurrentCorrFile(){
        return this.corrFiles.get(0);
    }
}
