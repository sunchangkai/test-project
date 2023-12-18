import Vue from 'vue';
import Vuex from 'vuex';

import d2admin from './modules/d2admin';

Vue.use(Vuex);

export default new Vuex.Store({
  // 定义全局变量
  state: {
    tableid: '-1',
    objectnumber: -1,
  },

  getters: {},

  mutations: {
    changeid(state, tableid) {
      state.tableid = tableid;
    },
    saveObjectnumber(state, number) {
      state.objectnumber = number;
    },
  },
  actions: {},

  modules: {
    d2admin,
  },
});
