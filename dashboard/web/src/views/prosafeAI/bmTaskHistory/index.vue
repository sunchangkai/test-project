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
        <div
          style="background-color: #fdf6ec;display: flex;flex-direction: column;justify-content: center"
        ></div>
        <crud-toolbar
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>

      <template slot="table_idSlot" slot-scope="scope">
        <el-button
          type="primary"
          @click="downloadReport(scope)"
          icon="el-icon-download"
          style="width: 32px;height: 32px;padding: 1px"
        ></el-button>
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
          <div>
            <p class="ptitle">User Guide:</p>
          </div>
          <div class="div-user-guide">
            <el-container style="width: 100%;padding: 0px;" direction="vertical">
              <el-main style="height: 200px;padding: 0px;background-color: #2d2d2d">
                <pre class="psamplecode">{{ codeSingleLine }}</pre>
              </el-main>
              <div style="height: 40px;position: relative;top: -40px">
                <el-button class="copybtn-rb" type="primary" @click="copyCode" size="small"
                  >Copy</el-button
                >
              </div>
            </el-container>
          </div>
          <p style="font-size: 12px;color: #999;margin-top: 5px;">
            Note: Please copy the sample code to your IDE and run the task
          </p>
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
  name: 'bmTaskHistory',
  mixins: [d2CrudPlus.crud],
  data() {
    return {
      scDialogVisible: false,
      codeSingleLine: '',
      taskId: '',
    };
  },
  mounted() {
    this.taskId = this.$route.query.task_id;
  },

  watch: {},

  methods: {
    subFields(wholeStr) {
      return util.subFields(wholeStr);
    },
    /**
     * 复制文本到剪切板中
     */
    copyCode() {
      // 动态创建 textarea 标签
      const textarea = document.createElement('textarea');
      // 将该 textarea 设为 readonly 防止 iOS 下自动唤起键盘，同时将 textarea 移出可视区域
      textarea.readOnly = 'readonly';
      textarea.style.position = 'absolute';
      textarea.style.left = '-9999px';
      // 将要 copy 的值赋给 textarea 标签的 value 属性
      // 网上有些例子是赋值给innerText,这样也会赋值成功，但是识别不了\r\n的换行符，赋值给value属性就可以
      textarea.value = this.codeSingleLine;
      // 将 textarea 插入到 body 中
      document.body.appendChild(textarea);
      // 选中值并复制
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
      query.task_id = this.taskId;
      const res = api.GetHistoryList(query);
      return res;
    },
    downloadReport(scope) {
      const query = {};
      query.run_id = scope.row.id;
      return api.exportData(query);
    },

    goTaskInfo(scope) {
      this.$router.push({
        name: 'taskChart',
        query: {
          table_id: scope.row.table_id,
          task_id: scope.row.task_id,
          id: scope.row.id,
          model_path: scope.row.model_path,
          data_path: scope.row.data_path,
          machine_info: scope.row.machine_info,
          task_desc: scope.row.description,
          algorithm_type: scope.row.algorithm_type,
          prerouter_name: this.$options.name,
          pre_taskid: this.taskId,
          parent_name: 'bmTaskHistory',
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
