/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder;

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
    private static File backgroundImageFile;

    public static File getBackgroundImageFile() {
        return backgroundImageFile;
    }

    public static void setBackgroundImageFile(File backgroundImageFile) {
        AppImage.backgroundImageFile = backgroundImageFile;
    }
    
    
    
    
    
}
