<template>
  <section class="primary-section">
    <Notifications :content="notification_text" color="red" />
    <div class="main-container">
      <div>
        <!-- Header -->
        <h1 class="mb-3 mt-12">Alle gasten</h1>
        <!-- New client button -->
        <v-row>
          <v-dialog v-model="add_dialog" persistent max-width="600px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="white--text mt-9 mb-12"
                color="#0f78b2"
                rounded
                v-bind="attrs"
                v-on="on"
              >
                <v-icon color="white">mdi-account-plus-outline</v-icon>
                Toevoegen
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">Nieuwe gebruiker</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="new_client.name"
                        label="Name*"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="new_client.phone_number"
                        label="Tel*"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="new_client.email"
                        label="Email*"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="new_client.company"
                        label="Bedrijf*"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="new_client.license_plate"
                        label="Kenteken*"
                        required
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                <small>*Verplichte velden</small>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="red darken-1" text @click="add_dialog = false">
                  Sluiten
                </v-btn>
                <v-btn
                  color="green darken-1"
                  text
                  @click="
                    add_dialog = false;
                    newClient();
                  "
                >
                  Toevoegen
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>
        <!-- Search bar -->
        <v-text-field
          class="mb-9"
          v-model="search"
          append-icon="mdi-magnify"
          label="Zoeken"
          single-line
          hide-details
        ></v-text-field>
        <!-- Datatable -->
        <v-card class="mb-15">
          <v-data-table :headers="headers" :items="clients" :search="search">
            <template v-slot:item="row">
              <!-- Template data -->
              <tr>
                <td>{{ row.item.name }}</td>
                <td>{{ row.item.company }}</td>
                <td>{{ row.item.email }}</td>
                <td>{{ row.item.license_plate }}</td>
                <td>{{ row.item.phone_number }}</td>
                <!-- Delete button -->
                <td>
                  <v-btn
                    class="mx-2 darken-4"
                    rounded
                    elevation="2"
                    @click.stop="confirmationDialog(row.item)"
                  >
                    <v-icon color="red" dense>
                      mdi-delete
                    </v-icon>
                  </v-btn>
                </td>
                <!-- Edit button -->
                <td>
                  <v-btn
                    class="mx-2 darken-4"
                    rounded
                    elevation="2"
                    @click="editDialog(row.item)"
                  >
                    <v-icon color="orange" dense>
                      mdi-wrench
                    </v-icon>
                  </v-btn>
                </td>
                <!-- Checkin button -->
                <td>
                  <v-btn
                    class="mx-2 darken-4"
                    rounded
                    elevation="2"
                    @click="checkinDialog(row.item)"
                  >
                    <v-icon color="green" dense>
                      mdi-check-bold
                    </v-icon>
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-card>
      </div>
    </div>
    <!-- Checkin Dialoge -->
    <v-dialog v-model="checkin_dialog" max-width="290">
      <v-card>
        <v-card-title class="headline">
          Weet je het zeker?
        </v-card-title>
        <v-card-text>
          Om deze persoon in te checken
        </v-card-text>
        <v-card-actions>
          <!-- Annuleer button -->
          <v-btn
            color="red darken-1"
            align="center"
            text
            @click="checkin_dialog = false"
          >
            Annuleren
          </v-btn>
          <v-spacer></v-spacer>
          <!-- Checkin button -->
          <v-btn
            color="green darken-1"
            align="center"
            text
            @click="
              checkIn(currentUserData);
              checkin_dialog = false;
            "
          >
            Bevestigen
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- Del Dialoge -->
    <v-dialog v-model="del_dialog" max-width="290">
      <v-card>
        <v-card-title class="headline">
          Weet je het zeker?
        </v-card-title>
        <v-card-text>
          Deze actie kan je niet ongedaan maken.
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="red darken-1"
            align="center"
            text
            @click="del_dialog = false"
          >
            Annuleren
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            align="center"
            text
            @click="
              delClient(currentUserData);
              del_dialog = false;
            "
          >
            Verwijderen
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- Edit Dialoge -->
    <v-dialog v-model="edit_dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Gebruiker bewerken</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  :label="edit_form.length > 0 ? edit_form[0].name : null"
                  placeholder="Naam"
                  v-model="edit_client.name"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  :label="edit_form.length > 0 ? edit_form[0].company : null"
                  placeholder="Bedrijf"
                  v-model="edit_client.company"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  :label="edit_form.length > 0 ? edit_form[0].email : null"
                  placeholder="Email"
                  v-model="edit_client.email"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  :label="
                    edit_form.length > 0 ? edit_form[0].phone_number : null
                  "
                  placeholder="Tel"
                  v-model="edit_client.phone_number"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  :label="
                    edit_form.length > 0 ? edit_form[0].license_plate : null
                  "
                  placeholder="Kenteken"
                  v-model="edit_client.licence_plate"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <small>*Verplichte velden</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="edit_dialog = false">
            Sluiten
          </v-btn>
          <v-btn
            color="green darken-2"
            text
            @click="
              edit_dialog = false;
              editClient(currentUserData);
            "
          >
            Bevestigen
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </section>
</template>

