google.charts.load("current", { packages: ["corechart"] });

let chart = null;

function createPlot(args) {
  if (chart != null)
    chart.clearChart();
  var rows = args.map(i => ([
      i.item, i.frequency, "#17a2b8"
    ])
  )
  
  rows = [["Item", "Frequency", {role: "style"}], ...rows]

  var data = google.visualization.arrayToDataTable(rows);
  var view = new google.visualization.DataView(data);

  view.setColumns([0, 1,
    {
      calc: "stringify",
      sourceColumn: 1,
      type: "string",
      role: "annotation"
    },
    2]);

  var options = {
    title: "Frequency of Items",
    width: '100%',
    height: args.length * 25,
    chartArea: {'width': '85%', 'height': '95%'},
    legend: { position: "none" },
    fontName: 'Arial',
    fontSize: 12,
  };
  chart = new google.visualization.BarChart(document.getElementById("chart_div"));
  chart.draw(view, options);
}