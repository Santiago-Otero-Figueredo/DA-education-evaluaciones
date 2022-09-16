am5.ready(function () {
  graficas.forEach((grafica) => {
    /**
     * ---------------------------------------
     * This demo was created using amCharts 5.
     *
     * For more information visit:
     * https://www.amcharts.com/
     *
     * Documentation is available at:
     * https://www.amcharts.com/docs/v5/
     * ---------------------------------------
     */

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
        layout: root.verticalLayout,
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

    var data = grafica[1]["datos"]

    // Create axes
    // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/

    var xRenderer = am5xy.AxisRendererX.new(root, {});
    xRenderer.grid.template.set("visible", false);

    var xAxis = chart.xAxes.push(
      am5xy.CategoryAxis.new(root, {
        categoryField: "categoria",
        renderer: xRenderer,
        tooltip: am5.Tooltip.new(root, {}),
      })
    );

    xAxis.data.setAll(data);

    xAxis.get("renderer").labels.template.setAll({
      oversizedBehavior: "wrap",
      maxWidth: 125
    });

    var yRenderer = am5xy.AxisRendererY.new(root, {});
    //yRenderer.grid.template.set("visible", false);

    var yAxis = chart.yAxes.push(
      am5xy.ValueAxis.new(root, {
        calculateTotals: true,
        min: 0,
        extraMax: 0.15,
        renderer: yRenderer,
      })
    );

    // Add series
    // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
    function makeSeries(name, fieldName, showTotal) {
      var series = chart.series.push(
        am5xy.ColumnSeries.new(root, {
          name: name,
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: fieldName,
          categoryXField: "categoria",
          stacked: true,
          maskBullets: false,
        })
      );

      series.columns.template.setAll({
        tooltipText: "{name}, {categoryX}:{valueY}",
        width: am5.percent(90),
        tooltipY: 0,
      });

      if (showTotal) {
        series.bullets.push(function () {
          return am5.Bullet.new(root, {
            locationY: 1,
            sprite: am5.Label.new(root, {
              text: "{valueYTotal}",
              fill: am5.color(0x000000),
              centerY: am5.p100,
              centerX: am5.p50,
              populateText: true,
            }),
          });
        });
      } else {
        series.bullets.push(function () {
          return am5.Bullet.new(root, {
            sprite: am5.Label.new(root, {
              text: "{valueY}",
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

    series.forEach(element => {
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
    })
    makeSeries("", "total", true);
    // Create modal for a "no data" note
    var modal = am5.Modal.new(root, {
      content: "La gráfica no tiene datos.",
    });
    // Make stuff animate on load
    // https://www.amcharts.com/docs/v5/concepts/animations/
    chart.appear(1000, 100);
  });
});
