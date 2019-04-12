package jni_st_mesh;

import java.text.DecimalFormat;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;
import javax.swing.JTable;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.axis.NumberTickUnit;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

/**
 *
 * Utility class that, given a data set, creates a chart with it.
 */
public class ChartMaker {
    
    /**
     * Create a line chart with the evolution of the area of a geometry through time.
     * @param statistics - map with the statistics over time (area, rotation angles...)
     * @param headerLegend - Title of the chart
     * @param xAxisLegend - x axis legend
     * @param yAxisLegend - y axis legend
     * @return the Chart Panel Swing component with the generated chart
     */
    public ChartPanel createLineChart(Map<String, Double> statistics, String headerLegend, String xAxisLegend, String yAxisLegend){
        
        XYSeries dataset = new XYSeries(headerLegend);
        //DefaultCategoryDataset dataset = new DefaultCategoryDataset( );
        
        //sort the key (by instant)and convert to int
        SortedSet<Integer> instants = sortMapKeys(statistics);
        
        DecimalFormat df = new DecimalFormat("#.00"); 
        /////add the sorted elements to the dataset
        for (Integer instant : instants) { 
            //System.out.println(instant+" -> "+statistics.get(instant.toString()));
           //dataset.add( Double.parseDouble(df.format(statistics.get(instant.toString()))), instant  );
           dataset.add( statistics.get(instant.toString()), instant  );
        }
        
        XYSeriesCollection datasetSeries = new XYSeriesCollection(dataset);
        
        JFreeChart lineChart = ChartFactory.createXYLineChart(headerLegend, yAxisLegend, xAxisLegend,
                datasetSeries, PlotOrientation.HORIZONTAL, true,true,false);
        
        // Assign it to the chart
        XYPlot plot = (XYPlot) lineChart.getPlot();
        //plot.setDomainAxis(xAxis);
        
        NumberAxis xAxis = (NumberAxis) plot.getRangeAxis();
        //xAxis.setTickUnit(new NumberTickUnit( NUMBER_OF_TICKS_X_AXIS ));
        xAxis.setRange(instants.first(), instants.last());
        xAxis.setAutoTickUnitSelection(true);
        //xAxis.setAutoRangeMinimumSize(instants.first());
        xAxis.setAutoRangeIncludesZero(true);
        
        NumberAxis yAxis = (NumberAxis) plot.getDomainAxis();
        //get max min value of area
        //double min = statistics.values().stream().min(Double::compare).get();
        double max = statistics.get(instants.last().toString());
        double min = statistics.get(instants.first().toString());
        DecimalFormat newFormat = new DecimalFormat("0.0");
        yAxis.setNumberFormatOverride(newFormat);
        yAxis.setRange(0, max+5);
        //yAxis.setAutoRange(true);
        //yAxis.setTickUnit(new NumberTickUnit(statistics.size()/2));
        
        return new ChartPanel(lineChart);
        
    }
    
    public ChartPanel createBarChart(Map<String, Double> statistics, String headerLegend, String xAxisLegend, String yAxisLegend){
        
        XYSeries dataset = new XYSeries(headerLegend);
        //DefaultCategoryDataset dataset = new DefaultCategoryDataset( );
        
        //sort the key (by instant)and convert to int
        SortedSet<Integer> instants = sortMapKeys(statistics);
        
        for (Integer instant : instants) { 
           dataset.add(instant, statistics.get(instant.toString()));
        }
        
        XYSeriesCollection datasetSeries = new XYSeriesCollection(dataset);
        
        JFreeChart lineChart = ChartFactory.createXYBarChart(headerLegend, xAxisLegend, false, yAxisLegend,
                datasetSeries);
        
        // Assign it to the chart
        XYPlot plot = (XYPlot) lineChart.getPlot();
        //plot.setDomainAxis(xAxis);
        
        NumberAxis xAxis = (NumberAxis) plot.getRangeAxis();
        //xAxis.setTickUnit(new NumberTickUnit( NUMBER_OF_TICKS_X_AXIS ));
        xAxis.setRange(0, statistics.get(instants.last().toString())+5);
        xAxis.setAutoTickUnitSelection(true);
        //xAxis.setAutoRangeMinimumSize(instants.first());
        xAxis.setAutoRangeIncludesZero(true);
        
        /*NumberAxis yAxis = (NumberAxis) plot.getDomainAxis();
        //get max min value of area
        //double min = statistics.values().stream().min(Double::compare).get();
        double max = statistics.get(instants.last().toString());
        double min = statistics.get(instants.first().toString());
        DecimalFormat newFormat = new DecimalFormat("0.00");
        yAxis.setNumberFormatOverride(newFormat);
        yAxis.setRange(min-5, max+5);
        //yAxis.setAutoRange(true);
        yAxis.setTickUnit(new NumberTickUnit(statistics.size()/2));*/
        
        return new ChartPanel(lineChart);
        
    }
    
    public JTable createJTable(Map<String, ?> dataset, String xAxisLegend, String yAxisLegend){
        //headers for the table
        String[] columns = new String[] {xAxisLegend, yAxisLegend };
        Object[][] data;
        
        //sort the key
        SortedSet<Integer> statKeys = sortMapKeys(dataset);
        
        data = new Object[dataset.size()][columns.length];
        int i = 0;
        for (Integer statKey : statKeys) {
            data[i][0] = statKey;
            data[i][1] = dataset.get(statKey.toString());
            i++;
        }
        
        //create table with data
        return new JTable(data, columns);
    }
    
    private SortedSet<Integer> sortMapKeys(Map<String, ?> map){
        //sort the key (by instant)and convert to int
        Set<String> keys = new HashSet<>(map.keySet());
        SortedSet<Integer> sortedKeys = new TreeSet<>();
        for (String inst : keys){
            sortedKeys.add(Integer.parseInt(inst));
        }
        return sortedKeys;
    }
}
