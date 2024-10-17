// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'algorithm.index',
    component: () => import('@/views/Overview.vue'),
  },
  {
    path: '/algoritme/aanmaken',
    name: 'algorithm.create',
    component: () => import('@/views/FormGenerator.vue'),
  },
  {
    path: '/algoritme/:lars/bewerken',
    name: 'algorithm.edit',
    component: () => import('@/views/FormGenerator.vue'),
    props: true,
  },
  {
    path: '/organisatie',
    name: 'organisation.index',
    component: () => import('@/views/Organisation.vue'),
  },
  {
    path: '/dashboard',
    name: 'dashboard.index',
    component: () => import('@/views/Dashboard.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
