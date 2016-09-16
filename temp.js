$(function() {

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

    $("#placeholder").bind("plothover", function (event, pos, item) {

		var str = "(" + pos.x.toFixed(2) + ", " + pos.y.toFixed(2) + ")";
		$("#hoverdata").text(str);

		if (item) {
			var x = new Date(item.datapoint[0]),
				y = item.datapoint[1].toFixed(2);

            hrs = x.getHours().toString();
            mins = x.getMinutes().toString();
            ttime = hrs.lpad("0",2) + ":" + mins.lpad("0", 2);
			$("#tooltip").html(item.series.label + "," + ttime + " = " + y +"°C")
				.css({top: item.pageY+5, left: item.pageX+5})
				.fadeIn(200);
		} else {
			$("#tooltip").hide();
		}
});

	var options = {
		lines: {
			show: true
		},
		points: {
			show: false
		},
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
                radius: 2
            }
        },
        legend:
        {
            show: true,
            position: "se",
            container: "#legend",
            noColumns: 3
        }

	};

	function onDataReceived(series) {
		//data = [ series ];
        data = series;
		$.plot("#placeholder", data, options);
	}

	$.ajax({
		url: "/temp.json",
		type: "GET",
		dataType: "json",
		success: onDataReceived
	});
});
