<template>
  <el-popover placement="top-start" trigger="hover">
    <div class="popoverBox">
      <span class="text">{{ text }}</span>
      <el-button
        v-clipboard:copy="text"
        v-clipboard:success="clipboardSuccess"
        class="btn"
        size="small"
        type="primary"
        >copy</el-button
      >
    </div>
    <span slot="reference" class="hoverText">{{ text }}</span>
  </el-popover>
</template>

<script>
import clipboard from '@/directive/clipboard/index.js';
export default {
  props: {
    text: {
      type: String,
      default: '',
    },
  },
  directives: {
    clipboard,
  },
  methods: {
    clipboardSuccess() {
      this.$message({
        message: 'Copy successfully',
        type: 'success',
        duration: 1500,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.hoverText {
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 30px;
  cursor: pointer;
  display: block;
}
.popoverBox {
  max-width: 400px;
  display: flex;
  flex-direction: column;
  .text {
    line-height: 1.5;
    margin-bottom: 5px;
  }
  .btn {
    width: 80px;
    align-self: flex-end;
  }
}
</style>
