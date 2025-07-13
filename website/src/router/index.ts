import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/HomePage.vue'
import RentDaysOnMarket from '../pages/RentDaysonMarket.vue'
import GeoRent from '../pages/GeoRent.vue'

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
      component: GeoRent,
    }, 
  ],
})

export default router
