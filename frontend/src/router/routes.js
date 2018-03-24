
export default [
  {
    path: '/home',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', name: 'home', component: () => import('pages/Home') }
    ]
  },
  {
    path: '/about',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', name: 'about', component: () => import('pages/about/About') },
      { path: 'goal', name: 'about_goal', component: () => import('pages/about/Goal') },
      { path: 'worth', name: 'about_worth', component: () => import('pages/about/Worth') }
    ]
  },
  {
    path: '/entrance',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', name: 'entrance', component: () => import('pages/entrance/Entrance') }
    ]
  },
  {
    path: '/agit',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', name: 'agit', component: () => import('pages/agit/Agit') },
      { path: 'agit1', name: 'agit1', component: () => import('pages/agit/Agit1') }
    ]
  },
  {
    path: '/community',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', name: 'community', component: () => import('pages/community/Community') }
    ]
  },
  {
    path: '/edu',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', name: 'edu', component: () => import('pages/edu/Edu') },
      { path: 'edu1', name: 'edu1', component: () => import('pages/edu/Edu1') },
      { path: 'edu2', name: 'edu2', component: () => import('pages/edu/Edu2') },
      { path: 'edu3', name: 'edu3', component: () => import('pages/edu/Edu3') },
      { path: 'edu4', name: 'edu4', component: () => import('pages/edu/Edu4') },
      { path: 'edu5', name: 'edu5', component: () => import('pages/edu/Edu5') },
      { path: 'edu6', name: 'edu6', component: () => import('pages/edu/Edu6') }
    ]
  },
  {
    path: '/story',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: 'story', name: 'story', component: () => import('pages/story/Story') },
      { path: 'notice', name: 'notice', component: () => import('pages/story/Notice') },
      { path: 'photo', name: 'photo', component: () => import('pages/story/Photo') },
      { path: 'story_view/:id', name: 'story_view', component: () => import('pages/story/StoryView'), props: true },
      { path: 'photo_view/:id', name: 'photo_view', component: () => import('pages/story/PhotoView'), props: true },
    ]
  },
  {
    path: '/login',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', name: 'login', component: () => import('pages/Login') }
    ]
  },
  {
    path: '/logout',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', name: 'logout', component: () => import('pages/Logout') }
    ]
  },
  {
    path: '/register',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', name: 'register', component: () => import('pages/Register') }
    ]
  },
  {
    path: '/hana',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: true},
    children: [
      { path: '', name: 'hana', component: () => import('pages/Hana'), props: true },
      { path: 'user', name: 'user', component: () => import('pages/User'), props: true },
      { path: 'user_form/:action', name: 'user_form', component: () => import('pages/UserForm'), props: true },
      { path: 'user_form/:action/:id', name: 'user_form_admin', component: () => import('pages/UserForm'), props: true },
      { path: 'student', name: 'student', component: () => import('pages/Student'), props: true },
      { path: 'student_record', name: 'student_record', component: () => import('pages/StudentRecord'), props: true },
      { path: 'class', name: 'class_admin', component: () => import('pages/Class'), props: true },
      { path: 'class/:major_category', name: 'class', component: () => import('pages/Class'), props: true },
      { path: 'class/:major_category/:id', name: 'teaching_classes', component: () => import('pages/Class'), props: true },
      { path: 'class_form/:major_category/:action', name: 'class_form_admin', component: () => import('pages/ClassForm'), props: true },
      { path: 'class_form/:major_category/:action/:id', name: 'class_form_teacher', component: () => import('pages/ClassForm'), props: true },
      { path: 'post', name: 'post_admin', component: () => import('pages/Post'), props: true },
      { path: 'post_card/:minor_category', name: 'post_card', component: () => import('pages/PostCard'), props: true },
      { path: 'post/:major_category/:minor_category', name: 'post_category', component: () => import('pages/Post'), props: true },
      { path: 'post/:class_id', name: 'post_class', component: () => import('pages/Post'), props: true },
      { path: 'post_view/:id', name: 'post_view', component: () => import('pages/PostView'), props: true },
      { path: 'post_form/:action/:id', name: 'post_form', component: () => import('pages/PostForm'), props: true },
      { path: 'post_form/:action', name: 'post_form_admin', component: () => import('pages/PostForm'), props: true },
      { path: 'agit_teacher_application_form', name: 'agit_teacher_application_form', component: () => import('pages/AgitTeacherApplicationForm'), props: true },
      { path: 'agit_teacher', name: 'agit_teacher', component: () => import('pages/AgitTeacher'), props: true },
      { path: 'howcs_teacher', name: 'howcs_teacher', component: () => import('pages/HowcsTeacher'), props: true },
      { path: 'enrollments/classes/:id', name: 'enrollment_class', component: () => import('pages/EnrollmentClass'), props: true },
      { path: 'enrollments/students/:id/:major_category', name: 'enrollment_student', component: () => import('pages/EnrollmentStudent'), props: true },
      { path: 'attendances/classes/:id', name: 'attendance_class', component: () => import('pages/AttendanceClass'), props: true }
      // { path: 'payments', component: () => import('pages/Payment'), props: true },
      // { path: 'payments/:action/:id', component: () => import('pages/PaymentForm'), props: true },
    ]
  },
  {
    path: '/',
    component: () => import('layouts/hana'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/Home') }
    ]
  },

  { // Always leave this as last one
    path: '*',
    component: () => import('pages/404')
  }
]
