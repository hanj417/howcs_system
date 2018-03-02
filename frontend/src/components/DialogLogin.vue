<template>
    <v-dialog v-model="login_visible" width="300px">
            <v-card width="300px" class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Login form</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field prepend-icon="person" name="username" label="Login" v-model="username" type="text"></v-text-field>
                  <v-text-field prepend-icon="lock" name="password" label="Password" id="password" v-model="password" type="password"></v-text-field>
                  <div v-if="login_failed" class="flex pb-2">Login Failed</div>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click.stop='submit' @success='onSuccess'>Login</v-btn>
              </v-card-actions>
            </v-card>
    </v-dialog>
</template>

<script>
import { mapState } from 'vuex'
import Vue from 'vue'
import axios from 'axios'
Vue.use(axios)

export default {
  name: 'DialogLogin',
  data () {
    return {
      username: '',
      password: '',
      login_failed: false,
    }
  },
  computed: {
    ...mapState(['login_visible', 'toolbar'])
  },
  methods: {
    submit() {
      axios({
        method: 'post',
        url: 'http://wonzi.net:3000/api/login',
        auth: 
            {
                username: 'admin',
                password: '123456',
            },
        headers: { 'Content-type': 'application/json' }
      }).then(({data}) => {
        this.$store.commit('setAuth', data)
        this.$store.commit('set_login_visible', false)
        this.$emit('login_success')
      }).catch(({data}) => {
        this.username = ''
        this.password = ''
        this.login_failed = true
      });
    },
    onSuccess (data) {
      this.$store.commit('setAuth', data)
      this.$router.replace('/')
      this.$store.commit('set_login_visible', false)
    }
  },
}
</script>
