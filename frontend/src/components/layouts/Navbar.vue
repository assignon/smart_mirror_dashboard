<template>
  <nav
    v-if="!$route.name.startsWith('Login')"
    class="hidden-md-and-up"
    role="navigation"
    aria-label="main navigation"
  >
    <div class="navbar-brand">
      <a class="navbar-item" href="/">
        <strong class="is-size-4">Soggeti Mirror</strong>
      </a>
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
  </nav>
</template>
<script>
export default {
  name: "Navbar"
};
</script>
<style lang="scss" scoped>
nav {
  margin-top: 25px;
  margin-bottom: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
  }
}
</style>
