<template>
  <div class="login-core">
    <h1 class='display-3'>Login page</h1>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "Login",

  components: {
  },

  data(){
    return{

    }
  },

  created(){},

  methods: {
    startSession(token, su, userId){
      // start a session
      this.$session.start()
      // store token en user id
      this.$session.set('token', token)
      this.$session.set('userId', userId)
      this.$session.set('authenticated', true)
      this.$session.set('su', su)
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
  .login-core{
    height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
