<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <template slot="header">
      <!--      <el-row>-->
      <!--        <el-col :span="24">-->
      <!--          <div class="grid-content bg-purple-dark">-->
      <!--            <p :style="{color:'#606266', fontSize:24+'px'}">Image Information:&nbsp;&nbsp;&nbsp;</p>-->
      <!--            &lt;!&ndash;            <span :style="{color:'#0477ff' }">Image name:</span> {{currentVersion}}&ndash;&gt;-->
      <!--          </div>-->
      <!--        </el-col>-->
      <!--      </el-row>-->
    </template>
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      crud.options.tableType="vxe-table"
    >
      <div slot="header">
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch">
          <template slot="slotExampleSearchSlot"> </template>
          <crud-toolbar
            :compact.sync="crud.pageOptions.compact"
            :columns="crud.columns"
            @refresh="doRefresh()"
            @columns-filter-changed="handleColumnsFilterChanged"
          />
        </crud-search>
      </div>
      <template slot="object_tagSlot" slot-scope="scope">
        <span v-for="(item, index) in noBboxTag(scope.row.object_tag)" :key="index">
          <span style="font-weight: 600;">{{ item.feature }}</span>
          <span style="padding: 6px;">{{ ':' + item.content + ';' }}</span>
        </span>
      </template>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api';
import { crudOptions } from './crud';
import { d2CrudPlus } from 'd2-crud-plus';

export default {
  name: 'objectTable',
  mixins: [d2CrudPlus.crud],
  data() {
    return {
      tableId: '',
      currentVersion: '',
      sampleId: '',
      chooseVersionTemp: '',
      tagKeys: [],
      tagValue: [],
      version: '1.0.0',
    };
  },
  mounted() {
    this.tableId = this.$route.query.table_id;
    this.currentVersion = this.$route.query.version;
    this.sampleId = this.$route.query.sample_id;
  },

  watch: {},

  methods: {
    noBboxTag(arr) {
      return arr.filter(i => i.feature !== 'bbox');
    },
    getCrudOptions() {
      return crudOptions(this);
    },
    pageRequest(query) {
      query.table_id = this.tableId;
      query.version = this.currentVersion;
      query.sample_id = this.sampleId;
      return api.GetList(query).then(ret => {
        return ret;
      });
    },
    addRequest(row) {
      return api.AddObj(row);
    },
    updateRequest(row) {
      return api.UpdateObj(row);
    },
    delRequest(row) {
      return api.DelObj(row.id);
    },
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
// 这里是设置分页工具栏居中
.el-pagination {
  text-align: center;
}

.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  padding-top: 10px;
  padding-left: 10px;
  height: 100px;
  background: #cee5ff;
}

.bg-purple {
  background: #d3dce6;
}

.bg-purple-light {
  background: #e5e9f2;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
</style>
