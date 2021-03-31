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
import io from "socket.io-client";
// let socket = io.connect('http://192.168.178.52:5000');

export default {
  name: "Login",

  components: {},

  data() {
    return {
      n:0,
      msgServer: '',
      host_name: '127.0.0.1',
      port: 5678,
      isConnected: false,

    };
  },

  created() {
    let socket = io.connect('http://192.168.178.52:5000');
    this.ws_test(socket)
  },

  //  sockets: {
  //   connect() {
  //     // Fired when the socket connects.
  //     this.isConnected = true;
  //   },

  //   disconnect() {
  //     this.isConnected = false;
  //   },

  //   // Fired when the server sends something on the "messageChannel" channel.
  //   messageChannel(data) {
  //     this.socketMessage = data
  //   }
  // },

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

    async ws_test(socket){

      let self = this

      socket.on('connect', function(msg) {
          console.log(msg);
          socket.emit('new_user', {user_id: 1});
      });

      socket.on('disconnect', function(msg){
        console.log( msg);
        socket.emit('user_disconnected', {user_id: 1});
      });

      socket.on('face_scanned', function(msg){
        console.log('client scanned with id:', msg);
        self.msgServer = `${msg.name} is niet herkend en is voor de eerst met id: ${msg.guest_id}`
      });

    //   // const ws = new WebSocket("ws://192.168.178.194:5678/")
    //    let self = this
    //   const opened = await this.connection(new WebSocket(`ws://${self.host_name}:${self.port}/`))
    //   // let ws = new WebSocket("ws://192.168.178.194:5678/")
      

    //  if(opened){
    //    const ws = new WebSocket(`ws://${self.host_name}:${self.port}/`)
    //     ws.onopen = function(){
    //       console.log('connected');
    //       ws.send('new message')
    //     }
    //     ws.onmessage = function(event){
    //       console.log(event.data);
    //       self.msgServer = event.data
    //       ws.send(`hallo there ${event.data}, hoe gaat het?`)
    //     }
    //  }
    //   // ws.onclose = function(){
    //   //   console.log('closed');
    //   // }
    },

    send(){
      console.log('hallo');   
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
