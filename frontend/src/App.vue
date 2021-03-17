<template>
  <v-app id='app'>
    <v-main>
      <div id="nav">
        <router-link v-if="authenticated" to="/login" v-on:click.native="logout()" replace>Logout</router-link>
        <Nav v-if="!$route.name.startsWith('Login')" class='hidden-md-and-up'/>
      </div>
      <router-view class="animated fadeIn" @authenticated="setAuthenticated"/>
    </v-main>
  </v-app>
</template>

<script>
import Nav from "./components/layouts/Nav";

export default {
  name: "App",
  components: {
    Nav,
  },
  data: () => ({
    return: {
      authenticated: false,
      mockAccount: {
        username: "test",
        password: "test"
      }
    }
  }),
  created() {
    if (!this.authenticated) {
      // this.$router.replace({name: "Login"})
    }
  },
  methods: {
    setAuthenticated(status) {
      this.authenticated = status;
    },
    logout() {
      this.authenticated = false;
    }
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
