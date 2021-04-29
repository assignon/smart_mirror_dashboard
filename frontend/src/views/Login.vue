<template>
  <div class="login-core">
    <!--    <input type="text" name="username" v-model="input.username" placeholder="Username"/>-->
    <!--    <input type="password" name="password" v-model="input.password" placeholder="Password">-->
    <v-form class="login-form">
      <h1 class="display-3 mb-15 mt-16">Soggeti Mirror Login</h1>
      <v-text-field v-model="input.email" label="Email"></v-text-field>
      <v-text-field v-model="input.password" label="Password" type="password"></v-text-field>
      <v-btn elevation="6" v-on:click="signIn()" class="blue darken-1"
        >Login
      </v-btn>
    </v-form>
    <!-- snack bar -->
    <v-snackbar
      v-model="snackbar"
      timeout="5000"
      :top='true'
      :right='true'
    >
      {{snackbarText}}

      <template v-slot:action="{ attrs }">
        <v-btn
          color="#1f88e5"
          text
          v-bind="attrs"
          @click="snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Login",
  components: {},
  data() {
    return {
      snackbar: false,
      snackbarText: '',
      n: 0,
      input: {
        email: "",
        password: ""
      }
    };
  },
  created() {
    // this.userConnected();
    this.userDisconnected();
    this.user_joinded()
  },

  methods: {
    startSession(token, su, userId, username) {
      // start a session
      this.$session.start();
      // store token en user id
      this.$session.set("token", token);
      this.$session.set("userId", userId);
      this.$session.set("authenticated", true);
      this.$session.set("su", su);
      this.$session.set("username", username);
    },

    userConnected(username) {
      // when users(receptionists) login add them to the socket
      let socket = this.$store.state.socket;
      // listen to connect event
      socket.on("connect", function(msg) {
        console.log("connected", msg);
        // send connected user id to flask backend
        socket.emit("new_user", { username: username });
      });
    },

    user_joinded(){
      let socket = this.$store.state.socket;
      let self = this
      // listen to connect event
      socket.on("user_joined", function(data) {
        self.snackbarText = data.username+' is verbonden'
        self.snackbar = true
        console.log(data.username+' is verbonden');
        // alert(data.username+' is verbonden');
      });
    },

    userDisconnected() {
      // when users(receptionists) logout remove them from the socket
      let socket = this.$store.state.socket;
      // listen to disconnect event
      socket.on("disconnect", function(msg) {
        console.log(msg);
        // send disconnected user id to flask backend
        socket.emit("user_disconnected", { user_id: 1 });
      });
    },

    // login() {
    //   if (this.input.username !== "a" && this.input.password !== "a") {
    //     this.startSession("string", true, 1);
    //     this.$router.push({ name: "Ingecheckt" });
    //   } else {
    //     console.log("Vul een gebruikersnaam en wachtwoord in");
    //   }
    // }

    signIn() {
      let self = this;
      // let formErrMsg = document.querySelector(".err-msg");
      let validationErrMsg = document.querySelector(".v-messages__message");
      if (
        !document.body.contains(validationErrMsg) &&
        self.input.email != null &&
        self.input.password != null
      ) {
        // self.startSession(Math.random().toString(36).substr(2), true, 1, self.input.email)
        let socket = this.$store.state.socket;
        socket.emit("new_user", { username: self.input.email });
        // self.userConnected(self.input.email)
        // this.$store.dispatch("publicPostReq", {
        //   url: "Login",
        //   params: {
        //     email: self.email,
        //     password: self.password
        //   },
        //   auth: null,
        //   csrftoken: null,
        //   callback: function(data) {
        //     console.log(data);
        //     if (data.authenticate) {
        //       self.startSession(data.token, data.is_superuser, data.id);
        //       self.$router.push({ name: "Dashboard" });
        //     } else {
        //       formErrMsg.innerHTML = data.msg;
        //     }
        //   }
        // });
      } else {
        // formErrMsg.innerHTML = "Email and password should not be empty";
        alert('Email and password should not be empty')
      }
    }
  }
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
