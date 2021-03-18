<template>
  <v-app id="app">
    <v-main>
      <Navbar />
      <router-view class="animated fadeIn" @authenticated="setAuthenticated" />
    </v-main>
  </v-app>
</template>

<script>
import Navbar from "@/components/layouts/Navbar";
export default {
  name: "App",
  components: {
    Navbar
  },
  data: () => ({
    return: {
      authenticated: false,
    }
  }),
  created() {
    if (!this.$session.get("authenticated")) {
      this.$router.push({name: "Login"})
    }
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
