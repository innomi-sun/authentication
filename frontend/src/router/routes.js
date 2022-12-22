
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'singup/loto', alias: ['/singup/loto', '/singup/racing'], component: () => import('pages/SignupPage.vue') },
      { path: 'login/loto', alias: ['/login/loto', '/login/racing'], component: () => import('pages/LoginPage.vue') }
    ]
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
