<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

const colorOptions = ['#DC143C', '#FFD700', '#00FF00', '#00CED1', '#1E90FF', '#FF00FF', '#FF1493', '#696969', '#D2691E', '#00BFFF', '#20B2AA', '#2E8B57']

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
    },
    title: {
      type: String,
      default: '',
      required: false
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
    },
    title: {
      deep: true,
      handler(val) {
        this.setTitle(val)
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
      this.setTitle(this.title)
    },
    setTitle(title) {
      if (this.chart) {
        this.chart.setOption({
          title: {
            text: title,
            x: '120',
            top: '20',
            textStyle: {
              color: '#000000',
              fontSize: '22'
            },
            subtextStyle: {
              color: '#90979c',
              fontSize: '16'
            }
            // textAlign: 'right'
          }
        })
      }
    },
    setOptions({ xData, yData, yAxis, yMax, titleString } = {}) {
      this.chart = this.chart.dispose()
      this.chart = echarts.init(this.$el, 'macarons')
      this.chart.setOption({
        // backgroundColor: '#344b58',
        title: {
          text: titleString,
          x: '120',
          top: '20',
          textStyle: {
            color: '#000000',
            fontSize: '22'
          },
          subtextStyle: {
            color: '#90979c',
            fontSize: '16'
          }
          // textAlign: 'right'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        grid: {
          left: '10%',
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
            interval: 10,
            show: true,
            rotate: 60
          },
          data: xData
        },
        yAxis: [
          {
            type: 'value',
            axisTick: {
              show: false
            },
            min: 0,
            max: yMax[0],
            axisLine: {
              lineStyle: {
                color: colorOptions[0]
              }
            },
            position: 'left'
          },
          {
            type: 'value',
            axisTick: {
              show: false
            },
            min: 0,
            max: yMax[1],
            axisLine: {
              lineStyle: {
                color: colorOptions[1]
              }
            },
            position: 'right'
          }
        ],
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
            color: '#fff'
          },
          borderColor: '#90979c'
        }, {
          type: 'inside',
          show: true,
          height: 15,
          start: 1,
          end: 35
        }],
        series: (function() {
          const defaultAnimationDuration = 2000
          const defaultSmooth = true
          // const defaultChartType = 'line'
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
              // type: defaultChartType,
              symbol: 'none',
              type: yAxis[_name]['type'],
              yAxisIndex: yAxis[_name]['yAxisIndex'],
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
