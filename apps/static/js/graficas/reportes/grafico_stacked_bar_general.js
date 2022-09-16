am5.ready(function () {
  graficas.forEach((grafica) => {
    // Create root element
    // https://www.amcharts.com/docs/v5/getting-started/#Root_element
    var root = am5.Root.new(grafica[0]);

    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    root.setThemes([am5themes_Animated.new(root)]);

    // Create chart
    // https://www.amcharts.com/docs/v5/charts/xy-chart/
    var chart = root.container.children.push(
      am5xy.XYChart.new(root, {
        panX: false,
        panY: false,
        wheelX: "panY",
        wheelY: "zoomY",
        layout: root.gridLayout,
        maxHeight: 390,
      })
    );

    // Add scrollbar
    // https://www.amcharts.com/docs/v5/charts/xy-chart/scrollbars/

    var data = grafica[1]["datos"];

    // Create axes
    // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/

    var yRenderer = am5xy.AxisRendererY.new(root, {});
    yRenderer.grid.template.set("visible", false);

    var yAxis = chart.yAxes.push(
      am5xy.CategoryAxis.new(root, {
        categoryField: "categoria",
        renderer: yRenderer,
        tooltip: am5.Tooltip.new(root, {}),
      })
    );

    yAxis.data.setAll(data);

    var xAxis = chart.xAxes.push(
      am5xy.ValueAxis.new(root, {
        min: 0,
        maxPrecision: 0,
        calculateTotals: true,
        renderer: am5xy.AxisRendererX.new(root, {}),
      })
    );

    // Add legend
    // https://www.amcharts.com/docs/v5/charts/xy-chart/legend-xy-series/
    var legend = chart.children.push(
      am5.Legend.new(root, {
        centerX: am5.p50,
        x: am5.p50,
      })
    );

    xAxis.children.push(
      am5.Label.new(root, {
        text: grafica[1]["titulo_x"],
        x: am5.p50,
        centerX: am5.p50,
      })
    );

    yAxis.children.unshift(
      am5.Label.new(root, {
        rotation: -90,
        text: grafica[1]["titulo_y"],
        y: am5.p50,
        centerX: am5.p50,
      })
    );

    yAxis.get("renderer").labels.template.setAll({
      oversizedBehavior: "wrap",
      maxWidth: 200,
      textAlign: "right",
    });

    // Add series
    // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
    function makeSeries(name, fieldName, showTotal) {
      var series = chart.series.push(
        am5xy.ColumnSeries.new(root, {
          name: name,
          stacked: true,
          xAxis: xAxis,
          yAxis: yAxis,
          baseAxis: yAxis,
          valueXField: fieldName,
          maskBullets: false,
          categoryYField: "categoria",
        })
      );

      series.columns.template.setAll({
        tooltipText: "{name}, {categoryY}: {valueX}",
        tooltipY: am5.percent(90),
      });

      if (showTotal) {
        series.bullets.push(function () {
          return am5.Bullet.new(root, {
            locationX: 1,
            sprite: am5.Label.new(root, {
              text: "{valueXTotal}",
              fill: am5.color(0x000000),
              centerY: am5.p50,
              centerX: am5.p0,
              populateText: true,
            }),
          });
        });
      } else {
        series.bullets.push(function () {
          return am5.Bullet.new(root, {
            sprite: am5.Label.new(root, {
              text: "{valueX}",
              fill: root.interfaceColors.get("alternativeText"),
              centerY: am5.p50,
              centerX: am5.p50,
              populateText: true,
            }),
          });
        });
      }

      series.data.setAll(data);
      series.appear();

      if (!showTotal) {
        legend.data.push(series);
      }
      return series
    }

    grafica[2].forEach((element) => {
      var series = makeSeries(element, element);

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
          // series.labels.template.set("forceHidden", true);
          // series.ticks.template.set("forceHidden", true);

          // Show modal
          modal.open();
        } else {
          // Re-enable ticks/labels
          // series.labels.template.set("forceHidden", false);
          // series.ticks.template.set("forceHidden", false);
          // Hide modal
          modal.close();
        }
      });
    });

    makeSeries("", "total", true);

    // Create modal for a "no data" note
    var modal = am5.Modal.new(root, {
      content: "La gráfica no tiene datos.",
    });

    // Make stuff animate on load
    // https://www.amcharts.com/docs/v5/concepts/animations/
    chart.appear(1000, 100);
  });
}); // end am5.ready()
