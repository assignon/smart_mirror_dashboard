<template>
    <div class='checkin-temp-core' v-if='$store.state.appointmentArr.length>0'>
    <!-- <div class='checkin-temp-core'> -->
        <div class="row mt-15 animated fadeInUp">
            <div class="col">
                <v-text-field label="Naam" v-model="name" outlined dense></v-text-field>
                <v-text-field label="Email" v-model="email" outlined dense></v-text-field>
                <v-text-field label="Telefoon" v-model="tel" outlined dense></v-text-field>
                <v-btn class="mx-2" @click="onButtonClick()">
                    Check-in
                </v-btn>
            </div>
            <div class="col">
                <v-text-field label="Afspraak met" v-model="appointment" outlined dense></v-text-field>
                <v-text-field label="Kenteken " v-model="licensePlate" outlined dense></v-text-field>
                <v-text-field label="Bedrijf" v-model="company" outlined dense></v-text-field>
                <v-select
                    :items="items"
                    label="Bewaartermijn"
                    outlined dense
                    v-model='retention'
                ></v-select>
            </div>
            <div class="col">
                <v-img
                    contain
                    lazy-src="https://picsum.photos/id/11/10/6"
                    max-height="300"
                    max-width="290"
                    src="https://picsum.photos/id/11/500/300"
                ></v-img>
            </div>
        </div>

        <!-- <div class='no-checkin' v-else>
            <v-icon style='font-size: 100px;color:black' class='mb-3'>fas fa-user</v-icon>
            <p>Geen nieuwe gemelde gasten</p>
        </div> -->
    </div>
</template>

<script>
export default {
    name: 'CheckinTemplate',

    data(){
        return{
            items: ['1 DAG','1 JAAR'],
            name: null,
            email: null,
            tel: null,
            appointment: null,
            licensePlate: null,
            company: null,
            retention: null,
            appointmentArr: [],
        }
    },

    created(){
        let self = this
        this.scannedGuestData(self.$store.state.socket)
    },

    methods: {
        onButtonClick() {
            //Todo API call + desserts.id
            this.$store.state.appointmentArr = []
        },

        scannedGuestData(socket){
            let self = this

            socket.on('face_scanned', function(data){
                console.log('socket data', data);
                self.$store.state.appointmentArr.push(data.guest_id)
                self.name = data.name
                self.email = data.email
                self.tel = data.tel
                self.appointment = data.appointment
                self.licensePlate = data.license_plate
                self.company = data.company
                self.retention = data.retention==1 ? '1 DAG' : '1 JAAR'
            });

        },
    }
}
</script>

<style scoped>
    .checkin-temp-core{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: auto;
    }
    .row {
        width: 1000px;
        margin: auto;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
    }

    div .col {
        width: 32%;
    }
    /* .no-checkin{
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
  } */
</style>