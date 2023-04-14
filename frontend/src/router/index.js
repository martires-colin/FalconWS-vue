import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LandingPage from '../views/LandingPage.vue'

const routes = [
  {
    path: '/home-test',
    name: 'home',
    component: HomeView
  },
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
