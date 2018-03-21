<template>
  <q-layout view="hHh lpr fff">
    <q-scroll-observable @scroll="userHasScrolled" />
    <q-layout-header class="no-shadow">
      <q-toolbar
        :class="{transparent: header_transparency}"
        inverted>
        <q-toolbar-title>
          <a
            href="/"
            class="navbar-brand">
            <img
              src="~assets/img/logo4.png"
              class="navbar__logo" >
          </a>
        </q-toolbar-title>
        <div class="row no-wrap gt-xs no-shadow">
          <template v-for="item in toolbar">
            <div>
              <q-btn-dropdown
                v-if="item.submenu"
                :label="item.label"
                class="no-shadow navbar__menu" >
                <q-list>
                  <template v-for="subitem in item.submenu">
                    <q-item :to="subitem.href">
                      <q-item-main>
                        <q-item-tile label>{{ subitem.label }}</q-item-tile>
                      </q-item-main>
                    </q-item>
                  </template>
                </q-list>
              </q-btn-dropdown>
              <q-btn
                v-else
                class="no-shadow"
                @click="$router.push({name: item.href, params: item.params})"
                :label="item.label"
                :no-ripple="true"/>
            </div>
          </template>
        </div>
        <div class="xs">
          <q-btn
            flat
            round
            dense
            icon="menu">
            <q-popover>
              <template v-for="item in toolbar">
                <q-collapsible
                  v-if="item.submenu"
                  :label="item.label"
                  class="no-shadow navbar__menu">
                  <template v-for="subitem in item.submenu">
                    <q-item :to="subitem.href">
                      <q-item-main :label="subitem.label" />
                    </q-item>
                  </template>
                </q-collapsible>
                <q-item v-else :to="item.href">
                  <q-item-main
                    :label="item.label"
                    class="navbar__menu"/>
                </q-item>
              </template>
            </q-popover>
          </q-btn>
        </div>
      </q-toolbar>
    </q-layout-header>

    <q-layout-footer class="no-shadow">
      <div class="hidden-xs">
        <div class="space"/>
        <div class="space"/>
        <div class="space"/>
      </div>
      <footer class="footer">
        <div class="container footer__container">
          <div>
            경기도 화성시 동탄반석로 196 아이프라자 7층
          </div>
          <div>
            T. (031) 613-0737
          </div>
          <div>
            E. how@howcs.kr
          </div>
          <div>
            ©howcs.kr since 2018
          </div>

          <div class="visible-xs">
            <div class="space"/>
          </div>
          <div class="social-media__icon-container--small">
            <a
              href="#"
              target="_blank">
              <img
                src="~assets/img/facebook.png"
                class="social-media__icon--small" >
            </a>
            <a
              href="#"
              target="_blank">
              <img
                src="~assets/img/twitter.png"
                class="social-media__icon--small" >
            </a>
          </div>

        </div>
      </footer>
    </q-layout-footer>
    <q-layout-drawer
      side="left"
      v-model="leftDrawerOpen"
      content-class='bg-grey-1'
    >
      <template v-for='item in menu'>
        <template v-if='item.heading'>
          <q-list-header>{{ item.heading }}</q-list-header>
        </template>
        <template v-else>
          <q-item :to="{name:item.href, params:item.params}">
            <!--<q-item-side :icon='item.icon' />-->
            <q-item-main :label='item.text' />
          </q-item>
        </template>
      </template>
    </q-layout-drawer>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { LocalStorage } from 'quasar'

export default {
  name: 'LayoutDefault',
  props: ['leftDrawerOpen'],
  data () {
    return {
      // leftDrawerOpen: this.$q.platform.is.desktop,
      header_transparency: true,
      lightdimm: false,
      toolbar: [],
      toolbar_default: [
        {'href': 'about', 'label': '학교소개'},
        {'href': 'entrance', 'label': '입학안내'},
        {'label': '교육',
          'submenu': [
            {'href': 'edu/edu1', 'label': '교육특징'},
            {'href': 'edu/edu2', 'label': '교육과정'},
            {'href': 'edu/edu3', 'label': '교육&학습과정편성'},
            {'href': 'edu/edu4', 'label': '주요일정'},
            {'href': 'edu/edu5', 'label': '하우의 하루'},
            {'href': 'edu/edu6', 'label': '교사소개'}
          ]},
        {'label': '이야기',
          'submenu': [
            {'href': 'notice', 'label': '공지사항'},
            {'href': 'story', 'label': '하우하다'},
            {'href': 'photo', 'label': '하우포토'}
          ]},
        {'href': 'agit', 'label': '아지트'},
        {'href': 'community', 'label': '교육공동체'}
      ],
      toolbar_loggedIn: [
        {'href': 'hana', 'label': '하우하나'},
        {'href': 'logout', 'label': '로그아웃'}
      ],
      toolbar_logged_out: [
        {'href': 'login', 'label': '로그인'},
        {'href': 'register', 'label': '회원가입'}
      ]
    }
  },
  watch: {
    user (new_user, old_user) {
      console.log(new_user)
      this.update_toolbar()
    }
  },
  computed: {
    menu: {
      get () {
        return this.$store.state.menu.menu_
      },
      set (val) {
        this.$store.commit('menu/UpdateMenu', val)
      }
    },
    user: {
      get () {
        return this.$store.state.auth.user_
      },
      set (val) {
        this.$store.commit('auth/SetAuth', val)
      }
    }
  },
  methods: {
    login () {
      let loggedIn = LocalStorage.has('user_')
      let _token = LocalStorage.has('user_')
      if (loggedIn) {
        let _user = LocalStorage.get.item('user_')
        let _token = LocalStorage.get.item('token_')
        this.$store.commit('auth/SetAuth', {_user, _token})
        this.$axios.defaults.headers.common['Authorization'] = 'Bearer ' + _token
        this.$axios.get('login')
          .then(({data}) => {
            this.fetch_menu()
          }).catch(({data}) => {
            this.$store.commit('auth/SetAuth', {user: {}, token: ''})
            LocalStorage.remove('user_')
            LocalStorage.remove('token_')
          })
      } else {
        this.$store.commit('auth/SetAuth', {user: {}, token: ''})
      }
    },
    fetch_menu () {
      this.$axios.get('menu')
        .then(({data}) =>
          this.$store.commit('menu/UpdateMenu', data)
        ).catch(function (data) {
          console.log('error')
        })
    },
    update_toolbar () {
      // let loggedIn = this.$q.localstorage.has('user_')
      let loggedIn = LocalStorage.has('user_')
      if (loggedIn) {
        this.toolbar = this.toolbar_default.concat(this.toolbar_loggedIn)
      } else {
        this.toolbar = this.toolbar_default.concat(this.toolbar_logged_out)
      }
    },
    userHasScrolled (scroll) {
      console.log(scroll)
      if (scroll.position > 100) {
        this.header_transparency = false
      } else {
        this.header_transparency = true
      }
      // {
      //   position: 56, // pixels from top
      //   direction: 'down', // 'down' or 'up'
      //   directionChanged: false, // has direction changed since this handler was called?
      //   inflexionPosition: 56 // last scroll position where user changed scroll direction
      // }
    }
  },
  created () {
    this.login()
    this.update_toolbar()
  }
}
</script>

<style lang="stylus">
.btn-fixed-width
  padding 10px 25px
</style>
