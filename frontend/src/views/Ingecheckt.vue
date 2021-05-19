<template>
  <section class="primary-section">
    <div class="main-container">
      <h1 class="mb-9 mt-12">Ingecheckte Gasten</h1>
      <div v-if='ingecheckt.length>0' class='data-table-container'>
        <v-data-table :headers="headers" :items="ingecheckt" hide-default-footer>
          <template v-slot:item="row">
            <tr class='animated fadeInUp' :id='row.item.appointment_id'>
              <td>{{ row.item.name }}</td>
              <td>{{ row.item.tel }}</td>
              <td>{{ row.item.email }}</td>
              <td>{{ row.item.company }}</td>
              <td>{{ row.item.plate }}</td>
              <td>
                <!-- <v-btn class="mx-2 darken-3" color='#0f78b2' rounded elevation="2" @click="checkGuestIn(row.item)" v-if='row.item.checkin==null'> -->
                <v-btn class="mx-2 darken-3" color='#0f78b2' rounded elevation="2" @click="confirmationDialog('checkin',row.item)" v-if='row.item.checkin==null'>
                  <strong style="color:white;text-transform:capitalize">Check-In</strong>
                </v-btn>
                <strong v-else>{{ row.item.checkin }}</strong>
              </td>
              <td>
                <!-- <v-btn class="mx-2 darken-3" color='#ff304c' rounded elevation="2" @click="checkGuestOut(row.item)" :disabled='row.item.checkin==null'> -->
                <v-btn class="mx-2 darken-3" color='#ff304c' rounded elevation="2" @click="confirmationDialog('checkout',row.item)" :disabled='row.item.checkin==null'>
                  <strong style='color:white;text-transform:capitalize'>Check-Uit</strong>
                </v-btn>
              </td>
            </tr>
          </template>
        </v-data-table>
      </div>
      <div class='no-checkin' v-else>
        <v-icon style='font-size: 100px;color:white' class='mb-3'>fas fa-user</v-icon>
        <p>Geen nieuwe gemelde gasten</p>
      </div>
    </div>
    <Notifications :content='notificationText' color='red'/>
    <v-dialog
      v-model="confirmDialog"
      persistent
      max-width="500"
      style='background-color: white;'
    >
      <div class='dialog-content'>
        <p class='mt-5 confirm-dialog-text'>
         {{confirmDialogText}}
        </p>
        <div class='btn-container'>
          <strong style='cursor:pointer;color:#ff304c;' class='pa-3' @click='confirmDialog=false'>NEE</strong>
          <strong style='cursor:pointer;color:#0f78b2;' class='pa-3' @click="checkGuest()">JA</strong>
        </div>
      </div>
    </v-dialog>
  </section>
</template>

