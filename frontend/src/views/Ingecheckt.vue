<template>
  <section class="primary-section">
    <div class="main-container">
      <h1 class="mb-9 mt-12">Ingecheckte Gasten</h1>
      <div>
        <v-data-table :headers="headers" :items="ingecheckt" hide-default-footer>
        <template v-slot:item="row">
          <tr>
            <td>{{ row.item.name }}</td>
            <td>{{ row.item.tel }}</td>
            <td>{{ row.item.email }}</td>
            <td>{{ row.item.company }}</td>
            <td>{{ row.item.plate }}</td>
            <td>{{ row.item.checkin }}</td>
            <td>
              <v-btn class="mx-2 red darken-3" elevation="2" @click="onButtonClick(row.item)">
                Check-Out
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
  name: "Gastenlijst",
  methods: {
    onButtonClick(desserts) {
      //Todo API call + desserts.id
      console.log('click on ' + desserts.id)
    }
  },
  data() {
    //Return: Dummy Data, vervangen door JSON in formaat als hieronder.
    return {
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
          id: '78',
          name: 'Frozen Yogurt',
          tel: '0293827267',
          email: 'e@mail.com',
          company: 'Sogetto',
          plate: 'dk-si-ks',
          checkin: '13:12:11/03-03-03',
          checkout: 'knop',
        },
        {
          id: '18',
          name: 'Frozen Yogurt',
          tel: '0293827267',
          email: 'e@mail.com',
          company: 'Sogetto',
          plate: 'dk-si-ks',
          checkin: '13:12:11/03-03-03',
          checkout: 'knop',
        },
      ],
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