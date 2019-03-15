package jni_st_mesh;

import java.util.Arrays;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import javax.swing.JTable;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

/**
 *
 * @author Bruno Silva
 */
public class ChartMaker {
    
    /**
     * Create a line chart with the evolution of the area of a geometry through time.
     * @param areaEV - array of values of the evolution of the area through time
     * @param beginTime
     * @param endTime
     * @return the Chart Panel Swing component with the generated chart
     */
    public static ChartPanel createLineChartAreaEV(double[] areaEV, double beginTime, double endTime){
        JFreeChart lineChart = ChartFactory.createXYLineChart("area evolution", "Area", "Time",
                createDataset(areaEV, 1000.0, 2000.0), PlotOrientation.HORIZONTAL, true,true,false);
        
        // Assign it to the chart
        XYPlot plot = (XYPlot) lineChart.getPlot();
        //plot.setDomainAxis(xAxis);
        
        NumberAxis xAxis = (NumberAxis) plot.getRangeAxis();
        //xAxis.setTickUnit(new NumberTickUnit( NUMBER_OF_TICKS_X_AXIS ));
        xAxis.setRange(beginTime, endTime);
        //xAxis.setAutoRangeMinimumSize(beginTime);
        
        NumberAxis yAxis = (NumberAxis) plot.getDomainAxis();
        //get max min value of area
        //double min = Arrays.stream(areaEV).min().getAsDouble();
        double max = Arrays.stream(areaEV).max().getAsDouble();
        yAxis.setRange(0, max+5);
        //yAxis.setTickUnit(new NumberTickUnit(10));
        
        return new ChartPanel(lineChart);
        
    }
    
    //add the data to show in the chart
    private static XYSeriesCollection createDataset(double[] areaEV, double beginTime, double endTime) {
        XYSeries dataset = new XYSeries("Area");
        //DefaultCategoryDataset dataset = new DefaultCategoryDataset( );
        double time = beginTime;
        for (double area : areaEV){
            dataset.add( area, ++time  );
            //dataset.addValue( d , "Area", ++v+"" );
        }
        return new XYSeriesCollection(dataset);
    }
    
    public static JTable createTable(Map<String, Double> data, String[] columnNames){
        //JTable jtable = new JTable(data, columnNames);
        Object[][] arr = new Object[data.size()][2];
        Set entries = data.entrySet();
        Iterator entriesIterator = entries.iterator();
        int i = 0;
        while(entriesIterator.hasNext()){

            Map.Entry mapping = (Map.Entry) entriesIterator.next();

            arr[i][0] = mapping.getKey();
            arr[i][1] = mapping.getValue();

            i++;
        }
        return null;
    }
}
