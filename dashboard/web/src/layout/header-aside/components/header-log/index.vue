<!--
 * @创建文件时间: 2021-06-01 22:41:20
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-06-09 11:37:44
 * 联系Qq:1638245306
 * @文件介绍: 前端日志
-->
<template>
  <el-tooltip effect="dark" :content="title" placement="bottom">
    <el-button class="d2-ml-0 d2-mr btn-text can-hover" type="text" @click="handleClick">
      <el-badge
        v-if="logLength > 0"
        :max="99"
        :value="logLengthError"
        :is-dot="logLengthError === 0"
      >
        <d2-icon :name="logLengthError === 0 ? 'dot-circle-o' : 'bug'" style="font-size: 20px" />
      </el-badge>
      <d2-icon v-else name="dot-circle-o" style="font-size: 20px" />
    </el-button>
  </el-tooltip>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
export default {
  data() {
    return {
      title: '',
    };
  },
  mounted() {
    this.initI18nStr();
  },
  watch: {
    '$i18n.locale': 'i18nHandle',
  },
  computed: {
    ...mapGetters('d2admin', {
      logLength: 'log/length',
      logLengthError: 'log/lengthError',
    }),
  },
  methods: {
    ...mapMutations('d2admin/log', ['clean']),
    handleClick() {
      this.$router.push({
        name: 'frontendLog',
      });
    },
    i18nHandle(value, oldVal) {
      this.initI18nStr();
    },
    // eslint-disable-next-line vue/return-in-computed-property
    initI18nStr() {
      const noLog = this.$t('layout.header-aside.header-log.empty');
      const logFormat = this.$t('layout.header-aside.header-log.log-length', {
        length: this.logLength,
      });
      const errFormat = this.$t('layout.header-aside.header-log.error-length', {
        length: this.logLengthError,
      });
      const errorStr = this.logLengthError > 0 ? errFormat : '';
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      this.title = this.logLength === 0 ? noLog : logFormat + errorStr;
    },
  },
};
</script>
