am4core.ready(function() {
    graficas.forEach(grafica => {
        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        var chart = am4core.create(grafica[0], am4charts.XYChart)

        chart.colors.step = 2;

        chart.data = grafica[1]["datos"]


        var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "nombre";
        categoryAxis.renderer.grid.template.location = 0;
        categoryAxis.renderer.minGridDistance = 30;
        categoryAxis.renderer.inversed = true;
        categoryAxis.title.text = grafica[1]['titulo_x']
        categoryAxis.title.marginTop = '18px'
        categoryAxis.title.fontSize = "18px"
        categoryAxis.renderer.grid.template.disabled = true;


        if (grafica[1]['rotar'] == 'Si'){
            categoryAxis.renderer.labels.template.wrap = true;
            categoryAxis.renderer.labels.template.maxWidth = 120;
            categoryAxis.renderer.labels.template.rotation = -90
            categoryAxis.renderer.labels.template.horizontalCenter = "middle";
            categoryAxis.renderer.labels.template.verticalCenter = "middle";
        }

        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = grafica[1]['titulo_y']
        valueAxis.title.fontSize = "18x"
        valueAxis.min = 0;
        valueAxis.extraMax = 0.1;
        valueAxis.calculateTotals = true;


        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries());
        series.dataFields.valueY = "cantidad";
        series.dataFields.categoryX = "nombre";
        series.name = "cantidad";
        series.columns.template.tooltipText = "{categoryX}: [bold]{valueY}[/]";
        series.columns.template.column.cornerRadiusTopLeft = 5;
        series.columns.template.column.cornerRadiusTopRight = 5;
        series.columns.template.fillOpacity = .8;


        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 0.2;
        columnTemplate.strokeOpacity = 1;

        series.columns.template.fill = am4core.color("#67B7DC");

        var totalBullet = series.bullets.push(new am4charts.LabelBullet());
        totalBullet.dy = -20;
        totalBullet.label.text = "{cantidad}";
        totalBullet.label.hideOversized = false;
        totalBullet.label.fontSize = 15;
        totalBullet.label.background.fill = series.stroke;
        totalBullet.label.background.fillOpacity = 0.2;
        totalBullet.label.padding(5, 10, 5, 10);

        categoryAxis.sortBySeries = series;


    });
}); // end am4core.ready()