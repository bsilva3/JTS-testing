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
