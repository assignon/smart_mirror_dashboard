<template>
  <div v-if="!$route.name.startsWith('Login')" class="hidden-sm-and-down mt-9 mb-9" role="navigation"
       aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" href="/">
        <v-img src="@/assets/logo.svg"></v-img>
      </a>
      <strong class="is-size-4">Smart Mirror</strong>
    </div>
    <div id="navbar" class="navbar-menu">
      <div class="navbar-start">
        <router-link to="/checkin" class="navbar-item">Checkin</router-link>
        <router-link to="/ingecheckt" class="navbar-item"
          >Ingecheckt</router-link
        >
        <router-link to="/zoeken" class="navbar-item">Zoeken</router-link>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <router-link
              v-if="authenticated"
              to="/login"
              v-on:click.native="logout()"
              replace
              >Logout</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "Navbar",
  methods: {
    setAuthenticated(status) {
      this.authenticated = status;
    },
    logout() {
      this.authenticated = false;
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
  color: #2c3e50;
  width: 100%;
}
</style>
