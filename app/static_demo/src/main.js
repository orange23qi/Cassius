import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue';
import Login from './Login.vue';
import Register from './Register.vue';

import BootstrapVue from 'bootstrap-vue';
import './css/main.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import VueResource from "vue-resource";

Vue.use(VueRouter);
Vue.use(VueResource);
Vue.use(BootstrapVue);

const routes = [
	{
		path : '/register',
		component : Register
	},
	{
		path : '/login',
		component : Login
	},
	{
		path : '/',
		component : Register
	}
];

const router = new VueRouter({
	routes,
	mode : 'history'
});

new Vue({
  el: '#app',
  router,
  render: h => h(App)
});
