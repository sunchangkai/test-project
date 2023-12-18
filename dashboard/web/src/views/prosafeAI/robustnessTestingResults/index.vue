<template>
  <d2-container
    id="robustnessTestingResults"
    class="robustnessTestingResults"
    :class="{ 'page-compact': compact, topType: topType === 0 }"
  >
    <template slot="header">
      <h3>Select the testing result you want to view</h3>
      <div class="test-reulst-type">
        <div
          class="item"
          @click="topType = item.id"
          v-for="item in testReulstTypeList"
          :key="item.name"
        >
          <d2-icon-svg :name="item.icon" :class="item.icon" />
          <d2-icon-svg name="selected" class="selected" v-if="topType === item.id" />
          <span>{{ item.name }}</span>
        </div>
      </div>
      <template v-if="topType === 0">
        <h4>You may choose one or two aspects to view test result:</h4>
        <div class="aspects">
          <div
            class="item"
            v-for="item in aspectsList"
            :key="item.id"
            :class="{ active: activeAspectIndexs.includes(item.id) }"
            @click="aspectsChange(item.id)"
          >
            <div class="box">
              <d2-icon-svg :name="item.icon" class="aspectsIcon" />
              <span>{{ item.name }}</span>
            </div>
            <div v-if="showTooltipMessage(item.id)" class="tooltip-message" @click.stop>
              Please chose another aspect to analysis together
            </div>
          </div>
        </div>
        <div class="select-box">
          <div class="item" v-if="showFullCategory">
            <el-radio-group v-model="fullCategory">
              <el-radio :label="0" border>Full dataset</el-radio>
              <el-radio :label="1" border>A certain category of the dataset</el-radio>
            </el-radio-group>
          </div>
          <div class="item" v-if="showRunlabel">
            <h5 class="title">Sample categories of the dataset:</h5>
            <div class="checkbox-box">
              <el-checkbox-group v-model="runlabel" :max="maxRunLabelLength">
                <el-checkbox :label="item.idx" v-for="item in runLabelList" :key="item.idx">{{
                  item.category
                }}</el-checkbox>
              </el-checkbox-group>
            </div>
          </div>
          <div class="item" v-if="showAttackMethod">
            <h5 class="title">Attack methods:</h5>
            <div class="checkbox-box needWidth">
              <el-checkbox-group v-model="attackMethods" :max="maxMethodsLength">
                <el-checkbox
                  :disabled="item.disable === 1"
                  :label="item.name"
                  v-for="item in runAttackMethodList"
                  :key="item.name"
                  >{{ item.name }}</el-checkbox
                >
                <el-button
                  v-if="showOk && showEok"
                  type="primary"
                  size="mini"
                  class="attackOk"
                  @click="handleSearch"
                  >ok</el-button
                >
              </el-checkbox-group>
              <div class="tips" v-if="showTips">
                (The non-optional methods are the ones not used in this test)
              </div>
            </div>
          </div>
          <div class="item" v-if="showDistanceType">
            <h5 class="title">Distance Type:</h5>
            <div class="radio-box">
              <el-radio-group v-model="distance">
                <el-radio :label="item.id" v-for="item in distanceTypeList" :key="item.id">{{
                  item.name
                }}</el-radio>
              </el-radio-group>
              <el-button v-if="showOk" type="primary" size="mini" class="ok" @click="handleSearch"
                >ok</el-button
              >
            </div>
          </div>
        </div>
      </template>
    </template>
    <attack-sample-info-table
      :runAttackMethodList="runAttackMethodList"
      :runLabelList="runLabelList"
      v-if="topType === 1"
      @updateCompact="updateCompact"
    ></attack-sample-info-table>
    <div v-else class="chart-box" v-loading="chartLaoding">
      <template v-if="showCategoryOrMethods">
        <Charts id="columnar" :option="categoryBarOption" className="columnar"></Charts>
        <div class="pie-box">
          <Charts id="pieAttack" :option="pieAttackOption" className="pie-item"></Charts>
          <Charts
            id="pieAttackSucess"
            :option="pieAttackSucessOption"
            className="pie-item"
          ></Charts>
        </div>
      </template>
      <template v-if="showDistanceType && Object.keys(distanceLineOption).length > 0">
        <Charts id="distanceLine" :option="distanceLineOption" className="line-item"></Charts>
      </template>
      <template v-if="showEok && Object.keys(barTotalOption).length > 0">
        <Charts id="barTotal" :option="barTotalOption" className="line-item"></Charts>
        <!-- <Charts id="barTotal1" :option="barTotalOption1" className="line-item"></Charts> -->
      </template>
      <el-card
        class="box-card"
        v-if="
          activeAspectIndexs.length &&
            !(isIncludes('2') && activeAspectIndexs.length === 1) &&
            showBoxCard
        "
      >
        <div>
          Conclusion:
        </div>
      </el-card>
    </div>
  </d2-container>
