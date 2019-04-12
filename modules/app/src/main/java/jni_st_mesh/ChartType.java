package jni_st_mesh;

import static jni_st_mesh.Ststistics.AREA_EVOLUTION;
import static jni_st_mesh.Ststistics.COLLINEAR_POINTS_BY_METHOD;
import static jni_st_mesh.Ststistics.QUALITY_MEASURES;
import static jni_st_mesh.Ststistics.ROTATION_ANGLES;

/**
 *
 * @author Bruno Silva
 */
public enum ChartType {
    LINE_CHART("Line Chart"), BAR_CHART("Bar Chart"), TABLE("Table");
	
    private String value;    

    private ChartType(String value) {
            this.value = value;
    }

    public String getValue() {
            return value;
    }
    
    public static String[] getChartTypeList(){
            String[] s = {LINE_CHART.getValue(), BAR_CHART.getValue(), TABLE.getValue()};
            return s;
    }
}
