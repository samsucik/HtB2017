var blue = '#0084b4';
$(document).ready(function(){

	Plotly.setPlotConfig({
	  modeBarButtonsToRemove: ['sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'select2d', 'resetScale2d', 'hoverClosestCartesian']
	});

	var nicknames = ["belize", "buchanan", "bingbingbing", "bernardo", "bilbo", "beast", "benedict", "realDonaldTrump", "bernie", "hillary", "angela", "nigel"]
	$("#topCarousel").Cloud9Carousel( {
	  // buttonLeft: $("#buttons > .left"),
	  // buttonRight: $("#buttons > .right"),
	  autoPlay: 1,
	  bringToFront: true,
	  speed: 0.1,
	  autoPlayDelay: 600
	});

	$(document).on("submit", "#searchForm", function(e) {
		e.preventDefault();
		console.log($(this).find("input").val());
	});

	$('#search').typeahead({
		source: nicknames
	})

	var datenames = ["Jan", "Feb", "Mar", "Apr"]
	var dates = ['2017-01-05 17:06:00', '2017-02-15 17:06:00', '2017-03-22 17:06:00', '2017-04-10 17:06:00']
	var sentiments = [13, 14, 11, 10]
	var nick = "realDonaldTrump"
	// var colors = ['rgb(0,0,0)']
	var retweets = [10, 15, 5, 20]
	var data = [];
	var result = {
		x: dates,
		y: sentiments,
		type: 'scatter',
		marker: {
		    color: 'rgb(100,100,100)',
		    size: retweets
		},
		mode: 'markers',
		name: "@" + nick,
		text: datenames,
		connectgaps: true
	};
	data.push(result)
	var layout = {
		// title: nickname,
		xaxis: {
			title: 'Timeline',
			showgrid: true,
			zeroline: false,
			type: "date"
		},
		yaxis: {
			showgrid: false,
			fixedrange: true
		},
		width: 700,
			height: 300,
			showlegend: true,
			autotick: false,
	    ticks: 'outside',
	    tickcolor: 'rgb(100,200,255)',
	    tickwidth: 3,
	    ticklen: 6,
	    tickfont: {
	      family: 'Arial',
	      size: 12,
	      color: 'rgb(82, 82, 82)'
	    },
	    margin: {
	    	l: 80,
	    	r: 80,
	    	t: 80,
	    	b: 80,
	    	pad: 0
	    },
	    paper_bgcolor: 'rgb(200,200,200)',
	    plot_bgcolor: 'rgb(222,222,222)',
	    // modeBarButtonsToRemove: ['sendDataToCloud','hoverCompareCartesian']
	};
	Plotly.setPlotConfig({
	  modeBarButtonsToRemove: ['sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'select2d', 'resetScale2d', 'hoverClosestCartesian']
	});
	// Plotly.newPlot('graph1', data, layout);


	var sentiments = [0.15289502164502164, 0.15015405015405014, 0.2790317874692875, 0.25101190476190477, 0.3113612313612314, 0.3521624979958313, 0.24654408274474066, 0.19675324675324676];
	plotSentimentWeekly("personalSentimentWeekly", sentiments, "NicolaSturgeon");
});

var plotSentimentWeekly = function(selector, sentiments, nick) {
	var dates = [];
	var now = new Date();
	for (i = 0; i < sentiments.length; i++) {
		d = new Date()
		d.setTime(new Date().getTime() - 24*60*60*1000*7*i)
		dates.push(d.toISOString());
	}

	var result = {
		x: dates,
		y: sentiments,
		type: 'scatter',
		marker: {
		    color: blue,
		    size: 15
		},
		line: {
			shape: 'spline'
		},
		mode: 'lines+markers',
		name: "sentiment",
	};
	plotdata = [result]

	var layout = {
		xaxis: {
			showgrid: false,
			zeroline: false,
			type: "date"
		},
		yaxis: {
			showgrid: true,
			fixedrange: true,
			range: [-1,1],
			zeroline: true,
			title: 'sentiment',
			showticklabels: false
		},
		height: 300,
		autotick: false,
	    ticks: 'inside',
	    tickcolor: 'rgb(100,200,255)',
	    tickwidth: 3,
	    ticklen: 6,
	    tickfont: {
	      family: 'Arial',
	      size: 12,
	      color: 'rgb(82, 82, 82)'
	    },
	    margin: {
	    	l: 30,
	    	r: 30,
	    	t: 30,
	    	b: 40,
	    	pad: 0
	    },
	    paper_bgcolor: 'white',
	    plot_bgcolor: 'white',
	    showlegend: true,
		legend: {
			orientation: "h"
		}
	};
	Plotly.newPlot(selector, plotdata, layout);
	// setTimeout(function(){
	// 	console.log("transforming...");
	// 	console.log($(selector).find(".legend"));
	// 	$(selector).find(".legend").attr("transform", "30,20");
	// }, 2000);
}