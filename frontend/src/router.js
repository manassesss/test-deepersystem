import { createRouter, createWebHistory } from 'vue-router'
import UserTable from './components/UsersTable.vue'
import UserDetail from './components/UsersDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: UserTable
  },
  {
    path: '/user/:username',
    name: 'UserDetail',
    component: UserDetail,
    props: true
  }
]

export default createRouter({
  history: createWebHistory(),
  routes,
})