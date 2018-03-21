<template>
  <q-page
    padding
    class="row justify-center gutter-md">
    <template v-for='item in menu'>
      <template v-if='item.heading'>
        <div class="col-xs-10">
          {{ item.heading }}
        </div>
      </template>
      <template v-else>
        <div class="col-xs-4">
          <q-btn
            color="secondary"
            @click.native="$router.push({name:item.href, params: item.params})"
            class="no-shadow col-xs-4"
            :label="item.label">
            {{ item.label }}
            <!--            <q-icon :name="item.icon" />-->
          </q-btn>
        </div>
      </template>
    </template>
  </q-page>
</template>

<script>
export default {
  data () {
    return {
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
    }
  },
  methods: {
  },
  created () {
  }
}
</script>
