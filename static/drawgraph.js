function drawGraph(prefix, units, url) {
    var graph = "#"+prefix+"_placeholder";
    var legend = "#"+prefix+"_legend";
    var choices = "#"+prefix+"_choices";
    var data_url = url;
    var data = [];
    var dataset = [];
    var choiceContainer;

    String.prototype.lpad = function(padString, length) {
        var str = this;
        while (str.length < length)
            str = padString + str;
        return str;
    }

    $("<div id='tooltip'></div>").css({
		position: "absolute",
		display: "none",
		border: "1px solid #fdd",
		padding: "2px",
		"background-color": "#fee",
		opacity: 0.80
	}).appendTo("body");

    $(graph).bind("plothover", function (event, pos, item) {

		var str = "(" + pos.x.toFixed(2) + ", " + pos.y.toFixed(2) + ")";
		$("#hoverdata").text(str);

		if (item) {
			var x = new Date(item.datapoint[0]),
				y = item.datapoint[1].toFixed(2);

            hrs = x.getHours().toString();
            mins = x.getMinutes().toString();
            ttime = hrs.lpad("0",2) + ":" + mins.lpad("0", 2);
			$("#tooltip").html(item.series.label + "," + ttime + " = " + y + units)
				.css({top: item.pageY+5, left: item.pageX+5})
				.fadeIn(200);
		} else {
			$("#tooltip").hide();
		}
});

	var options = {
        grid: {
            hoverable: true,
            backgroundColor: "#FFE5B3"
        },
		xaxis: {
            mode: "time",
            timezone: "browser",
            ticks: 40,
            minTickSize: [1, "hour"],
            min: new Date().getTime()-60*60*24*1000,
            panRange: [new Date().getTime()-60*60*48*1000, new Date().getTime()]
		},
        yaxis: {
            label: "Градусы цельсия",
            panRange: false
        },
        zoom: {
            interactive: false
        },
        pan: {
            interactive: true
        },
        series: {
            points: {
                radius: 2,
                show: false
            },
            lines: {
                show: true
            }
        },
        legend: {
            show: true,
            position: "se",
            container: legend,
            noColumns: 3
        }

	};

	function onDataReceived(series) {
        data = series;
        // Рисуем чекбоксы
        /*
        choiceContainer = $(choices);
        choiceContainer.html("");
            $.each(data, function(key, val) {
                choiceContainer.append("<br/><input type='checkbox' name='" + key +
                    "' checked='checked' id='id" + key + "'></input>" +
                    "<label for='id" + key + "'>"
                    + val.label + "</label>");
            });
        // Конец отрисовки
        choiceContainer.find("input").click(rePlot);
        */
		$.plot(graph, data, options);
	}

	$.ajax({
		url: data_url,
		type: "GET",
		dataType: "json",
		success: onDataReceived
	});
    /*
    function rePlot()
    {
        dataset = []
		choiceContainer.find("input:checked").each(function () {
			var key = $(this).attr("name");
			if (key && data[key]) {
				dataset.push(data[key]);
			}
		});

		if (data.length > 0) {
			$.plot(graph, dataset,options);
        }
    }
    */
}

$(function(){
    drawGraph("temp", "&deg;C", "/rrd/?filename=temperature.rrd");
    drawGraph("hum", "%","/rrd/?filename=misc.rrd&exclude=1");
    drawGraph("pre", " мм. рт. ст.","/rrd/?filename=pressure.rrd");
    drawGraph("brg", " ХЗ","/rrd/?filename=brightness.rrd");
    drawGraph("lightnings", " разр.","/rrd/?filename=lightnings.rrd");
});
