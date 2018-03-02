import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/', name: 'main', component: 'Main' },
  { path: '/user', name: 'user', component: 'User' },
  { path: '/class', name: 'class', component: 'Class' },
  { path: '/enrollments/classes/:id', name: 'enrollment_class', component: 'EnrollmentClass' },
  { path: '/student', name: 'student', component: 'Student' },
  { path: '/post', name: 'post', component: 'Post' },
  { path: '/login', name: 'login', component: 'Login' },
  { path: '/register', name: 'register', component: 'Register' },
  { path: '/register_student', name: 'register_student', component: 'RegisterStudent' },
  { path: '/profile/:action/:id', name: 'profile', component: 'Profile' },
  { path: '/user_form/:action', name: 'user_form', component: 'UserForm' },
  { path: '/user_form/:action/:id', name: 'user_form', component: 'UserForm' },
  { path: '/class_form/:action', name: 'class_form', component: 'ClassForm' },
  { path: '/class_form/:action/:id', name: 'class_form', component: 'ClassForm' },
  { path: '/post_form/:action', name: 'post_form', component: 'PostForm' },
  { path: '/post_form/:action/:id', name: 'post_form', component: 'PostForm' },
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/pages/${route.component}.vue`)
  }
})

Vue.use(Router)
export default new Router({
  routes,
  mode: 'history'
})
/*
import Vue from 'vue'
import Router from 'vue-router'

function route (path, file, name, children) {
  return {
    exact: true,
    path,
    name,
    children,
    component: require(`./pages/${file}.vue`)
  }
}

Vue.use(Router)

const router = new Router({
  base: __dirname,
  mode: 'hash',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    //route('/login', 'Login', 'login'),
    //route('/register', 'Register', 'register'),
    //route('/error', 'Error', 'error'),
    route('/', 'Main', 'Main', null)
  ]
})

export default router
*/
