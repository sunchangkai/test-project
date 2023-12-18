<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @goHistoryList="goHistoryList"
      @showCode="showCode"
      @detailDialog="detailDialog"
      crud.options.tableType="vxe-table"
      @cell-data-change="handleCellDataChange"
    >
      <div slot="header">
        <div style="margin: 20px;"></div>
        <el-button type="success" size="medium" @click="createTask">
          <i class="el-icon-plus" /> New Task
        </el-button>
        <crud-toolbar
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
        <div style="margin: 20px;"></div>
      </div>
    </d2-crud-x>

    <el-dialog title="Task Detail" :visible.sync="dialogVisible" width="60%">
      <div>
        <p class="dialog_grey_line"></p>

        <div style="margin: 10px 10px 10px 10px;">
          <el-container style="height: 350px;padding: 0;">
            <el-main style="height: 100%;padding: 1px">
              <div class="criteria-params">
                <div>
                  <span style="font-weight: bold;font-size: 20px;">Model Information</span>
                  <div style="display: flex;margin-top: 15px;">
                    <div style="width:50%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold;">Model Path:</span
                        ><span class="label-content">{{ detailTask.model_path }}</span>
                      </li>
                    </div>
                    <div style="width:50%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold">Domain:</span
                        ><span class="label-content">{{
                          detailTask.init_hyperparameter.domain
                        }}</span>
                      </li>
                    </div>
                  </div>
                  <div style="display: flex;margin-top: 15px;">
                    <div style="width:50%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold;">Model Framework:</span
                        ><span class="label-content">{{
                          detailTask.init_hyperparameter.model_framework
                        }}</span>
                      </li>
                    </div>
                    <div style="width:50%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold">Task Type:</span
                        ><span class="label-content">{{
                          detailTask.init_hyperparameter.task_type
                        }}</span>
                      </li>
                    </div>
                  </div>
                </div>
                <div></div>
              </div>
              <div class="criteria-params-mid">
                <div>
                  <span style="font-weight: bold;font-size: 20px;">Data Information</span>
                  <div style="display: flex;margin-top: 15px;">
                    <div style="width:50%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold;">Tabel:</span>
                        <span class="label-content">{{ detailTask.table_name_mysql }}</span>
                      </li>
                    </div>
                    <div style="width:50%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold">Data Path:</span
                        ><span class="label-content">{{ detailTask.data_path }}</span>
                      </li>
                    </div>
                  </div>
                  <div style="display: flex;margin-top: 15px;">
                    <div style="width:50%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold;">Table version:</span
                        ><span class="label-content">{{ detailTask.version }}</span>
                      </li>
                    </div>
                    <div style="width:50%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold">Dataset format:</span
                        ><span class="label-content">{{
                          detailTask.init_hyperparameter.dataset_format
                        }}</span>
                      </li>
                    </div>
                  </div>
                </div>
              </div>
              <div class="config-preview">
                <div>
                  <span style="font-weight: bold;font-size: 20px;">Config Information</span>
                  <div style="display: flex;margin-top: 15px;">
                    <div style="width:50%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold;">Device Info:</span
                        ><span class="label-content">{{
                          detailTask.init_hyperparameter.device
                        }}</span>
                      </li>
                    </div>
                  </div>
                  <div style="display: flex;margin-top: 15px;">
                    <div style="width:30%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold;">Model Type:</span
                        ><span class="label-content">{{
                          detailTask.init_hyperparameter.model_type
                        }}</span>
                      </li>
                    </div>
                    <div style="width:70%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold">Mutation Guidance:</span
                        ><span class="label-content">{{
                          detailTask.init_hyperparameter.mutation_guidance
                        }}</span>
                      </li>
                    </div>
                  </div>
                  <div style="display: flex;margin-top: 15px;margin-bottom: 10px">
                    <div style="width:100%;padding-left: 20px">
                      <li>
                        <span style="font-weight: bold;">Related Parameters:</span>
                        <span class="label-content">
                          p_min={{ detailTask.init_hyperparameter.p_min }};k_time={{
                            detailTask.init_hyperparameter.k_time
                          }};r={{ detailTask.init_hyperparameter.r }};try_number={{
                            detailTask.init_hyperparameter.try_num
                          }};alpha={{ detailTask.init_hyperparameter.alpha }};max_iter={{
                            detailTask.init_hyperparameter.max_iter
                          }};beta={{ detailTask.init_hyperparameter.beta }};batch_size={{
                            detailTask.init_hyperparameter.batch_size
                          }}
                        </span>
                      </li>
                    </div>
                  </div>
                </div>

                <span style="font-weight: bold;font-size: 20px;">Pixel Level Attacks:</span>
                <div
                  style="padding-left: 20px; margin-top: 15px;"
                  v-for="item in detailTask.init_hyperparameter.pixel_level"
                  :key="item.method"
                >
                  <li>
                    <span style="font-weight: bold;">{{ item.method }}</span
                    ><span>{{ parameterToString(item.parameters) }}</span>
                  </li>
                </div>

                <span style="font-weight: bold;font-size: 20px;margin-top: 10px;"
                  >Semantic Level Attacks:</span
                >
                <div
                  style="padding-left: 20px; margin-top: 15px;"
                  v-for="item in detailTask.init_hyperparameter.semantic_level"
                  :key="item.method"
                >
                  <li>
                    <span style="font-weight: bold;">{{ item.method }}</span
                    ><span>{{ parameterToString(item.parameters) }}</span>
                  </li>
                </div>
              </div>
            </el-main>
          </el-container>
        </div>
        <p class="dialog_grey_line"></p>
      </div>
      <div slot="footer">
        <el-button type="success" @click="dialogVisible = false" size="small">Confirm</el-button>
      </div>
    </el-dialog>

    <el-dialog title="Sample Code" :visible.sync="scDialogVisible" width="60%">
      <div>
        <p class="dialog_grey_line"></p>
        <div style="padding: 20px">
          <div class="dialog-left-title">
            <i class="el-icon-info" style="margin-right: 2px"></i>
            <div class="ptitle">Token:</div>
            <div class="pcontent">{{ tokenStr }}</div>
          </div>

          <div class="dialog-left-title">
            <p class="ptitle">Remaining times:</p>
            <p class="pcontent">{{ remainingTimes }}</p>
          </div>

          <p class="ptitle">User Guide:</p>

          <div class="user-guide">
            <p style="margin: 0 0 5px 0;font-size:16px;">
              Step1: Install the SDK to your IDE by "pip install xxxx.whl"
            </p>
            <div style="display: flex;align-items: center;">
              <div style="margin-right: 10px;">
                <p style="font-size:16px;">
                  Step2: Download the config file in including all the hyperparams you set
                </p>
                <p style="color: #49a1ff;font-size: 11px;">
                  (if you have downloaded the file when finish creating the task.just ignore this
                  step)
                </p>
              </div>
              <div>
                <el-button type="success" @click="downloadYaml" size="mini">Download</el-button>
              </div>
            </div>

            <p style="margin: 5px 0 5px 0;font-size:16px;">
              Step3: Copy the sample code to your IDE and run the test
            </p>

            <div class="step3-container">
              <div class="step3">
                <pre class="text">{{ codeSingleLine }}</pre>
                <el-button class="copy-btn" type="primary" @click="copyCode" size="small"
                  >Copy</el-button
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import * as api from './api';
import { crudOptions } from './crud';
import { d2CrudPlus } from 'd2-crud-plus';

