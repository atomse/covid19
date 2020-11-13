<template>
  <div class="dashboard-editor-container">
    <!-- <github-corner class="github-corner" /> -->

    <el-card class="box-card" style="">
      <div slot="header" class="clearfix">
        <svg-icon icon-class="international" />
        <span style="margin-left:10px;">{{ $t('trend.covidTrend') }}</span>
      </div>
      <div>
        <el-form ref="form" :model="formData" label-width="120px">
          <el-form-item :label="$t('trend.country')">
            <el-radio-group v-model="formData.country" size="medium" @change="handleFormChange">
              <el-radio label="China" border>{{ $t('trend.China') }}</el-radio>
              <el-radio label="United States of America" border>{{ $t('trend.US') }}</el-radio>
              <el-radio label="India" border>{{ $t('trend.India') }}</el-radio>
            </el-radio-group>
            <span style="margin-left:50px;">{{ $t('trend.otherCountry') }}</span>
            <el-select v-model="formData.country" @change="handleFormChange">
              <el-option v-for="type in allCountries" :key="type" :label="type" :value="type" />
            </el-select>
          </el-form-item>
          <br>

          <el-row>
            <el-col :span="8">
              <el-form-item :label="$t('trend.startDate')" prop="timestamp">
                <el-date-picker
                  v-model="formData.startDate"
                  :label="$t('trend.startDate')"
                  type="date"
                  :placeholder="$t('trend.pickStartDate')"
                  :picker-options="startDatePickerOptions"
                  value-format="yyyy-MM-dd"
                  @change="handleFormChange"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item :label="$t('trend.endDate')" prop="timestamp">
                <el-date-picker
                  v-model="formData.endDate"
                  :label="$t('trend.endDate')"
                  type="date"
                  :placeholder="$t('trend.pickEndDate')"
                  :picker-options="endDatePickerOptions"
                  value-format="yyyy-MM-dd"
                  @change="handleFormChange"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
      <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;margin">
        <line-chart :chart-data="lineChartData" :title="$t('trend.covidVisual')" />
      </el-row>
    </el-card>

    <br>

    <el-card class="box-card" style="">
      <div slot="header" class="clearfix">
        <svg-icon icon-class="international" />
        <span style="margin-left:10px;">{{ $t('trend.covidRatio') }}</span>
      </div>
      <div>
        <el-form ref="form" :model="formData" label-width="120px">
          <el-form-item :label="$t('trend.type')">
            <el-radio-group v-model="pieType" size="medium" @change="processPieChart">
              <el-radio label="cumulative_cases" border>{{ $t('trend.cumulative_cases') }}</el-radio>
              <el-radio label="new_cases" border>{{ $t('trend.new_cases') }}</el-radio>
              <el-radio label="cumulative_deaths" border>{{ $t('trend.cumulative_deaths') }}</el-radio>
              <el-radio label="new_deaths" border>{{ $t('trend.new_deaths') }}</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item :label="$t('trend.topN')">
            <el-radio-group v-model="topN" size="medium" @change="processPieChart">
              <el-radio label="5" border>5</el-radio>
              <el-radio label="8" border>8</el-radio>
              <el-radio label="10" border>10</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </div>
      <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;margin">
        <pie-chart :chart-data="pieChartData" :title="$t('trend.countryRatio')" />
      </el-row>
    </el-card>

    <br>

    <el-card>
      <div slot="header" class="clearfix">
        <svg-icon icon-class="international" />
        <span style="margin-left:10px;">{{ $t('trend.covidList') }}</span>
      </div>

      <el-table :data="listData" border fit highlight-current-row style="width: 100%;">
        <el-table-column :label="$t('trend.country')" prop="id" sortable min-width="80px">
          <template slot-scope="scope">
            <img v-if="getImageUrl(scope.row.country_code)!=''" width="30" height="20" :src="getImageUrl(scope.row.country_code)">
            <span>{{ scope.row.country }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('trend.cumulative_cases')" sortable align="left" min-width="100px">
          <template slot-scope="scope">
            <span>{{ formatCurrency(scope.row.cumulative_cases) }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('trend.new_cases')" sortable align="left" min-width="100px">
          <template slot-scope="scope">
            <span>{{ formatCurrency(scope.row.new_cases) }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('trend.cumulative_deaths')" sortable align="left" min-width="100px">
          <template slot-scope="scope">
            <span>{{ formatCurrency(scope.row.cumulative_deaths) }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('trend.new_deaths')" sortable align="left" min-width="100px">
          <template slot-scope="scope">
            <span>{{ formatCurrency(scope.row.new_deaths) }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { fetchCountries, fetchDateRange, fetchCovidID19Data,
  fetchAllData, fetchCovid19LatestNumbers } from '@/api/trend'

// import GithubCorner from '@/components/GithubCorner'
// import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'
// import RaddarChart from './components/RaddarChart'
import PieChart from './components/PieChart'
// import BarChart from './components/BarChart'
// import TransactionTable from './components/TransactionTable'
// import TodoList from './components/TodoList'
// import BoxCard from './components/BoxCard'

const defaultCountry = 'China'
const defaultAllCountries = ['China', 'United States of America', 'India']
const defaultYAxis = {
  new_cases: {
    type: 'bar',
    yAxisIndex: 1
  },
  cumulative_cases: {
    type: 'line',
    yAxisIndex: 0
  },
  new_deaths: {
    type: 'bar',
    yAxisIndex: 1
  },
  cumulative_deaths: {
    type: 'line',
    yAxisIndex: 1
  }
}
const defaultLineData = {
  xData: ['2020-11-1', '2020-11-2', '2020-11-3'],
  yData: {
    new_cases: [200, 300, 400],
    cumulative_cases: [100, 200, 300],
    new_deaths: [200, 300, 400],
    cumulative_deaths: [200, 300, 400]
  },
  yMax: [200, 300],
  yAxis: defaultYAxis
}
const defaultListData = [{
  country: 'China',
  country_code: 'CN',
  cumulative_cases: 100,
  new_cases: 10,
  cumulative_deaths: 50,
  new_deaths: 0
}]
const defaultPieChartData = {
  xData: [
    'United States of America', 'India', 'Brazil', 'Argentina',
    'Iran (Islamic Republic of)', 'Others'
  ],
  yData: [
    10124555, 8683916, 5700044, 1262476, 715068, 9797362
  ]
  // titleString: this.$t('trend.countryRatio')
}
const defaultDateRange = {
  min: '2020-01-01',
  max: '2020-12-31'
}
const defaultCovid19LatestNumbers = { 'xData': ['United States of America', 'India', 'Brazil', 'Argentina', 'Colombia', 'Others'], 'yData': { 'cumulative_cases': [10124555, 8683916, 5700044, 1262476, 1156675, 9355755], 'cumulative_deaths': [238573, 128121, 162829, 34183, 33148, 324725], 'new_cases': [133935, 47905, 25012, 11977, 7612, 69385], 'new_deaths': [1846, 550, 201, 276, 174, 2002] }}
const reducer = (accumulator, currentValue) => accumulator + currentValue

export default {
  name: 'TrendIndex',
  components: {
    // GithubCorner,
    // PanelGroup,
    LineChart,
    // RaddarChart,
    PieChart
    // BarChart,
    // TransactionTable,
    // TodoList,
    // BoxCard
  },
  data() {
    return {
      allCountries: defaultAllCountries,
      dateRange: defaultDateRange,
      lineChartData: defaultLineData,
      pieChartData: defaultPieChartData,
      covid19LatestNumbers: defaultCovid19LatestNumbers,
      topN: '10',
      listData: defaultListData,
      formData: {
        country: defaultCountry,
        startDate: defaultDateRange.min,
        endDate: defaultDateRange.max
      },
      pieType: 'cumulative_cases',
      startDatePickerOptions: {
        disabledDate: time => {
          if (this.dateRange.min) {
            return (
              time.getTime() < new Date(this.dateRange.min).getTime() - 24 * 60 * 60 * 1000
            )
          }
        }
      },
      endDatePickerOptions: {
        disabledDate: time => {
          if (this.dateRange.max) {
            return (
              time.getTime() > new Date(this.dateRange.max).getTime()
            )
          }
        }
      }
    }
  },
  mounted() {
    // await this.mountAll()
    // this.handleCovidData()
    this.mountAll().then(() => {
      this.handleCovidData()
      this.handleCovid19LatestNumbers()
      // this.handleCovid19List()
    }).then(() => {
      this.$message({
        title: this.$t('trend.success'),
        message: this.$t('trend.loadSuccess'),
        type: 'success',
        duration: 2000
      })
    })
  },
  methods: {
    dealDisabledDate(time) {
      return (
        time.getTime() < new Date(this.dateRange.min).getTime() ||
        time.getTime() > new Date(this.dateRange.max).getTime()
      )
    },
    mountCountries() {
      return fetchCountries().then(response => {
        this.allCountries = response.data
      })
    },
    mountDateRange() {
      return fetchDateRange().then(response => {
        this.dateRange = response.data
        this.formData.startDate = this.dateRange.min
        this.formData.endDate = this.dateRange.max
      })
    },
    mountAll() {
      this.mountCountries()
      return this.mountDateRange()
    },
    handleCovidData() {
      fetchCovidID19Data(this.formData).then(response => {
        // {xData, yData} = response.data
        var xData = response.data.xData
        var yData = response.data.yData
        var newYData = {}
        console.log(yData)
        var max1 = yData.cumulative_cases[yData.cumulative_cases.length - 1]
        var max2 = Math.max(max1 / 10, Math.max.apply(null, yData.new_cases))
        var yAxis = {}
        for (const key in yData) {
          // console.log('key:', key, this.$t('trend.' + key))
          var newKey = this.$t('trend.' + key)
          newYData[newKey] = yData[key]
          yAxis[newKey] = defaultYAxis[key]
        }
        // console.log(Object.keys(newYData))
        this.lineChartData = {
          xData: xData,
          yData: newYData,
          yAxis: yAxis,
          yMax: [max1, max2],
          titleString: this.formData.country + ' ' + this.$t('trend.covidVisual')
        }
        console.log([max1, max2])
      })
    },
    handleCovid19LatestNumbers() {
      return fetchCovid19LatestNumbers().then(response => {
        // console.log(response.data)
        this.covid19LatestNumbers = response.data
        this.processPieChart()
        this.processListData()
      })
    },
    processListData() {
      var data = this.covid19LatestNumbers
      var xData = data.xData
      var yData = data.yData
      this.listData = [{
        country: 'Global',
        country_code: 'Global',
        cumulative_cases: yData.cumulative_cases.reduce(reducer),
        new_cases: yData.new_cases.reduce(reducer),
        cumulative_deaths: yData.cumulative_deaths.reduce(reducer),
        new_deaths: yData.new_deaths.reduce(reducer)
      }]
      for (var i = 0; i < xData.length; i++) {
        this.listData.push({
          country: xData[i],
          country_code: data.countryCode[i],
          cumulative_cases: yData.cumulative_cases[i],
          new_cases: yData.new_cases[i],
          cumulative_deaths: yData.cumulative_deaths[i],
          new_deaths: yData.new_deaths[i]
        })
      }
    },
    processPieChart() {
      var data = this.covid19LatestNumbers
      var topN = this.topN
      var temp = data.yData[this.pieType]
      var cdata = temp.sort(function(a, b) {
        return b - a
      })
      // var index = [...Array(temp.length).keys()].sort(function(i, j) {
      //   return temp[j] - temp[i]
      // })
      var xData = []
      var i = 0
      for (i = 0; i < temp.length; i++) {
        xData.push(data.xData[i])
      }
      // cdata, xData sort together
      var yData = []
      for (i = 0; i < topN; i++) {
        yData.push({
          name: xData[i],
          value: cdata[i]
        })
      }
      yData.push({
        name: 'Other',
        value: cdata.slice(topN, cdata.length).reduce(reducer)
      })
      var pieChartData = {
        xData: xData,
        yData: yData,
        titleString: this.$t('trend.' + this.pieType) + ' ' + this.$t('trend.countryRatio') + ' top' + topN
      }
      this.pieChartData = pieChartData
    },
    handleAllData() {
      fetchAllData().then(response => {
        this.lineChartData = response.data
      })
    },
    handleFormChange() {
      // console.log(this.formData)
      this.handleCovidData()
    },
    formatCurrency(num) {
      if (num) {
        // 将num中的$,去掉，将num变成一个纯粹的数据格式字符串
        num = num.toString().replace(/\$|\,/g, '')
        // 如果num不是数字，则将num置0，并返回
        if (num === '' || isNaN(num)) {
          return 'Not a Number ! '
        }
        // 如果num是负数，则获取她的符号
        var sign = ''
        if (num.indexOf('-') !== -1) {
          sign = '-'
          num = num.substr(1)
        }
        // 如果存在小数点，则获取数字的小数部分
        var cents = num.indexOf('.') > 0 ? num.substr(num.indexOf('.')) : ''
        cents = cents.length > 1 ? cents : '' // 注意：这里如果是使用change方法不断的调用，小数是输入不了的
        // 获取数字的整数数部分
        num = num.indexOf('.') > 0 ? num.substring(0, (num.indexOf('.'))) : num
        // 如果没有小数点，整数部分不能以0开头
        if (cents === '') {
          if (num.length > 1 && num.substr(0, 1) === '0') {
            return 'Not a Number ! '
          }
        } else {
          if (num.length > 1 && num.substr(0, 1) === '0') {
            return 'Not a Number ! '
          }
        }
        // 针对整数部分进行格式化处理，这是此方法的核心，也是稍难理解的一个地方，逆向的来思考或者采用简单的事例来实现就容易多了
        /*
          也可以这样想象，现在有一串数字字符串在你面前，如果让你给他家千分位的逗号的话，你是怎么来思考和操作的?
          字符串长度为0/1/2/3时都不用添加
          字符串长度大于3的时候，从右往左数，有三位字符就加一个逗号，然后继续往前数，直到不到往前数少于三位字符为止
         */
        for (var i = 0; i < Math.floor((num.length - (1 + i)) / 3); i++) {
          num = num.substring(0, num.length - (4 * i + 3)) + ',' + num.substring(num.length - (4 * i + 3))
        }
        // 将数据（符号、整数部分、小数部分）整体组合返回
        return sign + num + cents
      } else {
        return '0'
      }
    },
    getImageUrl(countryCode) {
      if (['Global', 'Other', ' '].indexOf(countryCode) === -1) {
        const url = '/countryFlags/' + countryCode.toLowerCase() + '.png'
        return url
      } else {
        return ''
      }
    }
  }
}

</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  // .github-corner {
  //   position: absolute;
  //   top: 0px;
  //   border: 0;
  //   right: 0;
  // }

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}
.chart-container{
  position: relative;
  width: 100%;
  height: calc(100vh - 84px);
}
</style>
