<template>
  <div class="login-core">
    <h1 class="display-3">Login page</h1>
    <h1>{{msgServer}}</h1>
    <v-btn @click='send'>send to server</v-btn>
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
      n:0,
      msgServer: '',
      // ws: new WebSocket("ws://192.168.178.194:5678/")
    };
  },

  created() {
    this.ws_test()
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

    async connection (socket, timeout = 1000) {
      const isOpened = () => (socket.readyState === WebSocket.OPEN)

      if (socket.readyState !== WebSocket.CONNECTING) {
        return isOpened()
      }
      else {
        const intrasleep = 100
        const ttl = timeout / intrasleep // time to loop
        let loop = 0
        while (socket.readyState === WebSocket.CONNECTING && loop < ttl) {
          await new Promise(resolve => setTimeout(resolve, intrasleep))
          loop++
        }
        return isOpened()
      }
    },

    async ws_test(){
      // const ws = new WebSocket("ws://192.168.178.194:5678/")
      const opened = await this.connection(new WebSocket("ws://192.168.178.194:5678/"))
      // let ws = new WebSocket("ws://192.168.178.194:5678/")
      let self = this
      

     if(opened){
       const ws = new WebSocket("ws://192.168.178.194:5678/")
        ws.onopen = function(){
          console.log('connected');
          ws.send('new message')
        }
        ws.onmessage = function(event){
          console.log(event.data);
          self.msgServer = event.data
          ws.send(`hallo there ${event.data}, hoe gaat het?`)
        }
     }
      // ws.onclose = function(){
      //   console.log('closed');
      // }
    },

    send(){
      let ws = new WebSocket("ws://192.168.178.194:5678/")
      let self = this
      this.n+=1
      ws.onopen = function(){
        console.log('connected', self.n);
        ws.send(self.n)
      }
       ws.onmessage = function(event){
        console.log(event.data);
        // if(event.data == 'yan'){
        //   // ws.close()
        // }
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
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
