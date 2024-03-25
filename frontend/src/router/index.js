import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue';
import SearchPage from '@/components/SearchPage.vue';
import BookDetailsView from '@/views/BookDetailsView.vue';
import BookList from '@/views/BookList.vue';

const routes = [
  { path: '/', name: 'HomeView' ,component: HomeView },
  { path: '/search', name: 'SearchPage', component: SearchPage },
  { path: '/book/:book_id', name: 'BookDetailsView', component: BookDetailsView },
  { path: '/section/:section_id/books', name: 'BookList', component: BookList },
  // { path: '/mybooks', component: MyBooksView },
  // { path: '/mystats', component: MyStatsView },
  // { path: '/myprofile', component: MyProfileView },
  // { path: '/issues', component: IssuesView },
  // { path: '/analytics', component: AnalyticsView },
  { path: '/login', name: 'LoginView' ,component: LoginView },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
