var server_url="http://127.0.0.1:5000";

function get_flow(latitude,longitude,time_unit){
    $.ajax({
        type: 'GET',
            url: server_url+"/get_flow/",
            data:{
                'latitude':latitude,
                'longitude':longitude,
                'time_unit':time_unit,
            },
            dataType: 'json',
            contentType: "application/json",
            success: function(our_data,i) {

                time_data = [];
                for(i=0;i<our_data.length;i++){
                    // our_data[i].time = new Date(+our_data[i].time).toString();
                    time = new Date(+our_data[i].value[0]);
                    // our_data[i].value[0] = [time.getHours(),time.getMinutes(),time.getSeconds()].join('/');
                    time_data.push([(+our_data[i].value[0])*1000,+our_data[i].value[1]])
                }
                var dom = document.getElementById("coordChart");

                var myChart = echarts.init(dom);
                var app = {};
                option = null;

                // var data = our_data;
                option = {
                    title: {
                        text: '流量分析',
                        textStyle: {
                            fontWeight: "normal",
                            color: "#fff",
                            fontSize: 14
                        },
                        x:'center',
                        y:'top',
                    },
                    tooltip: {
                        trigger: 'axis',
                        formatter: function (params) {
                            params = params[0];
                            var time = new Date(+params.data[0]);
                            return time.getHours()+":"+time.getMinutes() + ",    " + params.data[1];
                        },
                        axisPointer: {
                            animation: false
                        }
                    },
                    xAxis: {
                        type: 'time',
                        splitLine: {
                            show: false
                        },
                        axisLine:{
                            lineStyle:{
                                    color:'#fafafa',
                            }
                        },
                    },
                    yAxis: {
                        type: 'value',
                        boundaryGap: [0, '30%'],
                        splitLine: {
                            show: false
                        },
                        axisLine:{
                            lineStyle:{
                                    color:'#fafafa',
                            }
                        },
                    },
                    series: [{
                        name: '模拟数据',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: time_data
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
}

function get_street_flow(street,time_unit){
    $.ajax({
        type: 'GET',
            url: server_url+"/get_street_flow/",
            data:{
                'street':street,
                'time_unit':time_unit,
            },
            dataType: 'json',
            contentType: "application/json",
            success: function(our_data,i) {

                time_data = [];
                for(i=0;i<our_data.length;i++){
                    // our_data[i].time = new Date(+our_data[i].time).toString();
                    time = new Date(+our_data[i].value[0]);
                    // our_data[i].value[0] = [time.getHours(),time.getMinutes(),time.getSeconds()].join('/');
                    time_data.push([(+our_data[i].value[0])*1000,+our_data[i].value[1]])
                }
                var dom = document.getElementById("heatmapChart");

                var myChart = echarts.init(dom);
                var app = {};
                option = null;

                // var data = our_data;
                option = {
                    title: {
                        text: street+'流量分析',
                        textStyle: {
                            fontWeight: "normal",
                            color: "#fff",
                            fontSize: 14
                        },
                        x:'center',
                        y:'top',
                    },
                    tooltip: {
                        trigger: 'axis',
                        formatter: function (params) {
                            params = params[0];
                            var time = new Date(+params.data[0]);
                            return time.getHours()+":"+time.getMinutes() + ",    " + params.data[1];
                        },
                        axisPointer: {
                            animation: false
                        }
                    },
                    xAxis: {
                        type: 'time',
                        splitLine: {
                            show: false
                        },
                        axisLine:{
                            lineStyle:{
                                    color:'#fafafa',
                            }
                        },
                    },
                    yAxis: {
                        type: 'value',
                        boundaryGap: [0, '30%'],
                        splitLine: {
                            show: false
                        },
                        axisLine:{
                            lineStyle:{
                                    color:'#fafafa',
                            }
                        },
                    },
                    series: [{
                        name: '模拟数据',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: time_data
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
}