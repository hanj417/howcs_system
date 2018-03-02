<template>
  <v-app id="inspire">
    <v-navigation-drawer
      fixed
      :clipped="$vuetify.breakpoint.mdAndUp"
      app
      v-model="menu_visible"
    >
      <v-list dense>
        <template v-for="item in menu">
          <v-layout
            row
            v-if="item.heading"
            align-center
            :key="item.heading"
          >
            <v-flex xs6>
              <v-subheader v-if="item.heading">
                {{ item.heading }}
              </v-subheader>
            </v-flex>
            <v-flex xs6 class="text-xs-center">
              <a href="#!" class="body-2 black--text">EDIT</a>
            </v-flex>
          </v-layout>
          <v-list-group
            v-else-if="item.children"
            v-model="item.model"
            :key="item.text"
            :prepend-icon="item.model ? item.icon : item['icon-alt']"
            append-icon=""
          >
            <v-list-tile slot="activator">
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ item.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile
              v-for="(child, i) in item.children"
              :key="i"
              @click=""
            >
              <v-list-tile-action v-if="child.icon">
                <v-icon>{{ child.icon }}</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ child.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list-group>
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
    <v-toolbar
      color="blue darken-3"
      dark
      app
      :clipped-left="$vuetify.breakpoint.mdAndUp"
      fixed
    >
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <span class="hidden-sm-and-down">하우학교</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <template v-for="item in toolbar">
        <v-menu offset-y>
          <v-btn flat dark slot="activator" :to='item.href'>{{ item.text }}</v-btn>
          <v-list v-if="item.children" v-for="child_item in item.children">
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ child_item.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-menu>
      </template>
    </v-toolbar>
    <router-view></router-view>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    menu: {},
    toolbar: {},
  }),
  methods: {
    fetch_menu() {
      this.$http.get('menu')
      .then(({data}) => 
        this.menu = data
      )
      this.$http.get('toolbar')
      .then(({data}) => 
        this.toolbar = data
      )
    },
  },
  created () {
    this.fetch_menu()
  }
}
</script>
