<template>
  <v-app id="inspire">
    <v-navigation-drawer
      app
      stateless hide-overlay :mini-variant.sync="mini" 
      v-model="menu_visible"
    >
      <v-toolbar flat class="transparent">
        <v-list class="pa-0">
          <v-list-tile avatar>
            <v-list-tile-avatar>
              <img src="//ssl.gstatic.com/s2/oz/images/sge/grey_silhouette.png">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title v-if="user">{{user.name}}</v-list-tile-title>
              <v-list-tile-title v-else></v-list-tile-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <v-btn icon @click.native.stop="mini = !mini">
                <v-icon>chevron_left</v-icon>
              </v-btn>
            </v-list-tile-action>
          </v-list-tile>
        </v-list>
      </v-toolbar>
      <v-list class="pt-0" dense>
        <v-list-tile v-if="!menu" :to="{name: 'login'}" :key="로그인">
          <v-list-tile-action>
            <v-icon>mdi-login</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>
              로그인
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile v-else @click="logout" :key="로그아웃">
          <v-list-tile-action>
            <v-icon>mdi-logout</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>
              로그아웃
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <template v-for="item in menu">
          <v-layout
            row
            v-if="item.heading"
            align-center
            :key="item.heading"
          >
            <v-flex xs4>
              <v-subheader v-if="item.heading">
                {{ item.heading }}
              </v-subheader>
            </v-flex>
            <v-divider></v-divider>
          </v-layout>
          <v-list-tile v-else :to="{name: item.href, params: item.params}" :key="item.text">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ item.text }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-navigation-drawer>
    <router-view></router-view>
  </v-app>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data: () => ({
    toolbar: {},
    mini: true,
    menu_visible: true,
  }),
  computed: {
    ...mapState(['user', 'token', 'menu'])
  },
  methods: {
    fetch_menu() {
      this.$store.commit('set_menu', false)
      this.$http.get('menu')
      .then(({data}) => 
        this.$store.commit('set_menu', data)
      ).catch(function(data) {
        localStorage.removeItem("token")
        localStorage.removeItem("user")
      })    
      this.$http.get('toolbar')
      .then(({data}) => 
        this.toolbar = data
      )
    },
    logout() {
      this.$store.commit('set_menu', false)
      localStorage.removeItem("token")
      localStorage.removeItem("user")
      this.$router.replace('/')
    }
  },
  created () {
    if (localStorage.getItem("token") !== null) {
      this.$http.defaults.headers.common['Authorization'] = 'Bearer ' + this.token
    }
    this.fetch_menu()
  }
}
</script>
