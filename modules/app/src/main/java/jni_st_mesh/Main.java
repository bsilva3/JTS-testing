/**
 *
 */
package jni_st_mesh;


import java.util.HashMap;

/**
 * @author jduarte
 *
 */
public class Main
{
    private static final long serialVersionUID = 4092938070485225093L;
    
    /*
    1. Add
    int triangulation_method,	// triangulation method to use
    boolean cw					// vertices order
    
    to:
    at_instant_poly()
    at_instant_mesh()
    
    2. Sort the maps befor plotting.
    
    New mapping of functions:
    
    at_instant_poly								-> at_instant_poly
    String[] during_period_poly_2				-> String[] during_period_poly
    String at_instant_mesh_2					-> String at_instant_mesh
    String[] during_period_mesh_2				-> String[] during_period_mesh
    HashMap<String, Double> quality_measures_2	-> HashMap<String, Double> quality_measures
    double[] area_EV							-> HashMap<String, Double> ststistics
    
    deleted
    String during_period_poly
    double[] at_instant_mesh
    double[] during_period_mesh
    double[] area_EV
    
    New
    String[] during_period_poly_bbox
    
    // enum Ststistics
    
    package jni_st_mesh;
    
    public enum Ststistics
    {
    AREA_EVOLUTION(1), ROTATION_ANGLES(2), COLLINEAR_POINTS_BY_METHOD(3);
    
    private int value;
    
    private Ststistics(int value) {
    this.value = value;
    }
    
    public int get_value() {
    return value;
    }
    }
    
    // End enum Ststistics
    
    Notes:
    When a function returns a map the keys must be sorted before plotting if the
    x axis is to be in some order!
    
    */
    
    /**
     * Returns the polygon WKT.
     */
    public native String at_instant_poly(
            double b,					// begin instant
            double e,					// end instant
            String source_wkt,			// P
            String target_wkt,			// Q
            double t,					// instant
            int triangulation_method,	// triangulation method to use
            boolean cw,					// vertices order
            double threshold			// threshold to find collinear points
    );
    
    /*
    native String during_period_poly
    (
    double b,					// begin instant
    double e,					// end instant
    String source_wkt,			// P
    String target_wkt,			// Q
    double period_b,			// period begin
    double period_e,			// period end
    int num_samples			// number of samples
    );
    
    // Returns an array of Polygon.
    native String[] during_period_poly_2
    (
    double b,					// begin instant
    double e,					// end instant
    String source_wkt,			// P
    String target_wkt,			// Q
    double period_b,			// period begin
    double period_e,			// period end
    int num_samples			// number of samples
    );
    */
    
    /**
     * Returns an array of Polygon WKTs.
     */
    public native String[] during_period_poly
    (
            double b,					// begin instant
            double e,					// end instant
            String source_wkt,			// P
            String target_wkt,			// Q
            double period_b,			// period begin
            double period_e,			// period end
            int num_samples,			// number of samples
            int triangulation_method,	// triangulation method to use
            boolean cw,					// vertices order
            double threshold			// threshold to find collinear points
    );

    /*
    native double[] at_instant_mesh
    (
    double b,					// begin instant
    double e,					// end instant
    String source_wkt,			// P
    String target_wkt,			// Q
    double t					// at instant
    );
    */

    /**
     * Returns a Multipolygon WKT.
     */
    public native String at_instant_mesh
    (
            double b,					// begin instant
            double e,					// end instant
            String source_wkt,			// P
            String target_wkt,			// Q
            double t,					// at instant
            int triangulation_method,	// triangulation method to use
            boolean cw,					// vertices order
            double threshold			// threshold to find collinear points
    );

    /*
    native double[] during_period_mesh
    (
    double b,					// begin instant
    double e,					// end instant
    String source_wkt,			// P
    String target_wkt,			// Q
    double period_b,			// period begin
    double period_e,			// period end
    int num_samples				// number of samples
    );

    // Returns an array of Multipolygon.
    native String[] during_period_mesh_2
    (
    double b,					// begin instant
    double e,					// end instant
    String source_wkt,			// P
    String target_wkt,			// Q
    double period_b,			// period begin
    double period_e,			// period end
    int num_samples				// number of samples
    );
    */

    /**
     * Returns an array of Multipolygon WKTs.
     */
    public native String[] during_period_mesh
    (
            double b,					// begin instant
            double e,					// end instant
            String source_wkt,			// P
            String target_wkt,			// Q
            double period_b,			// period begin
            double period_e,			// period end
            int num_samples,			// number of samples
            int triangulation_method,	// triangulation method to use
            boolean cw,					// vertices order
            double threshold			// threshold to find collinear points
    );

    /**
     * Returns an array of Polygon WKTs of the bboxs during interpolation.
     */
    public native String[] during_period_poly_bbox
    (
            double b,					// begin instant
            double e,					// end instant
            String source_wkt,			// P
            String target_wkt,			// Q
            double period_b,			// period begin
            double period_e,			// period end
            int num_samples,			// number of samples
            int triangulation_method,	// triangulation method to use
            boolean cw,					// vertices order
            double threshold			// threshold to find collinear points
    );

    /*
    native double[] area_EV
    (
    double b,
    double e,
    String source_wkt,
    String target_wkt,
    int num_samples
    );
    */

    /*
    native double[] ststistics
    (
    double b,
    double e,
    String source_wkt,
    String target_wkt,
    int num_samples,			// info to create the unit
    int triangulation_method,
    boolean cw,					// vertices order
    int statistic_type			// type of statistic
    );
    */

    /*
    native double[] area_evolution
    (
    double b,
    double e,
    String source_wkt,
    String target_wkt,
    int num_samples,
    int triangulation_method
    );
    */

    /*
    native double[] quality_measures
    (
    double b,
    double e,
    String source_wkt,
    String target_wkt,
    int num_samples
    );
    */

    /**
     * Returns a map of ststistics.
     * Available ststistics are defined in Ststistics.java (Ststistics enum).
     */
    public native HashMap<String, Double> ststistics
    (
            double b,
            double e,
            String source_wkt,
            String target_wkt,
            int num_samples,			// info to create the unit
            int triangulation_method,	// triangulation method to use
            boolean cw,					// vertices order
            double threshold,			// threshold to find collinear points
            int statistic_type			// type of statistic
    );

    /**
     * Returns a map of quality measures.
     */
    public native HashMap<String, Double> quality_measures
    (
            String geometry_wkt,		// Geometry wkt
            int triangulation_method,	// triangulation method to use
            boolean cw,					// vertices order
            double threshold,			// threshold to find collinear points
            int options					// for future use
    );


    public Main()
    {
        System.loadLibrary("java_mesh");
    }
                                                        
                                                        /*public static void main(String[] args)
                                                        {
                                                        Main ex = new Main();
                                                        
                                                        EventQueue.invokeLater(new Runnable()
                                                        {
                                                        public void run() {
                                                        try {
                                                        MainWindow frame = new MainWindow(ex);
                                                        frame.setVisible(true);
                                                        } catch (Exception e) {
                                                        e.printStackTrace();
                                                        }
                                                        }
                                                        });
                                                        }*/
}