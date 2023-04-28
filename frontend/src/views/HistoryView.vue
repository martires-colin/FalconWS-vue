<template>
  <div>
    <h1>HISTORY PAGE</h1>
  </div>
</template>

<script>
import axios from 'axios'

export default {
	name: "HistoryView",
  methods: {
    async getHistory() {
      console.log("Getting Transfer History")
      axios.post("http://localhost:3000/getHistory", {
        user_email: this.$store.state.user.email
      }).then((res) => {
        console.log(res)
      })
    }
  },
  created() {
    this.getHistory();
  },
}
</script>

<style>

</style>