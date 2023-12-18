<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x ref="d2Crud" :data="data" :columns="crud.columns" :options="crud.options">
      <template slot="body">
        <div class="div-root">
          <el-container class="chart-container" direction="vertical">
            <el-main class="chart-main" direction="vertical">
              <!-- 基本信息 -->
              <div class="topleft-info">
                <el-descriptions title="Table Information" border>
                  <el-descriptions-item label="Project">{{ project }}</el-descriptions-item>
                  <el-descriptions-item label="UseCase">{{ userCase }}</el-descriptions-item>
                  <el-descriptions-item label="Table Name">{{ tableName }}</el-descriptions-item>
                  <el-descriptions-item label="Current Version">{{ version }}</el-descriptions-item>
                  <el-descriptions-item label="Table Descripition">{{
                    tableDesc
                  }}</el-descriptions-item>
                </el-descriptions>
              </div>

              <!-- 筛选条件 -->
              <div style="margin-top: 20px;">
                <div style="margin-bottom: 10px;margin-top: 15px;margin-left: 20px">
                  <label class="xrequired form-label">You want to count: </label>
                  <el-radio-group v-model="countType">
                    <el-radio :label="0">Number of samples</el-radio>
                    <el-radio :label="1" :disabled="objectRatioEnable">Number of objects</el-radio>
                  </el-radio-group>
                </div>
                <div style="margin-bottom: 10px;margin-left: 20px">
                  <label class="xrequired form-label">Choose the fields you want to group: </label>
                  <el-select
                    class="select-filter"
                    v-model="oddListValue"
                    size="medium"
                    multiple
                    filterable
                    allow-create
                    default-first-option
                    :multiple-limit="3"
                    placeholder="please choose odd"
                  >
                    <el-option
                      v-for="item in oddOptions"
                      :key="item"
                      :label="item"
                      :value="item"
                    ></el-option>
                  </el-select>
                </div>
                <div style="margin-bottom: 20px;margin-left: 20px">
                  <label class="form-label">Choose the versions you want to view: </label>
                  <el-select
                    class="select-filter"
                    v-model="versionListValue"
                    multiple
                    filterable
                    default-first-option
                    :multiple-limit="3"
                    placeholder="please choose version"
                  >
                    <el-option
                      v-for="item in versionList"
                      :key="item.version"
                      :label="item.version + ' (' + item.description + ')'"
                      :value="item.version"
                    >
                    </el-option>
                  </el-select>
                </div>
                <div class="div-commit">
                  <div>
                    <el-button type="success" @click="requestChartData">Commit</el-button>
                    <el-button style="margin-left: 20px" type="warning" @click="resetParams"
                      >Reset</el-button
                    >

                    <el-drawer
                      title="Visualization List"
                      :visible.sync="drawer"
                      size="20%"
                      custom-class="drawer-class"
                    >
                      <div style="width:100%;">
                        <div style="height: 88%;">
                          <el-container style="width: 100%;height: 100%" direction="vertical">
                            <el-main style="width: 100%;height: 100%" direction="vertical">
                              <div v-for="item in thumbList" :key="item.id" class="thunbnail-item">
                                <el-checkbox
                                  @change="checked => thunbnailCheckChange(checked, item.id)"
                                  :key="item.id"
                                  >&nbsp;
                                </el-checkbox>
                                <el-image :src="item.url" :fit="imgFit" :key="item.id"></el-image>
                              </div>
                            </el-main>
                          </el-container>
                        </div>
                        <div v-show="showPreview" class="preview-footer">
                          <el-button
                            :disabled="canPreviewReport"
                            type="success"
                            @click="previewExportPDF"
                            round
                          >
                            Preview Report
                          </el-button>
                        </div>
                      </div>
                    </el-drawer>
                  </div>
                </div>

                <!--                <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="200px" class="demo-ruleForm">-->
                <!--                  <el-form-item label="You want to count:" prop="resource">-->
                <!--                    <el-radio-group v-model="countType" style="margin-left: 20px">-->
                <!--                      <el-radio :label="0">Number of samples</el-radio>-->
                <!--                      <el-radio :label="1" :disabled="objectRatioEnable">Number of objects</el-radio>-->
                <!--                    </el-radio-group>-->
                <!--                  </el-form-item>-->
                <!--                  <el-form-item label="Choose the fields you want to group:" prop="region">-->
                <!--                    <el-select-->
                <!--                      class="select-filter"-->
                <!--                      v-model="oddListValue"-->
                <!--                      size="medium"-->
                <!--                      multiple-->
                <!--                      filterable-->
                <!--                      allow-create-->
                <!--                      default-first-option-->
                <!--                      :multiple-limit='3'-->
                <!--                      placeholder="please choose odd">-->
                <!--                      <el-option v-for="item in oddOptions" :key="item" :label="item" :value="item"></el-option>-->
                <!--                    </el-select>-->
                <!--                  </el-form-item>-->
                <!--                  <el-form-item>-->
                <!--                    <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>-->
                <!--                    <el-button @click="resetForm('ruleForm')">重置</el-button>-->
                <!--                  </el-form-item>-->
                <!--                </el-form>-->
              </div>
              <!-- 底部绘制图表的布局-->
              <div class="footer">
                <div v-for="(item, index) in chartOddGroup" :key="item" style="display: flex">
                  <div class="chart-parentl">
                    <div :ref="'fc'" class="chartcol-one" @click="handleChartLeft(index)"></div>
                    <div class="checkbox-div">
                      <el-popover
                        placement="top"
                        title=""
                        width="200"
                        trigger="hover"
                        :content="
                          showTipLeftValues[index]
                            ? 'Uncheck to move out of the preview list'
                            : 'Tick to add to preview list'
                        "
                      >
                        <el-checkbox
                          slot="reference"
                          @change="checked => addLeftChartToPool(checked, index)"
                        ></el-checkbox>
                      </el-popover>
                    </div>
                  </div>
                  <div class="chart-parentr">
                    <div :ref="'sc'" class="chartcol-one" @click="handleChartRight(index)"></div>
                    <div class="checkbox-div">
                      <el-popover
                        placement="top"
                        title=""
                        width="200"
                        trigger="hover"
                        :content="
                          showTipRightValues[index]
                            ? 'Uncheck to move out of the preview list'
                            : 'Tick to add to preview list'
                        "
                      >
                        <el-checkbox
                          slot="reference"
                          @change="checked => addRightChartToPool(checked, index)"
                        ></el-checkbox>
                      </el-popover>
                    </div>
                  </div>
                </div>

                <el-badge
                  v-show="thumbList.length > 0"
                  :value="thumbList.length"
                  class="chart-cart"
                >
                  <el-image
                    @click="drawer = true"
                    style="width: 30px;height: 30px;background-color: rgba(0, 0, 0, 0);"
                    :src="require('@/assets/pool.png')"
                    :fit="imgFit"
                  ></el-image>
                </el-badge>
              </div>
            </el-main>
          </el-container>
        </div>
      </template>
    </d2-crud-x>

    <el-dialog title="" :visible.sync="exportPDFVisible" width="90%" top="30px">
      <div style="display: flex;">
        <div style="width: 350px;">
          <p class="dialog-tab-title">Basic Information</p>
          <div class="dialog-left-title">
            <p class="ptitle">Project:</p>
            <p class="pcontent">{{ project }}</p>
          </div>
          <div class="dialog-left-title">
            <p class="ptitle">UseCase:</p>
            <p class="pcontent">{{ userCase }}</p>
          </div>
          <div class="dialog-left-title">
            <p class="ptitle">Table Name:</p>
            <p class="pcontent">{{ tableName }}</p>
          </div>
          <div class="dialog-left-title">
            <p class="ptitle">Table Descripition:</p>
            <p class="pcontent">{{ tableDesc }}</p>
          </div>
          <div class="dialog-left-title">
            <p class="ptitle">Current Version:</p>
            <p class="pcontent">{{ version }}</p>
          </div>
        </div>
        <div style="margin: 0 10px 0 10px">
          <p class="grey_line_pre"></p>
        </div>
        <div style="width: 100%">
          <p class="dialog-tab-title">Visual report</p>
          <el-container style="width: 100%" direction="vertical">
            <el-main style="height: 380px;width:100%;" direction="vertical">
              <div v-for="item in this.reportChartList" :key="item.id" class="preview-chart">
                <el-image
                  style="width: 780px;height: 400px"
                  :src="item.url"
                  :fit="imgFit"
                ></el-image>
              </div>
            </el-main>
            <div style="display: flex;margin-top: 20px">
              <el-button
                style="margin: 0 auto;width:100px;font-size: 20px"
                type="success"
                @click="savePDF"
                round
                >OK
              </el-button>
            </div>
          </el-container>
        </div>
      </div>
    </el-dialog>

    <el-dialog title="" :visible.sync="chartPreviewVisible" width="80%" top="20px">
      <div style="display: flex;background-color: white;width: 100%">
        <!--        <el-button class="btn-close" type="info" icon="el-icon-close" @click="chartPreviewVisible = false" circle></el-button>-->
        <el-container style="width: 100%;" direction="vertical">
          <el-main style="height: 500px;width:100%;padding: 1px" direction="vertical">
            <div :ref="'tc'" class="chartcol-third"></div>
          </el-main>
        </el-container>
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import * as api from './api';
import { crudOptions } from './crud';
import { d2CrudPlus } from 'd2-crud-plus';
import { mapMutations, mapActions } from 'vuex';

