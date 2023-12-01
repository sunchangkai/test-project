<template>
  <div>
    <el-tooltip effect="dark" :content="notificationTitle" placement="bottom">
      <el-popover placement="bottom" width="400" trigger="click">
        <msg-list :msgObj="msgObj"></msg-list>
        <el-button
          class="d2-ml-0 d2-mr btn-text can-hover"
          type="text"
          slot="reference"
          @click="getList"
        >
          <el-badge v-if="unread > 0" :max="99" :value="unread" :is-dot="unread === 0">
            <d2-icon :name="unread === 0 ? 'dot-circle-o' : 'bell-o'" style="font-size: 20px" />
          </el-badge>
          <d2-icon v-else name="bell-o" style="font-size: 16px" />
        </el-button>
      </el-popover>
    </el-tooltip>
  </div>
</template>

<script>
import msgList from './components/msg-list';
import { request } from '@/api/service';
import { mapGetters } from 'vuex';
export default {
  computed: {
    ...mapGetters('d2admin', {
      unread: 'messagecenter/unread',
    }),
  },
  components: {
    msgList,
  },
  data() {
    return {
      msgObj: null,
      notificationTitle: '',
    };
  },
  mounted() {
    this.initI18nStr();
  },
  watch: {
    '$i18n.locale': 'i18nHandle',
  },
  methods: {
    getList() {
      request({
        url: '/api/system/message_center/get_newest_msg/',
        method: 'get',
        params: {},
      }).then(res => {
        const { data } = res;
        this.msgObj = data;
      });
    },
    initI18nStr() {
      this.notificationTitle = this.$t('global.notification');
    },
    i18nHandle(value, oldVal) {
      this.initI18nStr();
    },
  },
};
</script>
