<template>
  <div :id="id" :class="className" :style="{ height: height, width: width }" />
</template>

<script>
import resize from './mixins/resize';

export default {
  name: 'Charts',
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart',
    },
    id: {
      type: String,
      default: 'chart',
    },
    width: {
      type: String,
      default: '',
    },
    height: {
      type: String,
      default: '',
    },
    option: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  watch: {
    option: {
      handler: function(option) {
        if (this.chart) {
          this.$nextTick(() => {
            this.chart.setOption(option, { notMerge: true });
            this.resize();
          });
        }
      },
      deep: true,
    },
  },
  mounted() {
    this.initChart();
  },
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    initChart() {
      this.$nextTick(() => {
        this.chart = this.$echarts.init(document.getElementById(this.id));
        this.chart.setOption(this.option, { notMerge: true });
        this.resize();
      });
    },
  },
};
</script>
