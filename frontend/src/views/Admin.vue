<template>
  <section class="primary-section">
    <div class="main-container">
      <div>
        <!-- Title -->
        <div>
          <h1 class="mb-3 mt-12">Systeem gebruikers</h1>
        </div>
        <!-- New user button -->
        <v-row>
          <v-dialog v-model="add_dialog" persistent max-width="600px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="mt-9 mb-12 white--text"
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
                        v-model="new_user.name"
                        label="Name*"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="new_user.email"
                        label="Email*"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="new_user.password"
                        label="Password*"
                        type="password"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-select
                        v-model="new_user.is_admin"
                        :items="adminBool"
                        item-value="val"
                        label="Admin*"
                        required
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-container>
                <small>*Verplichte velden</small>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="#FF4411" text @click="add_dialog = false">
                  Sluiten
                </v-btn>
                <v-btn
                  color="green darken-1"
                  text
                  @click="
                    add_dialog = false;
                    newUser();
                  "
                >
                  Toevoegen
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>
        <!-- Data Table for system users / Admin administration -->
        <v-data-table :headers="headers" :items="users" hide-default-footer>
          <template v-slot:item="row">
            <tr :id="row.item.id">
              <td>{{ row.item.id }}</td>
              <td>{{ row.item.name }}</td>
              <td>{{ row.item.email }}</td>
              <td>{{ row.item.is_admin }}</td>
              <!-- Delete Button -->
              <td :class="row.item.name.replace(/ /g, '') + row.item.id">
                <v-btn
                  class="mx-2 darken-3"
                  rounded
                  elevation="2"
                  @click.stop="confirmationDialog(row.item)"
                >
                  <v-icon color="#FF4411">
                    mdi-delete
                  </v-icon>
                </v-btn>
              </td>
              <!-- Edit Button -->
              <td :class="row.item.name.replace(/ /g, '') + row.item.id">
                <v-btn
                  class="mx-2 darken-3"
                  rounded
                  @click.stop="editDialog(row.item)"
                >
                  <v-icon color="green">mdi-wrench</v-icon>
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
            @click="delUser(currentUserData)"
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
                  label="Naam*"
                  v-model="edit_user.name"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="Email*"
                  v-model="edit_user.email"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  :items="['True', 'False']"
                  label="Admin*"
                  v-model="edit_user.is_admin"
                  required
                ></v-select>
              </v-col>
            </v-row>
          </v-container>
          <small>*Verplichte velden</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="#FF4411" text @click="edit_dialog = false">
            Sluiten
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="
              edit_dialog = false;
              editUser(currentUserData);
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
  name: "Admin",
  data() {
    return {
      new_user: {},
      edit_user: {},
      adminBool: [
        { text: "Ja", val: true },
        { text: "Nee", val: false }
      ],
      add_dialog: false,
      del_dialog: false,
      edit_dialog: false,
      headers: [
        {
          text: "ID",
          align: "start",
          sortable: true,
          value: "id",
          class: "rounded-tl-lg darken-1"
        },
        {
          text: "Name",
          sortable: true,
          value: "name",
          class: "darken-1"
        },
        {
          text: "Email",
          sortable: true,
          value: "email",
          class: "darken-1"
        },
        {
          text: "Admin",
          sortable: true,
          value: "admin",
          class: "darken-1"
        },
        {
          text: "Verwijder",
          sortable: false,
          align: "center",
          value: "delete",
          class: "darken-1"
        },
        {
          text: "Bewerken",
          sortable: false,
          align: "center",
          value: "delete",
          class: "rounded-tr-lg darken-1"
        }
      ],
      users: []
    };
  },
  created() {
    this.allUsersData();
  },
  methods: {
    allUsersData() {
      let self = this;
      this.$store.dispatch("getReq", {
        url: "users",
        params: {},
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        callback: function(res) {
          res.data.users.forEach(data => {
            let userdata = {
              id: data.user_id,
              name: data.name,
              is_admin: data.is_admin,
              email: data.email
            };
            self.users.push(userdata);
          });
        }
      });
    },

    newUser() {
      let self = this;
      this.$store.dispatch("postReq", {
        url: "users",
        params: {
          name: this.new_user.name,
          is_admin: this.new_user.is_admin,
          email: this.new_user.email,
          password: this.new_user.password
        },
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function(res) {
          if (res.status === 200) {
            console.log("OK");
            window.location.reload()
          } else {
            console.log(res);
          }
        }
      });
    },

    confirmationDialog(userData) {
      this.del_dialog = true;
      this.currentUserData = userData;
    },

    editDialog(userData) {
      this.edit_dialog = true;
      this.currentUserData = userData;
    },

    editUser(userData) {
      let self = this;
      this.$store.dispatch("putReq", {
        url: `user/${userData.id}`,
        params: {
          name: this.edit_user.name,
          email: this.edit_user.email,
          is_admin: this.edit_user.is_admin
        },
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function(data) {
          console.log(data);
          window.location.reload()
        }
      });
    },

    delUser(userData) {
      let self = this;
      this.$store.dispatch("deleteReq", {
        url: `users/${userData.id}`,
        params: {},
        auth: self.$session.get("token"),
        csrftoken: self.$session.get("token"),
        xaccesstoken: self.$session.get("token"),
        callback: function(data) {
          console.log(data);
          window.location.reload()
        }
      });
    }
  }
};
</script>

<style scoped>
.new-user-button {
  text-align: left;
}

.v-card__title {
  display: revert;
}

.v-card-actions {
  display: revert;
}

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

h1 {
  text-align: left;
}
</style>
