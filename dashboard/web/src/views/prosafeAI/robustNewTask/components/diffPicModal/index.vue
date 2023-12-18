<template>
  <el-dialog
    title=""
    width="1000px"
    :visible="visible"
    @close="handleCancel"
    :destroy-on-close="true"
  >
    <div class="diy-container">
      <diy-pic :isOrigin="true" :atk="atk"></diy-pic>
      <diy-pic
        :isMinimum="true"
        :atk="atk"
        :minSelect="minSelect"
        :maxSelect="maxSelect"
        @change="data => sliderChange(data, true)"
      ></diy-pic>
      <diy-pic
        :atk="atk"
        :minSelect="minSelect"
        :maxSelect="maxSelect"
        @change="sliderChange"
      ></diy-pic>
    </div>
    <div slot="footer">
      <el-button @click="handleCancel">Cancel</el-button>
      <el-button type="primary" @click="saveParameters">OK</el-button>
    </div>
  </el-dialog>
</template>

<script>
import diyPic from '../diyPic';

export default {
  name: 'diff-pic-modal',
  props: ['visible', 'atk'],
  components: { diyPic },
  data() {
    return {
      minSelect: this.atk.parameters.map(i => ({
        name: i.name,
        value: Number(i.value.split(',')[0]),
        range: [i.min, i.max],
        dtype: i.dtype,
      })),
      maxSelect: this.atk.parameters.map(i => ({
        name: i.name,
        value: Number(i.value.split(',')[1]),
        range: [i.min, i.max],
        dtype: i.dtype,
      })),
    };
  },

  methods: {
    handleCancel() {
      this.$emit('cancel');
    },
    sliderChange(data, isMinSelect) {
      if (isMinSelect) {
        this.minSelect = data;
      } else {
        this.maxSelect = data;
      }
    },
    saveParameters() {
      const parameters = this.atk.parameters.map(i => {
        const minValue = this.minSelect.find(m => m.name === i.name).value;
        const maxValue = this.maxSelect.find(m => m.name === i.name).value;
        return {
          ...i,
          value: `${minValue},${maxValue}`,
        };
      });

      const final = {
        ...this.atk,
        parameters,
      };
      this.$emit('ok', final);
    },
  },
};
</script>

<style lang="scss" scoped>
.diy-container {
  display: flex;
  justify-content: space-between;
}
</style>
