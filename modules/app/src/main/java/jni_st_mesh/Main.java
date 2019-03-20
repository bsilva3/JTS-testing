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
	/**
	 * 
	 */
	private static final long serialVersionUID = 4092938070485225093L;

	//native String atinstant(double ts, double tf, String P, String Q, double t); 
		
	public native String at_instant_poly(
		double b,					// begin instant
		double e,					// end instant
		String source_wkt,			// P
		String target_wkt,			// Q
		double t	
	);

	public native String during_period_poly
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
	public native String[] during_period_poly_2
	(
		double b,					// begin instant
		double e,					// end instant
		String source_wkt,			// P
		String target_wkt,			// Q
		double period_b,			// period begin
		double period_e,			// period end
		int num_samples			// number of samples
	);
	
	public native double[] at_instant_mesh
	(
		double b,					// begin instant
		double e,					// end instant
		String source_wkt,			// P
		String target_wkt,			// Q
		double t					// at instant
	);

	// Returns a Multipolygon
	public native String at_instant_mesh_2
	(
		double b,					// begin instant
		double e,					// end instant
		String source_wkt,			// P
		String target_wkt,			// Q
		double t					// at instant
	);
	
	public native double[] during_period_mesh
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
	public native String[] during_period_mesh_2
	(
		double b,					// begin instant
		double e,					// end instant
		String source_wkt,			// P
		String target_wkt,			// Q
		double period_b,			// period begin
		double period_e,			// period end
		int num_samples				// number of samples
	);
	
	public native double[] area_EV
	(
		double b,
		double e,
		String source_wkt,
		String target_wkt,
		int num_samples
	);
	
	public native HashMap<String, Double> quality_measures_2
        (
            String geometry_wkt
        );

		
	public Main() 
        {
        }
		
	public static void main(String[] args) 
	{
		System.loadLibrary("java_mesh");
		
		Main m = new Main();
		
		// New interfaces.
		
		// An array of POLYGON
		String[] arr = m.during_period_poly_2(1000.0, 2000.0, "POLYGON((0 0, 0 8, 2 8, 2 2, 4 2, 4 8, 6 8, 6 0))", "POLYGON((6 8, 6 0, 4 0, 4 6, 2 6, 2 0, 0 0, 0 8))", 1000, 2000, 1000);
				
	      for(String name: arr)
	          System.out.println(name);

		// An array of MULTIPOLYGON
		String[] arr_p = m.during_period_mesh_2(1000.0, 2000.0, "POLYGON((0 0, 0 8, 2 8, 2 2, 4 2, 4 8, 6 8, 6 0))", "POLYGON((6 8, 6 0, 4 0, 4 6, 2 6, 2 0, 0 0, 0 8))", 1000, 2000, 1000);
			
		for(String name: arr_p)
			System.out.println(name);
	}
        /**
		 * 
		 */
	/*private static final long serialVersionUID = 1L;
		
	private int geom = 0;
        private int N = 0;
        private MultiPolygon col = null;
        Timer timer = null;
        IFrame f = this;

        public IFrame(MultiPolygon m_polygon) 
        {
        	col = m_polygon;
        	N = col.getNumGeometries();
        	
        	super.setBackground(Color.white);
        	
            timer = new Timer(16, new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) 
                {
                    repaint();
                    
                    BufferedImage bi = ScreenImage.createImage(f);
                    
        	        try {
        				ScreenImage.writeImage(bi, "D:\\fig_i_" + (100 + geom) + ".png");
        			} catch (IOException ex) {
        				ex.printStackTrace();
        			}        			
                }
            });
            
            timer.start();
        }

        @Override
        public Dimension getPreferredSize() {
            return new Dimension(800, 600);
        }*/

        /*@Override
        protected void paintComponent(Graphics g) 
        {
            super.paintComponent(g);
            //System.out.println("B");
            
            if(geom >= N) {
            	return; 
            }
            
        	Polygon p = (Polygon) col.getGeometryN(geom);
        	geom++;
        	
            Graphics2D gr = (Graphics2D) g.create();
            
            gr.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

            
            AffineTransform at = new AffineTransform();
            at.translate(100, 400);
            at.scale(20, -20);
	        
            gr.setColor(Color.blue);
            gr.fill(new LiteShape(p, at, false));
	        gr.draw(new LiteShape(p, at, false));     
	        
	        //File f = new File("D:\\i_" + (geom - 1) + ".png");
	        
	        //BufferedImage bi = ScreenImage.createImage(this);
        */
	        
	        /*
	        try {
				ScreenImage.writeImage(bi, "D:\\i_" + (geom - 1) + ".png");
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
		        //System.out.println("..........");
			}
			*/
	        	        
	        //ScreenImage.createImage( gr );
	        
            /*gr.dispose();
            
            if(geom >= N) {
            	timer.stop();
            	return;    	
            }
        }
    }*/
}