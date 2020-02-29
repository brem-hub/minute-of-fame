$(document).ready(function() {
 "use strict";
 Chart.defaults.global.defaultFontColor = "#75787c";
 var r = !0;
 $(window).outerWidth() < 576 && (r = !1);
 var a = $("#lineCahrt"),
  o = (new Chart(a, {
   type: "line",
   options: {
    scales: {
     xAxes: [{
      display: !0,
      gridLines: {
       display: !1
      }
     }],
     yAxes: [{
      ticks: {
       max: 100,
       min: 0
      },
      display: !0,
      gridLines: {
       display: !1
      }
     }]
    },
    legend: {
     display: r
    }
   },
   data: {
    labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    datasets: [{
     label: "Likes",
     fill: !0,
     lineTension: .2,
     backgroundColor: "transparent",
     borderColor: "#1e7e34",
     pointBorderColor: "#1e7e34",
     pointHoverBackgroundColor: "#1e7e34",
     borderCapStyle: "butt",
     borderDash: [],
     borderDashOffset: 0,
     borderJoinStyle: "miter",
     borderWidth: 2,
     pointBackgroundColor: "#fff",
     pointBorderWidth: 5,
     pointHoverRadius: 5,
     pointHoverBorderColor: "#fff",
     pointHoverBorderWidth: 2,
     pointRadius: 1,
     pointHitRadius: 0,
     data: [30, 27, 45, 62, 53, 75, 56, 74, 87, 99],
     spanGaps: !1
    }, {
     label: "Dislikes",
     fill: !0,
     lineTension: .2,
     backgroundColor: "transparent",
     borderColor: "#bd2130",
     pointBorderColor: "#bd2130",
     pointHoverBackgroundColor: "#bd2130",
     borderCapStyle: "butt",
     borderDash: [],
     borderDashOffset: 0,
     borderJoinStyle: "miter",
     borderWidth: 2,
     pointBackgroundColor: "#fff",
     pointBorderWidth: 5,
     pointHoverRadius: 5,
     pointHoverBorderColor: "#fff",
     pointHoverBorderWidth: 2,
     pointRadius: 1,
     pointHitRadius: 10,
     data: [35, 25, 28, 15, 20, 12, 16, 3, 7, 2],
     spanGaps: !1
    },{
     label: "Views",
     fill: !0,
     lineTension: .2,
     backgroundColor: "transparent",
     borderColor: "#d4c074",
     pointBorderColor: "#d4c074",
     pointHoverBackgroundColor: "#d4c074",
     borderCapStyle: "butt",
     borderDash: [],
     borderDashOffset: 0,
     borderJoinStyle: "miter",
     borderWidth: 2,
     pointBackgroundColor: "#fff",
     pointBorderWidth: 5,
     pointHoverRadius: 5,
     pointHoverBorderColor: "#fff",
     pointHoverBorderWidth: 2,
     pointRadius: 1,
     pointHitRadius: 0,
     data: [60, 43, 47, 98, 78, 71, 34, 49, 85, 100],
     spanGaps: !1
    }]
   }
  }), $("#barChartExample1"));
});

$( document ).ready(function() {
    $("#view-text").click(function(){
  $("#view-text").addClass( "tab__a-border" );
  $("#fame-text").removeClass( "tab__a-border" );
  $("#view").addClass( "show" ).removeClass( "hide" );
  $("#fame").addClass( "hide" ).removeClass( "show" );
});
    $("#fame-text").click(function(){
  $("#fame-text").addClass( "tab__a-border" );
  $("#view-text").removeClass( "tab__a-border" );
  $("#fame").addClass( "show" ).removeClass( "hide" );
  $("#view").addClass( "hide" ).removeClass( "show" );
});
});