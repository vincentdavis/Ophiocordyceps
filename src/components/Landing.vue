<template>
  <v-container>
    <v-dialog
      v-model="dialog"
      width="500"
    >
      

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          .csv format
        </v-card-title>

        <v-card-text>
          <v-data-table
          :items="[
          {'power': 250 , 'cadence': 85},
          {'power': 251 , 'cadence': 85},
          ]"
          hide-default-footer
          :headers="[{text: 'power' , value: 'power'}, {text: 'cadence' , value: 'cadence'}]"
          ></v-data-table>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
            Got It
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-card elevation="0">
      <v-overlay absolute :value="overlay">
        <v-btn
          class="text-decoration-none"
          large
          @click="
            overlay = false;
            tab = 0;
          "
          color="primary"
        >
          Basic</v-btn
        >

        <v-btn
          class="ml-2"
          large
          @click="
            overlay = false;
            tab = 1;
          "
          color="primary"
        >
          <v-icon>mdi-file-upload-outline</v-icon> File Upload</v-btn
        >
      </v-overlay>
      <v-card-text>
        <v-tabs v-model="tab">
          <v-tab v-show="false">Default</v-tab>
          <v-tab v-show="false">File Upload</v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item>
            <v-row>
              <v-col cols="12" sm="6">
                <v-icon
                  v-if="!overlay"
                  @click="
                    tab = 0;
                    overlay = true;
                  "
                  title="Back"
                  x-large
                  color="primary"
                  >mdi-keyboard-backspace</v-icon
                >
              </v-col>
              <v-col cols="12" sm="6" class="d-flex justify-end">
                <v-btn
                  class="text-decoration-none"
                  outlined
                  v-if="!overlay && !basic_running"
                  @click="
                    startOver = true;
                    basic_running = true;
                    load();
                  "
                  color="green"
                >
                  <v-icon>mdi-play</v-icon> Start</v-btn
                >
                <v-btn
                  class="ml-2"
                  v-if="!overlay && basic_running"
                  outlined
                  @click="
                    basic_running = false;
                    stop();
                  "
                  color="red"
                >
                  <v-icon>mdi-pause</v-icon> Stop</v-btn
                >
              </v-col></v-row
            >
            <v-row class="mt-2">
              <v-col cols="12" sm="6">
                <v-card color="primary">
                  <v-card-title class="white--text">Power</v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" sm="6">
                        <v-icon color="white" x-large>mdi-power-plug </v-icon>
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
            <v-icon
              @click="
                tab = 0;
                overlay = true;
              "
              title="Back"
              x-large
              color="primary"
              >mdi-keyboard-backspace</v-icon
            >
            <v-alert class="mt-1" dense type="info">
              RUN FILE will loop of the rows in the csv. Sending metrics
              <strong>1 second </strong> per row.
            </v-alert>
            <v-row>
              <v-col cols="12" sm="10">
                <v-file-input
                  v-model="file"
                  hint="Accept File format (.csv)"
                  persistent-hint
                  label="Upload file"
                  chips
                  truncate-length="15"
                ></v-file-input>
                <a  @click="dialog=true">see exmaple</a>
              </v-col>
              <v-col cols="12" sm="2">
                <v-btn
                  :disabled="!file"
                  class="mt-3"
                  @click="callAPI"
                  outlined
                  color="primary"
                  >Run File</v-btn
                >
              </v-col>
            </v-row>
            

            <!-- <v-data-table
              dense
              
              :items="DataItems"
              :headers="[
                { text: 'Id', value: 'id' },
                { text: 'Power', value: 'power' },
                { text: 'Cadence', value: 'cadence' },
              ]"
            >
            </v-data-table> -->
            <v-row v-if="DataItems.length >= 1 && file" class="mt-2">
              <v-col cols="12" sm="6">
                <v-card color="primary">
                  <v-card-title class="white--text">Power</v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" sm="6">
                        <v-icon color="white" x-large>mdi-power-plug </v-icon>
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
            <center v-if="DataItems.length >= 1 && file">
              <v-btn
              v-if="FileStop"
                class="mt-2"
                outlined
                @click="callAPI();FileStop=false"
                color="green"
              >
                <v-icon > mdi-play </v-icon>
                Start</v-btn>
                <v-btn
                v-if="!FileStop"
                class="mt-2"
                outlined
                @click="
                  stopFile();
                  FileStop = true;
                "
                color="red"
              >
                <v-icon > mdi-pause</v-icon>
                Stop</v-btn>
            </center>
            <v-simple-table v-if="DataItems.length >= 1 && file">
              <template v-slot:default>
                <thead>
                  <tr>
                    <th class="text-left">
                      Id
                    </th>
                    <th class="text-left">
                      Power
                    </th>
                    <th class="text-left">
                      Cadence
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="item in DataItems"
                    :key="item.id"
                  >
                    <td :bgcolor="item.id == currentIndex ? '#007bff': ''">  {{ item.id }} </td>
                    <td :bgcolor="item.id == currentIndex ? '#007bff': ''">{{ item.power }}</td>
                    <td :bgcolor="item.id == currentIndex ? '#007bff': ''">{{ item.cadence }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
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
    LoopFileData(data) {
      for (var i of data) {
        console.log(i);
        this.PW_O = i[0];
        this.COR_O = i[1];
        this.send();
        
      }
    },
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
          this.DataItems = []
          var temp= this
          data.forEach(function (value, i) {
              temp.DataItems.push({
              id: i,
              power: value[0],
              cadence: value[1],
            });
          });
          // for (var j,i of data) {
          //   this.DataItems.push({
          //     id: j,
          //     power: i[0],
          //     cadence: i[1],
          //   });
          // }

          this.loadFile(data);
        });
    },
    // sleep(ms) {
    //   return new Promise(resolve => setTimeout(resolve, ms));
    // },
    load() {
      this.overlay = false;
      var temp = this;
      this.timer = setInterval(function () {
        temp.send();
      }, 1000);
    },
    loadFile(data) {
      var temp = this;
      var datalocal = data
      var i =0
      this.Filetimer = setInterval(function () {
        console.log(i)
        console.log(datalocal[i])
        
        temp.PW_O = datalocal[i][0];
        temp.COR_O = datalocal[i][1];
        temp.send();
        temp.currentIndex = i
        i++
        if (i>=datalocal.length){
          i = 0
        }
        
        // temp.LoopFileData(data);
      }, 1000);
    },
    stop() {
      clearTimeout(this.timer);
    },
    stopFile() {
      clearTimeout(this.Filetimer);
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
          this.PW_O +
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
    currentIndex: null,
     dialog: false,
    basic_running: false,
    startOver: false,
    FileStop: false,
    overlay: true,
    DataItems: [],
    file: null,
    timer: null,
    Filetimer: null,
    tab: "2",
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
        this.stop();
      }
      if (value == 0 && this.startOver) {
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
