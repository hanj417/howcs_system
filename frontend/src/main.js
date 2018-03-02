import Vue from 'vue'
import helper from './helper'
global.helper = helper
import config from './config'
import store from './store/'
global.store = store

import router from './router'
import Vuetify from 'vuetify'
Vue.use(Vuetify)
import './http'

import 'vuetify/src/stylus/main.styl'
import 'vuetify/src/stylus/settings/_colors.styl'
import '@/styles/main.styl'

import App from './App'

import validator from 'Validator'
global.validator = validator

Vue.config.devtools = true
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App),
  methods: {
    back () {
      this.$router.go(-1)
    }
  },
  created () {
    this.$store.dispatch('checkPageTitle', this.$route.path)
    this.$store.dispatch('checkAuth')
  }
})
