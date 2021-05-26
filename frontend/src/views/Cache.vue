<template>
 <div>
   Hello World!
 </div>
</template>

<script>
// @ is an alias to /src

// import axios from "axios";
// import { mapActions } from "vuex";
import axios from "axios";

export default {
  name: "Cache",
  components: {

  },
  data() {
    return {
      cacheIdsAndTime: []
    };
  },
  created() {
    // this.userConnected();
    // this.userDisconnected();
    // this.user_joinded();
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
    GetCachedIds(){

    }



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
  width: 22%;
}
.btn-container {
  width: 50%;
  height: auto;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  flex-direction: column;
}
</style>
