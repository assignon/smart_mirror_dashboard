<template>
  <section class="primary-section">
    <div class="main-container">
      <h1 class="mb-9 mt-12">Ingecheckte Gasten</h1>
      <div v-if='ingecheckt.length>0' class='data-table-container'>
        <v-data-table :headers="headers" :items="ingecheckt" hide-default-footer>
          <template v-slot:item="row">
            <tr class='animated fadeInUp' :id='row.item.id'>
              <td>{{ row.item.name }}</td>
              <td>{{ row.item.tel }}</td>
              <td>{{ row.item.email }}</td>
              <td>{{ row.item.company }}</td>
              <td>{{ row.item.plate }}</td>
              <td>
                <v-btn class="mx-2 darken-3" color='#0f78b2' rounded elevation="2" @click="checkGuestIn(row.item)" v-if='!row.item.checkin'>
                  <strong style="color:white;text-transform:capitalize">Check-In</strong>
                </v-btn>
                <strong v-else>{{ row.item.time }}</strong>
              </td>
              <td>
                <v-btn class="mx-2 darken-3" color='#ff304c' rounded elevation="2" @click="checkGuestOut(row.item)" :disabled='!row.item.checkin'>
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
  </section>
</template>

<script>
export default {
  name: "Gastenlijst",

  data() {
    //Return: Dummy Data, vervangen door JSON in formaat als hieronder.
    return {
      currentDate: new Date().toLocaleDateString(),
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
      ingecheckt: [
        {
          id: 78,
          name: 'Appel',
          tel: '0293827267',
          email: 'e@mail.com',
          company: 'Sogetto',
          plate: 'dk-si-ks',
          checkin: false,
          checkout: false,
          time: new Date().toLocaleDateString()+'/'+new Date().toLocaleTimeString(), // change with time from DB
        },
        {
          id: 18,
          name: 'Frozen Yogurt',
          tel: '0293827267',
          email: 'e@mail.com',
          company: 'Sogetto',
          plate: 'dk-si-ks',
          checkin: false,
          checkout: false,
          time: new Date().toLocaleDateString()+'/'+new Date().toLocaleTimeString(), // change with time from DB
        },
      ],
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
          url: "/appointments",
          params: {
          },
          auth: self.$session.get('token'),
          csrftoken: self.$session.get('token'),
          callback: function(data) {
              console.log(data);
              self.ingecheckt.push(data)
              // store.getters["setData"]([store.state.product.productsArr, [data]]);
          },
      });
    },

    scannedGuestData(){
      // get and display current scanned guest
      let self = this
      let socket = self.$store.state.socket

      socket.on('face_scanned', function(data){
          console.log('socket data', data);
          let guestData = {
            id: data.id,
            name: data.name,
            tel: data.tel,
            email: data.email,
            company: data.company,
            plate: data.license_plate,
            checkin: false,
            checkout: false,
            time: new Date().toLocaleDateString()+'/'+new Date().toLocaleTimeString(), // change with time from DB
          }
          // add scanned guest data to the top of the table
          self.ingecheckt.unshift(guestData)
      });
    },

    checkGuestIn(guestData){
      // let self = this;

      guestData.checkin = true
      // this.$store.dispatch("putReq", {
      //     url: "guests/checkin",
      //     params: {
      //       guest_id: guestId
      //     },
      //     auth: self.$session.get('token'),
      //     csrftoken: self.$session.get('token'),
      //     callback: function(data) {
      //         console.log(data);
      //     },
      // });
      // console.log('checkin', guestData);
    },

    checkGuestOut(guestData){
      let self = this;
      // let currentGuest  = document.getElementById(guestData.id)

      // remove current guest data from array
      let currentGuestId = guestData.id
      // self.ingecheckt.filter((item) => item.id !== currentGuestId);
      let guestCheckedOut = self.ingecheckt.findIndex(item => item.id === currentGuestId);
      self.ingecheckt.splice(guestCheckedOut, 1)

      // currentGuest.classList.remove('zoomIn')
      // setTimeout(() => {
      //   currentGuest.classList.add('fadeOutUp')
      // }, 100)
      // remove defenitely from the DOM
      // setTimeout(() => {
      //   currentGuest.style.display = 'none'
      // }, 500)
      
      
      // this.$store.dispatch("deleteReq", {
      //     url: "guests/checkout",
      //     params: {
      //       guest_id: guestId
      //     },
      //     auth: self.$session.get('token'),
      //     csrftoken: self.$session.get('token'),
      //     callback: function(data) {
      //         console.log(data);
      //     },
      // });
      // console.log('checkout', guestData);
    },
  }
};
</script>

<style scoped>
.primary-section {
  background-color: beige;
  min-height: 80vh;
}
.main-container {
  width: 100%;
  margin: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  /* flex-wrap: wrap; */
}
.data-table-container{
  width: 80%;
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
</style>