export default {
  name: 'dataDisplayChart',
  mixins: [d2CrudPlus.crud],

  data: function() {
    return {
      ruleForm: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: '',
      },
      rules: {
        region: [{ required: true, message: '请选择活动区域', trigger: 'change' }],

        date2: [{ type: 'date', required: true, message: '请选择时间', trigger: 'change' }],
        type: [
          { type: 'array', required: true, message: '请至少选择一个活动性质', trigger: 'change' },
        ],
        resource: [{ required: true, message: '请选择活动资源', trigger: 'change' }],
        desc: [{ required: true, message: '请填写活动形式', trigger: 'blur' }],
      },

      cartVisiable: false,
      data: [],
      showTipLeftValues: [],
      showTipRightValues: [],
      chartShoppingCart: [],
      // 这里是记录小图的配置，看大图的时候用到
      chartOptionsList: [],

      objectRatioEnable: false,
      canPreviewReport: true,
      chartPreviewVisible: false,
      exportPDFVisible: false,
      showPreview: false,
      drawer: false,
      chartTitleStyle: {
        // 数值样式
        color: 'black',
        fontSize: 13,
      },
      chartColOneColor: [
        '#4CD964',
        '#5AC8FA',
        '#007AFF',
        '#5856D6',
        '#FF2D70',
        '#FF3B30',
        '#FF9500',
        '#FFCC00',
        '#8E8E93',
        '#2F4F4F',
      ],
      chartColTwoColor: [
        '#FFEBCD',
        '#98F5FF',
        '#76EEC6',
        '#7B68EE',
        '#00FF00',
        '#EEE685',
        '#1E90FF',
        '#EEC900',
        '#BC8F8F',
        '#8B7D7B',
      ],
      chartLegend: {
        orient: 'horizontal',
        left: '8%',
        top: '18%',
        // padding: [45, 10, 10, 0]
      },
      chartGrid: {
        left: '5%',
        right: '3%',
        top: '40%',
        bottom: '5%',
        containLabel: true,
      },
      // 记录每个echart实例
      chartGlobalList: [],
      // 记录用户选择了几个odd
      chartOddGroup: [],
      thumbList: [],
      // 导出pdf预览的列表
      reportChartList: [],
      imgFit: 'contain',
      oddOptions: [],
      oddListValue: [],
      versionListValue: [],
      versionList: [],
      oddUniqueList: [],
      countType: 0,
      chartThunbnailIndex: 0,
      // 初始化的时候从上个页面传进来的参数
      tableId: '',
      project: '',
      userCase: '',
      tableName: '',
      tableDesc: '',
      version: '',
      taskType: 0,
    };
  },
  mounted() {
    this.tableId = this.$route.params.table_id;
    this.project = this.$route.params.project;
    this.userCase = this.$route.params.usercase;
    this.tableName = this.$route.params.table_name;
    this.tableDesc = this.$route.params.table_desc;
    this.version = this.$route.params.version;
    this.taskType = this.$route.params.task_type;
    if (this.taskType > 0) {
      this.objectRatioEnable = false;
    } else {
      this.objectRatioEnable = true;
    }
    this.getVersion();
    this.getOddList();
    this.afterInit();
  },

  watch: {
    thumbList: function(newV, oldV) {
      const that = this;
      if (newV.length > 0) {
        that.showPreview = true;
      } else {
        that.showPreview = false;
      }
    },
  },
  methods: {
    ...mapMutations('d2admin/page', ['keepAliveRemove', 'keepAliveClean']),
    ...mapActions('d2admin/page', ['close']),

    /**
     * 第一次请求页面数据
     * initColumns初始化完成后调用
     * 可以用一个空方法覆盖它，阻止初始化后请求数据
     */
    doLoad() {
      // return this.doRefresh({ from: 'load' })
    },
    /**
     * 把当前的图添加到右侧缩略图列表中
     */
    thunbnailCheckChange(checked, itemId) {
      const result = this.thumbList.filter(item => item.id === itemId);
      if (checked) {
        this.reportChartList = this.reportChartList.concat(result);
      } else {
        this.reportChartList = this.reportChartList.filter(item => item.id !== itemId);
      }
      if (this.reportChartList.length > 0) {
        this.canPreviewReport = false;
      } else {
        this.canPreviewReport = true;
      }
    },

    handleChartLeft(index) {
      const that = this;
      that.chartPreviewVisible = true;
      setTimeout(function() {
        const thirdChart = that.$echarts.init(that.$refs.tc);
        thirdChart.setOption(that.chartOptionsList[index * 2], true);
      }, 350);
    },
    handleChartRight(index) {
      const that = this;
      that.chartPreviewVisible = true;
      setTimeout(function() {
        const thirdChart = that.$echarts.init(that.$refs.tc);
        const options = that.chartOptionsList[index * 2 + 1];
        if (that.oddListValue.length === 1 && that.versionListValue.length === 1) {
          options.series[0].radius = [60, 160];
        }
        thirdChart.setOption(options, true);
      }, 350);
    },
    /**
     * 把当前的图添加到右侧缩略图列表中
     */
    addLeftChartToPool(checked, index) {
      const thumbId = index * 2;
      if (checked) {
        this.showTipLeftValues[index] = true;
        this.addThunbnailChart(thumbId);
      } else {
        this.showTipLeftValues[index] = false;
        this.thumbList = this.thumbList.filter(item => item.id !== thumbId);
      }
    },
    /**
     * 把当前的图添加到右侧缩略图列表中
     */
    addRightChartToPool(checked, index) {
      const thumbId = index * 2 + 1;
      if (checked) {
        this.showTipRightValues[index] = true;
        this.addThunbnailChart(thumbId);
      } else {
        this.showTipRightValues[index] = false;
        this.thumbList = this.thumbList.filter(item => item.id !== thumbId);
      }
    },

    /**
     * 关闭导出PDF弹框
     */
    savePDF() {
      this.exportPDFVisible = false;
    },
    /**
     * 导出PDF
     */
    previewExportPDF() {
      this.exportPDFVisible = true;
    },
    /**
     * 过滤重复odd
     */
    uniqueList(arr) {
      return arr.filter((item, index, arr) => arr.indexOf(item) === index);
    },
    /**
     * 把当前的图添加到右侧缩略图列表中
     */
    addThunbnailChart(index) {
      // 因为每行画了2个chart，所以用索引来得到两个dom元素。
      const fChart = this.chartGlobalList[index];
      this.generThumbnail(fChart, index);
    },
    /**
     * 获取绘图的缩略图
     */
    generThumbnail(chart, index) {
      const that = this;
      setTimeout(function() {
        var baseImage = chart.getDataURL('png');
        const imgItem = {
          id: index,
          url: baseImage,
        };
        that.thumbList.push(imgItem);
      }, 250);
    },
    resetParams() {
      this.oddListValue = [];
      this.versionListValue = [];
      this.countType = 0;
    },
    /**
     * 请求绘图数据
     */
    requestChartData() {
      const that = this;
      // 清空echart DOM 组件容器 div
      that.chartOddGroup = [];
      // 及时的去创建echart 的dom组件
      for (const odditem of that.oddListValue) {
        const chartdiv = {
          odd: odditem,
          disableArr: false,
        };
        that.chartOddGroup.push(chartdiv);
      }
      if (this.oddListValue.length > 0) {
        const requestObj = {};
        requestObj.table_id = this.tableId;
        requestObj.table_name = this.tableName;
        requestObj.count_type = this.countType;
        requestObj.fields = this.oddListValue;
        requestObj.versions = this.versionListValue;
        // 把缩略图源列表清空。
        this.chartGlobalList = [];
        this.chartOptionsList = [];
        this.showTipLeftValues = [];
        api.GetChartData(requestObj).then(ret => {
          if (ret.data.length > 0) {
            if (that.oddListValue.length === 1) {
              if (that.versionListValue.length === 0) {
                // 如果用户不选择版本，需要遍历出来服务器返回的版本信息
                for (const item of ret.data) {
                  const defaultVersionArr = [];
                  for (const ov of item.detail) {
                    defaultVersionArr.push(ov.data_version);
                  }
                  const versionUniqueList = that.uniqueList(defaultVersionArr);
                  that.versionListValue = [].concat(versionUniqueList);
                }
              }
              that.drawOneOddChart(ret);
            } else {
              if (that.versionListValue.length === 0) {
                // 如果用户不选择版本，需要遍历出来服务器返回的版本信息，然后
                for (const item of ret.data) {
                  const defaultVersionArr = [];
                  for (const ov of item.detail) {
                    defaultVersionArr.push(ov.data_version);
                  }
                  const versionUniqueList = that.uniqueList(defaultVersionArr);
                  that.versionListValue = [].concat(versionUniqueList);
                }
              }
              that.drawMultOddChart(ret);
            }
          } else {
            this.$message.success('No record found');
          }
        });
      } else {
        this.$message.error('please choose one odd at least');
      }
    },
    /**
     * 处理odd title过长的问题
     */
    getOddTitle(title) {
      let oddTitle = '';
      if (title.length > 20) {
        const pre = title.substring(0, 8);
        const tail = title.substring(title.length - 8, title.length);
        oddTitle = pre + '...' + tail;
      } else {
        oddTitle = this.oddListValue[0];
      }
      return oddTitle;
    },
    /**
     * 1个odd绘制柱状图
     */
    drawOneOddChart(ret) {
      // 1个odd && 1个version  ==》 一个饼图 + 一个柱状图
      const ctype = this.countType === 0 ? 'Samples' : 'Objects';
      if (this.versionListValue.length === 1) {
        for (const item of ret.data) {
          const firstChart = this.$echarts.init(this.$refs.fc[0]);
          // console.log('init type111: ',JSON.stringify(firstChart))
          const secondChart = this.$echarts.init(this.$refs.sc[0]);
          const oddArrValues = [];
          // 每个odd对应的数组
          for (const ov of item.detail) {
            // 把所有odd_value 放进一个数组
            oddArrValues.push(ov.odd_value);
          }
          // 对odd_value 放进一个数组去重
          const oddUniqueList = this.uniqueList(oddArrValues);
          const map = this.getChartMap(this.versionListValue, oddUniqueList, item.detail, false);
          const title = '#' + ctype + ' comparison ' + this.getOddTitle(this.oddListValue[0]);
          this.drawBarChart(firstChart, map, title, 'X-axis = version');
          this.showTipLeftValues.push(false);
          const mapSecond = this.getChartMap(
            this.versionListValue,
            oddUniqueList,
            item.detail,
            false,
          );
          const titleRose =
            this.getOddTitle(this.oddListValue[0]) +
            ' types proportion version ' +
            this.versionListValue[0];
          this.drawRosePieChart(secondChart, mapSecond, titleRose);
          this.chartGlobalList.push(firstChart);
          this.chartGlobalList.push(secondChart);
          this.showTipRightValues.push(false);
        }
      } else {
        // 1个odd && 多个version ==》两个柱状图（一个是比较同一version下的odd值，一个是比较同一odd下的version）
        for (const item of ret.data) {
          const firstChart = this.$echarts.init(this.$refs.fc[0]);
          const secondChart = this.$echarts.init(this.$refs.sc[0]);
          const oddArrValues = [];
          for (const ov of item.detail) {
            oddArrValues.push(ov.odd_value);
          }
          // 对odd_value 放进一个数组去重
          const oddUniqueList = this.uniqueList(oddArrValues);
          const title = '#' + ctype + ' comparison ' + this.getOddTitle(this.oddListValue[0]);
          const map = this.getChartMap(this.versionListValue, oddUniqueList, item.detail, false);
          this.drawBarChartOneOdd(
            firstChart,
            this.versionListValue,
            map,
            title,
            'Legend = version',
          );
          this.showTipLeftValues.push(false);
          const mapSecond = this.getChartMap(
            oddUniqueList,
            this.versionListValue,
            item.detail,
            true,
          );
          this.drawBarChartOneOddInverse(
            secondChart,
            oddUniqueList,
            mapSecond,
            title,
            'X-axis = version',
          );
          this.showTipRightValues.push(false);
          this.chartGlobalList.push(firstChart);
          this.chartGlobalList.push(secondChart);
        }
      }
    },
    /**
     * 多个odd绘制柱状图
     */
    drawMultOddChart(ret) {
      // 多个odd ==》odd数量 * 两个柱状图（一个是比较同一version下的odd值，一个是比较同一odd下的version）
      let oddIndex = 0;
      const ctype = this.countType === 0 ? 'Samples' : 'Objects';
      for (const item of ret.data) {
        const oddArrValues = [];
        const firstChart = this.$echarts.init(this.$refs.fc[oddIndex]);
        const secondChart = this.$echarts.init(this.$refs.sc[oddIndex]);
        for (const ov of item.detail) {
          oddArrValues.push(ov.odd_value);
        }
        const oddUniqueList = this.uniqueList(oddArrValues);
        const title = '#' + ctype + ' comparison ' + this.oddListValue[oddIndex];
        const map = this.getChartMap(this.versionListValue, oddUniqueList, item.detail, false);
        this.drawBarChartOneOdd(firstChart, this.versionListValue, map, title, 'Legend = version');
        const mapSecond = this.getChartMap(oddUniqueList, this.versionListValue, item.detail, true);
        this.drawBarChartOneOddInverse(
          secondChart,
          oddUniqueList,
          mapSecond,
          title,
          'X-axis = version',
        );
        oddIndex++;
        this.chartGlobalList.push(firstChart);
        this.chartGlobalList.push(secondChart);
      }
    },
    /**
     * 获取odd列表
     */
    getOddList() {
      const that = this;
      const query = {};
      query.table_id = that.tableId;
      return api.GetOddList(query).then(ret => {
        for (const item of ret.data.data) {
          that.oddOptions.push(item.field_name);
        }
      });
    },
    /**
     * 获取版本列表
     */
    getVersion() {
      const that = this;
      const query = {};
      query.table_id = that.tableId;
      return api.GetVersion(query).then(ret => {
        if (that.versionList.length <= 0) {
          for (const item of ret.data.data) {
            that.versionList.push(item);
          }
        }
      });
    },
    /**
     * 获取每个odd对应的数值
     */
    getChartMap(outerList, innerList, globalGroupArr, inverse) {
      const oddVersionMap = new Map();
      // 遍历左侧Y轴的维度 例如 v4,5,6
      for (const version of outerList) {
        // // 遍历X轴的纬度 例如 cloudy, windy,car-park
        var iterateCount = 0;
        for (const oddEnum of innerList) {
          if (inverse) {
            iterateCount = this.searchCountFromGoup(oddEnum, version, globalGroupArr);
          } else {
            iterateCount = this.searchCountFromGoup(version, oddEnum, globalGroupArr);
          }

          const array = oddVersionMap.get(oddEnum + '');

          // 如果key没有对应的数组，新建一个加进去
          if (typeof array === 'undefined') {
            const tempArr = [];
            tempArr.push(iterateCount);
            oddVersionMap.set(oddEnum + '', tempArr);
          } else {
            array.push(iterateCount);
          }
        }
      }
      return oddVersionMap;
    },
    /**
     *  绘制柱状图
     */
    drawBarChart: function(myChart, oddVersionMap, title, subTitle) {
      var xAixes = [].concat(this.versionListValue);
      const seriesArr = [];
      var oddValuesArr = [];
      oddValuesArr.push('product');
      oddVersionMap.forEach((value, key) => {
        oddValuesArr.push(key);
        xAixes.push(value);
        const seriesObj = {
          type: 'bar',
          barMaxWidth: '20%',
          itemStyle: {
            normal: {
              label: {
                show: true, // 开启显示
                position: 'top', // 在上方显示
                formatter: function(params) {
                  if (params.value[params.seriesIndex + 1] === 0) {
                    return '';
                  } else {
                    return params.value[params.seriesIndex + 1];
                  }
                },
                textStyle: this.chartTitleStyle,
              },
            },
          },
        };
        seriesArr.push(seriesObj);
      });
      const options = {
        title: {
          text: title,
          subtext: subTitle,
          left: 'center',
          textStyle: this.chartTitleStyle,
        },
        tooltip: {},
        legend: this.chartLegend,
        color: this.chartColOneColor,
        grid: this.chartGrid,
        dataset: {
          source: [oddValuesArr, xAixes],
        },
        xAxis: { type: 'category' },
        yAxis: {},
        series: seriesArr,
      };
      myChart.setOption(options, true);
      this.chartOptionsList.push(options);
    },
    /**
     * 绘制南丁格尔玫瑰图
     */
    drawRosePieChart(myChart, oddVersionMap, title) {
      var xAixes = [];
      xAixes = xAixes.concat(this.versionListValue);
      const seriesArr = [];
      oddVersionMap.forEach((valueStr, key) => {
        const seriesObj = {
          name: key,
          value: valueStr,
          label: {
            normal: {
              show: true,
              formatter: '{b}:{c}' + '\n\r' + '({d}%)',
            },
          },
        };
        seriesArr.push(seriesObj);
      });
      const options = {
        title: {
          text: title,
          left: 'center',
          textStyle: this.chartTitleStyle,
        },
        legend: this.chartLegend,
        color: this.chartColTwoColor,
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)',
        },
        series: [
          {
            name: 'Version ' + xAixes[0],
            type: 'pie',
            radius: [30, 80],
            center: ['50%', '60%'],
            roseType: 'pie',
            itemStyle: {
              borderRadius: 4,
            },
            data: seriesArr,
          },
        ],
      };
      myChart.setOption(options, true);
      this.chartOptionsList.push(options);
    },
    /**
     *  绘制柱状图
     */
    drawBarChartOneOdd(myChart, legendList, oddVersionMap, title, subTitle) {
      const sourceArr = [];
      // 这里有可能是数字类型的legend，需要转成字符串，否则显示有问题。
      var stringOddArr = legendList.map(function(element) {
        return element.toString();
      });
      var legendArr = ['product'].concat(stringOddArr);

      const seriesObj = {
        type: 'bar',
        barMaxWidth: '30%',
        itemStyle: {
          normal: {
            label: {
              show: true, // 开启显示
              position: 'top', // 在上方显示
              formatter: function(params) {
                if (params.value[params.seriesIndex + 1] === 0) {
                  return '';
                } else {
                  // return params.seriesName + ':' + params.value[params.seriesIndex + 1]
                  return params.value[params.seriesIndex + 1];
                }
              },
              textStyle: this.chartTitleStyle,
            },
          },
        },
      };
      const seriesArr = new Array(legendList.length).fill(seriesObj);

      sourceArr.push(legendArr);
      oddVersionMap.forEach((value, key) => {
        var xAixes = [];
        xAixes.push(key);
        xAixes = xAixes.concat(value);
        sourceArr.push(xAixes);
      });
      const options = {
        title: {
          text: title,
          subtext: subTitle,
          left: 'center',
          textStyle: this.chartTitleStyle,
        },
        tooltip: {},
        legend: this.chartLegend,
        color: this.chartColOneColor,
        grid: this.chartGrid,
        dataset: {
          source: sourceArr,
        },
        xAxis: { type: 'category' },
        yAxis: {},
        series: seriesArr,
      };
      myChart.setOption(options, true);
      this.chartOptionsList.push(options);
    },
    /**
     *  绘制柱状图
     */
    drawBarChartOneOddInverse(myChart, legendList, oddVersionMap, title, subTitle) {
      const sourceArr = [];
      var stringOddArr = legendList.map(function(element) {
        return element.toString();
      });
      var legendArr = ['product'].concat(stringOddArr);
      const seriesObj = {
        type: 'bar',
        barMaxWidth: '30%',
        itemStyle: {
          normal: {
            label: {
              show: true,
              position: 'top',
              formatter: function(params) {
                if (params.value[params.seriesIndex + 1] === 0) {
                  return '';
                } else {
                  return params.value[params.seriesIndex + 1];
                }
              },
              textStyle: this.chartTitleStyle,
            },
          },
        },
      };
      const seriesArr = new Array(legendList.length).fill(seriesObj);
      sourceArr.push(legendArr);
      oddVersionMap.forEach((value, key) => {
        var xAixes = [];
        xAixes.push(key);
        xAixes = xAixes.concat(value);
        sourceArr.push(xAixes);
      });
      const options = {
        title: {
          text: title,
          subtext: subTitle,
          left: 'center',
          textStyle: this.chartTitleStyle,
        },
        tooltip: {},
        color: this.chartColTwoColor,
        legend: this.chartLegend,
        grid: this.chartGrid,
        dataset: {
          source: sourceArr,
        },
        xAxis: { type: 'category' },
        yAxis: {},
        series: seriesArr,
      };
      myChart.setOption(options, true);
      this.chartOptionsList.push(options);
    },
    /**
     * 获取每个odd的数值
     */
    searchCountFromGoup(version, oddEnum, groupArray) {
      let count = 0;
      for (const item of groupArray) {
        if (item.data_version === version && item.odd_value === oddEnum) {
          count = item.count;
        }
      }
      return count;
    },
    /**
     *  关闭当前页面
     */
    handleCloseCurrent() {
      this.close({
        tagName: this.$route.fullPath,
      });
    },
    /**
     *  隐藏表格
     */
    afterInit() {
      this.crud.options.hide = true;
    },
    /**
     *  获取表格配置
     */
    getCrudOptions() {
      return crudOptions(this);
    },
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
.topleft-info {
  margin-right: 5px;
  padding: 20px;
  /*border-radius: 5px 5px 5px 5px;*/
  /*border-style: solid;*/
  /*border-width: 1px;*/
  /*border-color: #ddd*/
}

