import Vue from "vue";
import Vuex from "vuex";

import dashboard from "./modules/dashboard";  // store file from modules map import example

import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    HOST:
      window.location.port != ""
        ? "http://127.0.0.1:5000"
        : "live-server",
      //  "http://127.0.0.1:8000",
    AUTHENTICATED: undefined,
    usertoken: undefined,
    // vuetify form validator
    rules: {
      required: value => !!value || "This field is required",
      min: v => v.length >= 8 || "8 characters minimal",
      textareaMin: v => v.length >= 10 || "100 characters minimal",
      emailMatch: () => "Email and password don't match"
    },
    emailRules: [
      v => !!v || "Email is required",
      v => /.+@.+/.test(v) || "Email is not valid"
    ],
  },

  getters: {
    setData: (state) => (data) => {
      // data[array]: contain array and api response data
      console.log(state);

      if (data[0].length > 0) {
        data[0].length = 0
      }
      data[1].forEach((items) => {
        data[0].push(items)
      })
    },
    
    getRandomString: (state) => (length) => {
      console.log(state);
      let randomChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let result = '';
      for ( var i = 0; i < length; i++ ) {
          result += randomChars.charAt(Math.floor(Math.random() * randomChars.length));
      }
      return result;
    },
  },

  mutations: {
    splitToArray(state, str) {
      /*
      split a string words in to array
      params:
        str: [str]: [string to split]
      returns: return array
      */
      let arr = str.split(",");
      return arr;
    },

    get$(state, session, key) {
     /*  get session data by key
      params:
        state
        key:[str]: session key
        session:[$session obj]: session instance */
      return session.get(key)
    },

    destroy$(state, session) {
     /*  destroy session
      params:
        state
        session:[$session obj]: session instance */
      session.destroy()
    },

    getAxiosCall(state, payload) {
      /*
                      http get request
                      params:
                          payload: [object]: [data sended with the request]
                  */
      axios
        .get(`${payload.host}/api/${payload.url}/`, {
          params: payload.params,
          headers: {
              "X-CSRFToken": payload.csrftoken,
              Authorization: `token ${payload.auth}`,
          },
        })
        .then(response => {
          let res = response.data;
          payload.callback(res);
        })
        .catch(error => {
          console.log(error);
        });
    },

    postAxiosCall(state, payload) {
      /*
           http post request
           params:
               payload: [object]: [data sended with the request]
       */
      let body = {
        body: payload.params
      }
      axios
        .post(`${payload.host}/api/${payload.url}/`, body,{
          headers: {
              "X-CSRFToken": payload.csrftoken,
              Authorization: `token ${payload.auth}`,
          },
        })
        .then(response => {
          let res = response.data;
          payload.callback(res);
        })
        .catch(error => {
          console.log(error);
        });
    },

    publicPostAxiosCall(state, payload) {
      /*
           http post request
           params:
               payload: [object]: [data sended with the request]
       */
      axios
        .post(`${payload.host}/api/${payload.url}/`, {
          body: payload.params,
          headers: {
              "X-CSRFToken": payload.csrftoken,
              Authorization: `token ${payload.auth}`,
          },
        })
        .then(response => {
          let res = response.data;
          payload.callback(res);
        })
        .catch(error => {
          console.log(error);
        });
    },

    putAxiosCall(state, payload) {
      /*
           http put request
           params:
               payload: [object]: [data sended with the request]
       */
      let body = {
        body: payload.params
      }
      axios
        .put(`${payload.host}/api/${payload.url}/`, body, {
          headers: {
              "X-CSRFToken": payload.csrftoken,
              Authorization: `token ${payload.auth}`,
          },
        })
        .then(response => {
          let res = response.data;
          payload.callback(res);
        })
        .catch(error => {
          console.log(error);
        });
    },

    deleteAxiosCall(state, payload) {
      /*
           http delete request
           params:
               payload: [object]: [data sended with the request]
       */
      axios
        .delete(`${payload.host}/api/${payload.url}/`, {
          params: payload.params,
          headers: {
              "X-CSRFToken": payload.csrftoken,
              Authorization: `token ${payload.auth}`,
          },
        })
        .then(response => {
          let res = response.data;
          payload.callback(res);
        })
        .catch(error => {
          console.log(error);
        });
    },
  },

  actions: {
    getReq({ commit, rootState }, payload) {
      commit("getAxiosCall", {
        url: payload.url,
        params: payload.params,
        auth: payload.auth,
        csrftoken: payload.csrftoken,
        callback: payload.callback,
        host: rootState.HOST,
      });
    },

    publicPostReq({ commit, rootState }, payload) {
      commit("publicPostAxiosCall", {
        url: payload.url,
        params: payload.params,
        auth: payload.auth,
        csrftoken: payload.csrftoken,
        callback: payload.callback,
        host: rootState.HOST,
      });
    },

    postReq({ commit, rootState }, payload) {
      commit("postAxiosCall", {
        url: payload.url,
        params: payload.params,
        auth: payload.auth,
        csrftoken: payload.csrftoken,
        callback: payload.callback,
        host: rootState.HOST,
      });
    },

    putReq({ commit, rootState }, payload) {
      commit("putAxiosCall", {
        url: payload.url,
        params: payload.params,
        auth: payload.auth,
        csrftoken: payload.csrftoken,
        callback: payload.callback,
        host: rootState.HOST,
      });
    },

    deleteReq({ commit, rootState }, payload) {
      commit("deleteAxiosCall", {
        url: payload.url,
        params: payload.params,
        auth: payload.auth,
        csrftoken: payload.csrftoken,
        callback: payload.callback,
        host: rootState.HOST,
      });
    },
  },

  modules: {
    dashboard: dashboard,
  }
});