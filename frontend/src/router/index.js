import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import SearchPage from '@/components/SearchPage.vue';
import BookDetailsView from '@/views/BookDetailsView.vue';
import BookList from '@/views/BookList.vue';
import IssuesView from '@/views/IssuesView.vue';
import SectionForm from '@/components/SectionForm.vue';
import BookForm from '@/components/BookForm.vue';
import AuthorsPage from '@/views/AuthorsPage.vue';

const routes = [
  { path: '/', name: 'HomeView' ,component: HomeView },
  { path: '/search', name: 'SearchPage', component: SearchPage },
  { path: '/book/:book_id', name: 'BookDetailsView', component: BookDetailsView },
  { path: '/section/:section_id/books', name: 'BookList', component: BookList },
  { path: '/mybooks', component: IssuesView },
  { path: '/issues', component:IssuesView },
  { path: '/section/:section_id/update', component: SectionForm},
  { path: '/section/create', component: SectionForm},
  { path: '/book/:book_id/update', component: BookForm},
  { path: '/book/create', component: BookForm},
  { path: '/authors', component: AuthorsPage},
  // { path: '/mystats', component: MyStatsView },
  // { path: '/myprofile', component: MyProfileView },
  // { path: '/analytics', component: AnalyticsView },
  { path: '/login', name: 'LoginView' ,component: LoginView },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
