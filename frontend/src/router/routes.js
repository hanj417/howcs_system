
export default [
  {
    path: '/home',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/Home') }
    ]
  },
  {
    path: '/about',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/about/About') },
      { path: 'goal', component: () => import('pages/about/Goal') },
      { path: 'worth', component: () => import('pages/about/Worth') }
    ]
  },
  {
    path: '/entrance',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/entrance/Entrance') }
    ]
  },
  {
    path: '/agit',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/agit/Agit') },
      { path: 'agit1', component: () => import('pages/agit/Agit1') }
    ]
  },
  {
    path: '/community',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/community/Community') }
    ]
  },
  {
    path: '/edu',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/edu/Edu') },
      { path: 'edu1', component: () => import('pages/edu/Edu1') },
      { path: 'edu2', component: () => import('pages/edu/Edu2') },
      { path: 'edu3', component: () => import('pages/edu/Edu3') },
      { path: 'edu4', component: () => import('pages/edu/Edu4') },
      { path: 'edu5', component: () => import('pages/edu/Edu5') },
      { path: 'edu6', component: () => import('pages/edu/Edu6') },
    ]
  },
  {
    path: '/story',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: 'story', component: () => import('pages/story/Story') },
      { path: 'notice', component: () => import('pages/story/Notice') },
      { path: 'photo', component: () => import('pages/story/Photo') },
    ]
  },
  {
    path: '/login',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/Login') }
    ]
  },
  {
    path: '/logout',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/Logout') }
    ]
  },
  {
    path: '/register',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/Register') }
    ]
  },
  {
    path: '/profile',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: false},
    children: [
      { path: '', component: () => import('pages/UserForm') }
    ]
  },
  {
    path: '/hana',
    component: () => import('layouts/default'),
    props: {leftDrawerOpen: true},
    children: [
      { path: '', component: () => import('pages/404'), props: true },
      { path: 'class', component: () => import('pages/Class'), props: true },
      { path: 'class/:major_category', component: () => import('pages/Class'), props: true },
      { path: 'class/:major_category/:id', component: () => import('pages/Class'), props: true },
      { path: 'user_form/:action', component: () => import('pages/UserForm'), props: true },
      { path: 'user_form/:action/:id', component: () => import('pages/UserForm'), props: true },
    ]
  },
  {
    path: '/',
    component: () => import('layouts/default'),
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
