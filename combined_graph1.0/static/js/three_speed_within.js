$.ajax({
        type: 'GET',
            url: server_url+"/get_speed/",
            data:{
                'latitude':latitude,
                'longitude':longitude,
                'time_unit':time_unit,
            },
            dataType: 'json',
            contentType: "application/json",
            success: function(our_data,i) {

                let time_data = {};
                let str_all = ['0.0','0.3','1.0'];
                let legend_all=["0.3km内",'0.3km-1.0km','1.0km-10.0km'];
                for (j=0; j<str_all.length;j++){
                    tempstr = str_all[j];
                    time_data[tempstr] = [];
                    for(i=0;i<our_data[tempstr].length;i++){
                        time_data[tempstr].push([(+our_data[tempstr][i].value[0])*1000,+our_data[tempstr][i].value[1]])
                    }
                }

                var dom = document.getElementById("speed_graph");
				var myChart = echarts.init(dom, 'dark');

                var app = {};
                option = null;
                option = {
        title: {
            text: '区域平均速度分析',
            x:'center'
        },
		// grid: {
        //     x:100,
		// 	y:100,
		// 	x2:100,
		// 	y2:100,
		// },

		// backgroundColor:'#eafff4',
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'time',
            splitLine: {
                show: false
            }
        },
        yAxis: {
            // bottom:1,
            min:10,
            splitLine: {
                show: false
            }
        },
        // dataZoom: [{
        //     startValue: '2018-05-01'
        // }, {
        //     type: 'inside'
        // }],
        visualMap: {
            show:false,
            top: 10,
            right : -10,
            pieces: [{
                gt: 0,
                lte: 20,
                color: '#096'
            }, {
                gt: 20,
                lte: 25,
                color: '#ffde33'
            }, {
                gt: 25,
                lte: 30,
                color: '#ff9933'
            }, {
                gt: 30,
                lte: 35,
                color: '#cc0033'
            }, {
                gt: 35,
                lte: 40,
                color: '#660099'
            }, {
                gt: 40,
                color: '#7e0023'
            }],
            outOfRange: {
                color: '#999'
            }
        },
        color: ['#000','#000','#000'],
        legend: {
            top:30,

            data:legend_all
        },

        series: [{
                        name: legend_all[0],
                        type: 'line',
                        symbol:'star',//拐点样式
                        symbolSize: 8,//拐点大小
                        // hoverAnimation: false,
                        data: time_data[str_all[0]],
                        markLine: {
                                silent: true,
                                data: [{
                                    yAxis: 20
                                }, {
                                    yAxis: 25
                                }, {
                                    yAxis: 30
                                }, {
                                    yAxis: 35
                                }, {
                                    yAxis: 40
                                }, {
                                    yAxis: 45
                                }]
                        }
        },{
                        name: legend_all[1],
                        type: 'line',
                        symbolSize: 8,//拐点大小
                        // hoverAnimation: false,
                        data: time_data[str_all[1]],
        },{
                        name: legend_all[2],
                        type: 'line',
                        symbol:'triangle',//拐点样式
                        symbolSize: 8,//拐点大小
                        // hoverAnimation: false,
                        data: time_data[str_all[2]],
        }]

    };
                if (option && typeof option === "object") {
                    myChart.setOption(option, true);
                }
            },
            error: function(xhr, type) {
                alert("error")
            },
        });

$.ajax({
        type: 'GET',
            url: server_url+"/get_scatter_speed/",
            data:{
            },
            dataType: 'json',
            contentType: "application/json",
            success: function(our_data,i) {
				var dom = document.getElementById("speed_scatter");
				var myChart = echarts.init(dom,'dark');
var xData = [];
var yData = [];
function generateData(theta, min, max) {
    var data = [];
    var counter = 0;
    for (var i = 0; i < 200; i++) {
        for (var j = 0; j < 90; j++) {
            data.push([i, j, our_data[counter][2]]);
            counter++;
            // data.push([i, j, normalDist(theta, x) * normalDist(theta, y)]);
        }
        xData.push(parseInt(i/200*24));
    }
    xData.push(24);
    for (var j = 0; j < 90; j++) {
        yData.push(j);
    }
    yData.push(90);
    return data;
}
var data = generateData(2, -5, 5);

option = {
       title: {
            text: '速度随时间变化热力图',
            x:'center'
        },
    tooltip: {},
	grid:{
           top:30,
	},
    xAxis: {
        type: 'category',
        data: xData
    },
    yAxis: {
        type: 'category',
        data: yData
    },
	// backgroundColor:'#eafff4',
    visualMap: {
		show:true,
		orient:"horizontal",
        min: 0,
        max: 1,
		left:"center",
		width:10,
        calculable: true,
        realtime: false,
        inRange: {
            color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
        }
    },
    series: [{
        name: 'Gaussian',
        type: 'heatmap',
        data: data,
        itemStyle: {
            emphasis: {
                borderColor: '#333',
                borderWidth: 1
            }
        },
        progressive: 1000,
        animation: false
    }]
};
if (option && typeof option === "object") {
                    myChart.setOption(option, true);
                }
            },
            error: function(xhr, type) {
                alert("error")
            },
        });