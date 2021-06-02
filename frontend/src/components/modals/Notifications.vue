<template>
    <v-snackbar
      v-model="$store.state.notificationStatus"
      timeout="5000"
      :top='true'
      :right='true'
      :color= color
    >
      {{content}}

      <template v-slot:action="{ attrs }">
        <v-btn
          color="#fff"
          text
          v-bind="attrs"
          @click="$store.state.notificationStatus = false"
        >
          <v-icon small>fas fa-times</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
</template>

<script>
export default {
    name: 'Notification',

    props: {
      content: String,
      color: String
    },

    data () {
        return {
        }
    },

    created(){},

    methods: {

    }
}
</script>