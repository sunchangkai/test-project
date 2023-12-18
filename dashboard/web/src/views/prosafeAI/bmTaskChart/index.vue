<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x ref="d2Crud" :data="data" :columns="crud.columns" :options="crud.options">
      <template slot="body">
        <div class="div-root">
          <!--            Task 信息布局-->
          <el-container class="chart-container">
            <el-main class="chart-main">
              <div class="task-info">
                <el-collapse v-model="activeNames" style="border:none;margin-left:20px;">
                  <el-collapse-item name="1">
                    <span class="collapse-title" slot="title">Task Info</span>

                    <div class="div-tableinfo">
                      <div>
                        <p>
                          Model path: <span class="pcontent">{{ modelPath }}</span>
                        </p>
                      </div>
                      <div>
                        <p>
                          Data path: <span class="pcontent">{{ dataPath }}</span>
                        </p>
                      </div>
                      <div>
                        <p>
                          Machine info: <span class="pcontent">{{ mechineInfo }}</span>
                        </p>
                      </div>
                      <div>
                        <p>
                          Task description: <span class="pcontent">{{ taskDesc }}</span>
                        </p>
                      </div>
                    </div>
                  </el-collapse-item>
                </el-collapse>

                <div style="padding: 0 20px 20px 20px">
                  <el-tabs v-model="activeName" @tab-click="handleTabClick" stretch>
                    <el-tab-pane label="Basic Metrics" name="basic">
                      <div>
                        <div class="form-item" v-if="isObjDet">
                          <p class="item-label">Choose IoU:</p>
                          <el-input-number
                            v-model="iou"
                            :precision="2"
                            :min="0.5"
                            :max="0.95"
                            :step="0.05"
                          ></el-input-number>
                        </div>
                        <div
                          style="height: 7vh;display: flex;flex-direction: row;align-items: center"
                        >
                          <p class="choose-label">Choose the metrics:</p>
                          <template v-if="!isObjDet">
                            <el-checkbox
                              label="accuracy"
                              v-model="accCb"
                              style="margin-right: 10px;margin-left: 10px"
                            ></el-checkbox>
                            <el-select
                              v-model="accAlg"
                              placeholder="please choose"
                              class="select-alg"
                              :disabled="!accCb"
                            >
                              <el-option
                                v-for="item in accAlgArr"
                                :key="item"
                                :label="item"
                                :value="item"
                              >
                              </el-option>
                            </el-select>
                          </template>

                          <el-checkbox
                            label="precision"
                            v-model="preCb"
                            style="margin-right: 10px;margin-left: 10px"
                          ></el-checkbox>
                          <el-select
                            v-model="preAlg"
                            placeholder="please choose"
                            class="select-alg"
                            :disabled="!preCb"
                          >
                            <el-option
                              v-for="item in algsArr"
                              :key="item"
                              :label="item"
                              :value="item"
                            >
                            </el-option>
                          </el-select>

                          <el-checkbox
                            label="recall"
                            v-model="recallCb"
                            style="margin-right: 10px;margin-left: 10px"
                          ></el-checkbox>
                          <el-select
                            v-model="recallAlg"
                            placeholder="please choose"
                            class="select-alg"
                            :disabled="!recallCb"
                          >
                            <el-option
                              v-for="item in algsArr"
                              :key="item"
                              :label="item"
                              :value="item"
                            >
                            </el-option>
                          </el-select>
                          <el-checkbox
                            label="f1-score"
                            v-model="f1Cb"
                            style="margin-right: 10px;margin-left: 10px"
                          ></el-checkbox>
                          <el-select
                            v-model="f1Alg"
                            placeholder="please choose"
                            class="select-alg"
                            :disabled="!f1Cb"
                          >
                            <el-option
                              v-for="item in algsArr"
                              :key="item"
                              :label="item"
                              :value="item"
                            >
                            </el-option>
                          </el-select>
                          <el-checkbox
                            v-if="isObjDet"
                            label="MAP"
                            v-model="mapCb"
                            style="margin-right: 10px;margin-left: 10px"
                          ></el-checkbox>

                          <el-button
                            style="margin-left: 15px"
                            type="success"
                            @click="requestBasicChart"
                            round
                            >Confirm
                          </el-button>
                        </div>

                        <div
                          style="width: 100%;height: 250px;margin:0px 10px 0 10px;display: flex;flex-direction: row; justify-content: center;"
                        >
                          <div
                            v-for="item in metricsCheckList"
                            :key="item"
                            style="width: 20%;height: 200px;margin:0px 10px 0 10px;"
                          >
                            <div :ref="'fc'" class="chartcol-one"></div>
                          </div>
                        </div>
                        <div
                          v-if="showHeatMap"
                          style="width: 100%;height: 380px;margin:0px 10px 0 10px;"
                        >
                          <div :ref="'hc'" class="heat-one"></div>
                        </div>
                      </div>
                    </el-tab-pane>

                    <el-tab-pane label="Basic Metrics on Different Slices" name="slice">
                      <div>
                        <template v-if="isObjDet">
                          <div class="form-item">
                            <p class="item-label">Slicing by:</p>
                            <el-radio v-model="slicingType" label="0">Class</el-radio>
                            <el-radio v-model="slicingType" label="1">ODD dimension</el-radio>
                          </div>
                          <div style="display: flex;">
                            <div class="form-item" style="width: 410px;">
                              <template v-if="slicingType == '0'">
                                <p class="item-label">
                                  Choose one class:
                                </p>
                                <el-select
                                  class="select-filter"
                                  v-model="selectedCls"
                                  default-first-option
                                >
                                  <el-option
                                    v-for="item in classList"
                                    :key="item.idx"
                                    :label="item.category"
                                    :value="item.idx"
                                  ></el-option>
                                </el-select>
                              </template>
                              <template v-if="slicingType == '1'">
                                <p class="item-label">
                                  Choose one ODD domension:
                                </p>
                                <el-select
                                  class="select-filter"
                                  v-model="selctedOdd"
                                  default-first-option
                                  placeholder="please choose odd"
                                >
                                  <el-option
                                    v-for="item in oddOptions"
                                    :key="item"
                                    :label="item"
                                    :value="item"
                                  ></el-option>
                                </el-select>
                              </template>
                            </div>
                            <div class="form-item" style="margin-left: 8px;">
                              <p class="item-label">Choose IoU:</p>
                              <el-input-number
                                v-model="slicingIou"
                                :precision="2"
                                :min="0.5"
                                :max="0.95"
                                :step="0.05"
                              ></el-input-number>
                            </div>
                          </div>
                        </template>

                        <div style="margin-bottom: 10px;" v-if="!isObjDet">
                          <span class="choose-label">Choose the ODD dimension or label: </span>
                          <el-select
                            class="select-filter"
                            v-model="oddListValue"
                            size="medium"
                            default-first-option
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

                        <div
                          style="height: 7vh;display: flex;flex-direction: row;align-items: center"
                        >
                          <p class="choose-label">Choose the metrics:</p>

                          <template v-if="!isObjDet">
                            <el-checkbox
                              label="accuracy"
                              v-model="accSliceCb"
                              style="margin-right: 10px;margin-left: 10px"
                            ></el-checkbox>
                            <el-select
                              v-model="accSliceAlg"
                              placeholder="please choose"
                              class="select-alg"
                              :disabled="!accSliceCb"
                            >
                              <el-option
                                v-for="item in accAlgArr"
                                :key="item"
                                :label="item"
                                :value="item"
                              >
                              </el-option>
                            </el-select>
                          </template>

                          <el-checkbox
                            label="precision"
                            v-model="preSliceCb"
                            style="margin-right: 10px;margin-left: 10px"
                          ></el-checkbox>
                          <el-select
                            v-model="preSliceAlg"
                            placeholder="please choose"
                            class="select-alg"
                            :disabled="!preSliceCb"
                          >
                            <el-option
                              v-for="item in algsArr"
                              :key="item"
                              :label="item"
                              :value="item"
                            >
                            </el-option>
                          </el-select>

                          <el-checkbox
                            label="recall"
                            v-model="recallSliceCb"
                            style="margin-right: 10px;margin-left: 10px"
                          ></el-checkbox>
                          <el-select
                            v-model="recallSliceAlg"
                            placeholder="please choose"
                            class="select-alg"
                            :disabled="!recallSliceCb"
                          >
                            <el-option
                              v-for="item in algsArr"
                              :key="item"
                              :label="item"
                              :value="item"
                            >
                            </el-option>
                          </el-select>
                          <el-checkbox
                            label="f1-score"
                            v-model="f1SliceCb"
                            style="margin-right: 10px;margin-left: 10px"
                          ></el-checkbox>
                          <el-select
                            v-model="f1SliceAlg"
                            placeholder="please choose"
                            class="select-alg"
                            :disabled="!f1SliceCb"
                          >
                            <el-option
                              v-for="item in algsArr"
                              :key="item"
                              :label="item"
                              :value="item"
                            >
                            </el-option>
                          </el-select>
                          <el-checkbox
                            v-if="isObjDet && slicingType == '0'"
                            label="AP"
                            v-model="apSliceCb"
                            style="margin: 0 10px;"
                          ></el-checkbox>
                          <el-checkbox
                            v-if="isObjDet && slicingType == '1'"
                            label="MAP"
                            v-model="mapSliceCb"
                            style="margin: 10px;"
                          ></el-checkbox>

                          <el-button
                            style="margin-left: 15px"
                            type="success"
                            @click="requestSliceChart"
                            round
                            >Confirm
                          </el-button>
                        </div>

                        <!--                        <div style="height: 40vh;display: flex;flex-direction: column;">-->
                        <div
                          v-if="!!classMetricsCheckList.length"
                          style="width: 100%;height: 250px;margin:0px 10px 0 10px;display: flex;flex-direction: row; justify-content: center;"
                        >
                          <div
                            v-for="item in classMetricsCheckList"
                            :key="item"
                            style="width: 20%;height: 200px;margin:0px 10px 0 10px;"
                          >
                            <div :ref="'ringChart'" class="chartcol-one"></div>
                          </div>
                        </div>
                        <div
                          v-if="isObjDet && slicingType == '0'"
                          style="width: 100%;height: 292px;margin:0px 10px 0 10px;"
                        >
                          <div :ref="'classAreaChart'" style="width: 100%;height: 100%"></div>
                        </div>

                        <div
                          v-if="!(isObjDet && slicingType == '0')"
                          style="width: 100%;height: 290px;margin:0px 10px 0 10px;"
                        >
                          <div :ref="'sliceChart'" style="width: 100%;height: 100%"></div>
                        </div>

                        <div
                          v-show="showSliceHeatMap"
                          style="width: 100%;height: 380px;margin:0px 10px 0 10px;"
                        >
                          <div>
                            <span>Choose the odd value you want to view: </span>
                            <el-select
                              class="select-filter"
                              v-model="heatMapOddValue"
                              size="medium"
                              default-first-option
                              placeholder="please choose value"
                              @change="heatOddValueChange"
                            >
                              <el-option
                                v-for="item in oddValuesOptions"
                                :key="item"
                                :label="item"
                                :value="item"
                              ></el-option>
                            </el-select>
                          </div>

                          <div>
                            <div :ref="'heatsc'" class="heat-one"></div>
                          </div>
                        </div>
                        <!--                        </div>-->
                      </div>
                    </el-tab-pane>
                  </el-tabs>
                </div>
              </div>
            </el-main>
          </el-container>
        </div>
      </template>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api';
