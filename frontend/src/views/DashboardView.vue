<template>
  <div class="">
		balls
	</div>
</template>

<script>
import axios from 'axios';

export default {
	name: "DashboardView",
  methods: {
    getUser() {
      const path = 'http://localhost:3000/get_user';
      axios.get(path)
        .then((res) => {
          // this.books = res.data.books;
          console.log(res)
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getUser();
  },
}
</script>

<style>

</style>