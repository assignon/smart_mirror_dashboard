<template>
  <v-app id='app'>
    <v-main>
      <Nav v-if="!$route.name.startsWith('Login')" class='hidden-md-and-up' />
      <router-view class="animated fadeIn"></router-view>
    </v-main>
  </v-app>    
</template>

<script>
import Nav from "./components/layouts/Nav"

export default {
  name: "App",

  components: {
    Nav
  },

  data: () => ({
    //
  }),

  created(){},

  methods: {}
};
</script>

<style scoped>
html,
body {
  scroll-behavior: smooth;
  overflow-x: hidden;
  width: 100%;
  margin: 0px;
  padding: 0px;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0px;
  padding: 0px;
  width: 100%;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>