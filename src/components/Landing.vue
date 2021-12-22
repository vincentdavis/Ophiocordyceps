<template>
  <v-container>
    <v-card elevation="0">
      <v-card-text>
        <v-tabs v-model="tab">
          <v-tab>Default</v-tab>
          <v-tab>File Load</v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item>
            <v-row class="mt-2">
              <v-col cols="12" sm="6">
                <v-card color="primary">
                  <v-card-title class="white--text">Power</v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" sm="6">
                        <v-icon color="white" x-large>mdi-hydro-power</v-icon>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <b
                          class="text-h4 white--text"
                          v-show="response && response.power"
                          >{{
                            response && response.power ? response.power : ""
                          }}</b
                        >
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" sm="6">
                <v-card color="primary">
                  <v-card-title class="white--text">Cadence</v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" sm="6">
                        <v-icon color="white" x-large>mdi-bike-fast</v-icon>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <b class="text-h4 white--text">{{
                          response && response.cadence ? response.cadence : ""
                        }}</b>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row class="text-center mt-8">
              <v-col cols="12" sm="12">
                <v-slider
                  label="Power"
                  v-model="PW"
                  max="1000"
                  min="10"
                  thumb-label="always"
                ></v-slider>

                <v-text-field
                  type="number"
                  :rules="PV_Rule"
                  v-model="PV"
                  label="Power Variability"
                >
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
          </v-tab-item>
          <v-tab-item>
            <v-file-input
              v-model="file"
              @change="callAPI"
              hint="Add power and cadence column in excel"
              persistent-hint
              label="Upload file"
              chips
              truncate-length="15"
            ></v-file-input>
            <v-data-table
            v-if="DataItems.length >=1"
            :items="DataItems"
            :headers="[
            {'text': 'Power', 'value': 'power'},
            {'text': 'Cadence', 'value': 'cadence'}
            ]"
            >
            </v-data-table>
          </v-tab-item>
        </v-tabs-items>
      </v-card-text>
      <v-card-actions>
        <!-- <b v-if="response">Response :{{ response }}</b> -->

        <v-spacer></v-spacer>
        <!-- <v-btn small color="primary" :loading="loading" @click="send"
          >Send</v-btn
        > -->
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "HelloWorld",
  mounted() {
    // this.load()
  },
  methods: {
    callAPI() {
      var data = new FormData();
      data.append("file", this.file);
      fetch("http://127.0.0.1:9010/fileLoad", {
        method: "POST",
        body: data,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          for(var i of data){
            this.DataItems.push({
              "power" : i[0], "cadence" : i[1]
            })
                console.log(i)
                this.PW_O = i[0]
                this.COR_O = i[1]
                this.send()
              }
          

          
        });
    },
    load() {
      var temp = this;
      this.timer = setInterval(function () {
        temp.send();
      }, 1000);
    },
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
          this.PRL +
          "&PW_O=" +
          this.PW_O+
          "&COR_O=" +
          this.COR_O
      )
        .then((response) => response.json())
        .then((data) => {
          // console.log(data);
          this.response = data;
          this.loading = false;
        })
        .catch((error) => {
          console.log(error);
          this.response =
            "Backend Server Not Running.. please run backend server";
          this.loading = false;
        });
    },
  },
  data: () => ({
    DataItems: [],
    file: null,
    timer: null,
    tab: null,
    loading: false,
    response: null,
    PW: 0,
    PV: 0,
    WPR1: 0.75,
    WPR2: 1.25,
    COR: 0,
    PRL: 0,
    PW_O: null,
    COR_O: null,
    PV_Rule: [
      (v) => !!v || "This field is required",
      (v) => (v && v >= -5) || "Loan should be above -5",
      (v) => (v && v <= 5) || "Max should not be above 5",
    ],
  }),
  watch: {
    tab(value) {
      console.log(value);
      if (value == 1) {
        clearTimeout(this.timer);
      }
      if (value == 0) {
        console.log("Start Over");
        this.load();
        // var temp = this;
        // this.timer = null
        // this.timer = setInterval(function () {
        //   temp.send();
        // }, 1000);
      }
      // else {
      //   var temp = this;

      //   this.timer = setInterval(function () {
      //     temp.send();
      //   }, 1000);
      // }
    },

    // PW(value) {
    //   value;
    //   this.send();
    // },
    // PV(value) {
    //   value;
    //   this.send();
    // },
    // WPR1(value) {
    //   value;
    //   this.send();
    // },
    // WPR2(value) {
    //   value;
    //   this.send();
    // },
    // COR(value) {
    //   value;
    //   this.send();
    // },
    // PRL(value) {
    //   value;
    //   this.send();
    // },
  },
};
</script>
