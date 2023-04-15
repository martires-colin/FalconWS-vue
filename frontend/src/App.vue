<template>
  <v-app>

    <!-- Navigation Bar -->
    <v-app-bar :elevation="1" class="px-2">
      <v-avatar :tile="true">
        <img :src="require('@/assets/falcon-icon.png')" alt="logo">
      </v-avatar>

      <v-app-bar-title>Falcon</v-app-bar-title>

      <template v-slot:append>
        <v-btn @click="login" variant="outlined">Login</v-btn>
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
    //
  }),
  methods: {
    async login() {
      console.log("logging in!")
      window.location.href = "http://localhost:3000/login";
    }
  }
}
</script>
