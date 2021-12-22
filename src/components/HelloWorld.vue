<template>
  <v-container>
    <v-card elevation="0">
      <v-card-title> Bot </v-card-title>
      <v-card-text>
        <v-row class="text-center">
          <v-col cols="12" sm="12">
            <v-slider
              label="Power"
              v-model="PW"
              max="1000"
              min="10"
              thumb-label="always"
            ></v-slider>

            <v-text-field v-model="PV" label="Power Variability">
            </v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="WPR1"
              label="Within power range"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="WPR2"
              label="Within power range"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="12">
            <v-text-field
              v-model="COR"
              label="Cadence Offset Range"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="12">
            <v-text-field
              v-model="PRL"
              label="Power Range Limits"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <b v-if="response">Response :{{ response }}</b>

        <v-spacer></v-spacer>
        <v-btn small color="primary" :loading="loading" @click="send"
          >Send</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "HelloWorld",
  mounted() {},
  methods: {
    send() {
      this.loading = true;
      this.response = null;
      fetch(
        "http://127.0.0.1:9010/request?PW=" +
          this.PW +
          "&PV=" +
          this.PV +
          "&WPR1=" +
          this.WPR1 +
          "&WPR2=" +
          this.WPR2 +
          "&COR=" +
          this.COR +
          "&PRL=" +
          this.PRL
      )
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.response = data;
          this.loading = false;
        })
        .catch((error) => {
          console.log(error)
            this.response = "Backend Server Not Running.. please run backend server";
          this.loading = false;
          });
    },
  },
  data: () => ({
    loading: false,
    response: null,
    PW: 0,
    PV: 0,
    WPR1: 0.75,
    WPR2: 1.25,
    COR: 0,
    PRL: 0,
  }),
};
</script>
