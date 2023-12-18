<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @moreDetails="moreDetail"
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
      <template slot="fieldsSlot" slot-scope="scope">
        <el-tooltip effect="light" placement="bottom">
          <div slot="content" style="max-width: 400px;">
            <el-tag
              type="success"
              v-for="item in scope.row.fields"
              :key="item"
              style="margin: 5px"
              >{{ item }}</el-tag
            >
          </div>
          <span>
            {{ subFields(scope.row.fields) }}
          </span>
        </el-tooltip>
      </template>
      <template slot="task_typeSlot" slot-scope="scope">
        <span>
          {{ scope.row.task_type === 0 ? 'Classification' : 'Object Detection' }}
        </span>
      </template>
    </d2-crud-x>
    <el-dialog title="Tip" :visible.sync="dialogVisible" width="30%">
      <div class="no-record">
        <span>There is no record for this user,please contact the administrator to create!</span>
      </div>
      <p class="grey_line"></p>
      <div slot="footer">
        <el-button type="primary" @click="dialogVisible = false" style="width: 70px">OK</el-button>
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import * as api from './api';
import { crudOptions } from './crud';
import { d2CrudPlus } from 'd2-crud-plus';

export default {
  name: 'dataDisplay',
  mixins: [d2CrudPlus.crud],
  data() {
    return {
      dialogVisible: false,
    };
  },
  mounted() {},

  watch: {},

  methods: {
    getFieldSummary(arr) {
      let tString = '';
      if (arr !== undefined && arr.length > 0) {
        if (arr.length > 2) {
          tString += arr[0] + ',' + arr[1] + '...';
        } else if (arr.length === 2) {
          tString += arr[0] + ',' + arr[1];
        } else if (arr.length === 1) {
          tString += arr[0];
        }
      }
      return tString;
    },

    subFields(arr) {
      return this.getFieldSummary(arr);
    },
    getCrudOptions() {
      return crudOptions(this);
    },
    pageRequest(query) {
      const res = api.GetList(query);
      // 把vue的this先赋值给一个变量，否则在回调里调用就不是vue实例了
      var _this = this;
      res.then(
        function(ret) {
          _this.dialogVisible = ret.data.data.length === 0;
        },
        function(ret) {},
      );
      return res;
    },
    moreDetail(scope) {
      // 跳转传参有两个方式，一个是用query，一个是用params，前者必须用path属性表示路径，后者必须用name属性表示路径。
      this.$router.push({
        name: 'dataDisplayChart',
        params: {
          table_id: scope.row.id,
          project: scope.row.project_name,
          usercase: scope.row.usercase_name,
          table_name: scope.row.table_name_mysql,
          table_desc: scope.row.table_description,
          version: scope.row.latest_version,
          fields: scope.row.fields,
          task_type: scope.row.task_type,
        },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.no-record {
  display: flex;
  flex-display: row;
  flex-wrap: wrap;
  padding: 10px 40px 10px 40px;
  min-height: 100px;
}
.dialog-body-style {
  display: flex;
  flex-display: row;
  flex-wrap: wrap;
  padding: 10px 40px 10px 40px;
}

::v-deep .el-dialog__body {
  padding: 0;
}

::v-deep .el-dialog {
  border-radius: 8px;
}

::v-deep .el-dialog__title {
  line-height: 24px;
  font-size: 18px;
  color: #666;
}

::v-deep .el-dialog__wrapper {
  background-color: rgba(0, 0, 0, 0.2);
}

.dialog_grey_line {
  height: 1px;
  border-top: 1px solid #ddd;
  text-align: center;
  margin-bottom: 10px;
}

.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}

.el-pagination {
  text-align: center;
}
</style>
