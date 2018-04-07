<template>
  <q-page
    padding
    class="row wrap justify-start">
    <template v-for='item in menu'>
      <template v-if='item.heading'>
        <div class="col-xs-12 q-mt-lg q-subheading">
          {{ item.heading }}
          <hr>
        </div>
      </template>
      <template v-else>
        <div class="col-auto justify-center">
            <div @click="$router.push({name: item.href, params: item.params})"><q-icon :name="item.icon" size="150px"/></div>
            <div class="text-center">{{ item.text }}</div>
        </div>
      </template>
    </template>
  </q-page>
</template>

<script>
export default {
  data: function() {
    return {
    }
  },
  computed: {
    menu: {
      get:function () {
        return this.$store.state.menu.menu_
      },
      set: function (val) {
        this.$store.commit('menu/UpdateMenu', val)
      }
    }
  },
  methods: {
  },
  created: function () {
  }
}
</script>
