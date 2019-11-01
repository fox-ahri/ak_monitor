<template>
    <div id="disk_io-line" class="disk_io-line">
        <div id="child_disk_io_chart" style="width: 100%;height: 100%;"></div>
    </div>
</template>

<script>
export default {
    name: "disk_io-line",
    props: ["disk_io_data", "theme"],
    data() {
        return {
            child_disk_io_chart: {}
        };
    },
    methods: {
        handle(data) {
            let disk = {};
            let date_time = "";
            for (let k in data[0]) {
                disk[k] = { t1: [], t2: [], t3: [] };
            }
            data.forEach(element => {
                for (let k in element) {
                    disk[k]["t1"].push(element[k].date_time.slice(14));
                    disk[k]["t2"].push(
                        (
                            element[k].read_bytes /
                            1024 /
                            element[k].read_time
                        ).toFixed(2)
                    );
                    disk[k]["t3"].push(
                        (
                            element[k].write_bytes /
                            1024 /
                            element[k].write_time
                        ).toFixed(2)
                    );
                }
            });
            let series = [];
            let t = [];
            let legend = [];
            for (let k in disk) {
                t = disk[k].t1;
                series.push(
                    {
                        name: k + "读",
                        type: "line",
                        stack: "总量",
                        data: disk[k].t2
                    },
                    {
                        name: k + "写",
                        type: "line",
                        stack: "总量",
                        data: disk[k].t3
                    }
                );
                legend.push(k + "读");
                legend.push(k + "写");
            }
            this.update(legend, series, t);
        },
        update(legend, series, t) {
            this.child_disk_io_chart.setOption({
                title: {
                    text: "磁盘 / kb "
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    data: legend,
                    top: 30,
                    width: 500
                },
                grid: {
                    top: 90,
                    left: "4%",
                    right: "15%",
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: "category",
                    boundaryGap: false,
                    data: t
                },
                yAxis: {
                    type: "value"
                },
                series: series
            });
        }
    },
    mounted() {
        this.child_disk_io_chart = echarts.init(
            document.getElementById("child_disk_io_chart"),
            this.theme
        );
        let self = this;
        window.addEventListener("resize", function() {
            self.child_disk_io_chart.resize();
        });
    },
    watch: {
        disk_io_data(n, o) {
            this.handle(n);
        }
    }
};
</script>

<style lang="scss" scoped>
#disk_io-line {
    width: 100%;
    height: 100%;
}
</style>