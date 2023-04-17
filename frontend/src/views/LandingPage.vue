<template>
  <div>

    <!-- Header -->
    <v-container class="header" fluid style="height: 95vh;">
      <v-row align="center" no-gutters style="height: 80vh;">
        <v-col align-self="center">
          <v-container>
            <div class="text-center text-h2 mb-4">
              FALCON
            </div>
            <div class="text-center text-h4 mb-4">
              ONLINE HIGH-SPEED FILE TRANSFER OPTIMIZATION ALGORITHM
            </div>
            <div class="text-center text-subtitle-1 mb-4">
              Falcon combines a game theory-inspired utility function with state-of-the-art online search algorithms to swiftly discover "just-enough" transfer settings to obtain near-optimal transfer throughput while lowering system overhead and improving fairness.
            </div>
            <div class="text-center">
              <v-btn v-if="this.$store.state.user.email" @click="logout" color="white">Logout</v-btn>
              <v-btn v-else @click="login" color="white">Login</v-btn>
            </div>
          </v-container>
        </v-col>
      </v-row>
    </v-container>

    <!-- Graphics -->
    <v-container fluid>
      <section class="mb-2">
        <v-container>
          <h1 class="text-center text-h3">Speed</h1>
          <div>
              <v-img src="@/assets/discover.png"></v-img>
          </div>
          <div class="text-center mt-2 text-h6 font-weight-light">
              <p>Falcon can discover optimal transfer settings in as little as 20 seconds.</p>
          </div>
        </v-container>
      </section>

      <section class="middle rounded-lg mb-2">
        <v-container>
          <h1 class="text-center text-h3 mb-4">Performance</h1>
          <v-row align="center">
            <v-col>
              <v-img src="@/assets/outperforms.png" alt="outperforms_figure" class="rounded-lg"></v-img>
            </v-col>
            <v-col>
              <div class="text-center text-h6 font-weight-light">
                <p>Falcon outperforms existing transfer applications by up to an order of magnitude.</p>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </section>

      <section class="mb-2">
        <v-container>
          <h1 class="text-center text-h3">Fairness</h1>
            <div>
                <v-img src="@/assets/fairness.png" alt="fairness_figure" class="fig_img"></v-img>
            </div>
            <div class="text-center text-h6 font-weight-light mt-2">
                <p>Falcon ensures fairness among competing Falcon transfers.</p>
            </div>
        </v-container>
      </section>

    </v-container>

    <!-- Footer -->
    <v-footer>
      <div class="d-flex align-center justify-center w-100">
        High Performance Computing and Networking Lab @ University of Nevada, Reno
      </div>
    </v-footer>

  </div>
</template>

<script>
export default {
  name: "LandingPage",
  methods: {
    async login() {
      console.log("logging in!")
      window.location.href = "http://localhost:3000/login";
    },
    async logout() {
      console.log("logging out!")
      const path = 'http://localhost:3000/logout';
      const response = await fetch(path, {
        method: 'GET',
        credentials: 'include'
      });
      const jsonData = await response.json();
      console.log(jsonData);
    }
  }
}
</script>

<style>

.header {
  color: white;
  background-image: linear-gradient(to top, #30cfd0 0%, #330867 100%);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
}

@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

section.middle {
  background-color: #E9F2F9;
}


</style>