<template>
  <div class='checkin-core'>
    <h1>Nieuwe gemelde gasten</h1>
    
    <CheckinTemp />
    <div class='no-checkin' v-if='$store.state.appointmentArr.length==0'>
        <v-icon style='font-size: 100px;color:black' class='mb-3'>fas fa-user</v-icon>
        <p>Geen nieuwe gemelde gasten</p>
    </div>

    <!-- <div class="row mt-15">
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

    </div> -->

  </div>
</template>

<script>
import CheckinTemp from "../components/layouts/CheckinTemp";

export default {
  name: "Checkin",

  components: {
    CheckinTemp,
  },

  data() {
    return {
      msgServer: '',
    };
  },

  created(){

  },

  methods: {

  }
};
</script>

<style scoped>
  .checkin-core{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: auto;
  }
   .no-checkin{
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      width: 100%;
      height: 70vh;
  }
  .no-checkin p{
      text-align: center;
      font-size: 20px;
      font-weight: bold;
  }
</style>
