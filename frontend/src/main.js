
// 导入Vue框架
import Vue from 'vue'
// 导入主视图文件
import App from './App'
// 导入路由文件
import { router } from './router'
// 导入状态管理器
import store from './store'

// 导入element组件
import ElementUi from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// 导入全局svg-icon组件
// 导入介绍组件的组件
import SvgIcon from '@/components/SvgIcon'
// 导入中英互译组件
import i18n from './lang'
// 导入点击波浪组件
import Wave from '@/directive/wave/index'
import Exclude from '@/directive/exclude/index'
import EventBus from '@/utils/eventBus'


// 注册全局svg-icon组件
Vue.component('svg-icon', SvgIcon)

// 待开发组件提示
Vue.config.productionTip = false
Vue.prototype.$bus = EventBus

// 使用element-ui
Vue.use(ElementUi)
// 使用v-wave 波浪效果
Vue.use(Wave)
Vue.use(Exclude)

// add baidu count
if (process.env.NODE_ENV === 'production') {
  let hm = document.createElement('script')
  hm.src = 'https://hm.baidu.com/hm.js?0b2c26b40000cc8d4a441a66a12bc772'
  let s = document.getElementsByTagName('script')[0]
  s.parentNode.insertBefore(hm, s)
}

import Router from 'vue-router'

const originalPush = Router.prototype.push
Router.prototype.push = function push(location, onResolve, onReject) {
  if (onResolve || onReject) return originalPush.call(this, location, onResolve, onReject)
  return originalPush.call(this, location).catch(err => err)
}

new Vue({
  i18n,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
