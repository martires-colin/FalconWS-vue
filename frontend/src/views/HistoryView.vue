<template>
  <v-container>
    <v-row class="my-4">
      <div class="text-h4 text-center w-100">Transfer History</div>
    </v-row>
    <v-row class="mt-2">
      <v-expansion-panels>
        <v-expansion-panel
          v-for="t in transfers"
          :key="t._id.$oid"
        >
        <v-expansion-panel-title>
          <v-container>
            <v-row justify="space-between">
              <div class="panel-title">
                {{ t.srcIP }}<v-icon icon="mdi-arrow-right-bold-outline" class="mx-4"></v-icon>{{ t.destIP }} 
              </div>
              <div class="mx-6 d-flex align-center">
                {{ t.requestTime }}
              </div>
            </v-row>
          </v-container>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          
          <v-list>
            <v-list-item
              prepend-icon="mdi-bank-transfer-out"
            >
            <v-container class="px-2">
              <v-row>
                <v-col cols="3" class="p-0 mr-0">
                  Source
                </v-col>
                <v-divider vertical></v-divider>
                <v-col cols class="ml-6">
                  <v-row>
                    <p>
                      IP:&emsp;&emsp;&emsp;&emsp;&emsp;{{ t.srcIP }}
                    </p>
                  </v-row>
                  <v-row>
                    <p>
                      File Path:&emsp;&emsp;{{ t.srcDir }}
                    </p>
                  </v-row>
                </v-col>
              </v-row>
            </v-container>
            </v-list-item>

            <v-divider inset></v-divider>

            <v-list-item
              prepend-icon="mdi-bank-transfer-in"
            >
            <v-container class="px-2">
              <v-row>
                <v-col cols="3" class="p-0 mr-0">
                  Destination
                </v-col>
                <v-divider vertical></v-divider>
                <v-col cols class="ml-6">
                  <v-row>
                    <p>
                      IP:&emsp;&emsp;&emsp;&emsp;&emsp;{{ t.destIP }}
                    </p>
                  </v-row>
                  <v-row>
                    <p>
                      File Path:&emsp;&emsp;{{ t.destDir }}
                    </p>
                  </v-row>
                </v-col>
              </v-row>
            </v-container>
            </v-list-item>

            <v-divider inset></v-divider>

            <v-list-item
              prepend-icon="mdi-email-outline"
            >
            <v-container class="px-2">
              <v-row>
                <v-col cols="3" class="p-0 mr-0">
                  User Email
                </v-col>
                <v-divider vertical></v-divider>
                <v-col cols class="ml-6">
                  <div class=" d-flex align-center">
                    {{ t.email }}
                  </div>
                </v-col>
              </v-row>
            </v-container>
            </v-list-item>

            <v-divider inset></v-divider>

            <v-list-item
              prepend-icon="mdi-bank-outline"
            >
            <v-container class="px-2">
              <v-row>
                <v-col cols="3" class="p-0 mr-0">
                  Affiliation
                </v-col>
                <v-divider vertical></v-divider>
                <v-col cols class="ml-6">
                  <div class=" d-flex align-center">
                    {{ t.idp_name }}
                  </div>
                </v-col>
              </v-row>
            </v-container>
            </v-list-item>

            <v-divider inset></v-divider>

            <v-list-item
              prepend-icon="mdi-clock-time-four"
            >
            <v-container class="px-2">
              <v-row>
                <v-col cols="3" class="p-0 mr-0">
                 Request Time
                </v-col>
                <v-divider vertical></v-divider>
                <v-col cols class="ml-6">
                  <div class=" d-flex align-center">
                    {{ t.requestTime }}
                  </div>
                </v-col>
              </v-row>
            </v-container>
            </v-list-item>

            <v-divider inset></v-divider>

          </v-list>

        </v-expansion-panel-text>
      </v-expansion-panel>
      </v-expansion-panels>
    </v-row>

  </v-container>
</template>

<script>
import axios from 'axios'

export default {
	name: "HistoryView",
  data() {
    return {
      transfers: []
    }
  },
  methods: {
    async getHistory() {
      console.log("Getting Transfer History")
      axios.post("http://localhost:3000/getHistory", {
        user_email: this.$store.state.user.email
      }).then((res) => {
        const transfer_list = JSON.parse(res.data.transferData)
        const transfers = transfer_list
        transfers.forEach(transfer => {
          console.log(transfer)
          this.transfers.push(transfer)
        })
      })
    },
  },
  created() {
    this.getHistory();
  },
}
</script>

<style>

.panel-title {
  font-size: 1.2em;
}

</style>