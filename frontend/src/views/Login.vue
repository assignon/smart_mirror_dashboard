<template>
  <div class="login-core">
    <h1 class="display-3 mb-15 mt-16">Soggeti Mirror Login</h1>
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
          class="blue darken-1"
      >Login
      </v-btn>
    </v-form>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Login",
  components: {},
  data() {
    return {
      n:0,
      input: {
        username: "",
        password: ""
      }
    };
  },

  created() {
    this.userConnected()
    this.userDisconnected()
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

    userConnected(){
       // when users(receptionists) login add them to the socket
       let socket = this.$store.state.socket
       // listen to connect event
       socket.on('connect', function(msg) {
          console.log('connected', msg);
          // send connected user id to flask backend
          socket.emit('new_user', {user_id: 1});
      });
    },

    userDisconnected(){
      // when users(receptionists) logout remove them from the socket
      let socket = this.$store.state.socket
      // listen to disconnect event
      socket.on('disconnect', function(msg){
        console.log( msg);
        // send disconnected user id to flask backend
        socket.emit('user_disconnected', {user_id: 1});
      });
    },

    login() {
      if (this.input.username != "a" && this.input.password != "a") {
        this.startSession("string", true, 1)
        this.$router.push({name: "Ingecheckt"})
      } else {
        console.log('Vul een gebruikersnaam en wachtwoord in');
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
  },

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
