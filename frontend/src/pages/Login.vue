<template>
<q-page padding class="row justify-center">
    <div class="page-intro">
      <img src="~assets/img/login_background_image.png" class="section__background-image" />

      <div class="title--emphasized">
		하우학교에 오신것을 환영합니다!
      </div>
     
    </div>

   <div class="container">
      <div class="page-name">
      로그인
      </div>
      <hr class="page-name--bottom-border" />
    </div> 
<div style="width: 400px; max-width: 80vw;">
    <q-input v-model="username" float-label="아이디" autofocus style="border-bottom: 1px solid;" />
    <q-input v-model="password" float-label="비밀번호" type="password" style="border-bottom: 1px solid;" />
<div class="row justify-end">
  <q-btn @click="login" label="로그인" />
</div>
</div>

</q-page>
</template>

<script>
import { LocalStorage } from 'quasar'
import './docs-input.styl'

export default {
  data () {
    return {
      username: '',
      password: '',
      login_fail: false,
    }
  },
  methods: {
    fetch_menu() {
      this.$axios.get('menu')
      .then(({data}) => 
        this.$store.commit('menu/UpdateMenu', data)
      ).catch(function(data) {
        console.log('error')
      })    
    },
    login() {
      this.$axios({
        method: 'post',
        url: 'login',
        auth: {username: this.username, password: this.password},
        headers: { 'Content-type': 'application/json' }
      }).then(({data}) => {
        this.$store.commit('auth/SetAuth', data)
        this.$axios.defaults.headers.common['Authorization'] = 'Bearer ' + data.token
        this.fetch_menu()
        LocalStorage.set('user_', data.user)
        LocalStorage.set('token_', data.token)
        this.$router.replace('/')
      }).catch(({data}) => {
        this.login_fail = true
      });
    },
  },
}
/*
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
      this.$axios.get('menu')
      .then(({data}) => 
        this.$store.commit('menu/SetMenu', data)
      ).catch(function(data) {
        console.log('error')
      })    
    },
    submit() {
      this.$axios({
        method: 'post',
        url: 'http://howcs.kr:3000/api/login',
        auth: {username: this.username, password: this.password},
        headers: { 'Content-type': 'application/json' }
      }).then(({data}) => {
        this.$store.commit('set_auth', data)
        this.$axios.defaults.headers.common['Authorization'] = 'Bearer ' + data.token
        this.fetch_menu()
        this.$router.replace('/')
      }).catch(({data}) => {
        this.login_failed = true
      });
    },
  },
}
*/
</script>