.drawer-class.el-drawer {
  .el-drawer__header {
    background-color: #f5f5f5;
    height: 50px;
    color: #000000;
    margin-bottom: 0px;
  }

  .el-drawer__body {
    /*background-color: #ecf1f5;*/
    background-color: white;
    padding: 0px;
  }
}

// 这里重置dialog 的布局
::v-deep .el-dialog__body {
  padding: 1px;
}

::v-deep .el-dialog {
  padding: 0 20px 20px 20px;
  border-radius: 18px;
}

::v-deep .el-dialog__title {
  /*display: none;*/
  line-height: 14px;
  font-size: 22px;
  color: #333;
}

::v-deep .el-dialog__wrapper {
  background-color: rgba(0, 0, 0, 0.2);
}

.dialog-left-title {
  margin-bottom: 20px;
}

.select-filter {
  width: 450px;
}

.plabel {
  margin-bottom: 10px;
}

.dialog-tab-title {
  margin-bottom: 10px;
  font-size: 25px;
  color: #46a0fb;
}

.ptitle {
  margin-bottom: 4px;
  font-weight: bold;
  line-height: 15px;
  font-size: 20px;
}

.pcontent {
  font-size: 20px;
}

.ptitle-left {
  margin-bottom: 5px;
  font-weight: bold;
  margin-right: 5px;
}

