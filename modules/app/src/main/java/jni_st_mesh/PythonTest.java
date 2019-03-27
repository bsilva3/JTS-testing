package jni_st_mesh;

import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

/**
 *
 * @author Bruno Silva
 */
public class PythonTest {
    
    public static void main(String[] args){
        PythonInterpreter interpreter = new PythonInterpreter();
        interpreter.execfile("C:\\Users\\bjpsi\\Desktop\\Investigacao\\pyt.py");
        PyObject str = interpreter.eval("test(5)");
        System.out.println(str.toString());  
    }
}
