<template>
  <v-content>
  <v-container>
<Sidebar/>
  </v-container>
    <v-container class="pa-4(fluid)">
        <v-alert v-bind='message' v-model='message.body' dismissible> {{message.body}} </v-alert>
        <div class="py-2">
          <v-slide-y-transition mode='out-in'>
            <router-view></router-view>
          </v-slide-y-transition>
        </div>
    </v-container>
  </v-content>
</template>

<script>

import { mapState } from 'vuex'
import Sidebar from './Sidebar'
import About from './About'

export default {
  components: {Sidebar, About},
  computed: {
    ...mapState(['message'])
  },
}
</script>

