import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import InquiryList from '../views/InquiryList.vue'
import InquiryDetail from '../views/InquiryDetail.vue'
import CustomerList from '../views/CustomerList.vue'

const router = createRouter({
  history: createWebHistory('/sales-system/'),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', component: Dashboard },
    { path: '/inquiries', component: InquiryList },
    { path: '/inquiry/:id', component: InquiryDetail },
    { path: '/customers', component: CustomerList },
  ]
})

export default router
