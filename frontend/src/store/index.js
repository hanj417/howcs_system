import Vue from 'vue'
import Vuex from 'vuex'
import config from '../config'
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    user: {},
    menu: [],
    token: null,
    message: {
      type: null,
      body: null
    },
    config: config
  },
  mutations: {
    set_auth (state, { user, token }) {
      state.user = user
      state.token = token
      global.helper.ls.set('user', user)
      global.helper.ls.set('token', token)
    },
    show_message (state, type, body) {
      state.message = { type, body }
    },
    set_menu (state, data) {
      state.menu = data
    },
  },
  actions: {
    check_auth ({ commit }) {
      let data = {
        user: global.helper.ls.get('user'),
        token: global.helper.ls.get('token')
      }
      commit('set_auth', data)
    },
  }
})

export default store
