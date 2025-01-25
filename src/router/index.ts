import { createRouter, createWebHistory } from 'vue-router'
import RentDaysOnMarket from '../pages/RentDaysonMarket.vue'
import Home from '../pages/HomePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Home,
    }, 
    {
      path: '/rent-days-on-market',
      component: RentDaysOnMarket,
    }, 
    {
      path: '/geo-rent',
      component: RentDaysOnMarket,
    }, 
  ],
})

export default router
