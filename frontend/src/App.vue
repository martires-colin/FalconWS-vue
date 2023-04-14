<template>
  <v-app>

    <!-- Navigation Bar -->
    <v-app-bar :elevation="1" class="px-2">
      <v-avatar :tile="true">
        <img :src="require('@/assets/falcon-icon.png')" alt="logo">
      </v-avatar>

      <v-app-bar-title>Falcon</v-app-bar-title>

      <template v-slot:append>
        <v-btn variant="outlined" class="">Login</v-btn>
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
}
</script>
