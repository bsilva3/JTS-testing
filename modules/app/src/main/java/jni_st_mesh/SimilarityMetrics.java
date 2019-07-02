package jni_st_mesh;

/**
 *
 * @author Bruno Silva
 */
public enum SimilarityMetrics 
{
	GEOMETRIC_SIMILARITY(1), JACCARD_INDEX(2);
			
	private int value;    

	private SimilarityMetrics(int value) {
		this.value = value;
	}

	public int get_value() {
		return value;
	}
        
        public static String[] getStatStringList(){
            return new String[]{GEOMETRIC_SIMILARITY.toString(), JACCARD_INDEX.toString()};
        }
}