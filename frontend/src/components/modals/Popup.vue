<template>
  <div class="text-center">
    <v-dialog
      v-model="dialog"
      width="600"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="red lighten-2"
          dark
          v-bind="attrs"
          v-on="on"
          class="mt-9"
          elevation="6"
        >
          bevestigen
        </v-btn>
      </template>

      <v-card>
        
        <v-card-title class="headline grey lighten-2">
          Weet u zeker dat u het wachtwoord wilt wijzigen?
        </v-card-title>

        <!-- <v-card-text>
          Weet u zeker dat u het wachtwoord wil wijzigen?
        </v-card-text> -->

        <!-- <v-divider></v-divider> -->

        <v-card-actions class="v-card-actions">

          <v-btn
            color="primary"
            text
            @click="dialog = false"            
          >
            Ja
          </v-btn>
          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
            Nee
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
  export default {
    data () {
      return {
        dialog: false,
      }
    },
    methods: {
      validate () {
        this.$refs.observer.validate()
      },
      test () {
        console.log(this.input.password_new)
      },
    }
  }
</script>

<style scoped>
div {
  /* margin: auto;
  display: flex;
  flex-wrap: wrap; */
  justify-content: center;
}

.v-card-actions {
    position: relative;
    color: black;
}



/* .v-spacer {
    width: 30vw;
} */

.v-card__actions > .v-btn.v-btn {
    padding: 5vh;
    margin-inline: 50px;
}

.v-btn.v-size--default {
    font-size: 1.2rem;
}


</style>