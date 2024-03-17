import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const routes = [
  { path: '/', component: HomeView },
  // { path: '/mybooks', component: MyBooksView },
  // { path: '/mystats', component: MyStatsView },
  // { path: '/myprofile', component: MyProfileView },
  // { path: '/issues', component: IssuesView },
  // { path: '/analytics', component: AnalyticsView },
  // { path: '/login', component: LoginView },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
