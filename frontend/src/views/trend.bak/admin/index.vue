<template>
  <div class="dashboard-editor-container">
    <!-- <github-corner class="github-corner" /> -->

    <el-card class="box-card" style="">
      <div slot="header" class="clearfix">
        <svg-icon icon-class="international" />
        <span style="margin-left:10px;">服装品类</span>
      </div>
      <div>
        <el-form ref="form" :model="fashionForm" label-width="120px">
          <el-radio-group v-model="fashionForm.clothType" size="medium" @change="setDefaultPropertyLocation()">
            <el-radio label="cloth" border>
              上衣
            </el-radio>
            <el-radio label="trousers" border>
              裤子
            </el-radio>
            <el-radio label="dress" border>
              连衣裙
            </el-radio>
            <el-radio label="shoes" border>
              鞋子
            </el-radio>
            <el-radio label="bag" border>
              箱包
            </el-radio>
            <!-- <el-radio label="skirt" border>
              裙子
            </el-radio>
            <el-radio label="suit" border>
              套装
            </el-radio> -->
          </el-radio-group>
          <!-- <el-tag style="margin-top:15px;display:block;" type="info">
            {{ $t('i18nView.note') }}
          </el-tag> -->

          <el-radio-group v-model="fashionForm.location" style="margin-top:20px;" name="地域" size="medium" @change="setFashionData()">
            <el-radio label="不限" border>
              不限
            </el-radio>
            <!-- <el-radio label="欧美" border>
              欧美
            </el-radio> -->
            <el-radio label="日本" border>
              日本
            </el-radio>
            <el-radio label="韩国" border>
              韩国
            </el-radio>
            <!-- <el-radio label="中国" border>
              中国（暂无数据）
            </el-radio> -->
          </el-radio-group>

          <el-radio-group v-model="fashionForm.dataType" style="margin-top:20px;" name="历史/预测" size="medium" @change="setFashionData()">
            <el-radio label="history" border>
              历史
            </el-radio>
            <!-- <el-radio label="prediction_lstm_zyx" border>
              预测_LSTM
            </el-radio> -->
            <el-radio label="prediction_dt_lh" border>
              预测_决策树
            </el-radio>
            <el-radio label="prediction_lstm_hfx" border>
              预测_LSTM
            </el-radio>
          </el-radio-group>

          <el-form-item style="margin-top:20px;" label="属性类型">
            <el-select v-model="fashionForm.propertyType" placeholder="请选择您想查看的属性" @change="setFashionData()">
              <el-option v-for="property in fashionTypesConst[fashionForm.clothType]" :key="property" :label="property" :value="property" />
            </el-select>
          </el-form-item>

        </el-form>
      </div>
      <!-- <div class="chart-container">
        <chart :chart-date="fashionLineData" height="100%" width="100%" />
      </div> -->
    </el-card>

    <!-- <panel-group @handleSetLineChartData="handleSetLineChartData" /> -->

    <el-row style="padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="fashionLineData" />
    </el-row>

    <!-- <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <raddar-chart />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <pie-chart />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <bar-chart />
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 12}" :xl="{span: 12}" style="padding-right:8px;margin-bottom:30px;">
        <transaction-table />
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}" style="margin-bottom:30px;">
        <todo-list />
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}" style="margin-bottom:30px;">
        <box-card />
      </el-col>
    </el-row> -->
  </div>
</template>

<script>
// import GithubCorner from '@/components/GithubCorner'
// import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'
// import RaddarChart from './components/RaddarChart'
// import PieChart from './components/PieChart'
// import BarChart from './components/BarChart'
// import TransactionTable from './components/TransactionTable'
// import TodoList from './components/TodoList'
// import BoxCard from './components/BoxCard'
// import Chart from './components/MixChart'

const lineChartData = {
  newVisitis: {
    expectedData: [100, 120, 161, 134, 105, 160, 165],
    actualData: [120, 82, 91, 154, 162, 140, 145]
  },
  messages: {
    expectedData: [200, 192, 120, 144, 160, 130, 140],
    actualData: [180, 160, 151, 106, 145, 150, 130]
  },
  purchases: {
    expectedData: [80, 100, 121, 104, 105, 90, 100],
    actualData: [120, 90, 100, 138, 142, 130, 130]
  },
  shoppings: {
    expectedData: [130, 140, 141, 142, 145, 150, 160],
    actualData: [120, 82, 91, 154, 162, 140, 130]
  },
  malls: {
    expectedData: [130, 140, 141, 142, 145, 150, 160],
    actualData: [120, 82, 91, 154, 162, 140, 130]
  }
}