export default {
  name: 'robustTaskList',
  mixins: [d2CrudPlus.crud],

  data() {
    return {
      downloadYamlId: 0,
      formDisabled: false,
      scDialogVisible: false,
      dialogVisible: false,
      tokenStr: '',
      remainingTimes: 0,
      sampleCodeStr: [],
      codeSingleLine: '',
      detailTask: {
        id: 0,
        model_path: '',
        data_path: '',
        algorithm_type: '',
        machine_info: '',
        token: '',
        description: '',
        table_name_mysql: '',
        version: 0,
        init_hyperparameter: {
          device: '',
          model_type: 'white box',
          mutation_guidance: 'NC',
          mutation_params: null,
          p_min: 0,
          r: 0,
          alpha: 0,
          beta: 0,
          k_time: 0,
          try_num: 0,
          max_iter: 0,
          batch_size: 0,
          pixel_level: [],
          semantic_level: [],
        },
        status: '0',
        create_time: '06/01/2023 17:15:38',
        usercase_name: 'TSR_Classifier',
        project_name: 'TSR',
      },
    };
  },
  mounted() {
    console.log('steven', 'mounted invoke.....');
  },

  watch: {},

  methods: {
    createTask() {
      this.$router.push({
        name: 'robustNewTask',
        params: {},
      });
    },
    // 计算表达式的值
    evil(fn) {
      var Fn = Function; // 一个变量指向Function，防止有些前端编译工具报错
      return new Fn('return ' + fn)();
    },
    parameterToString(para) {
      let str = '';
      // console.log('params item :', JSON.stringify(para))
      for (let i = 0; i < para.length; i++) {
        const valueStr = para[i].value.replace(',', '-');
        str += para[i].name + ':' + valueStr;
        if (i !== para.length - 1) {
          str += ', ';
        }
      }
      return '(' + str + ')';
    },
    downloadYaml() {
      const query = {
        task_id: this.downloadYamlId,
      };
      api.downloadYaml(query);
    },
    /**
     * 获取版本列表
     */
    getSampleCode(scope) {
      const that = this;
      that.tokenStr = '';
      that.codeSingleLine = '';
      that.remainingTimes = 0;
      const query = {};
      query.task_id = scope.row.id;
      api.GetSampleCode(query).then(ret => {
        that.tokenStr = ret.data.token;
        that.codeSingleLine = ret.data.code;
        that.remainingTimes = ret.data.remaining_times;
      });
    },
    handleCellDataChange({ rowIndex, key, value, row }) {},
    /**
     * 复制文本到剪切板中
     */
    copyCode() {
      const textarea = document.createElement('textarea');
      textarea.readOnly = 'readonly';
      textarea.style.position = 'absolute';
      textarea.style.left = '-9999px';
      textarea.value = this.codeSingleLine;
      document.body.appendChild(textarea);
      textarea.select();
      textarea.setSelectionRange(0, textarea.value.length);
      document.execCommand('Copy');
      document.body.removeChild(textarea);
      // cb()
      this.$message({
        message: 'Copy successful',
        type: 'success',
      });
    },

    getCrudOptions() {
      return crudOptions(this);
    },

    pageRequest(query) {
      // task类型: 0: robustness;1: basic_metrics
      query.task_type = 0;
      return api.GetTaskList(query).then(ret => {
        if (ret.data.data.length <= 0) {
          this.$alert('You haven’t create any task', 'Tip', {
            confirmButtonText: 'Confirm',
            callback: action => {},
          });
        }
        return ret;
      });
    },

    goHistoryList(scope) {
      console.log('task id :', scope.row.id);
      const params = this.evil('(' + scope.row.init_hyperparameter + ')');
      this.$router.push({
        name: 'robustTaskHistory',
        query: { task_id: scope.row.id, model_type: params.model_type },
      });
    },
    goDataManagement() {
      this.$router.push({
        path: '/api/prosafeai/data_management',
        query: {},
      });
    },
    showCode(scope) {
      this.scDialogVisible = true;
      this.downloadYamlId = scope.row.id;
      this.getSampleCode(scope);
    },

    detailDialog(scope) {
      this.dialogVisible = true;
      this.detailTask.model_path = scope.row.model_path;
      this.detailTask.data_path = scope.row.data_path;
      this.detailTask.table_name_mysql = scope.row.table_name_mysql;
      this.detailTask.version = scope.row.version;
      this.detailTask.description = scope.row.description;
      const json = this.evil('(' + scope.row.init_hyperparameter + ')');
      this.detailTask.init_hyperparameter = json;
    },
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
.label-content {
  color: #666;
  font-size: 14px;
  margin-left: 5px;
}

.config-preview {
  display: flex;
  flex-direction: column;
  background-color: #b9def0;
  margin-top: 10px;
  border-radius: 5px;
  padding: 8px;
}

.criteria-params {
  background-color: #b9def0;
  border-radius: 5px;
  padding: 8px;
}

.criteria-params-mid {
  margin-top: 10px;
  background-color: #b9def0;
  border-radius: 5px;
  padding: 8px;
}

.select-filter {
  width: 350px;
}

label.xrequired:before {
  content: '* ';
  color: red;
}

// 这里重置dialog 的布局
::v-deep .el-dialog__body {
  padding: 0px;
}

::v-deep .el-dialog {
  border-radius: 8px;
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

.confirmbtn-rb {
  position: absolute;
  right: 15px;
  bottom: 10px;
}

.el-dialog__header {
  height: 50px;
}

.user-guide {
  /*style="padding-left: 10px;margin-top: 10px;"*/
  margin-top: 10px;
  padding: 20px 10px 20px 10px;
  border-style: solid;
  border-color: #666;
  border-width: 1px;
  border-radius: 5px;
}

.step3-container {
  position: relative;
  .step3 {
    padding: 16px 10px 26px 10px;
    background-color: #2d2d2d;
    overflow: auto;
    .text {
      color: #fff;
    }
    .copy-btn {
      position: absolute;
      right: 16px;
      bottom: 16px;
    }
  }
}

.dialog-left-title {
  display: flex;
  margin-bottom: 20px;
}

.div-hyperpara {
  margin-bottom: 20px;
}

.cdialog-title {
  font-weight: bold;
  line-height: 25px;
  font-size: 20px;
  color: #666;
}

.ptitle {
  font-weight: bold;
  line-height: 15px;
  font-size: 15px;
  color: #333;
}

.pcontent {
  margin-left: 5px;
  line-height: 15px;
  font-size: 15px;
  font-size: 15px;
  color: #999;
}

.dialog-body-style {
  margin: 20px 0 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.dialog_grey_line {
  height: 1px;
  border-top: 1px solid #ddd;
  text-align: center;
}

.el-pagination {
  text-align: center;
}
</style>
