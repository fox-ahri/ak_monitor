<template>
    <div class="home" style="overflow: hidden;">
        <div style="display: flex;justify-content: space-between;width: 96%;margin: 10px auto">
            <div style="height: 400px;width: 50%;">
                <CpuLine :cpu_data="cpu_data" :theme="theme"></CpuLine>
            </div>
            <div style="height: 400px;width: 50%;">
                <MemoryLine :memory_data="memory_data" :theme="theme"></MemoryLine>
            </div>
        </div>
        <br />
        <br />
        <div style="display: flex;justify-content: space-between;width: 96%;margin: 10px auto">
            <div style="height: 400px;width: 50%;">
                <NetworkLine :network_data="network_data" :theme="theme"></NetworkLine>
            </div>
            <div style="height: 400px;width: 50%;">
                <DiskioLine :disk_io_data="disk_io_data" :theme="theme"></DiskioLine>
            </div>
        </div>
    </div>
</template>

<script>
import CpuLine from "@/components/CpuLine";
import MemoryLine from "@/components/MemoryLine";
import NetworkLine from "@/components/NetworkLine";
import DiskioLine from "@/components/DiskioLine";
export default {
    name: "home",
    components: {
        CpuLine,
        MemoryLine,
        NetworkLine,
        DiskioLine
    },
    data() {
        return {
            theme: "purple-passion",
            cpu_data: [],
            memory_data: [],
            network_data: [],
            disk_io_data: []
        };
    },
    methods: {
        print(v1, v2, v3, v4) {
            this.cpu_data = v1;
            this.memory_data = v2;
            this.network_data = v3;
            this.disk_io_data = v4;
        },
        init() {
            let xmlhttp = null;
            if (window.XMLHttpRequest) {
                xmlhttp = new XMLHttpRequest();
            } else if (window.ActiveXObject) {
                xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
            }
            let self = this;
            xmlhttp.onreadystatechange = function() {
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                    let data = JSON.parse(xmlhttp.responseText);
                    self.print(
                        data.cpu,
                        data.memory,
                        data.network,
                        data.disk_io
                    );
                }
            };
            xmlhttp.open("get", "http://156.232.1.135:9000/");
            xmlhttp.send();
            setInterval(() => {
                xmlhttp.open("get", "http://156.232.1.135:9000/");
                xmlhttp.send();
            }, 15000);
        }
    },
    mounted() {
        this.init();
    }
};
</script>
