<template>
  <div>
    <v-container >
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
        <div class="text-h4 text-center w-100" >File Transfer Portal</div>
      </v-row>

      <!-- File Browser Section -->
      <v-row>

        <!-- Site 1 -->
        <v-col>
          <v-row>

            <!-- If user not logged into site, display button, else display form -->
            <div v-if="this.$store.state.site_1" class="text-center w-100">
              <div class="text-h5">{{ this.$store.state.site_1.idp_name }}</div>
              
              <form @submit.prevent="submit">

                <v-select
                  v-model="ip_address_s1.value.value"
                  :items="this.$store.state.site_1.ips"
                  item-text="ip"
                  item-value="ip"
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

        </v-col>

        <!-- Site 2 -->
        <v-col>
          <v-row>
            <div class="text-h5 text-center w-100" >Site 2</div>
          </v-row>
          <v-row>
            <!-- If user not logged into site, display button, else display form -->
            <div class="text-center w-100">
              <v-btn @click="loginSite2" color="blue-lighten-1">Site 2 Login</v-btn>
 
            </div>
          </v-row>
        </v-col>
      </v-row>

    </v-container>
	</div>
</template>

<script>
import { ref } from 'vue'
import { useField, useForm } from 'vee-validate'

export default {
	name: "DashboardView",
  data() {
    return {
      
    }
  },
  setup () {
    const { handleSubmit, handleReset } = useForm({
      validationSchema: {
        file_path_s1 (value) {
          if (value) return true

          return 'Must be a valid file path.'
        },
        ip_address_s1 (value) {
          if (value) return true

          return 'Select an IP address.'
        }
      },
    })

    const file_path_s1 = useField('file_path_s1')
    const ip_address_s1 = useField('ip_address_s1')

    const items = ref([
      'Item 1',
      'Item 2',
      'Item 3',
      'Item 4',
    ])

    const submit = handleSubmit(values => {
      alert(JSON.stringify(values, null, 2))
    })

    return { file_path_s1, ip_address_s1, items, submit, handleReset }
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
    },
  },
  created() {
    this.getUser();
  },
}
</script>

<style>

.v-container {
  border-style: solid;
  border-color: red;
}
.v-row {
  border-style: solid;
  border-color: blue;
}
.v-col {
  border-style: solid;
  border-color: green;
}

</style>