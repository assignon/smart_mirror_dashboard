import "material-design-icons-iconfont/dist/material-design-icons.css";
// import "vue-material-design-icons/styles.css";
import "@fortawesome/fontawesome-free/css/all.css";
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./registerServiceWorker";
import VAnimateCss from "v-animate-css";
import Vuex from "vuex";
import Axios from "axios";

// vue session
import VueSession from "vue-session";

import vuetify from "./plugins/vuetify";

Vue.config.productionTip = false;
Vue.use(VAnimateCss);
Vue.use(Vuex);
Vue.use(VueSession, { persist: true });

Axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
Axios.defaults.xsrfCookieName = "XCSRF-TOKEN";
Axios.defaults.withCredentials = false;

Vue.prototype.$axios = Axios;

new Vue({
  created() {},
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
