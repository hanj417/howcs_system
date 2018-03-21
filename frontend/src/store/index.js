import Vue from 'vue'
import Vuex from 'vuex'

import menu from './menu'
import auth from './auth'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    menu,
    auth
  }
})

export default store
