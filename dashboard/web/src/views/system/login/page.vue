<template>
  <div
    class="w3l-signinform"
    :style="{
      background: 'url(' + (loginBackground || require('./image/bg.jpg')) + ') no-repeat center',
      backgroundSize: '100% 100%',
    }"
  >
    <!-- container -->
    <div class="wrapper">
      <!-- main content -->
      <div class="w3l-form-info">
        <!-- logo -->
        <h2 class="w3_info_big">C&nbsp;A&nbsp; R&nbsp; I&nbsp; A&nbsp; D</h2>
        <div class="w3_info">
          <div class="lines">
            <span class="line"></span><span id="font">ProSafeAI</span><span class="line"></span>
          </div>

          <el-card shadow="always" class="card">
            <el-tabs v-model="activeName">
              <el-tab-pane label="Account password login" name="first" stretch="true">
                <span slot="label" class="span"> Account password login</span>
                <br />
                <el-form
                  ref="loginForm"
                  label-position="top"
                  :rules="rules"
                  :model="formLogin"
                  size="default"
                >
                  <el-form-item prop="username">
                    <el-input
                      type="text"
                      v-model="formLogin.username"
                      prefix-icon="el-icon-user-solid"
                      placeholder="please input username"
                    >
                    </el-input>
                  </el-form-item>
                  <el-form-item prop="password">
                    <el-input
                      type="password"
                      v-model="formLogin.password"
                      prefix-icon="el-icon-s-promotion"
                      show-password
                      placeholder="please input password"
                      @keyup.enter.native="submit"
                    >
                    </el-input>
                  </el-form-item>
                  <el-form-item
                    prop="captcha"
                    v-if="captchaState"
                    :rules="{ required: true, message: 'verification code', trigger: 'blur' }"
                  >
                    <el-input
                      type="text"
                      v-model="formLogin.captcha"
                      placeholder="verification code"
                      @keyup.enter.native="submit"
                    >
                      <template slot="append">
                        <img
                          class="login-code"
                          style="cursor: pointer;"
                          height="33px"
                          width="145px"
                          slot="suffix"
                          :src="image_base"
                          @click="getCaptcha"
                        />
                      </template>
                    </el-input>
                  </el-form-item>
                </el-form>
                <button
                  class="btn btn-primary btn-block"
                  style="padding: 10px 10px;"
                  @click="submit"
                >
                  Login
                </button>
                <component v-if="componentTag" :is="componentTag"></component>
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </div>
      </div>
      <!-- //main content -->
    </div>
  </div>
</template>
<script>
import base from './base.vue';
const pluginImport = require('@/libs/util.import.plugin');
export default {
  extends: base,
  name: 'page',
  data() {
    return {
      activeName: 'first',
      componentTag: '',
    };
  },
  created() {
    // 注册第三方登录插件
    var componentTag = '';
    try {
      componentTag = pluginImport('dvadmin-third-web/src/login/index');
    } catch (error) {
      componentTag = '';
    }
    this.componentTag = componentTag;
  },
  mounted() {},
  methods: {},
};
</script>

<style lang="scss" scoped>
@import './css/style.css';

.copyrights {
  text-indent: -9999px;
  height: 0;
  line-height: 0;
  font-size: 0;
  overflow: hidden;
}

// 快速选择用户面板
.page-login--quick {
  margin-top: 20px;
}

.page-login--quick-user {
  @extend %flex-center-col;
  padding: 10px 0px;
  border-radius: 4px;

  &:hover {
    background-color: $color-bg;

    i {
      color: $color-text-normal;
    }

    span {
      color: $color-text-normal;
    }
  }

  i {
    font-size: 36px;
    color: $color-text-sub;
  }

  span {
    font-size: 12px;
    margin-top: 10px;
    color: $color-text-sub;
  }
}
</style>
