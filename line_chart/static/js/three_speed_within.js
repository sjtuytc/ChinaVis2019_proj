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
                let legend_all=["据赛事中心0.3km内",'距赛事中心0.3km-1.0km','据赛事中心1.0km-10.0km'];
                for (j=0; j<str_all.length;j++){
                    tempstr = str_all[j];
                    time_data[tempstr] = [];
                    for(i=0;i<our_data[tempstr].length;i++){
                        time_data[tempstr].push([(+our_data[tempstr][i].value[0])*1000,+our_data[tempstr][i].value[1]])
                    }
                }

                var dom = document.getElementById("speed_graph");
				var myChart = echarts.init(dom);
                dom.style.backgroundColor = "#cdffe6";

                var app = {};
                option = null;
                option = {
        title: {
            text: '区域平均速度分析',
            x:'center'
        },
		grid: {
            x:100,
			y:100,
			x2:100,
			y2:100,
		},
		backgroundColor:'#cdffe6',
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
            min:10,
            splitLine: {
                show: false
            }
        },
        dataZoom: [{
            startValue: '2018-05-01'
        }, {
            type: 'inside'
        }],
        visualMap: {
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
			dom.style.backgroundColor = "#cdffe6";
            },
            error: function(xhr, type) {
                alert("error")
            },
        });