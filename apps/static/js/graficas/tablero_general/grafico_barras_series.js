am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    var chart = am4core.create("datos", am4charts.XYChart)
    chart.colors.step = 2;
    
    chart.legend = new am4charts.Legend()
    chart.legend.position = 'top'
    chart.legend.paddingBottom = 20
    chart.legend.labels.template.maxWidth = 95
    chart.legend.labels.template.truncate = false;
    chart.legend.labels.template.wrap = true;
    
    var xAxis = chart.xAxes.push(new am4charts.CategoryAxis())
    xAxis.dataFields.category = 'nombre'
    xAxis.title.text = datos['titulo_x']
    xAxis.title.fontSize = "20px"
    xAxis.renderer.cellStartLocation = 0.1
    xAxis.renderer.cellEndLocation = 0.9
    xAxis.renderer.grid.template.location = 0;
    
    var yAxis = chart.yAxes.push(new am4charts.ValueAxis());
    yAxis.title.text = datos['titulo_y']
    yAxis.title.fontSize = "20px"
    yAxis.min = 0;
    
    function createSeries(value, name) {
        var series = chart.series.push(new am4charts.ColumnSeries())
        series.dataFields.valueY = value
        series.dataFields.categoryX = 'nombre'
        series.name = name
        series.columns.template.tooltipText = "{name}: [bold]{valueY}[/]";
    
        series.events.on("hidden", arrangeColumns);
        series.events.on("shown", arrangeColumns);
    
        var bullet = series.bullets.push(new am4charts.LabelBullet())
        bullet.interactionsEnabled = false
        bullet.dy = 30;
        bullet.label.fill = am4core.color('#ffffff')
    
        return series;
    }
    
    chart.data = datos['datos']
    
    series.forEach(serie => {
        createSeries(serie, serie);
    });
    
    
    function arrangeColumns() {
    
        var series = chart.series.getIndex(0);
    
        var w = 1 - xAxis.renderer.cellStartLocation - (1 - xAxis.renderer.cellEndLocation);
        if (series.dataItems.length > 1) {
            var x0 = xAxis.getX(series.dataItems.getIndex(0), "categoryX");
            var x1 = xAxis.getX(series.dataItems.getIndex(1), "categoryX");
            var delta = ((x1 - x0) / chart.series.length) * w;
            if (am4core.isNumber(delta)) {
                var middle = chart.series.length / 2;
    
                var newIndex = 0;
                chart.series.each(function(series) {
                    if (!series.isHidden && !series.isHiding) {
                        series.dummyData = newIndex;
                        newIndex++;
                    }
                    else {
                        series.dummyData = chart.series.indexOf(series);
                    }
                })
                var visibleCount = newIndex;
                var newMiddle = visibleCount / 2;
    
                chart.series.each(function(series) {
                    var trueIndex = chart.series.indexOf(series);
                    var newIndex = series.dummyData;
    
                    var dx = (newIndex - trueIndex + middle - newMiddle) * delta
    
                    series.animate({ property: "dx", to: dx }, series.interpolationDuration, series.interpolationEasing);
                    series.bulletsContainer.animate({ property: "dx", to: dx }, series.interpolationDuration, series.interpolationEasing);
                })
            }
        }
    }
    
}); // end am4core.ready()