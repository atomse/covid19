<template>
  <div class="dashboard-editor-container">
    <!-- <github-corner class="github-corner" /> -->

    <el-card class="box-card" style="">
      <div slot="header" class="clearfix">
        <svg-icon icon-class="international" />
        <span style="margin-left:10px;">新冠数据</span>
      </div>
      <div>
        <el-form ref="form" :model="formData" label-width="120px">
          <el-form-item :label="$t('trend.country')">
            <el-radio-group v-model="formData.country" size="medium" @change="handleFormChange">
              <el-radio label="China" border>中国</el-radio>
              <el-radio label="United States of America" border>美国</el-radio>
              <el-radio label="India" border>印度</el-radio>
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
                  @change="handleFormChange"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </el-card>

    <br>

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;margin">
      <line-chart :chart-data="lineChartData" :title="$t('trend.covidVisual')" />
    </el-row>

  </div>
</template>

<script>
import { fetchCountries, fetchDateRange, fetchCovidID19Data, fetchAllData } from '@/api/trend'

// import GithubCorner from '@/components/GithubCorner'
// import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'
// import RaddarChart from './components/RaddarChart'
// import PieChart from './components/PieChart'
// import BarChart from './components/BarChart'
// import TransactionTable from './components/TransactionTable'
// import TodoList from './components/TodoList'
// import BoxCard from './components/BoxCard'

const defaultCountry = 'China'
const defaultAllCountries = ['China', 'United States of America', 'India']
const defaultLineData = {
  xData: ['2020-11-1', '2020-11-2', '2020-11-3'],
  yData: {
    'New_cases': [200, 300, 400],
    'Cumulative_cases': [100, 200, 300],
    'New_deaths': [200, 300, 400],
    'Cumulative_deaths': [200, 300, 400]
  }
}
const defaultDateRange = {
  min: '2020-01-01',
  max: '2020-12-31'
}

export default {
  name: 'TrendIndex',
  components: {
    // GithubCorner,
    // PanelGroup,
    LineChart
    // RaddarChart,
    // PieChart,
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
      formData: {
        country: defaultCountry,
        startDate: defaultDateRange.min,
        endDate: defaultDateRange.max
      },
      startDatePickerOptions: {
        disabledDate: time => {
          if (this.dateRange.min) {
            return (
              time.getTime() < new Date(this.dateRange.min).getTime()
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
      return this.mountCountries().then(() => {
        this.mountDateRange()
      })
    },
    handleCovidData() {
      fetchCovidID19Data(this.formData).then(response => {
        // {xData, yData} = response.data
        var xData = response.data.xData
        var yData = response.data.yData
        var newYData = {}
        console.log(yData, Object.keys(yData))
        for (const key in yData) {
          console.log('key:', key, this.$t('trend.' + key))
          newYData[this.$t('trend.' + key)] = yData[key]
        }
        // console.log(Object.keys(newYData))
        this.lineChartData = {
          xData: xData,
          yData: newYData,
          titleString: this.$t('trend.covidVisual')
        }
      })
    },
    handleAllData() {
      fetchAllData().then(response => {
        this.lineChartData = response.data
      })
    },
    handleFormChange() {
      console.log(this.formData)
      this.handleCovidData()
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
