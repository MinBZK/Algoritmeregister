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
    path: '/archief',
    name: 'archive.index',
    component: () => import('@/views/Archive.vue'),
  },
  {
    path: '/dashboard',
    name: 'dashboard.index',
    component: () => import('@/views/Dashboard.vue'),
  },
  {
    path: '/beheer',
    component: () => import('@/views/admin-page/AdminPage.vue'),
    redirect: '/beheer/user',
    children: [
      {
        path: 'user',
        name: 'beheer.user',
        component: () => import('@/views/admin-page/UserManagement.vue'),
      },
      {
        path: 'organisation',
        name: 'beheer.organisation',
        component: () => import('@/views/admin-page/org/OrgsOverview.vue'),
      },
      {
        path: 'organisation/:orgCode',
        name: 'orgView',
        component: () => import('@/views/admin-page/org/OrgDetails.vue'),
        props: true,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
