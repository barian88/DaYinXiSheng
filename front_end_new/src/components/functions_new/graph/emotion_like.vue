<template>
    <div>
        <div class="main">
            <div class="box_gragh">
                <!-- ? -->
                <div id="figure" class="figure"></div>
                <div class="details">
                    <div class="h2">近十五天内平台动态平均情绪值</div>
                    <div class="rate">0.6457</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import * as echarts from "echarts";
    import util from "@/util";
    export default {
        name: "emotion",
        components: {},
        data(){
          return{
            data: [0.6428,0.7236,0.6974,0.6732,0.6342,0.5243,0.7738,0.6457,0.5978,0.4987,0.5113,0.5576,0.6213,0.6345]
          }
        },
        mounted() {
            var myChart = echarts.init(document.getElementById("figure"));
            window.onresize = function () {
                myChart.resize({
                    width: 60,
                    height: 10,
                });
            };
            var option = {
                legend: {
                    orient: "horizontal",
                    x: "left",
                    y: "top",
                    data: ["情绪值%"],
                    textStyle: {
                        fontSize: 14,
                        color: "#E9E9E9",
                    },
                },
                grid: {
                    top: "16%", // 等价于 y: '16%'
                    left: "3%",
                    right: "8%",
                    bottom: "3%",
                    containLabel: true,
                },
                tooltip: {
                    trigger: "axis",
                    textStyle: {
                        fontSize: 18,
                        color: "#E9E9E9"
                    },
                    backgroundColor: "rgb(32, 32, 35, 0.5)",
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}, //下载工具
                    },
                },
                xAxis: {
                    name: "日期",
                    type: "category",
                    axisLine: {
                        lineStyle: {
                            // 设置x轴颜色
                            color: "#E9E9E9",
                        },
                    },
                    data: util.getLast14Days()
                },
                yAxis: {
                    name: "",
                    type: "value",
                    min: 0,
                    max: 100, // 设置y轴刻度的最大值
                    splitNumber: 5, // 设置y轴刻度间隔个数
                    axisLine: {
                        lineStyle: {
                            color: "#E9E9E9",
                        },
                    },
                },
                series: [


                    {
                        name: "情绪值%",
                        data: this.data.map((item) => (item * 100).toFixed(2)),
                        type: "line",
                        color: "#E9E9E9",
                        // 设置折线上圆点大小
                        symbolSize: 8,
                        itemStyle: {
                            normal: {
                                // 拐点上显示数值
                                label: {
                                    show: true,
                                    color: "#E9E9E9"
                                },
                                lineStyle: {
                                    width: 5, // 设置线宽
                                    type: "dotted", //'dotted'虚线 'solid'实线
                                },
                            },
                        },
                    },
                ],
            };
            myChart.setOption(option);
        },
    };
</script>

<style lang="scss" scoped>
@import "../../../assets/style/base.scss";
    /* 表格处? */
    .box_gragh {
        position: relative;
        display: flex;
        width: 100%;
        height: 32vh;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        margin-top: 2vh;
    }
    .box_gragh .figure {
        width: 100%;
        height: 100%;
    }
    .box_gragh .details {
        position: absolute;
        width: 30%;
        height:15%;
        padding: 5%;
        border: $border-width solid $border-color;
        border-radius: $default-border-radius;
        background-color: $background-color;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transform: scale(1, 1);
        transition: transform 200ms;
    }
    .box_gragh:hover .details {
        transform: scale(0.5, 0);
    }
    .box_gragh .details .h2 {
        text-align: center;
        color: $default-font-color;
        font-size: 1rem;
        font-weight: 700;
        font-family: YaHei;
        line-height: 1.5rem;
    }
    .rate {
        padding: 0.25rem 1.25rem;
        margin: 0.25rem 0.25rem;
        background: $theme-color;
        color: #f4f2ff;
        font-size: 1rem;
        font-weight: 900;
        font-family: YaHei;
        transition: all 500ms ease-in-out;
    }
</style>