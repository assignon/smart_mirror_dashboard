<template>
  <div class="login-core">
    <h1 class="display-3">Soggeti Mirror Login</h1>
    <input type="text" name="username" v-model="input.username" placeholder="Username" />
    <input type="password" name="password" v-model="input.password" placeholder="Password">
    <button type="button" v-on:click="login()">Login</button>
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

  created() {},

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
        if(this.input.username != "" && this.input.password != "") {
          if(this.input.username == this.$parent.mockAccount.username && this.input.password == this.$parent.mockAccount.password) {
            this.$emit("authenticated", true);
            this.$router.replace({name: "Dashboard"})
          } else {
            console.log('Gebruikersnaam en of wachtwoord is verkeerd');
          }
        } else {
          console.log('Vul een gebruikersnaam en wachtwoord in');
        }
      }
  }

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
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 24px;
}
</style>
