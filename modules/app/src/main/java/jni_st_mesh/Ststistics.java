package jni_st_mesh;

public enum Ststistics 
{
	AREA_EVOLUTION(1), ROTATION_ANGLES(2), COLLINEAR_POINTS_BY_METHOD(3), QUALITY_MEASURES(4);
	
	private int value;    

	private Ststistics(int value) {
		this.value = value;
	}

	public int get_value() {
		return value;
	}
        
        public static String[] getStatStringList(){
            String[] s = {AREA_EVOLUTION.toString(), ROTATION_ANGLES.toString(), COLLINEAR_POINTS_BY_METHOD.toString(), 
                QUALITY_MEASURES.toString()};
            return s;
        }
        
        public static int stringToInt(String statisticString){
            int statistic = 0;
            if(statisticString.equals(AREA_EVOLUTION.toString())){
            statistic = AREA_EVOLUTION.get_value();
            }
            else if(statisticString.equals(ROTATION_ANGLES.toString())){
                statistic = ROTATION_ANGLES.get_value();
            }
            else if(statisticString.equals(COLLINEAR_POINTS_BY_METHOD.toString())){
                statistic = COLLINEAR_POINTS_BY_METHOD.get_value();
            }
            else if(statisticString.equals(QUALITY_MEASURES.toString())){
                statistic = QUALITY_MEASURES.get_value();
            }
            return statistic;
        }
}
