<template>
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
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
                <v-btn color="primary" @click.stop='submit'>Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: '',
      login_failed: false,
    }
  },
  computed: {
    ...mapState(['user', 'token', 'menu'])
  },
  methods: {
    fetch_menu() {
      this.$http.get('menu')
      .then(({data}) => 
        this.$store.commit('set_menu', data)
      ).catch(function(data) {
        console.log('error')
      })    
    },
    submit() {
      this.$axios({
        method: 'post',
        url: 'http://wonzi.net:3000/api/login',
        auth: 
            {
                username: this.username,
                password: this.password
            },
        headers: { 'Content-type': 'application/json' }
      }).then(({data}) => {
        this.$store.commit('set_auth', data)
        this.$http.defaults.headers.common['Authorization'] = 'Bearer ' + data.token
        this.fetch_menu()
        this.$router.replace('/')
      }).catch(({data}) => {
        this.login_failed = true
      });
    },
  },
}
</script>
