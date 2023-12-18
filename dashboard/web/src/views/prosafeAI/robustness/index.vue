<template>
  <el-tabs v-model="activeName" class="tabs">
    <el-tab-pane label="Task List" name="robustTaskList">
      <robustTaskList />
    </el-tab-pane>
    <el-tab-pane label="Quick Check List" name="robustQuickCheckList">
      <robustQuickCheckList />
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import robustTaskList from './robustTaskList/index.vue';
import robustQuickCheckList from './robustQuickCheckList/index.vue';

export default {
  name: 'robustness',
  components: {
    robustTaskList,
    robustQuickCheckList,
  },
  data() {
    return {
      activeName: 'robustTaskList',
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
