import Main from '@/views/Main'
// 非侧边栏路由一般都放在这里
export default [
  {
    path: '/order',
    component: Main,
    icon: 'dashboard',
    children: [
      {
        path: 'order/:id',
        name: 'order_index',
        meta: {
          title: 'orderDetail'
        },
        component: () => import('@/views/RouterPage/order.vue')
      }
    ]
  }
]
