<template>
  <section class="primary-section">
    <div class="main-container">
      <h1 class="mb-9 mt-12">Ingecheckte Gasten</h1>
      <div v-if="ingecheckt.length > 0" class="data-table-container">
        <v-data-table
          :headers="headers"
          :items="ingecheckt"
        >
          <template v-slot:item="row">
            <tr
              class="animated fadeInUp table-tr"
              :id="row.item.appointment_id"
            >
              <td>{{ row.item.name }}</td>
              <td>{{ row.item.tel }}</td>
              <td>{{ row.item.email }}</td>
              <td>{{ row.item.company }}</td>
              <td>{{ row.item.plate }}</td>
              <td>{{ row.item.employee_name }}</td>
              <td
                :class="
                  row.item.name.replace(/ /g, '') + row.item.appointment_id
                "
              >
                <!-- <v-btn class="mx-2 darken-3" color='#0f78b2' rounded elevation="2" @click="checkGuestIn(row.item)" v-if='row.item.checkin==null'> -->
                <v-btn
                  class="mx-2 darken-3"
                  rounded
                  elevation="2"
                  @click="confirmationDialog('checkin', row.item)"
                  v-if="row.item.checkin == null"
                >
                  <strong
                    style="color:white;text-transform:capitalize"
                  ></strong>
                  <v-icon color="green" dense>
                    mdi-check-bold
                  </v-icon>
                </v-btn>
                <v-tooltip bottom v-else>
                  <template v-slot:activator="{ on, attrs }">
                    <strong v-bind="attrs" v-on="on">
                      <!-- {{ new Date(row.item.checkin.split('T')).toLocaleDateString() }} -->
                      {{ row.item.checkin.split('T')[1] }}
                    </strong>
                  </template>
                  <strong >{{ new Date(row.item.checkin.split('T')[0]).toLocaleDateString() }} - {{row.item.checkin.split('T')[1]}}</strong>
                </v-tooltip>
                
              </td>
              <td>
                <!-- <v-btn class="mx-2 darken-3" color='#ff304c' rounded elevation="2" @click="checkGuestOut(row.item)" :disabled='row.item.checkin==null'> -->
                <v-btn
                  class="mx-2 darken-3"
                  :class="
                    row.item.name.replace(/ /g, '') +
                      '-checkout-' +
                      row.item.appointment_id
                  "
                  rounded
                  elevation="2"
                  @click="confirmationDialog('checkout', row.item)"
                  :disabled="row.item.checkin == null"
                >
                  <strong
                    :class="row.item.name.replace(/ /g, '')"
                    style="color:#ff304c;text-transform:capitalize"
                  ></strong>
                  <v-icon color="#ff304c" dense>
                    mdi-close-thick
                  </v-icon>
                </v-btn>
              </td>
            </tr>
          </template>
        </v-data-table>
      </div>
      <div class="no-checkin" v-else>
        <v-icon style="font-size: 100px;color:white" class="mb-3"
          >fas fa-user</v-icon
        >
        <p>Geen nieuwe gemelde gasten</p>
      </div>
    </div>

    <Notifications :content="notificationText" color="red" />
    <v-dialog
      v-model="confirmDialog"
      persistent
      max-width="500"
      style="background-color: white;"
    >
      <div class="dialog-content">
        <p class="mt-5 confirm-dialog-text">
          {{ confirmDialogText }}
        </p>
        <div class="btn-container">
          <strong
            style="cursor:pointer;color:#ff304c;"
            class="pa-3"
            @click="confirmDialog = false"
            >NEE</strong
          >
          <strong
            style="cursor:pointer;color:#0f78b2;"
            class="pa-3"
            @click="checkGuest()"
            >JA</strong
          >
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
      notificationText: "",
      confirmDialog: false,
      checkedOutLoader: false,
      check: null, // determine of guest is checked in or out
      currentGuestData: null,
      confirmDialogText: null,
      checkedConfirm: false, // check if guest ckeck confirmation dialog is JA or NEE
      headers: [
        {
          text: "Naam",
          align: "start",
          sortable: true,
          value: "name",
          class: "rounded-tl-lg darken-1"
        },
        { text: "Telefoon", value: "tel", class: "darken-1" },
        { text: "E-mail", value: "email", class: "bdarken-1" },
        { text: "Bedrijf", value: "company", class: "darken-1" },
        { text: "Kenteken", value: "plate", class: "darken-1" },
        { text: "Contact Persoon", value: "employee_name", class: "darken-1" },
        { text: "Check-in", value: "checkin", class: "darken-1" },
        {
          text: "Check-out",
          value: "checkout",
          class: "rounded-tr-lg darken-1"
        }
      ],
      ingecheckt: []
    };
  },

  watch: {},

  created() {
    this.scannedGuestData();
    this.getScannedGuestData();
    // let self = this

    // guest checked in socket
    this.$store.state.socket.on("checked_in", function(guestdata) {
      guestdata.checkin =
        new Date().toLocaleDateString() + "T" + new Date().toLocaleTimeString();

      document.querySelector(
        "." + guestdata.name.replace(/ /g, "") + guestdata.appointment_id
      ).innerHTML =
        new Date().toLocaleDateString() + "T" + new Date().toLocaleTimeString();
      // let checkinBtn = document.querySelector('.'+guestdata.name.replace(/ /g,'')+guestdata.appointment_id)
      // checkinBtn.firstChild.innerHTML = new Date().toLocaleDateString()+'/'+new Date().toLocaleTimeString()
      // checkinBtn.elevation = '0';
      // checkinBtn.classList.add('v-btn--disabled')
      // checkinBtn.style.backgroundColor = 'white'

      // update checkout btn style
      let checkoutBtn = document.querySelector(
        "." +
          guestdata.name.replace(/ /g, "") +
          "-checkout-" +
          guestdata.appointment_id
      );
      checkoutBtn.disabled = false;
      checkoutBtn.classList.remove("v-btn--disabled");
      checkoutBtn.style.backgroundColor = "#f5f5f5";
    });

    // checkout socket
    this.checkedOutSocket();
  },

  methods: {
    checkedOutSocket() {
      let self = this;
      let increase = 0;
      // let tableBody

      // setTimeout(() => {
      //   tableBody = self.ingecheckt.length > 0 ? tableBody = document.getElementsByTagName('tbody')[0].children.length : null
      // }, 1000)

      this.$store.state.socket.on("checked_out", function(guestData) {
        guestData.checkout = true;
        document.querySelector(
          "." + guestData.name.replace(/ /g, "")
        ).innerHTML = "...";

        setTimeout(() => {
          // let currentGuestId = guestData.appointment_id
          // let guestCheckedOut = self.ingecheckt.findIndex(item => item.appointment_id === currentGuestId);
          // self.ingecheckt.splice(guestCheckedOut, 1)

          // reset checkout btn text
          // document.querySelector(
          //   "." + guestData.name.replace(/ /g, "")
          // ).innerHTML = "Check-Uit";

          document.querySelector(
            "." + guestData.name.replace(/ /g, "")
          ).style.color = "#ff314d";

          // // reset check in btn
          // let checkInBtn = document.querySelector('.'+guestData.name.replace(/ /g,'')+guestData.appointment_id)
          // checkInBtn.firstChild.innerHTML = 'Check-In'
          // checkInBtn.firstChild.style.color = 'white'
          // checkInBtn.elevation = '2';
          // checkInBtn.style.backgroundColor = '#0f78b2'
          // checkInBtn.style.textTransform = 'capitalize'
          // checkInBtn.classList.remove('v-btn--disabled')

          // remove from DOM
          let currentGuest = document.getElementById(guestData.appointment_id);
          currentGuest.style.display = "none";

          // show no scan guest view when all guest checked out
          // check if there is any tr in the DOM
          increase += 1;
          // let ingechecktArrLen = self.ingecheckt.length
          let updatedIngechecktArrLen = self.ingecheckt.length - increase;

          console.log(updatedIngechecktArrLen);
          console.log(self.ingecheckt.length);
          if (updatedIngechecktArrLen < 1) {
            // update ingecheckt array length to 0 if all guest checked out
            // to be able to display the no guest scan view
            self.ingecheckt = [];
            increase = 0;
          }
        }, 2000);
      });
    },

    getScannedGuestData() {
      // get and display all scanned, in and outchecked guest data from DB in case de page is reloaded
      let self = this;
      this.$store.dispatch("getReq", {
        url: "appointments",
        params: {},
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function(res) {
          // check if token is valid
          if (res.data.message == "Token is invalid!") {
            self.notificationText =
              "Lijk erop dat u uitgelogd bent, u wordt doorgestuurd naar de login pagina.";
            self.$store.state.notificationStatus = true;
            // destroy session
            self.$session.destroy();
            // sen d to login page
            setTimeout(() => {
              self.$router.push({ name: "Login" });
            }, 3000);
          }

          if (res.status == 200) {
            res.data.appointments.forEach(data => {
              let guestData = {
                id: data.guest.guest_id,
                appointment_id: data.appointment_id,
                employee_name: data.employee_name,
                name: data.guest.name,
                tel: data.guest.phone_number,
                email: data.guest.email,
                company: data.guest.company,
                plate: data.guest.license_plate,
                checkin: data.checked_in,
                checkout: data.checked_out
              };
              self.ingecheckt.push(guestData);
            });
          } else {
            self.notificationText = "Gasten worden opgehaald...";
            self.$store.state.notificationStatus = true;
          }
        }
      });
    },

    scannedGuestData() {
      // get and display current scanned guest
      let self = this;
      let socket = self.$store.state.socket;
      socket.on("face_scanned", function(data) {
        if (data) {
          let guestData = {
            id: data.id,
            name: data.name,
            tel: data.tel,
            email: data.email,
            company: data.company,
            plate: data.license_plate,
            appointment_id: data.appointment_id,
            employee_name: data.employee_name,
            checkin: null,
            checkout: null
            // time: new Date().toLocaleDateString()+'/'+new Date().toLocaleTimeString(), // change with time from DB
          };
          // add scanned guest data to the top of the table
          self.ingecheckt.unshift(guestData);
        } else {
          self.notificationText = "Lijk erop dat u uitgelogd bent";
          self.$store.state.notificationStatus = true;
        }
      });
    },

    confirmationDialog(checkName, guestData) {
      let self = this;
      // display dialog
      this.confirmDialog = true;
      // get current guest data
      this.currentGuestData = guestData;
      this.check = checkName;
      if (checkName == "checkin") {
        self.confirmDialogText = "Weet u zeker dat u deze gast wilt inchecken?";
      } else {
        self.confirmDialogText =
          "Weet u zeker dat u deze gast wilt uitchecken?";
      }
    },

    checkGuest() {
      let self = this;
      if (self.check == "checkin") {
        // self.currentGuestData.checkin = true
        self.checkGuestIn(self.currentGuestData);
      } else {
        // self.currentGuestData.checkout = true
        self.checkGuestOut(self.currentGuestData);
      }
    },

    checkGuestIn(guestData) {
      let self = this;
      let socket = self.$store.state.socket;
      this.confirmDialog = false;
      this.$store.dispatch("putReq", {
        url: `appointment/${guestData.appointment_id}`,
        params: {
          // appoinment_id: guestData.appointment_id,
          checked_in:
            new Date().toLocaleDateString() +
            "T" +
            new Date().toLocaleTimeString()
        },
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function(data) {
          data;
          // self.getScannedGuestData()
        }
      });
      // let guestdata = guestData;
      socket.emit("update_checkedin", guestData);
      // socket.on('checked', function(data){
      //   console.log('checked data', data);
      //   console.log('hallo there')
      //   guestdata.checkin = new Date().toLocaleDateString()+'/'+new Date().toLocaleTimeString()
      // })
    },

    checkGuestOut(guestData) {
      let self = this;
      let socket = self.$store.state.socket;
      // let currentGuest  = document.getElementById(guestData.appointment_id)

      this.confirmDialog = false;
      // remove current guest data from array
      // let currentGuestId = guestData.appointment_id
      // let guestCheckedOut = self.ingecheckt.findIndex(item => item.appointment_id === currentGuestId);
      // self.ingecheckt.splice(guestCheckedOut, 1)

      // currentGuest.classList.remove('zoomIn')
      // setTimeout(() => {
      //   currentGuest.classList.add('fadeOutUp')
      // }, 100)
      // remove defenitely from the DOM
      // setTimeout(() => {
      // currentGuest.style.display = 'none'
      // }, 500)

      this.$store.dispatch("putReq", {
        url: `appointment/${guestData.appointment_id}`,
        params: {
          checked_out:
            new Date().toLocaleDateString() +
            "/" +
            new Date().toLocaleTimeString()
        },
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        callback: function(data) {
          data;
          // self.getScannedGuestData()
        }
      });
      socket.emit("update_checkedout", guestData);
    }
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
.data-table-container {
  width: 80%;
  height: auto;
  margin-bottom: 30px;
}
h1 {
  text-align: left;
  width: 80%;
}
tr td {
  text-align: left;
}
.no-checkin {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 70vh;
}
.no-checkin p {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: white;
}
.dialog-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: white;
}
.btn-container {
  width: 90%;
  height: auto;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
}
</style>
