<template>
    <div id="network-line" class="network-line">
        <div id="child_network_chart" style="width: 100%;height: 100%;"></div>
    </div>
</template>

<script>
export default {
    name: "network-line",
    props: ["network_data", "theme"],
    data() {
        return {
            child_network_chart: {}
        };
    },
    methods: {
        handle(data) {
            let t1 = [];
            let t2 = [];
            let t3 = [];
            data.forEach(element => {
                t1.push(element.date_time.slice(14));
                t2.push((element.network.eth0.bytes_sent/1024).toFixed(3));
                t3.push((element.network.eth0.bytes_recv/1024).toFixed(3));
            });
            this.update(t1, t2, t3);
        },
        update(t1, t2, t3) {
            this.child_network_chart.setOption({
                title: {
                    text: "网络 / kb "
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    data: ["上行", "下行"]
                },
                grid: {
                    left: "5%",
                    right: "5%",
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
                    data: t1
                },
                yAxis: {
                    type: "value"
                },
                series: [
                    {
                        name: "上行",
                        type: "line",
                        stack: "总量",
                        data: t2
                    },
                    {
                        name: "下行",
                        type: "line",
                        stack: "总量",
                        data: t3
                    }
                ]
            });
        }
    },
    mounted() {
        this.child_network_chart = echarts.init(
            document.getElementById("child_network_chart"),
            this.theme
        );
        let self = this;
        window.addEventListener("resize", function() {
            self.child_network_chart.resize();
        });
    },
    watch: {
        network_data(n, o) {
            this.handle(n);
        }
    }
};
</script>

<style lang="scss" scoped>
#network-line {
    width: 100%;
    height: 100%;
}
</style>