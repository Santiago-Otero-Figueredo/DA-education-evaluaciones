am5.ready(function () {
  graficas_sorted.forEach((grafica) => {
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
        wheelX: "none",
        wheelY: "none",
      })
    );

    // We don't want zoom-out button to appear while animating, so we hide it
    chart.zoomOutButton.set("forceHidden", true);

    // Create axes
    // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
    var yRenderer = am5xy.AxisRendererY.new(root, {
      minGridDistance: 30,
    });

    // hide grid
    yRenderer.grid.template.set("visible", false);

    var yAxis = chart.yAxes.push(
      am5xy.CategoryAxis.new(root, {
        maxDeviation: 0,
        categoryField: grafica[1]["categoria"],
        renderer: yRenderer,
        tooltip: am5.Tooltip.new(root, { themeTags: ["axis"] }),
      })
    );

    var xAxis = chart.xAxes.push(
      am5xy.ValueAxis.new(root, {
        maxDeviation: 0,
        min: 0,
        extraMax: 0.1,
        renderer: am5xy.AxisRendererX.new(root, {}),
      })
    );

    // Add series
    // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
    var series = chart.series.push(
      am5xy.ColumnSeries.new(root, {
        name: "Series 1",
        xAxis: xAxis,
        yAxis: yAxis,
        valueXField: "cantidad",
        categoryYField: grafica[1]["categoria"],
        tooltip: am5.Tooltip.new(root, {
          pointerOrientation: "left",
          labelText: "{valueX}",
        }),
      })
    );

    // Rounded corners for columns
    series.columns.template.setAll({
      cornerRadiusTR: 5,
      cornerRadiusBR: 5,
    });

    //Colors
    series.set("fill", am5.color("#67B7DC"));

    // Set data
    var data = grafica[1]["datos"];

    yAxis.data.setAll(data);
    series.data.setAll(data);
    sortCategoryAxis();

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

    // Get series item by category
    function getSeriesItem(category) {
      for (var i = 0; i < series.dataItems.length; i++) {
        var dataItem = series.dataItems[i];
        if (dataItem.get("categoryY") == category) {
          return dataItem;
        }
      }
    }

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

    // Create modal for a "no data" note
    var modal = am5.Modal.new(root, {
      content: "La gráfica no tiene datos.",
    });

    // Axis sorting
    function sortCategoryAxis() {
      // Sort by value
      series.dataItems.sort(function (x, y) {
        return x.get("valueX") - y.get("valueX"); // descending
        //return y.get("valueY") - x.get("valueX"); // ascending
      });

      // Go through each axis item
      am5.array.each(yAxis.dataItems, function (dataItem) {
        // get corresponding series item
        var seriesDataItem = getSeriesItem(dataItem.get("category"));

        if (seriesDataItem) {
          // get index of series data item
          var index = series.dataItems.indexOf(seriesDataItem);
          // calculate delta position
          var deltaPosition =
            (index - dataItem.get("index", 0)) / series.dataItems.length;
          // set index to be the same as series data item index
          dataItem.set("index", index);
          // set deltaPosition instanlty
          dataItem.set("deltaPosition", -deltaPosition);
          // animate delta position to 0
          dataItem.animate({
            key: "deltaPosition",
            to: 0,
            duration: 1000,
            easing: am5.ease.out(am5.ease.cubic),
          });
        }
      });

      // Sort axis items by index.
      // This changes the order instantly, but as deltaPosition is set,
      // they keep in the same places and then animate to true positions.
      yAxis.dataItems.sort(function (x, y) {
        return x.get("index") - y.get("index");
      });
    }

    series.appear(1000);
    chart.appear(1000, 100);
  }); // end am5.ready()
});