.preview-footer {
  width: 100%;
  margin-top: 3%;
  text-align: center;
}

.el-image {
  width: 140px;
  height: 100px;
  background-color: whitesmoke;
}

.preview-chart {
  text-align: center;
  align-items: center;
  padding: 0px;
}

.thunbnail-item {
  margin: 0 auto;
  width: 200px;
  display: flex;
  padding: 10px 5px 10px 5px;
  text-align: center;
  align-items: center;
  margin-bottom: 10px;
  border-radius: 5px;
}

.div-side {
  height: 100%;
  width: 100%;
  background-color: white;
  padding: 10px;
  border-radius: 5px 0px 0px 5px;
}

.div-thunbnail {
  display: flex;
  width: 10%;
  height: 240px;
  justify-content: center;
  align-items: center;
}

.footer {
  /*border-style: solid;*/
  /*border-color: #ddd;*/
  /*border-width: 1px;*/
  /*border-radius: 5px 5px 0px 0px;*/
  width: 100%;
  margin-top: 10px;
  /*background-color: #ecf1f5;*/
  background-color: white;
  padding: 10px 10px 20px 10px;
}

.btn-close {
  position: absolute;
  right: -10px;
  top: -10px;
}

.chart-cart {
  position: absolute;
  right: 70px;
  bottom: 40px;
  width: 20px;
  height: 20px;
}

