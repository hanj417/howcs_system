import Vue from 'vue'
import Vuex from 'vuex'

import example from './module-example'
import menu from './menu'
import auth from './auth'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    example,
    menu,
    auth,
  }
})

export default store
