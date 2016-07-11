'use strict';

function analysisActivity(data) {
    $("#canvas_dahs").length && $.plot($("#canvas_dahs"), [data], {
        series: {
            lines: {
                show: true,
                fill: true
            },
            points: {
                radius: 0,
                show: true
            },
            shadowSize: 2
        },

        grid: {
            verticalLines: true,
            hoverable: true,
            clickable: true,
            tickColor: "#d5d5d5",
            borderWidth: 1,
            color: '#fff'
        },

        colors: ["rgba(38, 185, 154, 0.38)"],

        xaxis: {
            tickColor: "rgba(51, 51, 51, 0.06)",
            mode: "time",
            tickSize: [1, "day"],
            axisLabel: "Date",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 10
        },

        yaxis: {
            minTickSize: 1,
            tickDecimals: 0,
            tickColor: "rgba(51, 51, 51, 0.06)",
        }
    });
}
