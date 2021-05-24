<template>
  <section class="primary-section">
    <div class="main-container">
      <div>
        <!-- Header -->
        <h1 class="mb-3 mt-12">Gasten zoeken</h1>
        <!-- New client button -->
        <v-row>
          <v-dialog v-model="add_dialog" persistent max-width="600px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                  class="blue darken-1 mt-9 mb-12"
                  rounded
                  v-bind="attrs"
                  v-on="on"
              >
                <v-icon color="white">mdi-account-plus-outline</v-icon>
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
        <!-- Searchbar -->
        <v-text-field
            Naam
            label="Zoeken op naam"
            clearable
            class="mb-6"
        ></v-text-field>
        <!-- Datatable -->
        <v-data-table :headers="headers" :items="clients" hide-default-footer>
          <template v-slot:item="row">
            <tr>
              <td>{{ row.item.name }}</td>
              <td>{{ row.item.phone_number }}</td>
              <td>{{ row.item.email }}</td>
              <td>{{ row.item.company }}</td>
              <td>{{ row.item.licence_plate }}</td>
              <!-- Delete button -->
              <td>
                <v-btn
                    class="mx-2 red darken-3"
                    rounded
                    elevation="2"
                    @click.stop="confirmationDialog(row.item)"
                >
                  <v-icon color="white">
                    mdi-delete
                  </v-icon>
                </v-btn>
              </td>
              <!-- Edit button -->
              <td>
                <v-btn
                    class="mx-2 green darken-3"
                    rounded
                    elevation="2"
                    @click="editDialog(row.item)"
                >
                  <v-icon color="white">
                    mdi-wrench
                  </v-icon>
                </v-btn>
              </td>
            </tr>
          </template>
        </v-data-table>
      </div>
    </div>
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
          <v-spacer></v-spacer>
          <v-btn
              color="red darken-1"
              align="center"
              text
              @click="delClient(currentUserData)"
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
                    label="Naam"
                    v-model="edit_client.name"
                    required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                    label="Tel"
                    v-model="edit_client.phone_number"
                    required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                    label="Email"
                    v-model="edit_client.email"
                    required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                    label="Bedrijf"
                    v-model="edit_client.company"
                    required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                    label="Kenteken"
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
              color="green darken-1"
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
export default {
  name: "Clients",
  data() {
    return {
      add_dialog: false,
      del_dialog: false,
      edit_dialog: false,
      edit_client: {},
      new_client: {},
      clients: [],
      headers: [
        {
          text: "Naam",
          align: "start",
          sortable: true,
          value: "name",
          class: "blue white--text rounded-tl-lg darken-1"
        },
        {text: "Telefoon", value: "tel", class: "blue white--text darken-1"},
        {text: "E-mail", value: "email", class: "blue white--text darken-1"},
        {
          text: "Bedrijf",
          value: "company",
          class: "blue white--text darken-1"
        },
        {
          text: "Kenteken",
          value: "plate",
          class: "blue white--text darken-1"
        },
        {
          text: "Verwijderen",
          value: "plate",
          class: "blue white--text darken-1"
        },
        {
          text: "Bewerken",
          value: "plate",
          class: "blue white--text rounded-tr-lg darken-1"
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
        callback: function (res) {
          res.data.guests.forEach(data => {
            let clientdata = {
              id: data.guest_id,
              name: data.name,
              licence_plate: data.licence_plate,
              email: data.email,
              phone_number: data.phone_number,
              company: data.company
            };
            self.clients.push(clientdata);
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
          licence_plate: this.new_client.licence_plate,
          email: this.new_client.email,
          phone_number: this.new_client.phone_number,
          company: this.new_client.company
        },
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function (res) {
          if (res.status === 200) {
            console.log("OK");
          } else {
            console.log(res);
          }
        }
      });
    },

    editDialog(userData) {
      this.edit_dialog = true;
      this.currentUserData = userData;
    },

    editClient(userData) {
      let self = this;
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
        callback: function (data) {
          console.log(data);
        }
      });
    },

    delClient(userData) {
      let self = this;
      this.$store.dispatch("deleteReq", {
        url: `guests/${userData.id}`,
        params: {},
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function (data) {
          console.log(data);
        }
      });
    }
  }
};
</script>

<style scoped>
.main-container {
  width: 900px;
  margin: auto;
  display: flex;
  flex-wrap: wrap;
}

.primary-section {
  background-color: beige;
  min-height: 80vh;
}

h1 {
  text-align: left;
}
</style>
