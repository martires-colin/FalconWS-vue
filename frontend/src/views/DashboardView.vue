<template>
  <div>
    <v-container fluid>
    <!-- <div class="">
      {{ this.$store.state.user.full_name }}
      {{ this.$store.state.user.email }}
      {{ this.$store.state.user.idp_name }}
      {{ this.$store.state.user.access_token }}
      {{ this.$store.state.user.id_token_jwt }}
      {{ this.$store.state.site_1 }}
      {{ this.$store.state.site_2 }}
    </div> -->

      <!-- Page Header -->
      <v-row>
        <div class="text-h4 text-center w-100">File Transfer Portal</div>
      </v-row>

      <!-- File Browser Section -->
      <v-row>
        <!-- Site 1 -->
        <v-col class="ma-1">
          <v-row>
            <!-- If user not logged into site, display button, else display form -->
            <div v-if="this.$store.state.site_1" class="text-center w-100">
              <div class="text-h5 ma-2">{{ this.$store.state.site_1.idp_name }}</div>
              
              <form @submit.prevent="submit_s1">
                <v-select
                  v-model="ip_address_s1.value.value"
                  :items=site1_ips
                  item-text="ip"
                  item-value="ip"
                  :item-disabled="checkIsItemDisabled"
                  :error-messages="ip_address_s1.errorMessage.value"
                  label="IP Address"
                ></v-select>
                <v-text-field
                  v-model="file_path_s1.value.value"
                  :error-messages="file_path_s1.errorMessage.value"
                  label="File Path"
                ></v-text-field>
                <v-btn class="me-4" type="submit">
                  submit
                </v-btn>
              </form>

            </div>
            <div v-else class="text-center w-100">
              <div class="text-h5">Site 1</div>
              <v-btn @click="loginSite1" color="blue-lighten-1">Site 1 Login</v-btn>
            </div>
          </v-row>
          <v-row>
            <!-- {{ this.site1_files }} -->
            <v-table v-if="this.site2_files.length >= 0" class="w-100 my-4" style="max-height:50vh; overflow:auto">
                <thead>
                <tr>
                  <th class="text-center">
                    <v-btn @click="exploreS1(none, true)" icon="mdi-keyboard-backspace" size="small" variant="text"></v-btn>
                  </th>
                  <th class="text-left">
                  File Name
                  </th>
                  <th class="text-left">
                  Last Modified
                  </th>
                  <th class="text-center">
                  Type
                  </th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="file in this.site1_files" :key="file.name">
                    <td class="text-center"><input type="checkbox" :value="file.name" v-model="selected"></td>
                    <td class="text-left" style="max-width: 20vw; overflow:auto">
                      <a href="#" @click="exploreS1(file.name, false)" v-if="file.type == 'dir'">{{ file.name }}</a>
                      <p v-else>{{ file.name }}</p>
                    </td>
                    <td class="text-left">{{ file.last_modified }}</td>
                    <td class="text-center">
                      <v-icon v-if="file.type == 'dir'" icon="mdi-folder-outline"></v-icon>
                      <v-icon v-else icon="mdi-file-outline"></v-icon>
                    </td>
                </tr>
                </tbody>
            </v-table>
          </v-row>
        </v-col>

        <v-col cols="1" class="d-flex justify-center align-center" style="height: 80vh">
            <!-- Initiate Transfer Button -->
          <!-- <v-row v-if="this.site1_files.length > 0 && this.site2_files.length > 0"> -->
          <v-row>
            <div class="text-center w-100">
              <!-- {{ selected }} -->
              <v-btn @click="transfer()" color="blue-lighten-1">Transfer</v-btn>
            </div>
          </v-row>
        </v-col>

        <!-- Site 2 -->
        <v-col class="ma-1">
          <v-row>
            <!-- If user not logged into site, display button, else display form -->
            <div v-if="this.$store.state.site_2" class="text-center w-100">
              <div class="text-h5 ma-2">{{ this.$store.state.site_2.idp_name }}</div>
              
              <form @submit.prevent="submit_s2">
                <v-select
                  v-model="ip_address_s2.value.value"
                  :items=site2_ips
                  item-text="ip"
                  item-value="ip"
                  :item-disabled="checkIsItemDisabled"
                  :error-messages="ip_address_s2.errorMessage.value"
                  label="IP Address"
                ></v-select>
                <v-text-field
                  v-model="file_path_s2.value.value"
                  :error-messages="file_path_s2.errorMessage.value"
                  label="File Path"
                ></v-text-field>
                <v-btn class="me-4" type="submit">
                  submit
                </v-btn>
              </form>

            </div>
            <div v-else class="text-center w-100">
              <div class="text-h5">Site 2</div>
              <v-btn @click="loginSite2" color="blue-lighten-1">Site 2 Login</v-btn>
            </div>
          </v-row>
          <v-row>
            <!-- {{ this.site2_files }} -->
            <v-table v-if="this.site2_files.length >= 0" class="w-100 my-4" style="max-height:50vh; overflow:auto">
                <thead>
                <tr>
                  <th class="text-center">
                    <v-btn @click="exploreS2(none, true)" icon="mdi-keyboard-backspace" size="small" variant="text"></v-btn>
                  </th>
                  <th class="text-left">
                  File Name
                  </th>
                  <th class="text-left">
                  Last Modified
                  </th>
                  <th class="text-center">
                  Type
                  </th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="file in this.site2_files" :key="file.name">
                    <td class="text-center"><input type="checkbox" disabled></td>
                    <td class="text-left" style="max-width: 20vw; overflow:auto">
                      <a href="#" @click="exploreS2(file.name)" v-if="file.type == 'dir'">{{ file.name }}</a>
                      <p v-else>{{ file.name }}</p></td>
                    <td class="text-left">{{ file.last_modified }}</td>
                    <td class="text-center">
                      <v-icon v-if="file.type == 'dir'" icon="mdi-folder-outline"></v-icon>
                      <v-icon v-else icon="mdi-file-outline"></v-icon>
                    </td>
                </tr>
                </tbody>
            </v-table>
          </v-row>

        </v-col>
      </v-row>

    </v-container>
	</div>
