package jni_st_mesh;

public enum TriangulationMethod 
{
	COMPATIBLE(1), EQUILATERAL(2);
	
	private int value;    

	private TriangulationMethod(int value) {
		this.value = value;
	}

	public int get_value() {
		return value;
	}
}
