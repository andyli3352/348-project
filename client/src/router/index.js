import Vue from 'vue';
import VueRouter from 'vue-router';
// import Home from '../views/Home.vue';
import Ping from '../components/Ping.vue';
import Books from '../components/Books.vue';
import Users from '../components/Users.vue';
import Songs from '../components/Songs.vue';
import Quotes from '../components/Quotes.vue';

Vue.use(VueRouter);

const routes = [
  // {
  //   path: '/',
  //   name: 'Home',
  //   component: Home,
  // },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  // },
  {
    path: '/',
    name: 'Books',
    component: Books,
  },
  {
    path: '/ping',
    name: 'Ping',
    component: Ping,
  },
  {
    path: '/users',
    name: 'Users',
    component: Users,
  },
  {
    path: '/songs',
    name: 'Songs',
    component: Songs,
  },
  {
    path: '/quotes',
    name: 'Quotes',
    component: Quotes,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
