<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @goTaskInfo="goTaskInfo"
      crud.options.tableType="vxe-table"
    >
      <div slot="header">
        <crud-toolbar
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>

      <template slot="table_idSlot" slot-scope="scope">
        <!-- todo: id=204 为demo展示效果用 特殊判断等后端有真实数据后去掉 -->
        <el-button
          type="primary"
          :disabled="scope.row.status !== 2 && scope.row.id !== 204"
          @click="downloadReport(scope)"
          icon="el-icon-download"
          style="width: 32px;height: 32px;padding: 1px"
        ></el-button>
      </template>

      <template slot="progressSlot" slot-scope="scope">
        <el-progress
          :width="60"
          :percentage="getPercentage(scope)"
          :status="getStatus(scope)"
        ></el-progress>
      </template>

      <template slot="descriptionSlot" slot-scope="scope">
        <el-popover
          placement="top"
          title=""
          width="400"
          trigger="hover"
          :content="scope.row.description"
        >
          <span slot="reference">
            {{ subFields(scope.row.description) }}
          </span>
        </el-popover>
      </template>
    </d2-crud-x>

    <el-dialog title="Review Code" :visible.sync="scDialogVisible" width="40%">
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
              Step1: Install the SDk to your IDE by "pip install xxxx.whl"
            </p>
            <div style="display: flex;align-items: center;">
              <div style="margin-right: 10px;">
                <p style="font-size:16px;">
                  Step2: Download the config file in including all the hyperparams you set
                </p>
                <p style="color: #49a1ff;font-size: 11px;margin-top: -5px;">
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

            <div class="div-user-guide">
              <el-container style="width: 100%;padding: 0px;" direction="vertical">
                <el-main style="height: 250px;padding: 0px;background-color: #2d2d2d">
                  <pre class="psamplecode">{{ codeSingleLine }}</pre>
                </el-main>

                <div style="height: 40px;position: relative;top: -40px">
                  <el-button class="copybtn-rb" type="primary" @click="copyCode" size="small"
                    >Copy</el-button
                  >
                </div>
              </el-container>
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
import util from '@/libs/util';

export default {
  name: 'robustTaskHistory',
  mixins: [d2CrudPlus.crud],
  data() {
    return {
      tokenStr: '',
      remainingTimes: 0,
      sampleCodeStr: [],
      codeSingleLine: '',

      scDialogVisible: false,
      taskId: '',
    };
  },
  mounted() {
    this.taskId = this.$route.query.task_id;
  },

  watch: {},

  methods: {
    getPercentage(scope) {
      // todo: 204 为demo展示效果用 特殊判断等后端有真实数据后去掉
      if (scope.row.id === 204) {
        return 100;
      }
      return (scope.row.process_rate || 0) * 100;
    },
    getStatus(scope) {
      // todo: 204 为demo展示效果用 特殊判断等后端有真实数据后去掉
      if (scope.row.id === 204) {
        return 'success';
      }
      const status = scope.row.status;
      if (status === 0) {
        return 'exception';
      } else if (status === 2) {
        return 'success';
      } else {
        return null;
      }
    },
    subFields(wholeStr) {
      return util.subFields(wholeStr);
    },
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
      this.$message({
        message: 'Copy successful',
        type: 'success',
      });
    },
    getCrudOptions() {
      return crudOptions(this);
    },

    pageRequest(query) {
      query.task_id = this.taskId;
      const res = api.GetHistoryList(query);
      return res;
    },
    downloadReport(scope) {
      const query = {};
      query.run_id = scope.row.id;
      return api.exportData(query);
    },
    downloadYaml() {},

    goTaskInfo(scope) {
      this.$router.push({
        path: '/robustnessTestingResults',
        query: {
          runId: scope.row.id,
          algType: scope.row.algorithm_type,
          modelType: this.$route.query.model_type,
        },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.copybtn-rb {
  position: absolute;
  top: 0px;
  right: 15px;
}

.psamplecode {
  margin: 10px 10px 50px 10px;
  color: white;
}

.div-user-guide {
  height: 200px;
  border-style: solid;
  border-color: #ddd;
  border-width: 1px;
  margin-top: 10px;
}

// 这里重置dialog 的布局
::v-deep .el-dialog__body {
  padding: 0px;
}

::v-deep .el-dialog {
  border-radius: 8px;
}

::v-deep .el-dialog__title {
  line-height: 14px;
  font-size: 22px;
  color: #333;
}

::v-deep .el-dialog__wrapper {
  background-color: rgba(0, 0, 0, 0.2);
}

.el-pagination {
  text-align: center;
}

.dialog_grey_line {
  height: 1px;
  border-top: 1px solid #ddd;
  text-align: center;
}
</style>
