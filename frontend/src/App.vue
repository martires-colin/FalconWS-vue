<template>
  <v-app>

    <!-- Navigation Bar -->
    <v-app-bar :elevation="1" class="px-6">
      <v-avatar :tile="true">
        <img :src="require('@/assets/falcon-icon.png')" alt="logo">
      </v-avatar>

      <v-app-bar-title @click="$router.push('/')">Falcon</v-app-bar-title>

      <template v-slot:append>
        <v-btn v-if="this.$store.state.user.email" @click="$router.push('/dashboard')">Dashboard</v-btn>
        <v-btn v-if="this.$store.state.user.email" @click="$router.push('/history')">History</v-btn>
        <v-btn v-if="this.$store.state.user.email" @click="logout" variant="outlined">Logout</v-btn>
        <v-btn v-else @click="login" variant="outlined">Login</v-btn>
      </template>
    </v-app-bar>


    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data: () => ({
    
  }),
  methods: {
    async login() {
      console.log("logging in!")
      window.location.href = "http://localhost:3000/login";
    },
    async logout() {
      console.log("logging out!")
      window.location.href = "http://localhost:3000/logout";
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
    }
  },
  created() {
    this.getUser();
  },
}
</script>

<style>

.v-app-bar-title {
  cursor: pointer;
}

</style>