/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.locationtech.jtstest.testbuilder;

import java.io.File;

/**
 *
 * @author Bruno Silva
 */
public class AppFiles {
    
    private static File corrFile;

    public static File getCorrFile() {
        return corrFile;
    }

    public static void setCorrFile(File corrFile) {
        AppFiles.corrFile = corrFile;
    }
    
    
    
}
