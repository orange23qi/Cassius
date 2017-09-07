import Vue from 'vue';
import Login from './Login.vue';
import BootstrapVue from 'bootstrap-vue';
import './css/main.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import VueResource from "vue-resource";
Vue.use(VueResource);
Vue.use(BootstrapVue);
new Vue({
  el: '#app',
  render: h => h(Login)
});
