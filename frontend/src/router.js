import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/', name: 'main', component: 'Main' },
  { path: '/login', name: 'login', component: 'Login' },
  { path: '/register', name: 'register', component: 'Register' },
  { path: '/user', name: 'user', component: 'User' },
  { path: '/user_form/:action', name: 'user_form', component: 'UserForm' },
  { path: '/user_form/:action/:id', name: 'user_form_admin', component: 'UserForm' },
  { path: '/student', name: 'student', component: 'Student' },
  { path: '/student_record/:action/:id', name: 'student_record', component: 'StudentRecord' },
  { path: '/class/:major_category/:id', name: 'teaching_classes', component: 'Class' },
  { path: '/class/:major_category', name: 'class', component: 'Class' },
  { path: '/class', name: 'class_admin', component: 'Class' },
  { path: '/class_form/:major_category/:action', name: 'class_form_new', component: 'ClassForm' },
  { path: '/class_form/:major_category/:action/:id', name: 'class_form_edit', component: 'ClassForm' },
  { path: '/post', name: 'post_admin', component: 'Post' },
  { path: '/post/:major_category/:minor_category', name: 'post_category', component: 'Post' },
  { path: '/post/:class_id', name: 'post_class', component: 'Post' },
  { path: '/post_view/:id', name: 'post_view', component: 'PostView' },
  { path: '/post_form/:action/:id', name: 'post_form', component: 'PostForm' },
  { path: '/agit_teacher_application_form', name: 'agit_teacher_application_form', component: 'AgitTeacherApplicationForm' },
  { path: '/agit_teacher', name: 'agit_teacher', component: 'AgitTeacher' },
  { path: '/howcs_teacher', name: 'howcs_teacher', component: 'HowcsTeacher' },
  { path: '/enrollments/classes/:id', name: 'enrollment_class', component: 'EnrollmentClass' },
  { path: '/enrollments/students/:id/:major_category', name: 'enrollment_student', component: 'EnrollmentStudent' },
  { path: '/attendances/classes/:id', name: 'attendance_class', component: 'AttendanceClass' },
  { path: '/payments', name: 'payment', component: 'Payment' },
  { path: '/payments/:action/:id', name: 'payment_form', component: 'PaymentForm' },
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
