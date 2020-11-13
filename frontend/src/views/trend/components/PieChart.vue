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
      default: '300px'
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
    setOptions({ xData, yData, titleString } = {}) {
      this.chart.setOption({
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
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
        legend: {
          left: 'center',
          bottom: '10',
          data: xData
        },
        calculable: true,
        series: [
          {
            name: 'Covid19',
            type: 'pie',
            // roseType: 'radius',
            radius: 95,
            // center: ['50%', '38%'],
            // data: [
            //   { value: 320, name: 'Industries' },
            //   { value: 240, name: 'Technology' },
            //   { value: 149, name: 'Forex' },
            //   { value: 100, name: 'Gold' },
            //   { value: 59, name: 'Forecasts' }
            // ],
            data: yData,
            animationEasing: 'cubicInOut',
            animationDuration: 2600
          }
        ]
      })
    }
  }
}
</script>
