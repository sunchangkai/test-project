<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @viewTestResult="viewTestResult"
      @downloadReport="downloadReport"
      crud.options.tableType="vxe-table"
    >
      <div slot="header">
        <div
          style="background-color: #fdf6ec;display: flex;flex-direction: column;justify-content: center"
        >
          <el-alert
            title="You may view the results of the last three tests here"
            type="info"
            :closable="false"
            show-icon
          >
          </el-alert>
        </div>
      </div>

      <template slot="descriptionSlot" slot-scope="scope">
        <el-popover
          placement="top-start"
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

      <template slot="model_pathSlot" slot-scope="scope">
        <el-popover
          placement="top"
          title=""
          width="400"
          trigger="hover"
          :content="scope.row.model_path"
        >
          <span slot="reference">
            {{ subFields(scope.row.model_path) }}
          </span>
        </el-popover>
      </template>

      <template slot="data_pathSlot" slot-scope="scope">
        <el-popover
          placement="top"
          title=""
          width="400"
          trigger="hover"
          :content="scope.row.data_path"
        >
          <span slot="reference">
            {{ subFields(scope.row.data_path) }}
          </span>
        </el-popover>
      </template>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api';
import { crudOptions } from './crud';
import { d2CrudPlus } from 'd2-crud-plus';

export default {
  name: 'robustQuickCheckResult',
  mixins: [d2CrudPlus.crud],
  data() {
    return {};
  },
  mounted() {},

  watch: {},

  methods: {
    subFields(wholeStr) {
      let ellipseStr = '';
      if (wholeStr?.length > 35) {
        ellipseStr = wholeStr.slice(0, 35) + '...';
      } else {
        ellipseStr = wholeStr;
      }
      return ellipseStr;
    },

    getCrudOptions() {
      return crudOptions(this);
    },

    pageRequest(query) {
      // task类型: 0: robustness;1: basic_metrics
      query.task_type = '0';
      const res = api.GetList(query);
      return res;
    },

    downloadReport(scope) {
      const query = {};
      query.run_id = scope.row.id;
      api.exportData(query);
    },

    viewTestResult(scope) {
      console.log('id', scope.row.id);
      console.log('tableid', scope.row.table_id);
      this.$router.push({
        path: '/robustnessTestingResults',
        query: {
          runId: scope.row.id,
        },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.el-pagination {
  text-align: center;
}
</style>
