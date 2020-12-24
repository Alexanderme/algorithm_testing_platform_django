import Main from '@/views/Main'
const Dashboard = () => import('@/views/Dashboard')
// 侧边栏路由一般都放在这里 需要权限校验
export const baseRoute = [
  {
    path: '',
    component: Main,
    title: 'dashboard',
    icon: 'dashboard',
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'dashboard_index',
        meta: {
          title: 'dashboard'
        },
        component: Dashboard
      }
    ]
  },
  {
    path: 'sdk', // 组件库
    name: 'sdk',
    component: Main,
    title: 'sdk',
    icon: 'component',
    children: [
      {
        path: 'DataSetVerification',
        name: 'DataSetVerification',
        meta: {
          title: 'DataSetVerification',
          access: ['admin']
        },
        component: () => import('@/views/ComponentsDemo/DataSetVerification.vue')
      },
      {
        path: 'AlgoPerformance',
        name: 'AlgoPerformance',
        meta: {
          title: 'AlgoPerformance'
        },
        component: () => import('@/views/ComponentsDemo/AlgoPerformance.vue')
      },
      {
        path: 'AlgoFilesResult',
        name: 'AlgoFilesResult',
        meta: {
          title: 'AlgoFilesResult'
        },
        component: () => import('@/views/ComponentsDemo/AlgoFilesResult.vue')
      },
      {
        path: 'AlgoPrecision',
        name: 'AlgoPrecision',
        meta: {
          title: 'AlgoPrecision'
        },
        component: () => import('@/views/ComponentsDemo/AlgoPrecision.vue')
      },
      {
        path: 'algoMessage',
        name: 'algoMessage',
        meta: {
          title: 'algoMessage'
        },
        component: () => import('@/views/ComponentsDemo/AlgoMessage.vue')
      },
      {
        path: 'AlgoPackaging',
        name: 'AlgoPackaging',
        meta: {
          title: 'AlgoPackaging'
        },
        component: () => import('@/views/ComponentsDemo/AlgoPackaging.vue')
      },
      {
        path: 'AlgoStandardTest',
        name: 'AlgoStandardTest',
        meta: {
          title: 'AlgoStandardTest'
        },
        component: () => import('@/views/ComponentsDemo/AlgoStandardTest.vue')
      }
    ]
  },
  {
    path: '/form', // 表单
    title: 'form',
    name: 'form',
    icon: 'form',
    component: Main,
    children: [
      {
        path: 'form-creat',
        name: 'form_creat',
        meta: {
          title: 'createForm'
        },
        component: () => import('@/views/FormPage/createForm.vue')
      },
      {
        path: 'form-editor',
        name: 'form_editor',
        meta: {
          title: 'editForm'
        },
        component: () => import('@/views/FormPage/editForm.vue')
      },
      {
        path: 'form-update',
        name: 'form_update',
        meta: {
          title: 'listenForm'
        },
        component: () => import('@/views/FormPage/formUpdate.vue')
      }
    ]
  },
  {
    path: '/advanced', // 高级路由
    name: 'advanced',
    icon: 'example',
    title: 'highRoute',
    component: Main,
    children: [
      {
        path: 'active',
        name: 'active_index',
        meta: {
          title: 'dynamicRoute'
        },
        component: () => import('@/views/RouterPage/index-one.vue')
      },
      {
        path: 'send',
        name: 'send_index',
        meta: {
          title: 'paramRoute'
        },
        component: () => import('@/views/RouterPage/index-two.vue')
      }
    ]
  },
  {
    path: '/composite', // 综合实例
    name: 'composite',
    icon: 'complex',
    title: 'composite',
    component: Main,
    children: [
      {
        path: 'article-list',
        name: 'article_index',
        meta: {
          title: 'articleList'
        },
        component: () => import('@/views/ArticleManage/ArticleList/index.vue')
      },
      {
        path: 'public-article',
        name: 'public_index',
        meta: {
          title: 'publicArticle'
        },
        component: () => import('@/views/ArticleManage/PublicArticle/index.vue')
      }
    ]
  },
  {
    path: '/userinfo',
    name: 'user',
    icon: 'user',
    component: Main,
    title: 'manageInfo',
    children: [
      {
        path: 'userinfo',
        name: 'user_info',
        meta: {
          title: 'userInfo',
          access: ['admin']
        },
        component: () => import('@/views/userInfo/setInfo.vue')
      },
      {
        path: 'editinfo',
        name: 'edit_info',
        meta: {
          title: 'editInfo',
          access: ['admin']
        },
        component: () => import('@/views/userInfo/editInfo.vue')
      }
    ]
  },
  {
    path: '/setting',
    name: 'set',
    icon: 'setting',
    component: Main,
    title: 'setting',
    children: [
      {
        path: 'setting',
        name: 'setting_index',
        meta: {
          title: 'setting',
          access: ['admin']
        },
        component: () => import('@/views/SettingPage/setting.vue')
      }
    ]
  }
]
