<template>
  <div class="">
		dashboard
	</div>
</template>

<script>
// import axios from 'axios';

export default {
	name: "DashboardView",
  methods: {
    async getUser() {
      console.log("Getting User")
      const path = 'http://localhost:3000/get_user';
      const response = await fetch(path, {
        method: 'GET',
        credentials: 'include'
      });
      const jsonData = await response.json();
      console.log(jsonData);
    },
  },
  created() {
    this.getUser();
  },
}
</script>

<style>

</style>