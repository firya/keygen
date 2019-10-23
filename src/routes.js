import VueRouter from 'vue-router';

import Home from './components/Home.vue';
import NotFound from './components/404.vue';

export default new VueRouter({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    }, {
      path: '/404',
      name: '404',
      component: NotFound,
    }, {
      path: '*',
      redirect: '/404'
    }
  ],
  mode: 'history'
});