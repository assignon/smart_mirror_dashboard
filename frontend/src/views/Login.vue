<template>
  <div class="login-core">
    <h1 class="display-3 mb-15 mt-16">Sogeti Mirror Login</h1>
    <form @submit.prevent="signIn" class="login-form">
      <!--      <input type="text" name="username" v-model="input.username" placeholder="Username"/>-->
      <!--      <input type="password" name="password" v-model="input.password" placeholder="Password">-->
      <v-text-field
          name="email"
          v-model="input.email"
          label="Email"
      ></v-text-field>
      <v-text-field
          name="password"
          v-model="input.password"
          label="Password"
          type="password"
      ></v-text-field>
      <div class='btn-container'>
        <p style='color:#0070ad;cursor:pointer'>Wachtwoord vergeten?</p>
        <v-btn elevation="6" color='#0070ad' rounded v-on:click="submit" class="pa-5">
          <span style='color:white;text-transform: capitalize'>Login <v-icon small>fas fa-chevron-right</v-icon></span>
        </v-btn>
      </div>
    </form>
    <Notifications :content='notificationText' color='red'/>
  </div>
</template>

<script>
// @ is an alias to /src

// import axios from "axios";
// import { mapActions } from "vuex";
import axios from "axios";
import Notifications from "../components/modals/Notifications";
export default {
  name: "Login",
  components: {
    Notifications
  },

  data() {
    return {
      notificationText: '',
      input: {
        email: "",
        password: ""
      },
      showError: false
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
      socket.on("connect", function (msg) {
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

    // userDisconnected() {
    //   // when users(receptionists) logout remove them from the socket
    //   let socket = this.$store.state.socket;
    //   // listen to disconnect event
    //   socket.on("disconnect", function (msg) {
    //     console.log(msg);
    //     // send disconnected user id to flask backend
    //     socket.emit("user_disconnected", {user_id: 1});
    //   });
    // },

    // login() {
    //   if (this.input.username !== "a" && this.input.password !== "a") {
    //     this.startSession("string", true, 1);
    //     this.$router.push({ name: "Ingecheckt" });
    //   } else {
    //     console.log("Vul een gebruikersnaam en wachtwoord in");
    //   }
    // }
    async submit() {
      // let formErrMsg = document.querySelector(".err-msg");
      let self = this;
      const auth = {
        username: this.input.email,
        password: this.input.password
      };
      const url = "login";
      this.success = false;
      this.error = null;

      if (this.input.email != '' && this.input.password != '') {
        try {
          const res = await axios.get(url, { auth }).then(res => res.data);
          if (res["x-access-token"]) {
            // console.log(res["x-access-token"]);
            self.startSession(res["x-access-token"], res['superuser'], res['user_id']);
            await this.$router.push("/ingecheckt");
          } else {
            self.notificationText = res.message
            self.$store.state.notificationStatus = true
            // formErrMsg.innerHTML = res.msg;
          }
          this.success = true;
        } catch (err) {
          this.error = err.message;
        }
      } else {
        self.notificationText = "Email and password should not be empty"
        self.$store.state.notificationStatus = true
        // formErrMsg.innerHTML = "Email and password should not be empty";
      }
    },
  }
};
</script>

<style scoped>
.login-core {
  width: 100%;
  height: 95vh;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
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
  width: 50%;
}
.btn-container{
  width: 50%;
  height: auto;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  flex-direction: column;
}
</style>
