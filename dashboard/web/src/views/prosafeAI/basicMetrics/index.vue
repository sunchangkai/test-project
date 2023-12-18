<template>
  <el-tabs v-model="activeName" class="tabs">
    <el-tab-pane label="Task List" name="taskList">
      <taskList />
    </el-tab-pane>
    <el-tab-pane label="Quick Check List" name="quickCheckList">
      <quickCheckList />
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import quickCheckList from './quickCheckList/index.vue';
import taskList from './taskList/index.vue';

export default {
  name: 'basicMetrics',
  components: {
    quickCheckList,
    taskList,
  },
  data() {
    return {
      activeName: 'taskList',
    };
  },
  mounted() {},

  watch: {},

  methods: {},
};
</script>

<style lang="scss" scoped>
.tabs {
  height: 100%;

  ::v-deep {
    .el-tabs__content {
      height: 100%;
    }
    .d2-crud-body {
      padding-bottom: 100px;
    }
    .d2-crud-footer {
      position: absolute;
      bottom: 50px;
    }
  }
}
</style>
