am5.ready(function () {
  graficas_donuts.forEach((grafica) => {
    // Create root element
    // https://www.amcharts.com/docs/v5/getting-started/#Root_element
    var root = am5.Root.new(grafica[0]);

    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    root.setThemes([am5themes_Animated.new(root)]);

    // Create chart
    // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
    var chart = root.container.children.push(
      am5percent.PieChart.new(root, {
        layout: root.verticalLayout,
        innerRadius: am5.percent(50),
      })
    );

    // Create series
    // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
    var series = chart.series.push(
      am5percent.PieSeries.new(root, {
        valueField: "cantidad",
        categoryField: grafica[1]["categoria"],
      })
    );

    // Set data
    // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
    series.data.setAll(grafica[1]["datos"]);

    series.labels.template.setAll({
      maxWidth: 150,
      oversizedBehavior: "wrap", // to truncate labels, use "truncate"
    });

    series.events.on("datavalidated", function (ev) {
      var series = ev.target;
      if (ev.target.data.length < 1) {
        // Generate placeholder data
        var categoryField = series.get("categoryField");
        var valueField = series.get("valueField");
        var placeholder = [];
        for (i = 0; i < 3; i++) {
          var item = {};
          item[categoryField] = "";
          item[valueField] = 1;
          placeholder.push(item);
        }
        series.data.setAll(placeholder);

        // Disable ticks/labels
        series.labels.template.set("forceHidden", true);
        series.ticks.template.set("forceHidden", true);

        // Show modal
        modal.open();
      } else {
        // Re-enable ticks/labels
        series.labels.template.set("forceHidden", false);
        series.ticks.template.set("forceHidden", false);

        // Hide modal
        modal.close();
      }
    });

    // Create modal for a "no data" note
    var modal = am5.Modal.new(root, {
      content: "La gráfica no tiene datos.",
    });

    // Create legend
    // https://www.amcharts.com/docs/v5/charts/percent-charts/legend-percent-series/
    var legend = chart.children.push(
      am5.Legend.new(root, {
        centerX: am5.percent(50),
        x: am5.percent(50),
        marginTop: 15,
        marginBottom: 15,
      })
    );

    legend.labels.template.setAll({
      fontSize: 12,
      fontWeight: "200",
    });

    // Play initial series animation
    // https://www.amcharts.com/docs/v5/concepts/animations/#Animation_of_series
    series.appear(1000, 100);
  });
});
