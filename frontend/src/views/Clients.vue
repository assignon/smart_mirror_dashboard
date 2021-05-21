<template>
  <section class="primary-section">
    <div class="main-container">
      <div>
        <h1 class="mb-3 mt-12">Gasten zoeken</h1>
      </div>
      <div>
        <v-text-field
          v-model="message2"
          Naam
          label="Zoeken op naam"
          clearable
          class="mb-6"
        ></v-text-field>
        <v-data-table :headers="headers" :items="clients" hide-default-footer>
          <template v-slot:item="row">
            <tr>
              <td>{{ row.item.name }}</td>
              <td>{{ row.item.tel }}</td>
              <td>{{ row.item.email }}</td>
              <td>{{ row.item.company }}</td>
              <td>{{ row.item.plate }}</td>
              <td>
                <v-btn
                  class="mx-2 red darken-3"
                  rounded
                  elevation="2"
                  @click="onButtonClick(row.item)"
                >
                  <v-icon color="white">
                    mdi-delete
                  </v-icon>
                </v-btn>
              </td>
              <td>
                <v-btn
                  class="mx-2 green darken-3"
                  rounded
                  elevation="2"
                  @click="onButtonClick(row.item)"
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
  </section>
</template>

<script>
export default {
  name: "Clients",
  data() {
    return {
      headers: [
        {
          text: "Naam",
          align: "start",
          sortable: true,
          value: "name",
          class: "blue white--text rounded-tl-lg darken-1"
        },
        { text: "Telefoon", value: "tel", class: "blue white--text darken-1" },
        { text: "E-mail", value: "email", class: "blue white--text darken-1" },
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
      ],
      clients: [
        {
          id: "78",
          name: "Frozen Yogurt",
          tel: "0293827267",
          email: "e@mail.com",
          company: "Sogetto",
          plate: "dk-si-ks"
        }
      ]
    };
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