const fashionTypesConst = {
  cloth: ['厚薄', '图案', '服装版型', '流行元素_工艺', '组合形式', '衣长', '衣门襟', '袖型', '袖长', '适用场景', '适用季节', '适用性别', '领型', '风格'],
  trousers: ['厚薄', '图案', '款式', '洗水工艺', '腰型', '裤长', '裤门襟', '适用场景', '适用季节', '适用对象', '风格'],
  dress: ['图案', '廓形', '衣门襟', '袖型', '袖长', '裙长', '适用场景', '适用季节', '适用对象', '领型', '风格'],
  skirt: ['图案', '廓形', '裙长', '适用场景', '适用季节', '适用对象', '风格'],
  shoes: ['开口深度', '款式', '皮质特征', '适用场景', '适用季节', '适用年龄', '适用性别', '鞋帮高度', '鞋跟', '风格'],
  suit: ['流行元素', '质地', '闭合方式'],
  bag: ['图案', '大小', '形状', '性别', '款式', '适用场景', '闭合方式', '风格']
}
const defaultClothType = 'cloth'
const defaultPropertyType = fashionTypesConst[defaultClothType][0]
const fashionTrendHistoryData = {}

const fashionTrendPredictionData_zyxlstm = {}
const fashionTrendPredictionData_lhdt = {}
const fashionTrendPredictionData_hfxlstm = {}

const fashionTrendData = {
  history: fashionTrendHistoryData,
  prediction_lstm_zyx: fashionTrendPredictionData_zyxlstm,
  prediction_dt_lh: fashionTrendPredictionData_lhdt,
  prediction_lstm_hfx: fashionTrendPredictionData_hfxlstm
}

const clothTypesName = {
  'cloth': '上衣',
  'trousers': '裤子',
  'dress': '连衣裙',
  'shoes': '鞋子',
  'bag': '箱包',
  'skirt': '裙子',
  'suit': '套装'
}

const locationTypesConst = ['不限', '欧美', '日本', '韩国', '中国(暂无数据)']
const defaultLocation = '不限'
const defaultDataType = 'history'

// const fashionTypesConst = {
//   cloth: ['newVisitis', 'messages', 'purchases', 'shoppings'],
//   trousers: ['newVisitis', 'messages', 'purchases', 'shoppings'],
//   dress: ['newVisitis', 'messages', 'purchases', 'shoppings'],
//   skirt: ['newVisitis', 'messages', 'purchases', 'shoppings'],
//   shoes: ['newVisitis', 'messages', 'purchases', 'shoppings'],
//   suit: ['newVisitis', 'messages', 'purchases', 'shoppings'],
//   bag: ['newVisitis', 'messages', 'purchases', 'shoppings']
// }

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
    // Chart
  },
  data() {
    return {
      lineChartData: lineChartData.newVisitis,
      fashionTypesConst: fashionTypesConst,
      // fashionTrendData: fashionTrendData,
      fashionForm: {
        clothType: defaultClothType,
        propertyType: defaultPropertyType,
        location: defaultLocation,
        dataType: defaultDataType // 预测/历史
      },
      // selectionReset: true,
      // fashionTrendHistoryData: fashionTrendHistoryData,
      // fashionTrendPredictionData: fashionTrendPredictionData,
      fashionLineData: {
        xData: fashionTrendHistoryData.__time_series__,
        yData: fashionTrendHistoryData[defaultClothType][defaultLocation][defaultPropertyType],
        titleString: defaultDataType + ' ' + '地域:' + defaultLocation + ' ' + clothTypesName[defaultClothType] + ':' + defaultPropertyType
      },
      locationTypesConst: locationTypesConst,
      defaultLocation: defaultLocation
    }
  },
  methods: {
    handleSetLineChartData(type) {
      // console.log(this.fashionForm)
      this.lineChartData = lineChartData[type]
    },
    // refreshSelections() {
    //   this.selectionReset = false
    //   this.$nextTick(() => {
    //     this.selectionReset = true
    //   })
    // },
    setDefaultPropertyLocation() {
      this.fashionForm.propertyType = fashionTypesConst[this.fashionForm.clothType][0]
      this.setFashionData()
    },
    optionSetLineChartData() {
      // console.log(this.fashionForm)
      // this.lineChartData = lineChartData[this.fashionForm.propertyType]
    },
    requestFashionData(type) {
      this.lineChartData = {
        expectedData: [130, 140, 141, 142, 145, 150, 160],
        actualData: [120, 82, 91, 154, 162, 140, 130]
      }
    },
    setFashionData() {
      // console.log(fashionTrendData[this.fashionForm.dataType].__time_series__)
      // console.log(fashionTrendData[this.fashionForm.dataType][this.fashionForm.clothType][this.fashionForm.location][this.fashionForm.propertyType])
      this.fashionLineData = {
        xData: fashionTrendData[this.fashionForm.dataType].__time_series__,
        yData: fashionTrendData[this.fashionForm.dataType][this.fashionForm.clothType][this.fashionForm.location][this.fashionForm.propertyType],
        titleString: this.fashionForm.dataType + ' ' + '地域:' + this.fashionForm.location + ' ' + clothTypesName[this.fashionForm.clothType] + ':' + this.fashionForm.propertyType
      }
      // console.log(this.fashionForm.clothType)
      // console.log(this.fashionForm.propertyType)
      // console.log(this.fashionLineData)
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
