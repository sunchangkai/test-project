<template>
  <el-dropdown placement="bottom" size="small" @command="handleChange">
    <el-button class="d2-mr btn-text can-hover" type="text">
      <d2-icon name="font" style="font-size: 16px;" />
    </el-button>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item v-for="item in options" :key="item.value" :command="item.value">
        <d2-icon :name="iconName(item.value)" class="d2-mr-5" />{{ item.label }}
      </el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex';
export default {
  name: 'd2-header-size',
  data() {
    return {
      fontDefault: '',
      fontMedium: '',
      fontMini: '',
      fontSmall: '',
      options: [],
    };
  },
  computed: {
    ...mapState('d2admin/size', ['value']),
  },
  mounted() {
    this.initI18nStr();
  },
  watch: {
    '$i18n.locale': 'i18nHandle',
  },
  methods: {
    ...mapMutations({
      pageKeepAliveClean: 'd2admin/page/keepAliveClean',
    }),
    ...mapActions({
      sizeSet: 'd2admin/size/set',
    }),
    initI18nStr() {
      this.fontDefault = this.$t('layout.header-aside.header-size.options.default');
      this.fontMedium = this.$t('layout.header-aside.header-size.options.medium');
      this.fontMini = this.$t('layout.header-aside.header-size.options.mini');
      this.fontSmall = this.$t('layout.header-aside.header-size.options.small');
      const array = [
        // { label: '默认', value: 'default' },
        { label: this.fontDefault, value: 'default' },
        { label: this.fontMedium, value: 'medium' },
        { label: this.fontMini, value: 'small' },
        { label: this.fontSmall, value: 'mini' },
      ];
      this.options = [].concat(array);
    },
    handleChange(value) {
      this.sizeSet(value);
      this.$notify({
        title: '提示',
        dangerouslyUseHTMLString: true,
        message: '已更新页面内 <b>组件</b> 的 <b>默认尺寸</b><br/>例如按钮大小，<b>非字号</b>',
        type: 'success',
      });
    },
    iconName(name) {
      return name === this.value ? 'dot-circle-o' : 'circle-o';
    },
    i18nHandle(value, oldVal) {
      this.initI18nStr();
    },
  },
};
</script>
