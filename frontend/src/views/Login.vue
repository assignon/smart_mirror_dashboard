<template>
  <div class="login-core">
    <h1 class="display-3 mb-15 mt-16">Soggeti Mirror Login</h1>
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
      <v-btn elevation="6" v-on:click="submit" class="blue darken-1">
        Login
      </v-btn>
    </form>
    <p class="err-msg"></p>
  </div>
</template>

<script>
// @ is an alias to /src

// import axios from "axios";
// import { mapActions } from "vuex";
import axios from "axios";

export default {
  name: "Login",
  components: {},
  data() {
    return {
      input: {
        email: "",
        password: ""
      },
      showError: false
    };
  },
  created() {
    this.userConnected();
    this.userDisconnected();
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

    userConnected() {
      // when users(receptionists) login add them to the socket
      let socket = this.$store.state.socket;
      // listen to connect event
      socket.on("connect", function(msg) {
        console.log("connected", msg);
        // send connected user id to flask backend
        socket.emit("new_user", { user_id: 1 });
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
    async submit() {
      let formErrMsg = document.querySelector(".err-msg");
      const auth = {
        username: this.input.email,
        password: this.input.password
      };
      const url = "login";
      this.success = false;
      this.error = null;

      if (this.input.email != "" && this.input.password != "") {
        try {
          const res = await axios.get(url, { auth }).then(res => res.data);
          if (res["x-access-token"]) {
            console.log(res["x-access-token"]);
            // self.startSession(res["x-access-token"], 1, 1);
            await this.$router.push("/ingecheckt");
          } else {
            formErrMsg.innerHTML = res.msg;
          }
          this.success = true;
        } catch (err) {
          this.error = err.message;
        }
      } else {
        formErrMsg.innerHTML = "Email and password should not be empty";
      }
    },

    signIn() {
      let formErrMsg = document.querySelector(".err-msg");
      // let validationErrMsg = document.querySelector(".v-messages__message");
      if (
        // !document.body.contains(validationErrMsg) &&
        this.input.email != null &&
        this.input.password != null
      ) {
        this.$store.dispatch("getAxiosCall", {
          url: "http://127.0.0.1:5000/login",
          params: {
            email: this.input.email,
            password: this.input.password
          },
          auth: null,
          csrftoken: null,
          callback: function(data) {
            console.log(data);
            if (data["x-access-token"]) {
              self.startSession(data.token, data.is_superuser, data.id);
              self.$router.push({ name: "Checkin" });
            } else {
              // formErrMsg.innerHTML = data.msg;
            }
          }
        });
      } else {
        formErrMsg.innerHTML = "Email and password should not be empty";
      }
      let body = {
        body: {
          email: this.email,
          password: this.password
        }
      };
      axios
        .get("http://127.0.0.1:5000/login", body, {
          headers: {
            "X-CSRFToken": null,
            Authorization: null
          }
        })
        .then(response => {
          let res = response.data;
          console.log(res);
          // payload.callback(res);
        })
        .catch(error => {
          console.log(error);
        });
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