</template>

<script>
import { ref } from 'vue'
// import { useStore} from "vuex";
// import {computed} from "vue";
import { useField, useForm } from 'vee-validate'
import axios from 'axios'

export default {
	name: "DashboardView",
  data() {
    return {
      selected: []
    }
  },
  setup () {
    // const store = useStore();

    const { handleSubmit, handleReset } = useForm({
      // validationSchema: {
      //   file_path_s1 (value) {
      //     if (value) return true
      //     return 'Must be a valid file path.'
      //   },
      //   ip_address_s1 (value) {
      //     if (value) return true
      //     return 'Select an IP address.'
      //   },
      //   file_path_s2 (value) {
      //     if (value) return true
      //     return 'Must be a valid file path.'
      //   },
      //   ip_address_s2 (value) {
      //     if (value) return true
      //     return 'Select an IP address.'
      //   }
      // },
    })

    const file_path_s1 = useField('file_path_s1')
    const ip_address_s1 = useField('ip_address_s1')
    const site1_ips = ref([])
    const site1_files = ref([])

    const submit_s1 = handleSubmit(values => {
      console.log("SITE 1")
      console.log(values.file_path_s1)
      console.log(values.ip_address_s1)

      axios.post("http://localhost:3000/site1_ip", {
        site1_IP: values.ip_address_s1,
        site1_access_token: "NB2HI4DTHIXS6Y3JNRXWO33OFZXXEZZPN5QXK5DIGIXTOZBTG43DCZTDMFRGENBQGEZGGOJUG5QTGMTFGQZDMMBUGVQTMNR7OR4XAZJ5MFRWGZLTONKG623FNYTHI4Z5GE3DQMJXHE2DEMRTGIYDIJTWMVZHG2LPNY6XMMROGATGY2LGMV2GS3LFHU4TAMBQGAYA",
        site1_id_token_jwt: "eyJ0eXAiOiJKV1QiLCJraWQiOiIyNDRCMjM1RjZCMjhFMzQxMDhEMTAxRUFDNzM2MkM0RSIsImFsZyI6IlJTMjU2In0.eyJlbWFpbCI6ImNtYXJ0aXJlc0BuZXZhZGEudW5yLmVkdSIsImdpdmVuX25hbWUiOiJDb2xpbiIsImZhbWlseV9uYW1lIjoiTWFydGlyZXMiLCJuYW1lIjoiQ29saW4gTCBNYXJ0aXJlcyIsImNlcnRfc3ViamVjdF9kbiI6Ii9EQz1vcmcvREM9Y2lsb2dvbi9DPVVTL089VW5pdmVyc2l0eSBvZiBOZXZhZGEsIFJlbm8vQ049Q29saW4gTWFydGlyZXMgRTE1Mjc2IiwiaWRwIjoiaHR0cHM6Ly9pZHAyLnVuci5lZHUvaWRwL3NoaWJib2xldGgiLCJpZHBfbmFtZSI6IlVuaXZlcnNpdHkgb2YgTmV2YWRhLCBSZW5vIiwiZXBwbiI6ImNtYXJ0aXJlc0B1bnIuZWR1IiwiZXB0aWQiOiJodHRwczovL2lkcDIudW5yLmVkdS9pZHAvc2hpYmJvbGV0aCFodHRwczovL2NpbG9nb24ub3JnL3NoaWJib2xldGghWmZaS1pVWFRhT2w2WmFmT3FXdmM0YWRVWnRnPSIsImFmZmlsaWF0aW9uIjoic3R1ZGVudEB1bnIuZWR1O21lbWJlckB1bnIuZWR1O2ZhY3VsdHlAdW5yLmVkdTtsaWJyYXJ5LXdhbGstaW5AdW5yLmVkdTtzdGFmZkB1bnIuZWR1O2VtcGxveWVlQHVuci5lZHUiLCJhY3IiOiJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YWM6Y2xhc3NlczpQYXNzd29yZFByb3RlY3RlZFRyYW5zcG9ydCIsImlzcyI6Imh0dHBzOi8vY2lsb2dvbi5vcmciLCJzdWIiOiJodHRwOi8vY2lsb2dvbi5vcmcvc2VydmVyRS91c2Vycy8xNTI3NiIsImF1ZCI6ImNpbG9nb246L2NsaWVudF9pZC8xYTA1MTE0NWVjYjQzNzUwOGVkOGE4ODcxYmVkN2I3NyIsImp0aSI6Imh0dHBzOi8vY2lsb2dvbi5vcmcvb2F1dGgyL2lkVG9rZW4vMTFlNDk2MTc0YjY0NWRjYTk1MmEwYzk1NTk2OGI5ZGUvMTY4MTc5NDIyMzA2MSIsIm5vbmNlIjoiTEhGcG9qSW8zV0JkT2hkZSIsImF1dGhfdGltZSI6MTY4MTc5MzY4NSwiZXhwIjoxNjgxNzk1MTIzLCJpYXQiOjE2ODE3OTQyMjN9.cL1EBdX2SmbOmBnD4iFpAg1seafL6gkuCkG21EOnUYp_KF9VCHDpzr-rVdLVPBW_jESL3Grr877jKwkdmXVZsNrLmWP2Y1nbEF587dw5UEwP38pUnfHgU63w7FP7kA1LnnCBtLisvLB-6XG-R8ahYCrDeYWMbOWILPHuZt0_nIW9Dc1BzqfAqN8u6mP-H6JB4g0BNUihcH63DN3qdUN-2J5mSIJQ8vIr4B2WLhTuGjw4mR4vttm-3x8jaW0-mFmcqAtEbSytkZ24d9WuYqMy5-a0YLn3w3r6fJomdKkV8zTYrl6odXbii-C_jq05Dj54nLoxm9x2dnVZV_Q-F4xgOg"
      }).then((res) => {
        console.log(res)
        if (!res.data.is_valid_ip) {
          alert("IP not found in database")
        } else {
          const payload = {
            ip_addr: values.ip_address_s1,
            file_path : values.file_path_s1
          }
          const path = "http://localhost:3000/listFiles"
          axios
            .post(path, payload)
            .then((res) => {
              console.log(res.data.files)
              site1_files.value = res.data.files
            })
            .catch((err) => {
              console.error(err)
            })
        }
      })
    })

    const file_path_s2 = useField('file_path_s2')
    const ip_address_s2 = useField('ip_address_s2')
    const site2_ips = ref([])
    const site2_files = ref([])

    const submit_s2 = handleSubmit(values => {
      console.log("SITE 2")
      console.log(values.file_path_s2)
      console.log(values.ip_address_s2)

      axios.post("http://localhost:3000/site2_ip", {
        site2_IP: values.ip_address_s2,
        site2_access_token: "NB2HI4DTHIXS6Y3JNRXWO33OFZXXEZZPN5QXK5DIGIXTEN3GGEYTOODEMQ2TMMDCG42DQNRRMMZGENRXHFRWKZDGGIYGENJ7OR4XAZJ5MFRWGZLTONKG623FNYTHI4Z5GE3DQMJXHE2DENJXHAZTIJTWMVZHG2LPNY6XMMROGATGY2LGMV2GS3LFHU4TAMBQGAYA",
        site2_id_token_jwt: "eyJ0eXAiOiJKV1QiLCJraWQiOiIyNDRCMjM1RjZCMjhFMzQxMDhEMTAxRUFDNzM2MkM0RSIsImFsZyI6IlJTMjU2In0.eyJlbWFpbCI6ImNtYXJ0aXJlc0BuZXZhZGEudW5yLmVkdSIsImdpdmVuX25hbWUiOiJDb2xpbiIsImZhbWlseV9uYW1lIjoiTWFydGlyZXMiLCJuYW1lIjoiQ29saW4gTWFydGlyZXMiLCJjZXJ0X3N1YmplY3RfZG4iOiIvREM9b3JnL0RDPWNpbG9nb24vQz1VUy9PPUFDQ0VTUy9DTj1Db2xpbiBNYXJ0aXJlcyBFMzc5NzEiLCJpZHAiOiJodHRwczovL2FjY2Vzcy1jaS5vcmcvaWRwIiwiaWRwX25hbWUiOiJBQ0NFU1MiLCJlcHBuIjoiY21hcnRpcmVzQGFjY2Vzcy1jaS5vcmciLCJlcHRpZCI6Imh0dHBzOi8vYWNjZXNzLWNpLm9yZy9pZHAhaHR0cHM6Ly9jaWxvZ29uLm9yZy9zaGliYm9sZXRoITJYZUZpSzNpNGhiNWxMVVM2L3JWZlcxck9jMD0iLCJhY3IiOiJodHRwczovL3JlZmVkcy5vcmcvcHJvZmlsZS9tZmEiLCJpc3MiOiJodHRwczovL2NpbG9nb24ub3JnIiwic3ViIjoiaHR0cDovL2NpbG9nb24ub3JnL3NlcnZlckUvdXNlcnMvMzc5NzEiLCJhdWQiOiJjaWxvZ29uOi9jbGllbnRfaWQvMWEwNTExNDVlY2I0Mzc1MDhlZDhhODg3MWJlZDdiNzciLCJqdGkiOiJodHRwczovL2NpbG9nb24ub3JnL29hdXRoMi9pZFRva2VuLzQ2NTA1YTk4YjZhNTNiN2M3NmVmYTMwZWFjMmRmODA2LzE2ODE3OTQyNTcxOTIiLCJub25jZSI6ImxlS1NVQzN0VW5VTHZoNDEiLCJhdXRoX3RpbWUiOjE2ODE3OTQyNTYsImV4cCI6MTY4MTc5NTE1NywiaWF0IjoxNjgxNzk0MjU3fQ.cC1plED_3D-MNPUPnRVSMipdR6_RUnNOxOKGBPBmP2CKJeiuT4u8zltfcoWuP-qwuRmeHca3NbUro-w5-R8TlKICAuBxe_Fbyuj60NV_sZXgmys3dLjNUI2FugBX45JR-OnBNxmFifeDwjefY9vP10R7XYWA-QvBrAnWHxmNA5LFSHkHlX45HPoXR4xwx4jEcuoZzre_Vsw1f8_QCpSWS4trjE39l2MvJEGHKOW73MWxl39jFl2_XFXH7648mKDeGwIEOWGP04V1Kn1Lci2mCxnrLR5CiTZB_96_Zq9sXxfKk6i1s7lgMXPnniAx1JoOqCZllPATJ7SjO9VZpSvjcQ"
      }).then((res) => {
        console.log(res)
        if (!res.data.is_valid_ip) {
          alert("IP not found in database")
        } else {
          const payload = {
            ip_addr: values.ip_address_s2,
            file_path : values.file_path_s2
          }
          const path = "http://localhost:3000/listFiles"
          axios
            .post(path, payload)
            .then((res) => {
              console.log(res.data.files)
              site2_files.value = res.data.files
            })
            .catch((err) => {
              console.error(err)
            })
        }
      })
    })
    
    return {
      file_path_s1,
      ip_address_s1,
      site1_ips,
      site1_files,
      file_path_s2,
      ip_address_s2,
      site2_ips,
      site2_files,
      submit_s1,
      submit_s2,
      handleReset
    }
  },
  methods: {
    async loginSite1() {
      console.log("logging in to Site1!")
      window.location.href = "http://localhost:3000/loginSite1";
    },
    async loginSite2() {
      console.log("logging in to Site2!")
      window.location.href = "http://localhost:3000/loginSite2";
    },
    async getUser() {
      console.log("Getting User")
      const path = 'http://localhost:3000/get_user';
      const response = await fetch(path, {
        method: 'GET',
        credentials: 'include'
      });
      const jsonData = await response.json();
      console.log(jsonData);
      try {
        this.$store.dispatch('setUser', {
          full_name: jsonData.user_info.full_name,
          email: jsonData.user_info.email,
          idp_name: jsonData.user_info.idp_name,
          access_token: jsonData.user_info.access_token,
          id_token_jwt: jsonData.user_info.id_token_jwt,
          site1_info: jsonData.site1_info,
          site2_info: jsonData.site2_info
        })
        console.log("Set User Info")
      }
      catch (err) {
        console.log(err)
        return;
      }

      // extract site 1 IP addresses
      const site1_ips = this.$store.state.site_1.ips.map(function (ip) {
        return ip.ip;
      });
      this.site1_ips = site1_ips

      // extract site 2 IP addresses
      const site2_ips = this.$store.state.site_2.ips.map(function (ip) {
        return ip.ip;
      });
      this.site2_ips = site2_ips

    },
    async transfer() {
      const payload = {
        file_list: this.selected,
        srcIP: this.ip_address_s1.value.value,
        srcPath: this.file_path_s1.value.value,
        destIP: this.ip_address_s2.value.value,
        destPath: this.file_path_s2.value.value,
      }
      console.log(payload)

      axios.post("http://localhost:3000/transferFiles", {
        srcIP: this.ip_address_s1.value.value,
        destIP: this.ip_address_s2.value.value,
        sender_dir: this.file_path_s1.value.value,
        dest_dir: this.file_path_s2.value.value,
        selected_files: this.selected
      }).then((res) => {
        console.log(res)
      }).catch((err) => {
        console.log(err)
      })

    },
    async exploreS1(new_folder, isBack) {

      let new_path = ""
      if (isBack) {
        const endPathStartIndex = this.file_path_s1.value.value.lastIndexOf("\\")
        new_path = this.file_path_s1.value.value.substring(0, endPathStartIndex)
      } else {
        new_path = this.file_path_s1.value.value.concat("\\", new_folder)
      }

      axios.post("http://localhost:3000/site1_ip", {
        site1_IP: this.ip_address_s1.value.value,
        site1_access_token: "NB2HI4DTHIXS6Y3JNRXWO33OFZXXEZZPN5QXK5DIGIXTOZBTG43DCZTDMFRGENBQGEZGGOJUG5QTGMTFGQZDMMBUGVQTMNR7OR4XAZJ5MFRWGZLTONKG623FNYTHI4Z5GE3DQMJXHE2DEMRTGIYDIJTWMVZHG2LPNY6XMMROGATGY2LGMV2GS3LFHU4TAMBQGAYA",
        site1_id_token_jwt: "eyJ0eXAiOiJKV1QiLCJraWQiOiIyNDRCMjM1RjZCMjhFMzQxMDhEMTAxRUFDNzM2MkM0RSIsImFsZyI6IlJTMjU2In0.eyJlbWFpbCI6ImNtYXJ0aXJlc0BuZXZhZGEudW5yLmVkdSIsImdpdmVuX25hbWUiOiJDb2xpbiIsImZhbWlseV9uYW1lIjoiTWFydGlyZXMiLCJuYW1lIjoiQ29saW4gTCBNYXJ0aXJlcyIsImNlcnRfc3ViamVjdF9kbiI6Ii9EQz1vcmcvREM9Y2lsb2dvbi9DPVVTL089VW5pdmVyc2l0eSBvZiBOZXZhZGEsIFJlbm8vQ049Q29saW4gTWFydGlyZXMgRTE1Mjc2IiwiaWRwIjoiaHR0cHM6Ly9pZHAyLnVuci5lZHUvaWRwL3NoaWJib2xldGgiLCJpZHBfbmFtZSI6IlVuaXZlcnNpdHkgb2YgTmV2YWRhLCBSZW5vIiwiZXBwbiI6ImNtYXJ0aXJlc0B1bnIuZWR1IiwiZXB0aWQiOiJodHRwczovL2lkcDIudW5yLmVkdS9pZHAvc2hpYmJvbGV0aCFodHRwczovL2NpbG9nb24ub3JnL3NoaWJib2xldGghWmZaS1pVWFRhT2w2WmFmT3FXdmM0YWRVWnRnPSIsImFmZmlsaWF0aW9uIjoic3R1ZGVudEB1bnIuZWR1O21lbWJlckB1bnIuZWR1O2ZhY3VsdHlAdW5yLmVkdTtsaWJyYXJ5LXdhbGstaW5AdW5yLmVkdTtzdGFmZkB1bnIuZWR1O2VtcGxveWVlQHVuci5lZHUiLCJhY3IiOiJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YWM6Y2xhc3NlczpQYXNzd29yZFByb3RlY3RlZFRyYW5zcG9ydCIsImlzcyI6Imh0dHBzOi8vY2lsb2dvbi5vcmciLCJzdWIiOiJodHRwOi8vY2lsb2dvbi5vcmcvc2VydmVyRS91c2Vycy8xNTI3NiIsImF1ZCI6ImNpbG9nb246L2NsaWVudF9pZC8xYTA1MTE0NWVjYjQzNzUwOGVkOGE4ODcxYmVkN2I3NyIsImp0aSI6Imh0dHBzOi8vY2lsb2dvbi5vcmcvb2F1dGgyL2lkVG9rZW4vMTFlNDk2MTc0YjY0NWRjYTk1MmEwYzk1NTk2OGI5ZGUvMTY4MTc5NDIyMzA2MSIsIm5vbmNlIjoiTEhGcG9qSW8zV0JkT2hkZSIsImF1dGhfdGltZSI6MTY4MTc5MzY4NSwiZXhwIjoxNjgxNzk1MTIzLCJpYXQiOjE2ODE3OTQyMjN9.cL1EBdX2SmbOmBnD4iFpAg1seafL6gkuCkG21EOnUYp_KF9VCHDpzr-rVdLVPBW_jESL3Grr877jKwkdmXVZsNrLmWP2Y1nbEF587dw5UEwP38pUnfHgU63w7FP7kA1LnnCBtLisvLB-6XG-R8ahYCrDeYWMbOWILPHuZt0_nIW9Dc1BzqfAqN8u6mP-H6JB4g0BNUihcH63DN3qdUN-2J5mSIJQ8vIr4B2WLhTuGjw4mR4vttm-3x8jaW0-mFmcqAtEbSytkZ24d9WuYqMy5-a0YLn3w3r6fJomdKkV8zTYrl6odXbii-C_jq05Dj54nLoxm9x2dnVZV_Q-F4xgOg"
      }).then((res) => {
        console.log(res)
        if (!res.data.is_valid_ip) {
          alert("IP not found in database")
        } else {
          const payload = {
            ip_addr: this.ip_address_s1.value.value,
            file_path : new_path
          }
          const path = "http://localhost:3000/listFiles"
          axios
            .post(path, payload)
            .then((res) => {
              console.log(res.data.files)
              this.site1_files = res.data.files
              this.file_path_s1.value.value = new_path
            })
            .catch((err) => {
              console.error(err)
            })
        }
      })
    },
    async exploreS2(new_folder, isBack) {

      let new_path = ""
      if (isBack) {
        const endPathStartIndex = this.file_path_s2.value.value.lastIndexOf("\\")
        new_path = this.file_path_s2.value.value.substring(0, endPathStartIndex)
      } else {
        new_path = this.file_path_s2.value.value.concat("\\", new_folder)
      }

      axios.post("http://localhost:3000/site2_ip", {
        site2_IP: this.ip_address_s2.value.value,
        site2_access_token: "NB2HI4DTHIXS6Y3JNRXWO33OFZXXEZZPN5QXK5DIGIXTOZBTG43DCZTDMFRGENBQGEZGGOJUG5QTGMTFGQZDMMBUGVQTMNR7OR4XAZJ5MFRWGZLTONKG623FNYTHI4Z5GE3DQMJXHE2DEMRTGIYDIJTWMVZHG2LPNY6XMMROGATGY2LGMV2GS3LFHU4TAMBQGAYA",
        site2_id_token_jwt: "eyJ0eXAiOiJKV1QiLCJraWQiOiIyNDRCMjM1RjZCMjhFMzQxMDhEMTAxRUFDNzM2MkM0RSIsImFsZyI6IlJTMjU2In0.eyJlbWFpbCI6ImNtYXJ0aXJlc0BuZXZhZGEudW5yLmVkdSIsImdpdmVuX25hbWUiOiJDb2xpbiIsImZhbWlseV9uYW1lIjoiTWFydGlyZXMiLCJuYW1lIjoiQ29saW4gTCBNYXJ0aXJlcyIsImNlcnRfc3ViamVjdF9kbiI6Ii9EQz1vcmcvREM9Y2lsb2dvbi9DPVVTL089VW5pdmVyc2l0eSBvZiBOZXZhZGEsIFJlbm8vQ049Q29saW4gTWFydGlyZXMgRTE1Mjc2IiwiaWRwIjoiaHR0cHM6Ly9pZHAyLnVuci5lZHUvaWRwL3NoaWJib2xldGgiLCJpZHBfbmFtZSI6IlVuaXZlcnNpdHkgb2YgTmV2YWRhLCBSZW5vIiwiZXBwbiI6ImNtYXJ0aXJlc0B1bnIuZWR1IiwiZXB0aWQiOiJodHRwczovL2lkcDIudW5yLmVkdS9pZHAvc2hpYmJvbGV0aCFodHRwczovL2NpbG9nb24ub3JnL3NoaWJib2xldGghWmZaS1pVWFRhT2w2WmFmT3FXdmM0YWRVWnRnPSIsImFmZmlsaWF0aW9uIjoic3R1ZGVudEB1bnIuZWR1O21lbWJlckB1bnIuZWR1O2ZhY3VsdHlAdW5yLmVkdTtsaWJyYXJ5LXdhbGstaW5AdW5yLmVkdTtzdGFmZkB1bnIuZWR1O2VtcGxveWVlQHVuci5lZHUiLCJhY3IiOiJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YWM6Y2xhc3NlczpQYXNzd29yZFByb3RlY3RlZFRyYW5zcG9ydCIsImlzcyI6Imh0dHBzOi8vY2lsb2dvbi5vcmciLCJzdWIiOiJodHRwOi8vY2lsb2dvbi5vcmcvc2VydmVyRS91c2Vycy8xNTI3NiIsImF1ZCI6ImNpbG9nb246L2NsaWVudF9pZC8xYTA1MTE0NWVjYjQzNzUwOGVkOGE4ODcxYmVkN2I3NyIsImp0aSI6Imh0dHBzOi8vY2lsb2dvbi5vcmcvb2F1dGgyL2lkVG9rZW4vMTFlNDk2MTc0YjY0NWRjYTk1MmEwYzk1NTk2OGI5ZGUvMTY4MTc5NDIyMzA2MSIsIm5vbmNlIjoiTEhGcG9qSW8zV0JkT2hkZSIsImF1dGhfdGltZSI6MTY4MTc5MzY4NSwiZXhwIjoxNjgxNzk1MTIzLCJpYXQiOjE2ODE3OTQyMjN9.cL1EBdX2SmbOmBnD4iFpAg1seafL6gkuCkG21EOnUYp_KF9VCHDpzr-rVdLVPBW_jESL3Grr877jKwkdmXVZsNrLmWP2Y1nbEF587dw5UEwP38pUnfHgU63w7FP7kA1LnnCBtLisvLB-6XG-R8ahYCrDeYWMbOWILPHuZt0_nIW9Dc1BzqfAqN8u6mP-H6JB4g0BNUihcH63DN3qdUN-2J5mSIJQ8vIr4B2WLhTuGjw4mR4vttm-3x8jaW0-mFmcqAtEbSytkZ24d9WuYqMy5-a0YLn3w3r6fJomdKkV8zTYrl6odXbii-C_jq05Dj54nLoxm9x2dnVZV_Q-F4xgOg"
      }).then((res) => {
        console.log(res)
        if (!res.data.is_valid_ip) {
          alert("IP not found in database")
        } else {
          const payload = {
            ip_addr: this.ip_address_s2.value.value,
            file_path : new_path
          }
          const path = "http://localhost:3000/listFiles"
          axios
            .post(path, payload)
            .then((res) => {
              console.log(res.data.files)
              this.site2_files = res.data.files
              this.file_path_s2.value.value = new_path
            })
            .catch((err) => {
              console.error(err)
            })
        }
      })
    }
  },
  created() {
    this.getUser();
  },
}
</script>

<style>

.v-container {
  padding-left: 7rem;
  padding-right: 7rem;  
}

.v-table {
  border-style: solid;
  border-color: #EEEEEE;
  border-width: thin;
}

td::-webkit-scrollbar{
  display: none;
}

/* .v-container {
  border-style: solid;
  border-color: red;
} */
/* .v-row {
  border-style: solid;
  border-color: blue;
} */
/* .v-col {
  border-style: solid;
  border-color: green;
} */

</style>