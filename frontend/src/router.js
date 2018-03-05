import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/', name: 'main', component: 'Main' },
  { path: '/login', name: 'login', component: 'Login' },
  { path: '/register', name: 'register', component: 'Register' },
  { path: '/user', name: 'user', component: 'User' },
  { path: '/user_form/:action', name: 'user_form', component: 'UserForm' },
  { path: '/user_form/:action/:id', name: 'user_form', component: 'UserForm' },
  { path: '/class', name: 'class', component: 'Class' },
  { path: '/class/:major_category/:id', name: 'class', component: 'Class' },
  { path: '/class_form/:action', name: 'class_form', component: 'ClassForm' },
  { path: '/class_form/:action/:id', name: 'class_form', component: 'ClassForm' },
  { path: '/post', name: 'post', component: 'Post' },
  { path: '/post/:major_category/:minor_category', name: 'post', component: 'Post' },
  { path: '/post/:id', name: 'post', component: 'Post' },
  { path: '/post_form/:action', name: 'post_form', component: 'PostForm' },
  { path: '/post_form/:action/:id', name: 'post_form', component: 'PostForm' },
  { path: '/agit_teacher_application_form', name: 'agit_teacher_application_form', component: 'AgitTeacherApplicationForm' },
  { path: '/agit_teacher', name: 'agit_teacher', component: 'AgitTeacher' },
  { path: '/enrollments/classes/:id', name: 'enrollment_class', component: 'EnrollmentClass' },
  { path: '/enrollments/students/:id/:major_category', name: 'enrollment_student', component: 'EnrollmentStudent' },
  { path: '/attendances/classes/:id', name: 'attendance_class', component: 'AttendanceClass' },
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
