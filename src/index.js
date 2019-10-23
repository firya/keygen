import Vue from 'vue';
import Vuex from 'vuex';
import VueRouter from 'vue-router';

import router from './routes.js';
import store from './store.js';

import App from './app.vue';

Vue.use(VueRouter)

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});