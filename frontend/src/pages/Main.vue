<template lang="pug">
v-app(:dark="dark",standalone)
  v-toolbar.darken-1(fixed,dark,:class="theme") 
    v-toolbar-title {{$t(pageTitle)}}
    //v-toolbar-title(slot="extension") {{$t(pageTitle)}}
    v-spacer
    template(v-for='item in topMenu')
      v-menu(offset-y)
        v-btn(flat, dark, slot="activator", :to='item.href') {{ item.title }}
        v-list(v-if='item.items')
          v-list-tile(v-for='subItem in item.items', :key='subItem.href',:to='subItem.href', v-bind:router='!subItem.target', ripple, v-bind:disabled='subItem.disabled', v-bind:target='subItem.target')
            v-list-tile-title {{ subItem.title }}
  router-view
</template>

<script>

import { mapState } from 'vuex'

export default {
  data () {
    return {
      dark: false,
      theme: 'primary',
    }
  },
  computed: {
    ...mapState(['topMenu', 'pageTitle'])
  },
  methods: {
    changeLocale (to) {
      global.helper.ls.set('locale', to)
      this.$i18n.locale = to
    },
    fetchMenu () {
      // fetch menu from server
      //this.$http.get('menu').then(({data}) => this.$store.commit('setMenu', data))
    }
  },

  created () {
    this.fetchMenu()
  }
}
</script>

