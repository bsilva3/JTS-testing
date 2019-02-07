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
    private int currentImageWidthInPanel1;
    private int currentImageWidthInPanel2;
    private int currentImageHeightInPanel1;
    private int currentImageHeightInPanel2;
    
    private List<Image> images = new ArrayList<>();
    
    private List<File> corrFiles = new ArrayList<>();
    
    //stores the index of the image selected in each panel in the list of images 
    //the index of the selected image in panel 1 will always be 1 less than the index of the image in panel2
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
        if (images.size() == 1){
            selectedImageIndexPanel2 = 0;
            //if there is only one image, immediately deactivate one
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
        //delete the previous coords since the geometries will be redrawn
        AppCorrGeometries.getInstance().clearCoords();
        AppCorrGeometries.getInstance().setGeometriesEdited(false);
    }
    
    //load next Image in the list, unless it is the last image in the list 
    //return true if the image changed is the last one, false otherwise
    public boolean loadNextImage(){
        if(selectedImageIndexPanel1 < images.size()-2){
            selectedImageIndexPanel1++;
            selectedImageIndexPanel2++;
            loadCorrFiles();
        }
        return selectedImageIndexPanel1 == images.size()-2; //the left panel only has 2nd image from the end maximum. Last image is on left panel
    }
    
    //load previous image in the list, unless the image in the first panel is the first one in the list
    //returns true if the image changed is the first image, false otherwise
    public boolean loadPreviousImage(){
        if(selectedImageIndexPanel1 > 0){
            selectedImageIndexPanel1--;
            selectedImageIndexPanel2--;
            loadCorrFiles();
        }
        return selectedImageIndexPanel1 == 0;
    }

    
    public Image getCurrentlySelectedImageForPanel(boolean isSecondPanel){
        if (isSecondPanel){
            return images.get(selectedImageIndexPanel2);
        }
        else{
            return images.get(selectedImageIndexPanel1);
        }
    }
    
    public int getTotalNumberOfImages(){
        return images.size();
    }
    
    public boolean imageExistForPanel1(int i){
        i--;//decrease because the index of an image in the list of images == the number of the image in the panel -1
        if (i <= images.size()-2 && i >= 0){
            //there is a image for both panels
            this.selectedImageIndexPanel1 = i;
            //the index of the selected image in panel 2 will always be 1 more than the index of the image in panel 1
            this.selectedImageIndexPanel2 = i+1;
            loadCorrFiles();
            return true;
        }
        return false;
    }
    
    public boolean isLastImageForPanel1(){
        if(images.size() == 1){
            return this.selectedImageIndexPanel2 == images.size()-1;
        }
        return this.selectedImageIndexPanel1 == images.size()-2;
    }
    
    public boolean isFirstImageForPanel1(){
        return this.selectedImageIndexPanel1 == 0;
    }
    
    public boolean isFirstImageForPanel2(){
        if(images.size() == 1){
            return this.selectedImageIndexPanel2 == 0;
        }
        return this.selectedImageIndexPanel2 == 1;
    }
    
    public boolean isLastImageForPanel2(){
        return this.selectedImageIndexPanel1 == images.size()-1;
    }
    
    public boolean imageExistForPanel2(int i){
        i--; //decrease because the index of an image in the list of images == the number of the image in the panel -1
        if (i <= images.size()-1 && i >= 1){
            this.selectedImageIndexPanel2 = i;
            //the index of the selected image in panel 1 will always be 1 less than the index of the image in panel2
            this.selectedImageIndexPanel1 = i-1;
            loadCorrFiles();
            return true;
        }
        return false;
    }
    
    public int getCurrentIndexImageForPanel1(){
        return selectedImageIndexPanel1;
    }
    
    public int getCurrentIndexImageForPanel2(){
        return selectedImageIndexPanel2;
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
        setImageHeightInPanel((int) Math.round(d.height), isSecondPanel);
        setImageWidthInPanel((int) Math.round(d.width), isSecondPanel);
        return d;
    }
      
    private Dimension getScaledDimension(Dimension imageSize, Dimension boundary) {
        double widthRatio = boundary.getWidth() / imageSize.getWidth();
        double heightRatio = boundary.getHeight() / imageSize.getHeight();
        double ratio = Math.min(widthRatio, heightRatio);

        return new Dimension((int) (imageSize.width * ratio), (int) (imageSize.height * ratio));
    }

    public int getImageWidthInPanel(boolean isSecondPanel) {
        if(isSecondPanel){
            return currentImageWidthInPanel2;
        }
        return currentImageWidthInPanel1;
    }

    public void setImageWidthInPanel(int imageWidthInPanel, boolean isSecondPanel) {
        if (isSecondPanel){
            this.currentImageWidthInPanel2 = imageWidthInPanel;
        }
        else{
            this.currentImageWidthInPanel1 = imageWidthInPanel;
        }
    }

    public int getImageHeightInPanel(boolean isSecondPanel) {
        if(isSecondPanel){
            return currentImageHeightInPanel2;
        }
        return currentImageHeightInPanel1;
    }

    public void setImageHeightInPanel(int imageHeightInPanel, boolean isSecondPanel) {
        if(isSecondPanel){
            this.currentImageHeightInPanel2 = imageHeightInPanel;
        }
        else{
            this.currentImageHeightInPanel1 = imageHeightInPanel;
        }   
    }

    public File getCurrentCorrFile(){
        return this.corrFiles.get(0);
    }
}
