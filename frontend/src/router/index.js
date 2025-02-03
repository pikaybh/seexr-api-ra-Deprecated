import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/ra',
      name: '위험성평가',
      component: () => import('../views/RAView.vue')
    },
    {
      path: '/ra/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/ra/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/test',
      name: 'test',
      component: () => import('../views/TestView.vue')
    }
  ],
})

export default router