</template>

<script>
import { getEchartsData, getRunLabels, getRunAttackMethods } from './api';
import attackSampleInfoTable from './attackSampleInfoTable.vue';
export default {
  name: 'RobustnessTestingResults',
  components: {
    attackSampleInfoTable,
  },
  data() {
    return {
      chartLaoding: false,
      showBoxCard: false,
      activeAspectIndexs: [],
      categoryBarOption: {},
      pieAttackOption: {},
      pieAttackSucessOption: {},
      runLabelList: [],
      runAttackMethodList: [],
      distanceTypeList: [
        {
          id: 'l0',
          name: 'L0',
        },
        {
          id: 'l1',
          name: 'L1',
        },
        {
          id: 'l2',
          name: 'L2',
        },
        {
          id: 'linf',
          name: 'Linf',
        },
        {
          id: 'ssim',
          name: 'Structural Dissimilarity',
        },
      ],
      fullCategory: 0,
      distance: '',
      runlabel: [],
      attackMethods: [],
      distanceLineOption: {},
      barTotalOption: {},
      barTotalOption1: {},
      runId: this.$route.query.runId,
      algType: this.$route.query.algType,
      compact: false,
      topType: 0,
      testReulstTypeList: [
        {
          id: 0,
          name: 'View test data',
          icon: 'viewTestData',
        },
        {
          id: 1,
          name: 'View attack sample info',
          icon: 'viewAttack',
        },
      ],
    };
  },
  computed: {
    aspectsList() {
      return [
        this.algType !== 'object_detection' && {
          id: '0',
          name: 'Dataset category',
          icon: 'category',
        },
        {
          id: '1',
          name: 'Attack methods',
          icon: 'methods',
        },
        {
          id: '2',
          name: 'Sample distance',
          icon: 'distance',
        },
      ].filter(Boolean);
    },
    showCategoryOrMethods() {
      const { isIncludes, activeAspectIndexs } = this;
      return (isIncludes('0') || isIncludes('1')) && activeAspectIndexs.length === 1;
    },
    showFullCategory() {
      const { isIncludes, activeAspectIndexs } = this;
      return isIncludes('0') && isIncludes('2') && activeAspectIndexs.length === 2;
    },
    showDistanceType() {
      const { isIncludes, activeAspectIndexs } = this;
      return (
        (isIncludes('0') || isIncludes('1')) && isIncludes('2') && activeAspectIndexs.length === 2
      );
    },
    showRunlabel() {
      const { showFullCategory, fullCategory, isIncludes } = this;
      return (showFullCategory && fullCategory === 1) || (isIncludes('0') && isIncludes('1'));
    },
    showAttackMethod() {
      const { isIncludes, activeAspectIndexs } = this;
      return (
        (isIncludes('0') || isIncludes('2')) && isIncludes('1') && activeAspectIndexs.length === 2
      );
    },
    showTips() {
      return (
        this.runAttackMethodList.some(item => item.disable === 1) ||
        this.$route.query.modelType !== 'black box'
      );
    },
    showOk() {
      return this.activeAspectIndexs.length === 2;
    },
    showEok() {
      const { isIncludes } = this;
      return this.showOk && isIncludes('0') && isIncludes('1');
    },
    maxMethodsLength() {
      if (this.showEok) {
        return 3;
      }
      return undefined;
    },
    maxRunLabelLength() {
      if (this.showFullCategory) {
        return 5;
      }
      return 3;
    },
    showTooltipMessage() {
      return id => {
        return id === '2' && this.activeAspectIndexs.length === 1 && this.isIncludes('2');
      };
    },
  },
  async created() {
    const { runId } = this;
    getRunLabels({ run_id: runId }).then(({ data }) => {
      this.runLabelList = data;
    });
    getRunAttackMethods({ run_id: runId }).then(({ data }) => {
      this.runAttackMethodList = data;
    });
  },
  methods: {
    updateCompact(val) {
      this.compact = val;
    },
    isIncludes(id) {
      return this.activeAspectIndexs.includes(id);
    },
    aspectsChange(id) {
      const { activeAspectIndexs, getEchartsDataByAspects } = this;
      this.categoryBarOption = {};
      this.pieAttackOption = {};
      this.pieAttackSucessOption = {};
      this.distanceLineOption = {};
      this.barTotalOption = {};
      this.barTotalOption1 = {};
      this.attackMethods = [];
      this.runlabel = [];
      this.showBoxCard = false;
      if (activeAspectIndexs.includes(id)) {
        const index = activeAspectIndexs.findIndex(item => item === id);
        this.activeAspectIndexs.splice(index, 1);
        getEchartsDataByAspects();
        return;
      }
      if (activeAspectIndexs.length === 2) {
        this.activeAspectIndexs.splice(1, 1, id);
        getEchartsDataByAspects();
        return;
      }
      this.activeAspectIndexs.push(id);
      getEchartsDataByAspects();
    },
    initCategoryOrMethodsBar(text, xData, seriesData) {
      return {
        title: [
          {
            text,
          },
        ],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow',
          },
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true,
        },
        xAxis: [
          {
            type: 'category',
            data: xData,
            axisTick: {
              alignWithLabel: true,
            },
          },
        ],
        yAxis: [
          {
            type: 'value',
          },
        ],
        series: [
          {
            // name: 'Direct',
            type: 'bar',
            barWidth: '60%',
            data: seriesData,
          },
        ],
      };
    },
    initCategoryOrMethodsBarPie(text, seriesData) {
      return {
        title: [
          {
            text,
          },
        ],
        tooltip: {
          trigger: 'item',
        },
        legend: {
          top: '5%',
          left: 'center',
        },
        series: [
          {
            name: text,
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2,
            },
            label: {
              show: false,
              position: 'center',
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 20,
                fontWeight: 'bold',
              },
            },
            labelLine: {
              show: false,
            },
            data: seriesData,
          },
        ],
      };
    },
    getChoose(item) {
      if (item === '0' && this.fullCategory === 0 && this.showFullCategory) {
        return undefined;
      }
      return item === '0' ? this.runlabel : item === '1' ? this.attackMethods : this.distance;
    },
    initDistanceLineOption(text, legendData, xAxisData, series) {
      return {
        title: {
          text: text,
        },
        tooltip: {
          trigger: 'axis',
        },
        legend: {
          data: legendData,
          orient: 'vertical',
          right: 0,
          // top: 'center'
        },
        grid: {
          left: '3%',
          right: this.isIncludes('0') ? '5%' : '14%',
          bottom: '3%',
          containLabel: true,
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: xAxisData,
        },
        yAxis: {
          type: 'value',
        },
        series: series,
      };
    },
    initBarTotalOption(yData, assSeries, failSeries) {
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            // Use axis to trigger tooltip
            type: 'shadow', // 'shadow' as default; can also be 'line' or 'shadow'
          },
        },
        legend: {},
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true,
        },
        xAxis: {
          type: 'value',
        },
        yAxis: {
          type: 'category',
          data: yData,
        },
        series: [
          {
            name: 'ASS',
            type: 'bar',
            stack: 'total',
            label: {
              show: true,
            },
            emphasis: {
              focus: 'series',
            },
            data: assSeries,
          },
          {
            name: 'Fail',
            type: 'bar',
            stack: 'total',
            label: {
              show: true,
            },
            emphasis: {
              focus: 'series',
            },
            data: failSeries,
          },
        ],
      };
    },
    async handleSearch() {
      this.chartLaoding = true;
      if (!this.distance && this.showDistanceType) {
        this.$message.warning('Please choose a distance type.');
        this.chartLaoding = false;
        return;
      }
      try {
        const { activeAspectIndexs, runId } = this;
        const detail = activeAspectIndexs.map(item => ({
          aspect: item,
          choose: this.getChoose(item),
        }));
        const { data } = await getEchartsData({
          run_id: runId,
          detail,
        });
        if (this.showDistanceType) {
          const xAxisData = data.x;
          const legendData = [];
          const series = [];
          data.detail.forEach(item => {
            legendData.push(item.slice);
            series.push({
              name: item.slice,
              type: 'line',
              data: item.y || item.detail,
            });
          });
          const distanceName = this.distanceTypeList.filter(item => item.id === this.distance).at()
            .name;
          let text = `ASR variation with ${distanceName} distance`;
          if (this.isIncludes('0') && this.fullCategory === 0) {
            text += ' (full dataset)';
          }
          if (this.isIncludes('0') && this.fullCategory === 1) {
            text += ' (certain category)';
          }
          this.distanceLineOption = this.initDistanceLineOption(
            text,
            legendData,
            xAxisData,
            series,
          );
        }
        if (this.showEok) {
          const yData = [];
          const assSeries = [];
          const failSeries = [];
          data.forEach(item => {
            yData.push(item.slice);
            assSeries.push(item.detail.attack_success || undefined);
            failSeries.push(item.detail.attack_failed || undefined);
          });
          const sortData = [...data];
          sortData.sort((x, y) => {
            return x.slice.split('*')[1].localeCompare(y.slice.split('*')[1], 'fr', {
              ignorePunctuation: true,
            });
          });
          const yData1 = [];
          const assSeries1 = [];
          const failSeries1 = [];
          sortData.forEach(item => {
            const nameList = item.slice.split('*');
            yData1.push(`${nameList[1]}*${nameList[0]}`);
            assSeries1.push(item.detail.attack_success || undefined);
            failSeries1.push(item.detail.attack_failed || undefined);
          });
          this.barTotalOption = this.initBarTotalOption(yData, assSeries, failSeries);
          this.barTotalOption1 = this.initBarTotalOption(yData1, assSeries1, failSeries1);
        }
      } catch (error) {}
      this.chartLaoding = false;
      this.$nextTick(() => {
        this.showBoxCard = true;
      });
    },
    async getEchartsDataByAspects() {
      const { activeAspectIndexs, runId } = this;
      if (
        !activeAspectIndexs.length ||
        activeAspectIndexs.length > 1 ||
        (activeAspectIndexs.length === 1 && activeAspectIndexs.includes('2'))
      )
        return;
      this.chartLaoding = true;
      try {
        const detail = activeAspectIndexs.map(item => ({
          aspect: item,
        }));
        const { data } = await getEchartsData({
          run_id: runId,
          detail,
        });
        if (this.showCategoryOrMethods) {
          const barXData = [];
          const barSeriesData = [];
          const pieSeriesData = [];
          const pieSuccessSeriesData = [];
          data.forEach((item, index) => {
            if (item.slice !== 'other') {
              barXData.push(item.slice);
              if (index === 0) {
                barSeriesData.push({
                  value: item.detail.ASR,
                  itemStyle: {
                    color: '#91cc75',
                  },
                });
              } else {
                barSeriesData.push(item.detail.ASR);
              }
            }
            pieSeriesData.push({
              value: item.detail.attack_samples,
              name: item.slice,
            });
            pieSuccessSeriesData.push({
              value: item.detail.attack_success,
              name: item.slice,
            });
          });
          const isCategory = activeAspectIndexs[0] === '0';
          const text = isCategory
            ? 'The Attacks Success Rate in different categories of dataset samples'
            : 'The Attacks Success Rate in different methods';
          this.categoryBarOption = this.initCategoryOrMethodsBar(text, barXData, barSeriesData);
          this.pieAttackOption = this.initCategoryOrMethodsBarPie('#Attack Sample', pieSeriesData);
          this.pieAttackSucessOption = this.initCategoryOrMethodsBarPie(
            '#Attack Success Sample',
            pieSuccessSeriesData,
          );
        }
      } catch (error) {}
      this.chartLaoding = false;
      this.$nextTick(() => {
        this.showBoxCard = true;
      });
    },
  },
};
</script>

