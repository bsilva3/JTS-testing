package jni_st_mesh;

/**
 *
 * @author Bruno Silva
 */
public enum Metrics 
{
	AREA(1), PERIMETER(2);
		
	private int value;    

	private Metrics(int value) {
		this.value = value;
	}

	public int get_value() {
		return value;
	}
        public static String[] getStatStringList(){
            return new String[]{AREA.toString(), PERIMETER.toString()};
        }
}
