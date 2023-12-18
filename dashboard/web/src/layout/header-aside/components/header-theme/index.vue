<template>
  <div>
    <el-tooltip effect="dark" :content="title" placement="bottom">
      <el-button class="d2-ml-0 d2-mr btn-text can-hover" type="text" @click="dialogVisible = true">
        <d2-icon name="diamond" style="font-size: 16px" />
      </el-button>
    </el-tooltip>
    <el-dialog :title="title" width="600px" :visible.sync="dialogVisible" :append-to-body="true">
      <d2-theme-list style="margin-top: -25px;" />
    </el-dialog>
  </div>
</template>

<script>
import themeList from './components/d2-theme-list';
export default {
  components: {
    'd2-theme-list': themeList,
  },
  data() {
    return {
      title: '',
      dialogVisible: false,
    };
  },
  mounted() {
    this.initI18nStr();
  },
  watch: {
    '$i18n.locale': 'i18nHandle',
  },
  methods: {
    initI18nStr() {
      this.title = this.$t('layout.header-aside.header-theme.dialog.title');
    },
    i18nHandle(value, oldVal) {
      this.initI18nStr();
    },
  },
};
</script>
