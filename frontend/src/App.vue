<template>
  <v-app id='app'>
    <v-main>
      <Nav v-if="!$route.name.startsWith('Login')" class='hidden-md-and-up' />
      <router-view class="animated fadeIn"></router-view>
    </v-main>
  </v-app>
</template>

<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.4.5/socket.io.min.js"></script>
<script>
import Nav from "./components/layouts/Nav";
export default {
  name: "App",
  components: {
    Nav,
  },
  data: () => ({
    //
  }),
  created(){
    
  },
  methods: {
    // createSession() {
    //   if (!this.$session.has("auth")) {
    //     this.$session.start();
    //     this.$session.set("auth", false);
    //   }
    //   this.$store.state.AUTHENTICATED = this.$session.get("auth");
    //   // console.log(this.$store.state.AUTHENTICATED);
    // },
  }
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
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /* color: #2c3e50; */
  margin: 0px;
  padding: 0px;
  width: 100%;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
