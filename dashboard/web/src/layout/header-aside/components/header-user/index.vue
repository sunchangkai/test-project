<!--
 * @创建文件时间: 2021-06-01 22:41:20
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-07-27 00:18:52
 * 联系Qq:1638245306
 * @文件介绍:
-->
<template>
  <el-dropdown size="small" class="d2-mr">
    <el-link
      type="primary"
      :underline="false"
      style="margin-bottom: 2px;margin-left: 10px"
      v-if="isTenants"
    >
      <span> 当前租户：{{ info.tenant_name }} </span>
      <span class="btn-text">{{ info.name ? `hello ${info.name}` : 'not logged in' }}</span>
    </el-link>
    <span class="btn-text" v-else>{{ info.name ? `hello ${info.name}` : 'not logged in' }}</span>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item @click.native="userInfo">
        <d2-icon name="cog" class="d2-mr-5" />
        {{ userinfo }}
      </el-dropdown-item>
      <el-dropdown-item @click.native="logOff" divided>
        <d2-icon name="power-off" class="d2-mr-5" />
        {{ exit }}
      </el-dropdown-item>
    </el-dropdown-menu>
    <el-image
      v-if="info.avatar"
      :src="info.avatar"
      :preview-src-list="[info.avatar]"
      style="width: 20px;height: 20px;border-radius: 20%;top: 5px;"
      alt="头像"
    ></el-image>
  </el-dropdown>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  computed: {
    ...mapState('d2admin/user', ['info']),
  },
  data() {
    return {
      userinfo: '',
      exit: '',
      isTenants: window.pluginsAll && window.pluginsAll.indexOf('dvadmin-tenants-web') !== -1,
    };
  },
  mounted() {
    this.initI18nStr();
  },
  watch: {
    '$i18n.locale': 'i18nHandle',
  },
  methods: {
    ...mapActions('d2admin/account', ['logout']),
    initI18nStr() {
      this.userinfo = this.$t('global.user-info');
      this.exit = this.$t('layout.header-aside.header-user.log-off');
    },
    i18nHandle(value, oldVal) {
      this.initI18nStr();
    },
    /**
     * @description 登出
     */
    logOff() {
      this.logout({
        confirm: true,
      });
    },
    /** 个人信息 */
    userInfo() {
      this.$router.push({ path: 'userInfo' });
    },
  },
};
</script>
