<template>
  <el-tooltip effect="dark" :content="color" placement="bottom">
    <el-color-picker
      class="can-hover"
      :value="value"
      :predefine="predefine"
      size="mini"
      @change="set"
    />
  </el-tooltip>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'd2-header-color',
  data() {
    return {
      color: '',
      predefine: ['#ff4500', '#ff8c00', '#ffd700', '#90ee90', '#00ced1', '#1e90ff', '#c71585'],
    };
  },
  mounted() {
    this.initI18nStr();
  },
  computed: {
    ...mapState('d2admin/color', ['value']),
  },
  watch: {
    '$i18n.locale': 'i18nHandle',
    value(value) {
      this.set(value);
    },
  },
  methods: {
    ...mapActions('d2admin/color', ['set']),
    i18nHandle(value, oldVal) {
      this.color = this.$t('global.hover-color');
    },
    initI18nStr() {
      this.color = this.$t('global.hover-color');
    },
  },
};
</script>
