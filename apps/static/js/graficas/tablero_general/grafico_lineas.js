am4core.ready(function() {
 
    lineas.forEach(grafica => {
        
        
       // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end
      
        var chart = am4core.create(grafica[0], am4charts.XYChart);
        chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
        
        chart.data = grafica[1]["datos"]
              
        chart.colors.step = 2;
        chart.padding(30, 30, 10, 30);
        chart.legend = new am4charts.Legend();

        // Create axes
        //var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
        dateAxis.renderer.minGridDistance = 50;      
        dateAxis.title.text = grafica[1]['titulo_x']
        dateAxis.title.fontSize = "20px"

        //var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());        
        valueAxis.title.text = grafica[1]['titulo_y']
        valueAxis.title.fontSize = "20px"
        
        // Create series if(grafica[1]['continua'] === 'No'){series.connect = false} 
        var series = chart.series.push(new am4charts.LineSeries());
        series.name = "Entradas";
        series.dataFields.valueY = "cantidad";
        series.dataFields.dateX = "nombre";
        series.strokeWidth = 2;
               
        series.minBulletDistance = 10;
        series.tooltipText = "{valueY}";
        series.tooltip.pointerOrientation = "vertical";
        series.tooltip.background.cornerRadius = 20;
        series.tooltip.background.fillOpacity = 0.5;
        series.tooltip.label.padding(12,12,12,12)

        if(grafica[1]['total']){
            var series2 = chart.series.push(new am4charts.LineSeries());
            series2.name = "Total personas";
            series2.dataFields.valueY = "total";
            series2.dataFields.dateX = "nombre";
            series2.strokeWidth = 2;        
            series2.minBulletDistance = 10;
            series2.tooltipText = "{valueY}";
            series2.tooltip.pointerOrientation = "vertical";
            series2.tooltip.background.cornerRadius = 20;
            series2.tooltip.background.fillOpacity = 0.5;
            series2.tooltip.label.padding(12,12,12,12)
        }

        // Add scrollbar
        chart.scrollbarX = new am4charts.XYChartScrollbar();
        if(grafica[1]['total']){
            chart.scrollbarX.series.push(series,series2);
        }else{
            chart.scrollbarX.series.push(series);
        }
        // Add cursor
        chart.cursor = new am4charts.XYCursor();
        chart.cursor.xAxis = dateAxis;
        
        if(grafica[1]['total']){
            chart.cursor.snapToSeries = [series, series2];
        }else{
            chart.cursor.snapToSeries = series;
        }
    });

}); // end am4core.ready()