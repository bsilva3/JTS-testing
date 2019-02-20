/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package jni_test;

/**
 *
 * @author Bruno Silva
 */
public class Main {
    public native String atinstant(double ts, double tf, String P, String Q, double t); 

    public static void main (String[] args){
        //System.out.println(System.getProperty("sun.arch.data.model"));
        //System.out.println(System.getProperty("java.class.path"));
        //System.out.println(System.getenv("JAVA_HOME"));
        //System.out.println(System.getProperty("java.library.path"));
        System.loadLibrary("jni_dll");
		
        Main m = new Main();
		
        System.out.println(m.atinstant(1000.0, 2000.0, "POLYGON(500 250, 600 450, 850 625)", "POLYGON(50 65, 80 90, 45 25)", 1500.0));
    }
}
