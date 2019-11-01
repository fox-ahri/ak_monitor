<template>
    <div id="cpu-line" class="cpu-line">
        <div id="child_cpu_chart" style="width: 100%;height: 100%;"></div>
    </div>
</template>

<script>
export default {
    name: "cpu-line",
    props: ["cpu_data", "theme"],
    data() {
        return {
            child_cpu_chart: {}
        };
    },
    methods: {
        handle(data) {
            let tmp = [];
            data.forEach(element => {
                tmp.push([element.date_time, element.cpu_percent]);
            });
            this.update(tmp);
        },
        update(data) {
            this.child_cpu_chart.setOption({
                title: {
                    text: "CPU 占用率 "
                },
                tooltip: {
                    trigger: "axis"
                },
                grid: {
                    left: "5%",
                    right: "15%",
                    containLabel: true
                },
                xAxis: {
                    data: data.map(function(item) {
                        return item[0].slice(14);
                    })
                },
                yAxis: {
                    splitLine: {
                        show: false
                    }
                },
                toolbox: {
                    top: 20,
                    left: "center",
                    feature: {
                        dataZoom: {
                            yAxisIndex: "none"
                        },
                        restore: {},
                        saveAsImage: {}
                    }
                },
                dataZoom: [
                    {
                        startValue: "2014-06-01"
                    },
                    {
                        type: "inside"
                    }
                ],
                visualMap: {
                    top: 10,
                    right: 10,
                    pieces: [
                        {
                            gt: 0,
                            lte: 3,
                            color: "#096"
                        },
                        {
                            gt: 3,
                            lte: 7,
                            color: "#ffde33"
                        },
                        {
                            gt: 7,
                            lte: 10,
                            color: "#ff9933"
                        },
                        {
                            gt: 10,
                            lte: 30,
                            color: "#cc0033"
                        },
                        {
                            gt: 30,
                            lte: 60,
                            color: "#660099"
                        },
                        {
                            gt: 60,
                            color: "#7e0023"
                        }
                    ],
                    outOfRange: {
                        color: "#999"
                    }
                },
                series: {
                    name: "CPU 占用率",
                    type: "line",
                    data: data.map(function(item) {
                        return item[1];
                    }),
                    markLine: {
                        silent: true,
                        data: [
                            {
                                yAxis: 0
                            },
                            {
                                yAxis: 5
                            },
                            {
                                yAxis: 10
                            },
                            {
                                yAxis: 30
                            },
                            {
                                yAxis: 60
                            },
                            {
                                yAxis: 100
                            }
                        ]
                    }
                }
            });
        }
    },
    mounted() {
        this.child_cpu_chart = echarts.init(
            document.getElementById("child_cpu_chart"),
            this.theme
        );
        let self = this;
        window.addEventListener("resize", function() {
            self.child_cpu_chart.resize();
        });
    },
    watch: {
        cpu_data(n, o) {
            this.handle(n);
        }
    }
};
</script>

<style lang="scss" scoped>
#cpu-line {
    width: 100%;
    height: 100%;
}
</style>