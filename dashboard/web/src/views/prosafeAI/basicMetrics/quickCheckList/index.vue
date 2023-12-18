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
  name: 'bmQuickCheckResult',
  mixins: [d2CrudPlus.crud],
  data() {
    return {
      test: 'https://www.google.com/search?q=%E7%B3%BB%E7%BB%9F%E5%8&sclient=gws-wiz-serp',
    };
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
      query.task_type = '1';
      const res = api.GetList(query);
      return res;
    },

    downloadReport(scope) {
      const query = {};
      query.run_id = scope.row.id;
      api.exportData(query);
      // })
    },

    viewTestResult(scope) {
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
          parent_name: 'bmQuickCheckResult',
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
