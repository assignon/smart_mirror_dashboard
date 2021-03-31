<template>
  <div>
    <h1 class="mb-9">Gasten zoeken</h1>
    <v-text-field
            v-model="message2"
            Naam
            label="Naam"
            clearable
          ></v-text-field>
    <v-btn class="mx-2 mt-3 mb-3" elevation="2" @click="onButtonClick(row.item)">
              Nieuwe Gast
            </v-btn>
    <v-data-table :headers="headers" :items="clients" hide-default-footer>
      <template v-slot:item="row">
        <tr>
          <td>{{ row.item.name }}</td>
          <td>{{ row.item.tel }}</td>
          <td>{{ row.item.email }}</td>
          <td>{{ row.item.company }}</td>
          <td>{{ row.item.plate }}</td>
          <td>
            <v-btn class="mx-2" elevation="2" @click="onButtonClick(row.item)">
              Verwijderen
            </v-btn>
          </td>
          <td>
            <v-btn class="mx-2" elevation="2" @click="onButtonClick(row.item)">
              Bewerken
            </v-btn>
          </td>
        </tr>
      </template>
    </v-data-table>
  </div>

</template>

<script>
export default {
  name: "Clients",
  data() {
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
        {text: 'Verwijderen', value: 'plate'},
        {text: 'Bewerken', value: 'plate'},
      ],
      clients: [
        {
          id: '78',
          name: 'Frozen Yogurt',
          tel: '0293827267',
          email: 'e@mail.com',
          company: 'Sogetto',
          plate: 'dk-si-ks',
        }
      ],
    }
  },
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