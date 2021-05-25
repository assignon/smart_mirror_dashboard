<template>
  <div>
    <h1>Wachtwoord wijzigen</h1>
    <v-flex id="failureAlert">
      <failure-alert />
    </v-flex>
    <v-flex id="successAlert">
      <succes-alert />
    </v-flex>
    <v-form class="login-form mt-9" ref="form" v-model="valid" lazy-validation>
      <v-text-field
          name="E-mail"
          :rules="emailRules"
          label="E-mail"
          v-model="input.email"
          required
      ></v-text-field>
      <v-text-field
          name="password_old"
          :rules="passwordRules"
          v-model="input.password_old"
          label="Oude wachtwoord"
          type="password"
          required
      ></v-text-field>
      <v-text-field
          name="password_new"
          :rules="passwordRules"
          v-model="input.password_new"
          label="Nieuw wachtwoord"
          type="password"
          required
      ></v-text-field>
      <v-text-field
          name="password_new_repeat"
          :rules="matchRules"
          v-model="input.password_new_repeat"
          label="Wachtwoord herhalen"
          type="password"
          required
      ></v-text-field>
    </v-form>
    <v-btn
      color="success"
      class="mr-4"
      v-on:click="validation"
    >
      Bevestigen
    </v-btn>
  </div>
</template>

<script>
// import axios from "axios";
// import Popup from '../components/modals/Popup.vue';
import succesAlert from '../components/modals/succesAlert.vue';
import failureAlert from '../components/modals/failureAlert.vue';

export default {
  name: "Instellingen",
  components: { succesAlert, failureAlert }, 
  data() {
    return {
      valid: true,
      input: {
        email: "",
        password_old: "",
        password_new: "",
        password_new_repeat: ""
      },
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      passwordRules: [
        v => !!v || "This field is required",
        v => (v && v.length <= 10) || 'Password must be less than 10 characters',
      ],
      matchRules: [
        () => (this.input.password_new_repeat === this.input.password_new) || 'Passwords must match',
        v => (v && v.length <= 10) || 'Password must be less than 10 characters',
      ],
      showError: false,
      dialog: false,
      succes_new_password: false,
      password_error: "" 
    };
  },

  methods: {
    validate () {
      this.$refs.observer.validate()
    },
    test () {
      console.log(this.input.password_new)
    },
    validation() {
      let self = this;
      this.error = null;
      if (self.input.password_new == self.input.password_new_repeat && self.input.password_new != ""){
        try{
          this.$store.dispatch("putReq", {
          url: "user/"+this.$session.getAll()['userId']+"",
          params: {
            "password": self.input.password_old,
            "new_password": self.input.password_new,
          },
          auth: self.$session.get('token'),
          csrftoken: self.$session.get('token'),
          xaccesstoken: self.$session.get('token'),
          callback: function(data) {
            console.log(data)
          }
        });
        } catch(err){
          this.error = err.message;
          console.log(this.error)
        }
      }
    }
  }
}
</script>

<style scoped>
  div {
    width: 300px;
    margin: auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }

  #failureAlert{
    display: none;
  }

  #successAlert{
    display: none;
  }
</style>