import { crudOptions } from './crud';
import { d2CrudPlus } from 'd2-crud-plus';
import { mapMutations, mapActions } from 'vuex';
import * as robTestApi from '../robustnessTestingResults/api';

export default {
  name: 'taskChart',
  mixins: [d2CrudPlus.crud],

  data: function() {
    return {
      data: [],
      activeNames: [],
      accDisable: true,

      iou: 0.5,
      accCb: false,
      mapCb: false,
      preCb: false,
      recallCb: false,
      f1Cb: false,
      accAlg: 'balance',
      preAlg: 'weighted',
      recallAlg: 'weighted',
      f1Alg: 'weighted',

      slicingType: '0',
      slicingIou: 0.5,
      selectedCls: '',
      selctedOdd: '',
      accSliceCb: false,
      preSliceCb: false,
      recallSliceCb: false,
      f1SliceCb: false,
      mapSliceCb: false,
      apSliceCb: false,
      accSliceAlg: 'balance',
      preSliceAlg: 'weighted',
      recallSliceAlg: 'weighted',
      f1SliceAlg: 'weighted',

      accAlgArr: ['balance', 'total'],
      algsArr: ['macro', 'micro', 'weighted'],
      oddValuesOptions: [],
      metricsCheckList: [],
      classMetricsCheckList: [],
      metricsSliceCheckList: [],
      activeName: 'basic',
      // 缓存用户勾选的计算标准
      chooseSliceCache: [],

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

      chartLegend: {
        orient: 'horizontal',
        left: '8%',
        top: '6%',
      },

      chartGrid: {
        left: '5%',
        right: '5%',
        top: '20%',
        bottom: '15%',
        containLabel: true,
      },

      oddOptions: [],
      classList: [],
      oddListValue: [],
      heatMapOddValue: [],

      // 初始化的时候从上个页面传进来的参数
      taskId: '',
      tableId: '',
      modelPath: '',
      dataPath: '',
      mechineInfo: '',
      taskDesc: '',
      runId: '',
      algType: '',

      // 缓存热力图的map
      basicChartsCache: [],
      sliceChartsCache: [],
      sliceHeatChartsCache: [],

      showHeatMap: false,
      showSliceHeatMap: false,
      heatChartMap: new Map(),
      heatChartLabels: [],

      // 记录从哪里跳过来的
      prePath: '',
      preTaskId: '',
      parentName: '',
    };
  },
  mounted() {
    this.runId = this.$route.query.id;
    this.tableId = this.$route.query.table_id;
    this.taskId = this.$route.query.task_id;
    this.parentName = this.$route.query.parent_name;
    this.algType = this.$route.query.algorithm_type;
    this.modelPath = this.$route.query.model_path == null ? 'null' : this.$route.query.model_path;
    this.dataPath = this.$route.query.data_path == null ? 'null' : this.$route.query.data_path;
    this.mechineInfo =
      this.$route.query.machine_info == null ? 'null' : this.$route.query.machine_info;
    this.taskDesc = this.$route.query.task_desc == null ? 'null' : this.$route.query.task_desc;
    this.afterInit();
    this.getOddList();
    this.getClassList();
  },

  watch: {},
  methods: {
    ...mapMutations('d2admin/page', ['keepAliveRemove', 'keepAliveClean']),
    ...mapActions('d2admin/page', ['close']),

    /**
     * 第一次请求页面数据
     * initColumns初始化完成后调用
     * 可以用一个空方法覆盖它，阻止初始化后请求数据
     */
    doLoad() {},

    handleTabClick() {},
    getClassList() {
      robTestApi.getRunLabels({ run_id: this.runId }).then(({ data }) => {
        this.classList = data;
        this.selectedCls = data[0].idx;
      });
    },
    /**
     * 过滤重复odd
     */
    uniqueList(arr) {
      return arr.filter((item, index, arr) => arr.indexOf(item) === index);
    },
    noParamsToast() {
      this.$message.warning('please choose one metrics at least');
    },
    /**
     * 请求绘图所需的数据
     */
    requestBasicChart() {
      const hasObjDetParams = this.preCb || this.recallCb || this.f1Cb || this.mapCb;
      const hasClassifyParams = this.accCb || this.preCb || this.recallCb || this.f1Cb;
      if (this.isObjDet && !hasObjDetParams) {
        return this.noParamsToast();
      } else if (!this.isObjDet && !hasClassifyParams) {
        return this.noParamsToast();
      }
      // todo
      this.releaseBasicRes();
      // 提前创建chart DOM 容器。否则会报错。
      const that = this;
      const query = {};
      query.run_id = that.runId;
      // todo 并且是 basic 的时候 才加iou参数
      if (this.isObjDet) {
        query.iou = this.iou;
      }
      const detail = [];
      if (this.accCb) {
        const obj = {
          metrics: 'accuracy',
          average: this.accAlg,
        };
        detail.push(obj);
      }

      if (this.preCb) {
        const obj = {
          metrics: 'precision',
          average: this.preAlg,
        };
        detail.push(obj);
      }
      if (this.recallCb) {
        const obj = {
          metrics: 'recall',
          average: this.recallAlg,
        };
        detail.push(obj);
      }
      if (this.f1Cb) {
        const obj = {
          metrics: 'f1score',
          average: this.f1Alg,
        };
        detail.push(obj);
      }
      if (this.mapCb) {
        const obj = {
          metrics: 'mAP',
        };
        detail.push(obj);
      }

      query.detail = detail;
      api.GetBasicChart(query).then(ret => {
        if (ret.data.length === 0) {
          that.$message('No matching data');
        } else {
          that.drawBasicChart(ret.data);
        }
      });
    },

    /**
     * 释放所有echart实例
     */
    releaseChart(list) {
      for (const i of list) {
        i.clear();
        i.dispose();
      }
    },
    /**
     * 重置basic 图表用到的资源
     */
    releaseBasicRes() {
      this.releaseChart(this.basicChartsCache);
      this.showHeatMap = true;
      this.metricsCheckList = [];
      if (!this.isObjDet && this.accCb) {
        this.metricsCheckList.push('accuracy');
      }
      if (this.preCb) {
        this.metricsCheckList.push('precision');
      }
      if (this.recallCb) {
        this.metricsCheckList.push('recall');
      }
      if (this.f1Cb) {
        this.metricsCheckList.push('f1-score');
      }
      if (this.isObjDet && this.mapCb) {
        this.metricsCheckList.push('map');
      }
    },
    /**
     * 重置slice 图表用到的资源
     */
    releaseSliceRes() {
      this.releaseChart(this.sliceChartsCache);
      this.releaseChart(this.sliceHeatChartsCache);
      this.heatChartMap.clear();
      this.heatChartLabels = [];
      this.classMetricsCheckList = [];
      this.chooseSliceCache = [];
      this.chooseSliceCache = [].concat(this.metricsSliceCheckList);
      if (this.isObjDet && this.slicingType === '0') {
        if (this.preSliceCb) {
          this.classMetricsCheckList.push('precision');
        }
        if (this.recallSliceCb) {
          this.classMetricsCheckList.push('recall');
        }
        if (this.f1SliceCb) {
          this.classMetricsCheckList.push('f1-score');
        }
        if (this.apSliceCb) {
          this.classMetricsCheckList.push('ap');
        }
      }
    },
    /**
     * 请求绘图数据
     */
    requestSliceChart() {
      const hasObjDetParams =
        this.preSliceCb ||
        this.recallSliceCb ||
        this.f1SliceCb ||
        (this.slicingType === '0' && this.apSliceCb) ||
        (this.slicingType === '1' && this.mapSliceCb);
      const hasClassifyParams =
        this.accSliceCb || this.preSliceCb || this.recallSliceCb || this.f1SliceCb;
      if (this.isObjDet && !hasObjDetParams) {
        return this.noParamsToast();
      } else if (!this.isObjDet && !hasClassifyParams) {
        return this.noParamsToast();
      }

      this.heatMapOddValue = '';
      this.releaseSliceRes();
      const detail = [];
      if (this.accSliceCb) {
        const obj = {
          metrics: 'accuracy',
          average: this.accSliceAlg,
        };
        detail.push(obj);
      }
      if (this.preSliceCb) {
        const obj = {
          metrics: 'precision',
          average: this.preSliceAlg,
        };
        detail.push(obj);
      }
      if (this.recallSliceCb) {
        const obj = {
          metrics: 'recall',
          average: this.recallSliceAlg,
        };
        detail.push(obj);
      }
      if (this.f1SliceCb) {
        const obj = {
          metrics: 'f1score',
          average: this.f1SliceAlg,
        };
        detail.push(obj);
      }
      // todo 对接口参数
      if (this.slicingType === '0' && this.apSliceCb) {
        detail.push({
          metrics: 'AP',
        });
      }
      if (this.slicingType === '1' && this.mapSliceCb) {
        detail.push({
          metrics: 'mAP',
        });
      }
      const objDetFields = this.slicingType === '0' ? [this.selectedCls] : [this.selctedOdd];

      const query = {
        run_id: this.runId,
        detail: detail,
        fields: this.isObjDet ? objDetFields : [].concat(this.oddListValue),
        field_type: this.isObjDet ? this.slicingType : null,
        iou: this.slicingIou,
      };
      api.GetSliceChart(query).then(ret => {
        if (ret.data.length === 0) {
          this.$message('No matching data');
        } else {
          if (!this.isObjDet) {
            this.showSliceHeatMap = true;
          }
          this.drawOneOddChart(ret.data);
        }
      });
    },

    heatOddValueChange(val) {
      this.releaseChart(this.sliceHeatChartsCache);
      const data = this.heatChartMap.get(val);
      this.drawHeatMap(val, this.heatChartLabels, data);
    },

    drawRingsPart(ret, source, container) {
      for (let i = 0; i < source.length; i++) {
        const itemOne = ret[i];
        const firstChart = this.$echarts.init(this.$refs[container][i]);
        let colorStr = 'rgba(63,158,255,0.5)'; // RGB(64,158,255)
        if (i === 1) {
          colorStr = 'rgba(245,108,108,0.5)'; // RGB(245,108,108)
        } else if (i === 2) {
          colorStr = 'rgba(114,198,72,0.5)'; // RGB(114,198,72)
        } else if (i === 3) {
          colorStr = 'rgba(255,192,0,0.5)'; // RGB(255,192,0)
        }
        let name = itemOne.metrics;
        if (itemOne.average) {
          name += '(' + itemOne.average + ')';
        }
        this.drawRingChart(firstChart, name, this.formatPercent(itemOne.value), colorStr);
        this.basicChartsCache.push(firstChart);
      }
    },

    /**
     * 绘制每个维度的图表。
     */
    drawBasicChart(ret) {
      const ringsCount = ret.length - 1;
      this.drawRingsPart(ret, this.metricsCheckList, 'fc');
      const heatObj = ret[ringsCount];
      const myChart = this.$echarts.init(this.$refs.hc);
      this.basicChartsCache.push(myChart);

      if (!this.isObjDet) {
        this.drawBisceHeat(myChart, heatObj);
      }
    },
    /**
     * 每个维度画3个圆环图。
     */
    drawRingChart(myChart, title, metricsValue, ringColor) {
      const gaugeData = [
        {
          value: metricsValue,
          name: title,
          title: {
            offsetCenter: ['0%', '-15%'],
          },
          detail: {
            valueAnimation: true,
            offsetCenter: ['0%', '15%'],
          },
        },
      ];
      const options = {
        series: [
          {
            type: 'gauge',
            startAngle: 90,
            endAngle: -270,
            pointer: {
              show: false,
            },
            progress: {
              show: true,
              overlap: false,
              clip: false,
              itemStyle: {
                color: ringColor,
                borderWidth: 1,
                borderColor: ringColor,
              },
            },
            axisLine: {
              lineStyle: {
                width: 20,
              },
            },
            splitLine: {
              show: false,
              distance: 0,
              length: 10,
            },
            axisTick: {
              show: false,
            },
            axisLabel: {
              show: false,
              distance: 50,
            },
            data: gaugeData,
            title: {
              color: ringColor,
              fontSize: 12,
            },
            detail: {
              width: 50,
              height: 12,
              fontSize: 12,
              color: ringColor, // 代表百分数的颜色
              borderColor: ringColor,
              borderRadius: 20,
              borderWidth: 1,
              formatter: '{value}%',
            },
          },
        ],
      };
      myChart.setOption(options, true);
    },

    /**
     * 绘制热力图
     */
    drawBisceHeat(myChart, heatObj) {
      const hours = heatObj.labels;
      const days = hours;
      const data = heatObj.detail;
      // 求出最大值。设置热力图的最大值。
      let maxValue = 0;
      let minValue = 0;
      if (data.length > 0) {
        minValue = data[0][2];
      }
      for (const xys of data) {
        if (maxValue < xys[2]) {
          maxValue = xys[2];
        }
        if (minValue > xys[2]) {
          minValue = xys[2];
        }
      }

      const options = {
        tooltip: {
          position: 'top',
        },
        grid: {
          height: '70%',
          top: '5%',
        },

        xAxis: {
          type: 'category',
          data: hours,
          splitArea: {
            show: true,
          },
        },
        yAxis: {
          type: 'category',
          data: days,
          splitArea: {
            show: true,
          },
        },
        visualMap: {
          min: minValue,
          max: maxValue,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '1%',
        },
        series: [
          {
            name: 'Basic Metrics',
            type: 'heatmap',
            data: data,
            label: {
              show: true,
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              },
            },
          },
        ],
      };
      myChart.setOption(options, true);
    },

    /**
     * 绘制热力图
     */
    drawHeatMap(nameStr, labels, datas) {
      const xLabels = labels;
      const yLabels = xLabels;
      const data = datas;
      // 求出最大值。设置热力图的最大值。
      let maxValue = 0;
      let minValue = 0;
      if (data.length > 0) {
        minValue = data[0][2];
      }
      for (const xys of data) {
        if (maxValue < xys[2]) {
          maxValue = xys[2];
        }
        if (minValue > xys[2]) {
          minValue = xys[2];
        }
      }
      const options = {
        tooltip: {
          position: 'top',
        },
        grid: {
          height: '70%',
          top: '5%',
        },
        xAxis: {
          type: 'category',
          data: xLabels,
          splitArea: {
            show: true,
          },
        },
        yAxis: {
          type: 'category',
          data: yLabels,
          splitArea: {
            show: true,
          },
        },
        visualMap: {
          min: minValue,
          max: maxValue,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '1%',
        },
        series: [
          {
            name: nameStr,
            type: 'heatmap',
            data: data,
            label: {
              show: true,
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              },
            },
          },
        ],
      };

      const heatChart = this.$echarts.init(this.$refs.heatsc);
      this.sliceHeatChartsCache.push(heatChart);
      heatChart.setOption(options, true);
    },

    /**
     * 1个odd绘制柱状图
     */
    drawOneOddChart(data) {
      if (this.isObjDet && this.slicingType === '0') {
        this.drawRingsPart(data, this.classMetricsCheckList, 'ringChart');
        this.drawAreaChart(data[data.length - 1], 'classAreaChart');
        return;
      }
      const sliceChart = this.$echarts.init(this.$refs.sliceChart);
      this.sliceChartsCache.push(sliceChart);
      this.drawBarChart(sliceChart, data);
    },
    drawAreaChart(data, container) {
      const chart = this.$echarts.init(this.$refs[container]);
      const cfg = {
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: data.detail.x,
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            data: data.detail.y,
            type: 'line',
            areaStyle: {},
          },
        ],
      };
      chart.setOption(cfg);
    },
    /**
     *  绘制柱状图
     */
    drawBarChart: function(myChart, result) {
      // result 是个数组
      // legend 数组，所有odd的value ，也就是fog1,flog2...
      const legendsArr = [];
      // X轴 标签，计算标准 + 计算方式 例如 accuracy（total）
      const sourceArr = [];
      const xLabels = [];
      const keys = [];
      const seriesArr = [];
      const oddMap = new Map();
      for (const i of result) {
        if (i.metrics !== 'matrix') {
          // 把所有的metric + 计算方法（micro,macro,weighted...）都放进了xLabels数组。
          xLabels.push(i.metrics + '(' + i.average + ')');
          keys.push(i.metrics);
          oddMap.set(i.metrics, i.detail);
          this.oddValuesOptions = i.values;
        } else {
          // 缓存热力图
          const heatDetail = i.detail;
          this.heatChartLabels = [].concat(i.labels);
          for (const heatd of heatDetail) {
            this.heatChartMap.set(heatd.odd1, heatd.detail);
          }
        }
      }
      // sourceArr.push(legendsArr)
      // 对map的第一个数组进行遍历出odd的value
      legendsArr.push('product');
      // 计算一个x label 对应几个柱子，现在来看就是odd几个value，就是几个柱子
      // 这个循环就计算出 source的第一个数组了
      if (oddMap.size > 0) {
        const oddArr = oddMap.get(keys[0]);
        for (const od of oddArr) {
          seriesArr.push({ type: 'bar', barMaxWidth: '6%' });
          legendsArr.push(od.odd1);
        }
      }
      sourceArr.push(legendsArr);
      // 拼装echart 柱状图官方source数组,取出每个odd的value
      for (let i = 0; i < oddMap.size; i++) {
        const pro = [];
        pro.push(xLabels[i]);
        const valueArr = oddMap.get(keys[i]);
        for (const val of valueArr) {
          pro.push(val.value);
        }
        sourceArr.push(pro);
      }
      const options = {
        tooltip: {},
        legend: this.chartLegend,
        color: this.chartColOneColor,
        grid: this.chartGrid,
        dataset: {
          // source 是个二维数组
          source: sourceArr,
        },
        xAxis: { type: 'category' },
        yAxis: {},
        series: seriesArr,
      };
      myChart.setOption(options, true);
    },
    /**
     * 获取odd列表
     */
    getOddList() {
      const that = this;
      const query = {};
      query.table_id = this.tableId;
      return api.GetOddList(query).then(ret => {
        this.selctedOdd = ret.data.data?.[0]?.field_name;
        for (const item of ret.data.data) {
          that.oddOptions.push(item.field_name);
        }
      });
    },
    formatPercent(num) {
      return (num * 100).toFixed(1);
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
  computed: {
    isObjDet() {
      return this.algType === 'object_detection';
    },
  },
};
</script>

