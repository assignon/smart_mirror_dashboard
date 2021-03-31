<template>
  <div>
    <h1 class="mb-9">Ingecheckte Gasten</h1>
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
            <v-btn class="mx-2" elevation="2" @click="onButtonClick(row.item)">
              Check-Out
            </v-btn>
          </td>
        </tr>
      </template>
    </v-data-table>

  </div>

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
        },
        {text: 'Telefoon', value: 'tel'},
        {text: 'E-mail', value: 'email'},
        {text: 'Bedrijf', value: 'company'},
        {text: 'Kenteken', value: 'plate'},
        {text: 'Check-in', value: 'checkin'},
        {text: 'Check-out', value: 'checkout'},
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
div {
  width: 900px;
  margin: auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>