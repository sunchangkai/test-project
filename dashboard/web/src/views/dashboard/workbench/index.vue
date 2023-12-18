<template>
  <d2-container>
    <div class="page-header">
      <el-avatar :src="info.avatar" class="user-avatar"> </el-avatar>
      <div class="title">
        <h1>Morning {{ info.name }}</h1>
        <span> Login time: {{ loginTime }} </span>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Quick navigation</span>
          </div>
          <el-row>
            <el-col
              :span="12"
              v-for="({ name, icon, route, color }, index) of navigators"
              :key="index"
              style="padding: 0"
            >
              <el-card shadow="hover" class="box-menu">
                <div
                  style="display: flex;align-items: center;flex-direction: column;cursor: pointer"
                  @click="
                    () => {
                      gotoRoute(route);
                    }
                  "
                >
                  <el-image
                    :src="icon"
                    style="width: 70px;height: 70px;background-color: transparent"
                  />
                  <div
                    style="text-align: center;font-size: 20px;margin-top: 10px"
                    v-text="name"
                  ></div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>

      <el-col :span="12">
        <div class="grid-content bg-purple">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>&nbsp;</span>
            </div>

            <div class="box-menu-right">
              <d2-icon-svg
                name="work"
                style="margin-left: 50%;transform: translateX(-50%);height: 216px"
              />
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </d2-container>
</template>

<script>
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import { mapState } from 'vuex';

use([CanvasRenderer, PieChart, TitleComponent, TooltipComponent, LegendComponent]);
export default {
  name: 'workbench',
  computed: {
    ...mapState('d2admin/user', ['info']),
  },
  mounted() {
    this.loginTime = this.formatDate();
    // console.log('info:' + JSON.stringify(this.info))
    // n 输出结果: 2021/1/8 上午10:12:26
  },
  data() {
    return {
      logLength: 6,
      logLengthError: 1,
      loginTime: '',
      navigators: [
        {
          name: 'Data management',
          icon: require('./image/main-datamanage.png'),
          route: {
            // 配置每个组件的name属性
            name: 'dataManagement',
          },
          color: 'rgb(31, 218, 202);',
        },
        {
          name: 'Data display',
          icon: require('./image/main-visual.png'),
          route: {
            name: 'dataDisplay',
          },
          color: 'rgb(225, 133, 37);',
        },
        {
          name: 'Data verification',
          icon: require('./image/main-check.png'),
          route: {
            name: 'ProsafeAIDataVerification',
          },
          color: 'rgb(191, 12, 44);',
        },
        {
          name: 'Model testing',
          icon: require('./image/main-test.png'),
          route: {
            name: 'bmTaskList',
          },
          color: 'rgb(63, 178, 127);',
        },
      ],
    };
  },
  methods: {
    gotoRoute(route) {
      this.$router.push(route);
    },
    // 不输入参数调用的就是当前时间
    // 参数--需转换时间的时间戳
    formatDate(time = new Date()) {
      const date = new Date(time);
      const YY = date.getFullYear();
      const MM = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
      const DD = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
      const hh = date.getHours() < 10 ? '0' + date.getHours() : date.getHours();
      const mm = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes();
      const ss = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds();
      // 这里修改返回时间的格式
      return MM + '/' + DD + '/' + YY + ' ' + hh + ':' + mm + ':' + ss;
    },
  },
};
</script>

<style scoped lang="scss">
$userAvatarLength: 72px;
.box-menu {
  /*style="height: 120px;background-color: blue"*/
  height: 150px;
}

.box-menu-right {
  /*style="height: 120px;background-color: blue"*/
  height: 300px;
}

.page-header {
  box-sizing: border-box;
  padding: 16px;

  .user-avatar {
    width: $userAvatarLength;
    height: $userAvatarLength;
    line-height: $userAvatarLength;
    display: inline-block;
  }

  .title {
    display: inline-block;
    padding: 0 0 0 15px;
    position: relative;
    top: -5px;

    h1 {
      font-size: 1.125rem;
      font-weight: 500;
      line-height: 1.75rem;
    }

    span {
      font-size: 14px;
      color: rgba(0, 0, 0, 0.45);
    }
  }
}

.project-detail {
  color: rgba(0, 0, 0, 0.45);
  height: 65px;

  img {
    width: 25px;
    height: 25px;
  }

  .name {
    margin-left: 1rem;
    font-size: 1rem;
    line-height: 2rem;
    height: 2rem;
    display: inline-block;
    color: rgba(0, 0, 0, 0.85);
    position: relative;
    top: -5px;
  }

  .slogan {
    font-size: 12px;
    padding: 5px 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .team {
    font-size: 14px;
  }
}

.activity {
  padding: 0;

  .activity-avatar {
    width: 40px;
    height: 40px;
    line-height: 40px;
  }

  .activity-detail {
    padding: 10px;
    line-height: 15px;
    font-size: 14px;
    color: rgba(0, 0, 0, 0.85);
  }
}

.chart {
  height: 408px;
}

.el-divider--horizontal {
  margin: 4px 0;
  background: 0 0;
  border-top: 1px solid #e8eaec;
}

.el-card,
.el-message {
  border-radius: 0;
}
</style>
