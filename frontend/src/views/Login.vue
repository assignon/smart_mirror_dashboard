<template>
  <div class="login-core">
    <h1 class="display-3 mb-10 mt-16">Soggeti Mirror Login</h1>
    <!--    <input type="text" name="username" v-model="input.username" placeholder="Username"/>-->
    <!--    <input type="password" name="password" v-model="input.password" placeholder="Password">-->
    <v-form class="login-form">
      <v-text-field
          label="Username"
      ></v-text-field>
      <v-text-field
          label="Password"
          type="password"
      ></v-text-field>
      <v-btn
          elevation="6"
          v-on:click="login()"
      >Login
      </v-btn>
    </v-form>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "Login",
  components: {},
  data() {
    return {
      input: {
        username: "",
        password: ""
      }
    };
  },
  created() {
  },
  methods: {
    startSession(token, su, userId) {
      // start a session
      this.$session.start();
      // store token en user id
      this.$session.set("token", token);
      this.$session.set("userId", userId);
      this.$session.set("authenticated", true);
      this.$session.set("su", su);

    },
    login() {
      if (this.input.username != "a" && this.input.password != "a") {
        this.startSession("string", true, 1)
        this.$router.push({name: "Checkin"})
      } else {
        console.log('Vul een gebruikersnaam en wachtwoord in');
      }
    }
  },

  // signin(){
  //   let self = this;
  //   let formErrMsg = document.querySelector('.err-msg')
  //   let validationErrMsg = document.querySelector('.v-messages__message');
  //   if(!document.body.contains(validationErrMsg) && self.email != null && self.password != null){
  //     this.$store.dispatch("publicPostReq", {
  //       url: "signin",
  //       params: {
  //           email: self.email,
  //           password: self.password
  //       },
  //       auth: null,
  //       csrftoken: null,
  //       callback: function(data) {
  //           console.log(data);
  //           if(data.authenticate){
  //             self.startSession(data.token, data.is_superuser, data.id)
  //             self.$router.push({name: "Dashboard"})
  //           }else{
  //               formErrMsg.innerHTML = data.msg
  //           }
  //       },
  //     });
  //   }else{
  //       formErrMsg.innerHTML = 'Email and password should not be empty';
  //   }
  // }
};
</script>

<style scoped>
.login-core {

}

.login-form {
  height: auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.login-form .v-text-field {
  width: 10%;
}
</style>
