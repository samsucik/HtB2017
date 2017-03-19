var blue = '#0084b4';
$(document).ready(function(){
	var html = '<table class="table"><thead class="thead-inverse"><tr><th>#</th><th>Name</th><th>Score</th></tr></thead><tbody>';
	for (i = 0; i < top5posit_sent.length; i++) {
	html += '<tr><th scope="row">' + (i+1) + '</th><td>' + autocompletionData[top5posit_sent[i][0]] + '</td><td>' + Math.ceil(top5posit_sent[i][1]*100)/100 + '</td></tr>';
	}
		html += '</tbody></table>';
	$("#top5posit_sent").html(html);
	var html = '<table class="table"><thead class="thead-inverse"><tr><th>#</th><th>Name</th><th>Score</th></tr></thead><tbody>';
	for (i = 0; i < top5neg_sent.length; i++) {
	html += '<tr><th scope="row">' + (i+1) + '</th><td>' + autocompletionData[top5neg_sent[i][0]] + '</td><td>' + Math.ceil(top5neg_sent[i][1]*100)/100 + '</td></tr>';
	}
		html += '</tbody></table>';
	$("#top5neg_sent").html(html);
	var html = '<table class="table"><thead class="thead-inverse"><tr><th>#</th><th>Name</th><th>Score</th></tr></thead><tbody>';
	for (i = 0; i < top5posrise_sent.length; i++) {
	html += '<tr><th scope="row">' + (i+1) + '</th><td>' + autocompletionData[top5posrise_sent[i][0]] + '</td><td>' + Math.ceil(top5posrise_sent[i][1]*100)/100 + '</td></tr>';
	}
	html += '</tbody></table>';
	$("#top5posrise_sent").html(html);
	
	var html = '<table class="table"><thead class="thead-inverse"><tr><th>#</th><th>Name</th><th>Score</th></tr></thead><tbody>';
	for (i = 0; i < top5negdec_sent.length; i++) {
		html += '<tr><th scope="row">' + (i+1) + '</th><td>' + autocompletionData[top5negdec_sent[i][0]] + '</td><td>' + Math.ceil(top5negdec_sent[i][1]*100)/100 + '</td></tr>';
	}
	html += '</tbody></table>';
	$("#top5negdec_sent").html(html);
	
	var html = '<table class="table"><thead class="thead-inverse"><tr><th>#</th><th>Name</th><th>Score</th></tr></thead><tbody>';
	for (i = 0; i < top5posit_subj.length; i++) {
		html += '<tr><th scope="row">' + (i+1) + '</th><td>' + autocompletionData[top5posit_subj[i][0]] + '</td><td>' + Math.ceil(top5posit_subj[i][1]*100)/100 + '</td></tr>';
	}
	html += '</tbody></table>';
	$("#top5posit_subj").html(html);
	
	var html = '<table class="table"><thead class="thead-inverse"><tr><th>#</th><th>Name</th><th>Score</th></tr></thead><tbody>';
	for (i = 0; i < top5neg_subj.length; i++) {
		html += '<tr><th scope="row">' + (i+1) + '</th><td>' + autocompletionData[top5neg_subj[i][0]] + '</td><td>' + Math.ceil(top5neg_subj[i][1]*100)/100 + '</td></tr>';
	}
	html += '</tbody></table>';
	$("#top5neg_subj").html(html);
	
	var html = '<table class="table"><thead class="thead-inverse"><tr><th>#</th><th>Name</th><th>Score</th></tr></thead><tbody>';
	for (i = 0; i < top5posrise_subj.length; i++) {
		html += '<tr><th scope="row">' + (i+1) + '</th><td>' + autocompletionData[top5posrise_subj[i][0]] + '</td><td>' + Math.ceil(top5posrise_subj[i][1]*100)/100 + '</td></tr>';
	}
	html += '</tbody></table>';
	$("#top5posrise_subj").html(html);
	
	var html = '<table class="table"><thead class="thead-inverse"><tr><th>#</th><th>Name</th><th>Score</th></tr></thead><tbody>';
	for (i = 0; i < top5negdec_subj.length; i++) {
		html += '<tr><th scope="row">' + (i+1) + '</th><td>' + autocompletionData[top5negdec_subj[i][0]] + '</td><td>' + Math.ceil(top5negdec_subj[i][1]*100)/100 + '</td></tr>';
	}
	html += '</tbody></table>';
	$("#top5negdec_subj").html(html);


	var nicknames = Object.keys(autocompletionData);//autocompletionData.map(function(k, v){return k;}, k);
	// console.log(nicknames);

	Plotly.setPlotConfig({
	  modeBarButtonsToRemove: ['sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'select2d', 'resetScale2d', 'hoverClosestCartesian']
	});

	//var nicknames = ["belize", "buchanan", "bingbingbing", "bernardo", "bilbo", "beast", "benedict", "realDonaldTrump", "bernie", "hillary", "angela", "nigel"]
	$("#topCarousel").Cloud9Carousel( {
	  // buttonLeft: $("#buttons > .left"),
	  // buttonRight: $("#buttons > .right"),
	  autoPlay: 1,
	  bringToFront: true,
	  speed: 0.1,
	  autoPlayDelay: 1200
	});

	$(document).on("submit", "#searchForm", function(e) {
		var nickname = $(this).find("input").val();
		if (nickname === "") return;
		e.preventDefault();
		console.log($(this).find("input").val());
		$.ajax({
	        url: '/?politician=' + nickname,
	        type: 'GET',
	        // data: { field1: "hello", field2 : "hello2"} ,
	        contentType: 'application/x-www-form-urlencoded',
	        success: function (response) {
	            console.log(response);
	            top3sent = response['top3sent'];
	            top3subj = response['top3subj'];
	            sentiments = response['sentiment_scores'];
	            subjectivities = response['subj_scores'];
	            tweets = response['tweets_by_politician'];
	            renderPolitician(nickname, top3sent, top3subj, sentiments, subjectivities, tweets);
	            //var sentiment_table = {{ top3sent|safe }};
	        },
	        error: function () {
	            alert("Sorry, couldn't fetch this politician for you!");
	            console.log("Sorry, couldn't fetch this politician for you!");//your error code
	        }
	    }); 	
	});

	$('#search').typeahead({
		source: nicknames
	})

	$(".profile-row").hide();
});
var renderPolitician = function(nickname, top3sent, top3subj, sentiments, subjectivities, tweets) {
	$(".stats-row").hide();
	$(".profile-row").css("visibility", "hidden").show();
	
	$(".profile").find("img").attr("src", "/static/" + nickname.toLowerCase() + ".jpg");
	$(".profile").find(".nickname").attr("href", "https://twitter.com/" + nickname).html("@" + nickname);
	$(".profile").find(".normal_name").html(autocompletionData[nickname]);
	plotTweets("allTweets", tweets, nickname);
	plotSentimentWeekly("personalSentimentWeekly", sentiments, subjectivities, nickname);

	generatePoliticianTable("#similarBySentiment", top3sent);
	generatePoliticianTable("#similarBySubjectivity", top3subj);

	$(".profile-row").css("visibility", "visible");
}

var plotTweets = function(selector, tweets, nick) {
	var dates = [];
	var subjectivities = [];
	var retweets_raw = [];
	var sentiments = [];
	// {"date": "2017-02-15 19:17:59", "subjectivity": 0.9, "name": "realDonaldTrump", "num_retweets": 14433, "sentiment": 0.8}, 
	var max_retweets = 1;
	tweets.map(function(obj){
		dates.push(obj.date);
		subjectivities.push(obj.subjectivity);
		retweets_raw.push(obj.num_retweets);
		sentiments.push(obj.sentiment);
		// console.log(obj.num_retweets)
		if (obj.num_retweets > max_retweets) max_retweets = obj.num_retweets;
	});
	// console.log(dates);
	// console.log(subjectivities);
	// console.log(retweets_raw)
	// console.log(max_retweets);
	// console.log(retweets_raw);
	var retweets = retweets_raw.map(function(v){return Math.ceil(7*Math.log(v*100.0/max_retweets));});
	// console.log(retweets);
	var result = {
		x: dates,
		y: sentiments,
		type: 'scatter',
		marker: {
		    color: 'rgb(0,0,0)',
		    size: retweets
		},
		line: {
			shape: 'spline'
		},
		mode: 'markers',
		// name: "sentiment",
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
			range: [-1.2,1.2],
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
	    showlegend: false,
		// legend: {
		// 	orientation: "h"
		// }
	};
	Plotly.newPlot(selector, plotdata, layout);
}

var plotSentimentWeekly = function(selector, sentiments, subjectivities, nick) {
	var dates = [];
	var now = new Date();
	for (i = 0; i < sentiments.length; i++) {
		d = new Date()
		d.setTime(new Date().getTime() - 24*60*60*1000*7*i)
		dates.push(d.toISOString());
	}

	var result1 = {
		x: dates,
		y: sentiments,
		type: 'scatter',
		marker: {
		    color: blue,
		    size: 10
		},
		line: {
			shape: 'spline',
		},
		mode: 'lines+markers',
		name: "sentiment",
	};
	var result2 = {
		x: dates,
		y: subjectivities,
		type: 'scatter',
		marker: {
		    color: 'rgb(255,140,0)',
		    size: 10
		},
		line: {
			shape: 'spline'
		},
		mode: 'lines+markers',
		name: "subjectivity",
	};
	plotdata = [result1, result2]

	var layout = {
		xaxis: {
			showgrid: false,
			zeroline: false,
			type: "date"
		},
		yaxis: {
			showgrid: true,
			fixedrange: true,
			range: [-1.2,1.2],
			zeroline: true,
			title: 'sentiment &amp; subjectivity',
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
}

var generatePoliticianTable = function(selector, data) {
	var html = '<table class="table"><thead class="thead-inverse"><tr><th>#</th><th>Name</th><th>Similarity</th></tr></thead><tbody>';
	for (i = 0; i < data.length; i++) {
		html += '<tr><th scope="row">' + (i+1) + '</th><td>' + autocompletionData[data[i][0]] + '</td><td>' + Math.ceil(data[i][1]*100) + '%</td></tr>';
	}
	html += '</tbody></table>';
	$(selector).html(html);
}