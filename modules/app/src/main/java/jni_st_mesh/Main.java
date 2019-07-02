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
    
    /**
     * Returns the polygon WKT.
     * NOCHANGE.
     */
    native String at_instant_poly(
            double b,					// begin instant
            double e,					// end instant
            String source_wkt,			// P
            String target_wkt,			// Q
            double t,					// instant
            int triangulation_method,	// triangulation method to use
            boolean cw,					// vertices order
            double threshold			// threshold to find collinear points
    );
    
    /**
     * Returns an array of Polygon wkts.
     *
     * New: add_rotation
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
                        double threshold,			// threshold to find collinear points
                        double add_rotation			// add extra rotation to the geometry during interpolation. Pass 0 here!
                );
                
        /**
         * Returns a Multipolygon WKT.
         * NOCHANGE.
         */
        public native String at_instant_mesh
        (
            double b,                    // begin instant
            double e,                    // end instant
            String source_wkt,           // P
            String target_wkt,           // Q
            double t,                    // at instant
            int triangulation_method,    // triangulation method to use
            boolean cw,                  // vertices order
            double threshold             // threshold to find collinear points
        );

    /**
     * Returns an array of Multipolygon WKTs.
     * NOCHANGE.
     */
    public native String[] during_period_mesh
    (
            double b,                                                                              // begin instant
            double e,                    // end instant
            String source_wkt,           // P
            String target_wkt,           // Q
            double period_b,             // period begin
            double period_e,             // period end
            int num_samples,             // number of samples
            int triangulation_method,    // triangulation method to use
            boolean cw,                  // vertices order
            double threshold             // threshold to find collinear points
    );

    /**
     * Returns an array of Polygon WKTs of the bboxs during interpolation.
     * NOCHANGE.
     */
    public native String[] during_period_poly_bbox
    (
            double b,                    // begin instant
            double e,                    // end instant
            String source_wkt,           // P
            String target_wkt,           // Q
            double period_b,             // period begin
            double period_e,             // period end
            int num_samples,             // number of samples
            int triangulation_method,    // triangulation method to use
            boolean cw,                  // vertices order
            double threshold             // threshold to find collinear points
    );

    /**
     * Returns a map of ststistics.
     * Available ststistics are defined in Ststistics.java (Ststistics enum).
     * NOCHANGE. 'DONTNOT' :) USE THIS F. TO COMPUTE THE AREA DURING INTERPOLATION!
     */
    public native HashMap<String, Double> ststistics
    (
            double b,
            double e,
            String source_wkt,
            String target_wkt,
            int num_samples,             // info to create the unit
            int triangulation_method,    // triangulation method to use
            boolean cw,                  // vertices order
            double threshold,            // threshold to find collinear points
            int statistic_type           // type of statistic
    );

    /**
     * Returns a map of quality measures.
     * NOCHANGE. I think this is mainly for meshes?
     * Anyways, use numerical_metric and compare_geometries to get metrics and compare geometries!
     */
    public native HashMap<String, Double> quality_measures
    (
            String geometry_wkt,         // Geometry wkt
            int triangulation_method,    // triangulation method to use
            boolean cw,                  // vertices order
            double threshold,            // threshold to find collinear points
            int options                  // for future use
    );

    /**
     * Returns a numerical metric about a geometry.
     * NEW.
     */
    public native double numerical_metric
        (
                String geometry_wkt,		// Geometry wkt
                int metric					// metric to use
        );

        /**
         * Compares two geometries using a metric.
         * NEW.
         */
    public native double compare_geometries
    (
            String ref_geometry_wkt,	// Reference geometry wkt, i.e. the geometry to compare with
            String geometry_wkt,		// Geometry wkt
            int metric					// metric to use for comparison
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