<script>
import Notifications from "../components/modals/Notifications";
// import checkin from "@/views/checkin";

export default {
  name: "Clients",
  components: { Notifications },
  data() {
    return {
      notification_text: "",
      search: "",
      add_dialog: false,
      del_dialog: false,
      edit_dialog: false,
      edit_form: [],
      checkin_dialog: false,
      edit_client: {},
      new_client: {},
      clients: [],
      headers: [
        {
          text: "Naam",
          align: "start",
          sortable: true,
          value: "name",
          class: "rounded-tl  darken-1"
        },
        {
          text: "Bedrijf",
          value: "company",
          class: "darken-1",
          sortable: false
        },
        { text: "E-mail", value: "email", class: "darken-1" },
        {
          text: "Kenteken",
          value: "plate",
          class: "darken-1",
          sortable: false
        },
        { text: "Telefoon", value: "tel", class: "darken-1" },
        {
          text: "Verwijderen",
          class: "darken-1",
          filterable: false,
          sortable: false
        },
        {
          text: "Bewerken",
          class: "darken-1",
          filterable: false,
          sortable: false
        },
        {
          text: "Inchecken",
          class: "darken-1",
          filterable: false,
          sortable: false
        }
      ]
    };
  },
  created() {
    this.allClientsData();
  },
  methods: {
    allClientsData() {
      let self = this;
      this.$store.dispatch("getReq", {
        url: "guests",
        params: {},
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        callback: function(res) {
          res.data.guests.forEach(data => {
            let clientdata = {
              id: data.guest_id,
              name: data.name,
              license_plate: data.license_plate,
              email: data.email,
              phone_number: data.phone_number,
              company: data.company
            };
            self.clients.push(clientdata);
            console.log(clientdata);
          });
        }
      });
    },

    confirmationDialog(userData) {
      this.del_dialog = true;
      this.currentUserData = userData;
    },

    newClient() {
      let self = this;
      this.$store.dispatch("postReq", {
        url: "guests",
        params: {
          name: this.new_client.name,
          license_plate: this.new_client.license_plate,
          email: this.new_client.email,
          phone_number: this.new_client.phone_number,
          company: this.new_client.company
        },
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function(res) {
          self.$store.dispatch("postReq", {
            url: `appointments`,
            params: {
              guest_id: res.guest_id,
              employee_name: res.name,
              checked_in: new Date().toISOString()
            },
            auth: self.$session.get("token"),
            csrftoken: self.$session.get("token"),
            xaccesstoken: self.$session.get("token"),
            callback: function(res) {
              if (res.error) {
                console.log(res.error);
              } else {
                self.$router.push({ name: "Ingecheckt" });
              }
            }
          });
        }
      });
    },

    checkIn(userData) {
      let self = this;
      this.$store.dispatch("postReq", {
        url: `appointments`,
        params: {
          guest_id: userData.id,
          employee_name: userData.name,
          checked_in: new Date().toISOString()
        },
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function(res) {
          if (res.error) {
            self.notification_text = res.error;
            self.$store.state.notificationStatus = true;
            console.log(res);
          } else {
            self.$router.push("/ingecheckt");
          }
        }
      });
    },

    editDialog(userData) {
      this.edit_dialog = true;
      this.currentUserData = userData;
      this.edit_form = [];
      this.edit_form.push(userData);
      console.log(this.edit_form[0].name);
      console.log(userData);
    },

    checkinDialog(userData) {
      this.checkin_dialog = true;
      this.currentUserData = userData;
    },

    editClient(userData) {
      let self = this;
      console.log(userData);
      // fill edit form with current guest data
      // this.edit_client.name = userData.name
      // this.edit_client.licence_plate = userData.licence_plate
      // this.edit_client.email = userData.email
      // this.edit_client.company = userData.company
      // this.edit_client.phone_number = userData.phone_number
      // if(this.edit_client.name != null){
      this.$store.dispatch("putReq", {
        url: `guest/${userData.id}`,
        params: {
          name: this.edit_client.name,
          licence_plate: this.edit_client.licence_plate,
          email: this.edit_client.email,
          phone_number: this.edit_client.phone_number,
          company: this.edit_client.company
        },
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function(data) {
          console.log(data);
          self.clients = [];
          self.allClientsData();
        }
      });
      // }else{
      //   alert('empty')
      // }
    },

    delClient(userData) {
      let self = this;
      this.$store.dispatch("deleteReq", {
        url: `guests/${userData.id}`,
        params: {},
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function(data) {
          console.log(data);
          self.clients = [];
          self.allClientsData();
        }
      });
    }
  }
};
</script>

<style scoped>
.main-container {
  width: auto;
  margin: auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.primary-section {
  background-color: beige;
  min-height: 80vh;
}

th {
  min-width: 350px;
}

h1 {
  text-align: left;
}
</style>