<style lang="scss" scoped>
::v-deep .el-tabs__item {
  color: #3b3c3d;
}

::v-deep .el-icon-arrow-left {
  color: #3b3c3d;
}

:deep(.el-checkbox__input.is-focus .el-checkbox__inner) {
  //悬浮
  border-color: none !important;
}

:deep(.el-checkbox__input.is-checked + .el-checkbox__label),
:deep(.el-checkbox__label) {
  //文字
  font-size: 14px;
  font-weight: 500;
  color: #3b3c3d;
}

.choose-label {
  font-size: 14px;
  font-weight: 500;
  color: #3b3c3d;
}

.collapse-title {
  flex: 1 0 90%;
  order: 1;
  font-size: 15px;
  font-family: Microsoft YaHei;
  font-weight: bold;
  color: #2992fa;
}

.el-collapse-item__header {
  flex: 1 0 auto;
  order: -1;
}

.title {
  font-size: 18px;
  font-family: Microsoft YaHei;
  font-weight: bold;
  color: #303133;
  padding-bottom: 17px;
  padding-top: 17px;
}

::v-deep .el-collapse-item__header.is-active {
  border-bottom: 1px solid #ebeef5;
}

::v-deep .el-collapse-item__wrap {
  border: none;
}

p {
  margin: 0;
  padding: 0;
}

