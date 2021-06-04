<template>
  <section class="primary-section">
    <div class="main-container">
      <div>
        <h1 class="mb-9 mt-12">Instellingen</h1>
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
              rounded
              v-on:click="login()"
          >
            <v-icon color="green">mdi-content-save</v-icon>
          </v-btn>
        </v-form>
      </div>
    </div>
  </section>


</template>

<script>

export default {
  name: "Instellingen",
  components: {}
};
</script>

<style scoped>
.main-container {
  width: 900px;
  height: 80vh;
  margin: auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.primary-section {
  background-color: beige;
  min-height: 500px;
}
</style>