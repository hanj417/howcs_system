
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
      { path: 'agit1', name: 'agit1', component: () => import('pages/agit/Agit1') },
      { path: 'class1/:id', name: 'class1', component: () => import('pages/agit/Class'), props: true }
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
      { path: 'photo_view/:id', name: 'photo_view', component: () => import('pages/story/PhotoView'), props: true }
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
      { path: 'student/:action', name: 'student', component: () => import('pages/Student'), props: true },
      { path: 'student_record/:action/:id', name: 'student_record', component: () => import('pages/StudentRecord'), props: true },
      { path: 'student_health_record/:action/:id', name: 'student_health_record', component: () => import('pages/StudentHealthRecord'), props: true },
      { path: 'student_health_record_new/:id', name: 'student_health_record_new', component: () => import('pages/StudentHealthRecordForm'), props: true },
      { path: 'student_health_record_edit/:id', name: 'student_health_record_edit', component: () => import('pages/StudentHealthRecordForm'), props: true },
      { path: 'student_fruit_record/:action/:id', name: 'student_fruit_record', component: () => import('pages/StudentFruitRecord'), props: true },
      { path: 'student_fruit_record_new/:id', name: 'student_fruit_record_new', component: () => import('pages/StudentFruitRecordForm'), props: true },
      { path: 'student_fruit_record_edit/:id', name: 'student_fruit_record_edit', component: () => import('pages/StudentFruitRecordForm'), props: true },
      { path: 'agit_class_teacher/:teacher_id/:major_category/:action', name: 'agit_class_teacher', component: () => import('pages/AgitClass'), props: true },
      { path: 'agit_class_admin/:major_category/:action', name: 'agit_class_admin', component: () => import('pages/AgitClass'), props: true },
      { path: 'class/:major_category/:action', name: 'class_all', component: () => import('pages/Class'), props: true },
      { path: 'class_teacher/:teacher_id/:major_category/:action', name: 'class_teacher', component: () => import('pages/Class'), props: true },
      { path: 'class_teacher/:teacher_id/:major_category/:minor_category/:action', name: 'howcs_class_teacher', component: () => import('pages/Class'), props: true },
      { path: 'agit_class_teacher/:teacher_id/:major_category/:action', name: 'agit_class_teacher', component: () => import('pages/AgitClass'), props: true },
      { path: 'agit_class_admin/:major_category/:action', name: 'agit_class_admin', component: () => import('pages/AgitClass'), props: true },
      { path: 'class_form/:role/:major_category', name: 'class_form_new', component: () => import('pages/ClassForm'), props: true },
      { path: 'class_form/:role/:major_category/:class_id', name: 'class_form_edit', component: () => import('pages/ClassForm'), props: true },
      { path: 'post', name: 'post_admin', component: () => import('pages/Post'), props: true },
      { path: 'post_card/:minor_category', name: 'post_card', component: () => import('pages/PostCard'), props: true },
      { path: 'post/:major_category/:minor_category', name: 'post_category', component: () => import('pages/Post'), props: true },
      { path: 'post/:class_id', name: 'post_class', component: () => import('pages/Post'), props: true },
      { path: 'post_view/:id', name: 'post_view', component: () => import('pages/PostView'), props: true },
      { path: 'post_form/:action/:id', name: 'post_form', component: () => import('pages/PostForm'), props: true },
      { path: 'post_form/:action', name: 'post_form_admin', component: () => import('pages/PostForm'), props: true },
      { path: 'agit_teacher_application', name: 'agit_teacher_application', component: () => import('pages/AgitTeacherApplication'), props: true },
      { path: 'agit_teacher', name: 'agit_teacher', component: () => import('pages/AgitTeacher'), props: true },
      { path: 'howcs_teacher', name: 'howcs_teacher', component: () => import('pages/HowcsTeacher'), props: true },
      { path: 'enrollments/classes/:class_id', name: 'enrollment_class', component: () => import('pages/EnrollmentClass'), props: true },
      { path: 'enrollments/classes/:class_id/:action', name: 'enrollment_class_action', component: () => import('pages/EnrollmentClass'), props: true },
      { path: 'agit_enrollments/classes/:class_id', name: 'agit_enrollment_class', component: () => import('pages/AgitEnrollmentClass'), props: true },
      { path: 'enrollments/students/:id/:major_category/:action', name: 'enrollment_student_all', component: () => import('pages/EnrollmentStudent'), props: true },
      { path: 'enrollments/students/:id/:major_category/:minor_category/:action', name: 'enrollment_student', component: () => import('pages/EnrollmentStudent'), props: true },
      { path: 'attendances/classes/:class_id', name: 'attendance_class', component: () => import('pages/AttendanceClass'), props: true },
      { path: 'attendances/students/:student_id/:class_id', name: 'attendance_student', component: () => import('pages/AttendanceStudent'), props: true },
      // { path: 'payments', component: () => import('pages/Payment'), props: true },
      // { path: 'payments/:action/:id', component: () => import('pages/PaymentForm'), props: true },
      { path: 'role', name: 'role', component: () => import('pages/Role'), props: true },
      { path: 'role_form/:id', name: 'role_form', component: () => import('pages/RoleForm'), props: true },
      { path: 'resource/:major_category/:minor_category', name: 'resource', component: () => import('pages/Resource'), props: true }
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
