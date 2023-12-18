<template>
  <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners">
    <div slot="header">
      <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch">
        <el-button
          slot="suffix"
          size="small"
          type="success"
          icon="el-icon-download"
          @click="download"
          >Download</el-button
        >
      </crud-search>
      <crud-toolbar
        :search.sync="crud.searchOptions.show"
        :compact.sync="crud.pageOptions.compact"
        :columns="crud.columns"
        :text="crud.toolBar.text"
        @refresh="doRefresh()"
        @columns-filter-changed="handleColumnsFilterChanged"
        @update:compact="updateCompact"
      />
    </div>
    <template slot="saved_pathSlot" slot-scope="scope">
      <d2-popover-copy :text="scope.row.saved_path"></d2-popover-copy>
    </template>
    <template slot="init_pathSlot" slot-scope="scope">
      <d2-popover-copy :text="scope.row.init_path"></d2-popover-copy>
    </template>
  </d2-crud-x>
</template>

<script>
import { getAttackSampleInfoList, downloadTxt } from './api';
import { crudOptions } from './crud';
import { d2CrudPlus } from 'd2-crud-plus';
import D2PopoverCopy from '@/components/d2-popover-copy';
export default {
  name: 'AttackSampleInfoTable',
  components: {
    D2PopoverCopy,
  },
  props: {
    runAttackMethodList: {
      type: Array,
      default: () => [],
    },
    runLabelList: {
      type: Array,
      default: () => [],
    },
  },
  mixins: [d2CrudPlus.crud],
  data() {
    return {
      show: true,
    };
  },
  mounted() {},
  methods: {
    download() {
      downloadTxt({
        run_id: this.$route.query.runId,
      });
    },
    getCrudOptions() {
      return crudOptions(this);
    },
    pageRequest(query) {
      return getAttackSampleInfoList(query);
    },
    updateCompact(val) {
      this.$emit('updateCompact', val);
    },
  },
};
</script>
