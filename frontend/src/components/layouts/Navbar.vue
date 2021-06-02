<template>
  <!-- Hide Nav if route is Login -->
  <div
    v-if="!$route.name.startsWith('Login')"
    class="hidden-sm-and-down mt-9"
    role="navigation"
    aria-label="main navigation"
  >
    <!-- Left side + Logo -->
    <div class="navbar-brand">
      <a class="navbar-item" href="/">
        <v-img
          src="@/assets/SogetiLabs_Logo_Primary_3COL_RGB (002).png"
          max-height="88"
          max-width="248"
        ></v-img>
      </a>
    </div>
    <!-- Right side Nav items -->
    <div id="navbar" class="navbar-menu">
      <div class="navbar-start">
        <router-link to="/ingecheckt" class="navbar-item"
          >In/Uit-checken</router-link
        >
        <router-link to="/clients" class="navbar-item">Gasten</router-link>
        <router-link to="/instellingen" class="navbar-item">
          Instellingen</router-link
        >
        <div class="navbar-item">
          <div class="buttons">
            <router-link v-if="(this.$session.su = true)" to="/admin" replace
              >Admin</router-link
            >
          </div>
        </div>
        <div class="navbar-item">
          <div class="buttons">
            <p
              style='color: #0070ad;cursor:pointer;font-weight:bold; position: relative;bottom:2px;'
              v-if="$session.get('authenticated')"
              @click="logout()"
              
              >
              Logout
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "Navbar",

  data() {
    return {
      authenticated: true,
      su: true
    };
  },

  methods: {
    setAuthenticated(status) {
      this.authenticated = status;
    },

    setSu(){

    },

    logout() {
      let self = this;
      this.$store.dispatch("getReq", {
        url: "logout",
        params: {
        },
        auth: self.$session.get('token'),
        csrftoken: self.$session.get('token'),
        callback: function(res) {
            if(res.data.logout){
                self.$session.destroy();
                self.$router.push({name: 'Login'})
            }
        },
      });
    }
  }
};
</script>
<style scoped>
div {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  gap: 30px;
}
div a {
  text-decoration: none;
  font-weight: bold;
  color: #0070AD;
  padding-bottom: 22px;
}
.router-link-exact-active{
  border-bottom: 2px solid #FF304C;
  color: #FF304C;
}
</style>
