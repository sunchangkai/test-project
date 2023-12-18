<template>
  <el-tooltip effect="dark" :content="screenTip" placement="bottom">
    <el-button class="d2-mr btn-text can-hover" type="text" @click="toggle">
      <d2-icon v-if="active" name="compress" />
      <d2-icon v-else name="arrows-alt" style="font-size: 16px" />
    </el-button>
  </el-tooltip>
</template>

<script>
import { mapState, mapActions } from 'vuex';
export default {
  data() {
    return {
      fullScreenText: '',
      unfullScreenText: '',
      screenTip: '',
    };
  },
  computed: {
    ...mapState('d2admin/fullscreen', ['active']),
  },
  watch: {
    '$i18n.locale': 'i18nHandle',
    active(value, oldValue) {
      this.screenTip = this.active ? this.unfullScreenText : this.fullScreenText;
    },
  },
  mounted() {
    this.initI18nStr();
  },
  methods: {
    ...mapActions('d2admin/fullscreen', ['toggle']),
    i18nHandle(value, oldVal) {
      this.fullScreenText = this.$t('layout.header-aside.header-fullscreen.active');
      this.unfullScreenText = this.$t('layout.header-aside.header-fullscreen.exit');
      this.screenTip = this.active ? this.unfullScreenText : this.fullScreenText;
    },
    initI18nStr() {
      this.fullScreenText = this.$t('layout.header-aside.header-fullscreen.active');
      this.unfullScreenText = this.$t('layout.header-aside.header-fullscreen.exit');
      this.screenTip = this.active ? this.unfullScreenText : this.fullScreenText;
    },
  },
};
</script>
