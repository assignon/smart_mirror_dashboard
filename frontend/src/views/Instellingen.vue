<template>
  <div>
    <h1>Instellingen</h1>
    <v-form class="login-form mt-9">
      <v-text-field
          label="Username"
      ></v-text-field>
      <v-text-field
          label="Password"
          type="password"
      ></v-text-field>
      <v-text-field
          label="Password herhalen"
          type="password"
      ></v-text-field>
      <v-btn
          class="mt-9"
          elevation="6"
          v-on:click="login()"
      >Bevestigen
      </v-btn>
    </v-form>
  </div>

</template>

<script>

export default {
  name: "Instellingen",
  components: {}
};
</script>

<style scoped>
div {
  width: 300px;
  margin: auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>