<template>
  <HelloWorld />
</template>

<script>
import { defineComponent } from 'vue';

// Components
import HelloWorld from '../components/HelloWorld.vue';

export default defineComponent({
  name: 'HomeView',

  components: {
    HelloWorld,
  },
  // methods: {
  //   getUser() {
  //     const path = 'http://localhost:3000/get_user';
  //     axios.get(path)
  //       .then((res) => {
  //         // this.books = res.data.books;
  //         console.log(res)
  //       })
  //       .catch((error) => {
  //         console.error(error);
  //       });
  //   },
  // },
  // created() {
  //   this.getBooks();
  // },
});
</script>