<style lang="scss" scoped>
#robustnessTestingResults {
  .chart-box {
    height: 100%;
  }
  :deep() .d2-container-full__header {
    padding-bottom: 0;
  }
  &.topType {
    :deep() .d2-container-full {
      overflow-y: auto;
      background: #fff;
      .d2-container-full__body {
        overflow: initial;
        height: initial;
      }
    }
  }
  .select-box {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    .ok {
      position: absolute;
      right: -75px;
      bottom: 0;
    }
    .item {
      display: flex;
      margin-bottom: 15px;
      .title {
        flex: none;
        margin: 0;
        margin-right: 15px;
      }
      .radio-box,
      .checkbox-box {
        position: relative;
        display: block;
      }
      .radio-box {
        :deep().el-radio-group {
          font-size: inherit;
        }
      }
      .checkbox-box {
        &.needWidth {
          :deep() .el-checkbox {
            width: 130px;
            margin-bottom: 10px;
          }
          .attackOk {
            margin-left: 30px;
          }
        }
        :deep().el-checkbox-group {
          font-size: inherit;
          display: flex;
          flex-wrap: wrap;
        }
        .tips {
          font-size: 13px;
          color: #73c3da;
          margin-top: 5px;
        }
      }
    }
  }
  .test-reulst-type {
    display: flex;
    margin: 20px 0;
    .item {
      flex: 0 0 300px;
      height: 95px;
      display: flex;
      align-items: center;
      background: #abe2fa;
      border-radius: 5px;
      margin-right: 30px;
      padding: 20px 10px 20px 20px;
      cursor: pointer;
      position: relative;
      &:last-child {
        background: #fcdeb6;
      }
      .selected {
        position: absolute;
        top: -1px;
        right: -1px;
        width: 50px;
        height: 50px;
      }
      .viewTestData,
      .viewAttack {
        display: block;
        width: 45px;
        height: 45px;
        margin-right: 20px;
      }
      .viewAttack {
        width: 38px;
        height: 38px;
      }
    }
  }
  .aspects {
    display: flex;
    margin: 20px 0;
    .item {
      flex: 0 0 220px;
      height: 70px;
      margin-right: 40px;
      border-radius: 8px;
      cursor: pointer;
      position: relative;
      .tooltip-message {
        position: absolute;
        top: -100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 10px;
        background: #fff;
        display: block;
        width: 200px;
        border-radius: 4px;
        border: 1px solid #ebeef5;
        color: #606266;
        line-height: 1.4;
        text-align: justify;
        font-size: 14px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        word-break: break-all;
        cursor: initial;
        &::after {
          content: ' ';
          border-width: 6px;
          position: absolute;
          display: block;
          width: 0;
          height: 0;
          border-color: transparent;
          border-style: solid;
          border-bottom-width: 0;
          border-top-color: #fff;
          bottom: -6px;
          left: 50%;
          transform: translateX(-50%);
          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        }
      }
      .box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        background: #909399;
        border-radius: 8px;
        position: relative;
      }
      &.active > .box {
        background: #8080ff;
        color: #fff;
      }
      &:last-child {
        margin-right: 0;
      }
      .aspectsIcon {
        width: 35px;
        height: 35px;
        margin-bottom: 5px;
      }
    }
  }
  .columnar {
    height: 600px;
    width: 100%;
  }
  .pie-box {
    display: flex;
    margin: 30px auto;
    .pie-item {
      width: 50%;
      height: 500px;
    }
  }
  .line-item {
    height: 600px;
    width: 100%;
    margin: 0 0 20px;
  }
  .box-card {
    width: 60%;
    height: 300px;
    border-radius: 15px;
    position: relative;
    margin: 0 auto;
    &:after {
      content: '';
      display: block;
      width: 30px;
      height: 100%;
      position: absolute;
      left: 0;
      top: 0;
      background: #82d4f8;
    }
    :deep().el-card__body {
      padding: 60px;
    }
  }
}
</style>
