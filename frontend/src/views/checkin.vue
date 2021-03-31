<template>
  <div>
    <h1>Nieuwe gemelde gasten</h1>
    <div class="row mt-15">
      <div class="col">
        <v-text-field label="Naam" v-model="message1" outlined dense></v-text-field>
        <v-text-field label="Email" v-model="message1" outlined dense></v-text-field>
        <v-text-field label="Telefoon" v-model="message1" outlined dense></v-text-field>
        <v-btn class="mx-2" @click="onButtonClick(message1)">
          Check-in
        </v-btn>
      </div>
      <div class="col">
        <v-text-field label="Afspraak met" v-model="message1" outlined dense></v-text-field>
        <v-text-field label="Kenteken " v-model="message1" outlined dense></v-text-field>
        <v-text-field label="Bedrijf" v-model="message1" outlined dense></v-text-field>
        <v-select
            :items="items"
            label="Bewaartermijn"
            outlined dense
        ></v-select>
      </div>
      <div class="col">
        <v-img
            contain
            lazy-src="https://picsum.photos/id/11/10/6"
            max-height="300"
            max-width="290"
            src="https://picsum.photos/id/11/500/300"
        ></v-img>
      </div>

    </div>
    <div class="row mt-15">
      <div class="col">
        <v-text-field label="Naam" v-model="message1" outlined dense></v-text-field>
        <v-text-field label="Email" v-model="message1" outlined dense></v-text-field>
        <v-text-field label="Telefoon" v-model="message1" outlined dense></v-text-field>
        <v-btn class="mx-2" @click="onButtonClick(message1)">
          Check-in
        </v-btn>
      </div>
      <div class="col">
        <v-text-field label="Afspraak met" v-model="message1" outlined dense></v-text-field>
        <v-text-field label="Kenteken " v-model="message1" outlined dense></v-text-field>
        <v-text-field label="Bedrijf" v-model="message1" outlined dense></v-text-field>
        <v-select
            :items="items"
            label="Bewaartermijn"
            outlined dense
        ></v-select>
      </div>
      <div class="col">
        <v-img
            contain
            lazy-src="https://picsum.photos/id/11/10/6"
            max-height="300"
            max-width="290"
            src="https://picsum.photos/id/11/500/300"
        ></v-img>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "Checkin",
  methods: {
    onButtonClick() {
      //Todo API call + desserts.id
      console.log('/')
    }
  },
  component: {},
  data() {
    return {
      message1: "Wes",
      items: ['1 DAG','1 JAAR'],
    };
  }
};
</script>

<style scoped>
.row {
  width: 1000px;
  margin: auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

div .col {
  width: 32%;
}
</style>
