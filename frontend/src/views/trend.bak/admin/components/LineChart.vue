<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '550px'
    },
    autoResize: {
      type: Boolean,
      default: true
    },
    chartData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        // console.log('chartData')
        // console.log(val)
        this.setOptions(val)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.setOptions(this.chartData)
    },
    setOptions({ xData, yData, titleString } = {}) {
      this.chart = this.chart.dispose()
      this.chart = echarts.init(this.$el, 'macarons')
      // console.log(Object.keys(yData))
      // console.log(yData['厚'])

      this.chart.setOption({
        backgroundColor: '#344b58',
        title: {
          text: titleString,
          x: '20',
          top: '20',
          textStyle: {
            color: '#fff',
            fontSize: '22'
          },
          subtextStyle: {
            color: '#90979c',
            fontSize: '16'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        grid: {
          left: '5%',
          right: '5%',
          borderWidth: 0,
          top: 150,
          bottom: 95,
          textStyle: {
            color: '#fff'
          }
        },
        legend: {
          x: '5%',
          top: '10%',
          textStyle: {
            color: '#90979c'
          },
          data: Object.keys(yData)
        },
        calculable: true,
        xAxis: {
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          },
          splitLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          splitArea: {
            show: false
          },
          axisLabel: {
            interval: 0
          },
          data: xData
        },
        yAxis: {
          axisTick: {
            show: false
          },
          min: 0,
          max: 1
        },
        dataZoom: [{
          show: true,
          height: 30,
          xAxisIndex: [
            0
          ],
          bottom: 30,
          start: 0,
          end: 100,
          handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
          handleSize: '110%',
          handleStyle: {
            color: '#d3dee5'

          },
          textStyle: {
            color: '#fff' },
          borderColor: '#90979c'

        }, {
          type: 'inside',
          show: true,
          height: 15,
          start: 1,
          end: 35
        }],
        // series: [{
        //   name: '厚',
        //   smooth: true,
        //   type: 'line',
        //   data: yData['厚'],
        //   animationDuration: 2800,
        //   animationEasing: 'cubicInOut'
        //   itemStyle: {
        //     normal: {
        //       color: '#FF005A',
        //       lineStyle: {
        //         color: '#FF005A',
        //         width: 2
        //       }
        //     }
        //   },
        // },
        // {
        //   name: '常规',
        //   smooth: true,
        //   type: 'line',
        //   itemStyle: {
        //     normal: {
        //       color: '#3888fa',
        //       lineStyle: {
        //         color: '#3888fa',
        //         width: 2
        //       },
        //       areaStyle: {
        //         color: '#f3f8ff'
        //       }
        //     }
        //   },
        //   data: yData['常规'],
        //   animationDuration: 2800,
        //   animationEasing: 'quadraticOut'
        // },
        // {
        //   name: '薄',
        //   smooth: true,
        //   type: 'line',
        //   itemStyle: {
        //     normal: {
        //       color: '#000000',
        //       lineStyle: {
        //         color: '#000000',
        //         width: 2
        //       },
        //       // areaStyle: {
        //       //   color: '#000000'
        //       // }
        //     }
        //   },
        //   data: yData['薄'],
        //   animationDuration: 2800,
        //   animationEasing: 'quadraticOut'
        // }
        // ]
        series: (function() {
          const defaultAnimationDuration = 2000
          const defaultSmooth = true
          const defaultChartType = 'line'
          const colorOptions = ['#DC143C', '#FFD700', '#00FF00', '#00CED1', '#1E90FF', '#FF00FF', '#FF1493', '#696969', '#D2691E', '#00BFFF', '#20B2AA', '#2E8B57']
          const lineColorOptions = colorOptions
          const animationEasingOptions = ['cubicInOut', 'quadraticOut']
          const defaultLineWidth = 2
          // const defaultAreaStyleColor = '#FFFFFF'
          var seriesList = []
          var _name
          var counter = 0
          // console.log('start')
          for (_name in yData) {
            var maxVal = Math.max.apply(null, yData[_name])
            // console.log(Array.isArray(yData[_name]))
            // console.log(maxVal)
            if (maxVal < 0.01) {
              // console.log(_name)
              continue
            }
            seriesList.push({
              name: _name,
              smooth: defaultSmooth,
              type: defaultChartType,
              symbol: 'circle',
              symbolSize: 10,
              itemStyle: {
                normal: {
                  color: colorOptions[counter % colorOptions.length],
                  lineStyle: {
                    color: lineColorOptions[counter % lineColorOptions.length],
                    width: defaultLineWidth
                  }
                  // areaStyle: {
                  //   color: defaultAreaStyleColor
                  // }
                }
              },
              data: yData[_name].map(function(each_element) {
                return Number(each_element.toFixed(2))
              }),
              animationDuration: defaultAnimationDuration,
              animationEasing: animationEasingOptions[counter % animationEasingOptions.length]
            })
            counter += 1
            // console.log(counter)
          }
          // console.log(seriesList)
          return seriesList
        }())
      })
    }
  }
}
</script>