.chart-container {
  width: 100%;
  height: 600px;
}

.chart-main {
  height: 300px;
  width: 100%;
  padding: 5px;
}

.checkbox-div {
  position: absolute;
  top: 20px;
  right: 20px;
}

.chart-parentl,
.chart-parentr {
  display: flex;
  align-items: center;
  background-color: #ecf1f5;
  margin-right: 7.5px;
  margin-bottom: 15px;
  width: 50%;
  border-radius: 5px;
  padding-top: 5px;
  position: relative;
}

.chartcol-one {
  width: 85%;
  height: 270px;
}

.chartcol-third {
  width: 100%;
  height: 100%;
}

.div-tableinfo {
}

.div-tableinfo p {
  /*margin-bottom: 5px;*/
  font-weight: bold;
  line-height: 28px;
  margin-left: 20px;
  margin-right: 5px;
}

.div-tableinfo span {
  line-height: 28px;
}

.div-tableinfo div {
  display: flex;
}

.div-filter {
  width: 70%;
  height: 100%;
  padding: 10px;
  background-color: white;
  border-radius: 5px 5px 5px 5px;
}

.div-chartparams {
  display: flex;
  height: 100%;
  width: 100%;
  border-radius: 5px 5px 0px 0px;
}

.drawer-class {
  padding: 1px;
}

.div-commit {
  padding-left: 410px;
}

label.xrequired:before {
  content: '* ';
  color: red;
}
.form-label {
  display: inline-block;
  width: 390px;
}

.grey_line_pre {
  height: 100%;
  border-left: 1px solid #dddddd;
  text-align: center;
}

.grey_line {
  height: 1px;
  border-top: 1px solid #ddd;
  text-align: center;
  margin-bottom: 10px;
}

.div-root {
  display: flex;
  width: 100%;
  height: 100%;
  background: white;
  padding: 20px;
}
</style>