<script>
import Notifications from "../components/modals/Notifications";
export default {
  name: "Gastenlijst",

  components: {
    Notifications
  },

  data() {
    //Return: Dummy Data, vervangen door JSON in formaat als hieronder.
    return {
      currentDate: new Date().toLocaleDateString(),
      notificationText: '',
      confirmDialog: false,
      check: null, // determine of guest is checked in or out
      currentGuestData: null,
      confirmDialogText: null,
      headers: [
        {
          text: 'Naam',
          align: 'start',
          sortable: true,
          value: 'name',
          class: "blue white--text rounded-tl-lg darken-1"
        },
        {text: 'Telefoon', value: 'tel', class: "blue white--text darken-1"},
        {text: 'E-mail', value: 'email', class: "blue white--text darken-1"},
        {text: 'Bedrijf', value: 'company', class: "blue white--text darken-1"},
        {text: 'Kenteken', value: 'plate', class: "blue white--text darken-1"},
        {text: 'Check-in', value: 'checkin', class: "blue white--text darken-1"},
        {text: 'Check-out', value: 'checkout', class: "blue white--text rounded-tr-lg darken-1"},
      ],
      ingecheckt: [],
    }
  },

  created() {
    this.scannedGuestData()
    this.getScannedGuestData()
  },

  methods: {
    getScannedGuestData(){
      // get and display all scanned, in and outchecked guest data from DB in case de page is reloaded
      let self = this;

      this.$store.dispatch("getReq", {
          url: "appointments",
          params: {
          },
          auth: self.$session.get('token'),
          csrftoken: self.$session.get('token'),
          xaccesstoken: self.$session.get('token'),
          callback: function(res) {  
            if(res.status == 200){
               res.data.appointments.forEach(data => {
                let guestData = {
                  id: data.guest.guest_id,
                  appointment_id: data.appointment_id,
                  name: data.guest.name,
                  tel: data.guest.phone_number,
                  email: data.guest.email,
                  company: data.guest.company,
                  plate: data.guest.license_plate,
                  checkin: data.checked_in,
                  checkout: data.checked_out,
                }
                self.ingecheckt.push(guestData)
              })
            }
            else{
              self.notificationText = 'Gasten worden opgehaald...'
              self.$store.state.notificationStatus = true
            }
          },
      });
    },

    scannedGuestData(){
      // get and display current scanned guest
      let self = this
      let socket = self.$store.state.socket

      socket.on('face_scanned', function(data){
          let guestData = {
            id: data.id,
            name: data.name,
            tel: data.tel,
            email: data.email,
            company: data.company,
            plate: data.license_plate,
            appointment_id: data.appointment_id,
            checkin: null,
            checkout: null,
            // time: new Date().toLocaleDateString()+'/'+new Date().toLocaleTimeString(), // change with time from DB
          }
          // add scanned guest data to the top of the table
          self.ingecheckt.unshift(guestData)
      });
    },

    confirmationDialog(checkName, guestData){
      let self = this
      // display dialog
      this.confirmDialog = true;
      // get current guest data
      this.currentGuestData = guestData
      this.check = checkName
      if(checkName == 'checkin'){
        self.confirmDialogText = 'Weet u zeker dat u deze gast wilt inchecken?'
      }else{
         self.confirmDialogText = 'Weet u zeker dat u deze gast wilt uitchecken?'
      }
    },

    checkGuest(){
      let self = this
      if (self.check == 'checkin'){
        self.checkGuestIn(self.currentGuestData)
      }else{
        self.checkGuestOut(self.currentGuestData)
      }
    },

    checkGuestIn(guestData){
      let self = this;
      // let socket = self.$store.state.socket

      console.log(guestData);
      this.confirmDialog=false
      this.$store.dispatch("putReq", {
          url: `appointment/${guestData.appointment_id}`,
          params: {
            // appoinment_id: guestData.appointment_id,
            checked_in: new Date().toLocaleDateString()+'/'+new Date().toLocaleTimeString(),
          },
          auth: self.$session.get('token'),
          csrftoken: self.$session.get('token'),
          xaccesstoken: self.$session.get('token'),
          callback: function(data) {
            data
            // socket.on('checked', function(data){
            //   console.log(data);
            //   guestData.checkin = new Date().toLocaleDateString()+'/'+new Date().toLocaleTimeString()
            // })
            
            // self.getScannedGuestData()
          },
      });
    },

    checkGuestOut(guestData){
      let self = this;
      let currentGuest  = document.getElementById(guestData.appointment_id)
      console.log(guestData);
      this.confirmDialog=false
      // remove current guest data from array
      let currentGuestId = guestData.appointment_id
      // self.ingecheckt.filter((item) => item.id !== currentGuestId);
      let guestCheckedOut = self.ingecheckt.findIndex(item => item.appointment_id === currentGuestId);
      self.ingecheckt.splice(guestCheckedOut, 1)

      // currentGuest.classList.remove('zoomIn')
      // setTimeout(() => {
      //   currentGuest.classList.add('fadeOutUp')
      // }, 100)
      // remove defenitely from the DOM
      // setTimeout(() => {
        currentGuest.style.display = 'none'
      // }, 500)
      
      this.$store.dispatch("putReq", {
          url: `appointment/${guestData.appointment_id}`,
          params: {
            checked_out: new Date().toLocaleDateString()+'/'+new Date().toLocaleTimeString(),
          },
          auth: self.$session.get('token'),
          csrftoken: self.$session.get('token'),
          callback: function(data) {
            data
            // self.getScannedGuestData()
          },
      });
    },
  }
};
</script>

<style scoped>
.primary-section {
  background-color: beige;
  min-height: 80vh;
  height: auto;
}
.main-container {
  width: 100%;
  height: auto;
  margin: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  /* flex-wrap: wrap; */
}
.data-table-container{
  width: 80%;
  height: auto;
  margin-bottom: 30px;
}
h1 {
  text-align: left;
  width: 80%;
}
tr td{
  text-align: left;
}
.no-checkin{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 70vh;
}
.no-checkin p{
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: white;
}
.dialog-content{
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: white;
}
.btn-container{
  width: 90%;
  height: auto;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
}
</style>