.row {
  overflow: hidden;
  margin-bottom: 22px;
}

.row .col_left {
  float: left;
  width: 420px;
}

.row .col_right {
  float: left;
}

.select-alg {
  margin-left: 0px;
  width: 120px;
}

.pcontent {
  margin-left: 5px;
  line-height: 15px;
  font-size: 15px;
  font-size: 15px;
  color: #999;
}

.task-info {
  width: 100%;
  height: 45vh;
}

.chart-container {
  width: 100%;
  height: 80vh;
}

.chart-main {
  height: 80vh;
  width: 100%;
  padding: 1px;
}

.chart-pdiv {
  width: 100%;
  height: 290px;
}

.chartcol-one {
  width: 100%;
  height: 100%;
}

.heat-basic {
  width: 1000px;
  height: 320px;
}

.heat-one {
  width: 100%;
  height: 320px;
}

.chart-dom {
  width: 100%;
  height: 100%;
}

.div-tableinfo {
}

.div-tableinfo p {
  font-weight: bold;
  line-height: 28px;
}

.div-tableinfo span {
  line-height: 28px;
}

.div-commit {
  text-align: center;
  margin: auto;
  width: 50%;
}

.grey_line {
  height: 1px;
  border-top: 1px solid #ddd;
  text-align: center;
  margin-bottom: 10px;
}

.div-root {
  width: 100%;
  height: 100%;
  padding: 0px;
}
.form-item {
  display: flex;
  align-items: center;
  margin-bottom: 16px;

  .item-label {
    font-weight: 500;
    font-size: 14px;
    margin-right: 8px;
  }
}
</style>
