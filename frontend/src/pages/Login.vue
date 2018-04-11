<template>
  <div>
    <div class="page-intro">
      <img
        src="~assets/img/login_background_image.png"
        class="section__background-image" >

      <div class="title--emphasized">
        하우학교에 오신것을 환영합니다!
      </div>

    </div>

    <div class="row justify-center">
      <div class="container col-xs-12">
        <div class="page-name">
          로그인
        </div>
        <hr class="page-name--bottom-border" >
      </div>
      <div
        class="docs-input"
        style="width: 400px; max-width: 80vw;">
        <q-field
          label="아이디"
          icon="account circle"
          :label-width="3"
        >
          <q-input
            v-model="username"
            autofocus />
        </q-field>
        <q-field
          label="비밀번호"
          icon="lock"
          :label-width="3"
          :error="login_fail"
          error-label="아이디 또는 비밀번호를 잘못 입력하였습니다."
        >
          <q-input
            v-model="password"
            type="password" />
        </q-field>
        <div class="row justify-end">
          <q-btn
            @click="login"
            label="로그인"
            class="q-mt-sm" />
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { LocalStorage } from 'quasar'
import './docs-input.styl'

export default {
  data: function () {
    return {
      username: '',
      password: '',
      login_fail: false
    }
  },
  methods: {
    fetch_menu: function () {
      var self = this
      this.$axios.get('menu')
        .then(function (response) {
          let data = response.data
          self.$store.commit('menu/UpdateMenu', data)
        }).catch(function (data) {
          console.log('error')
        })
    },
    login: function () {
      var self = this
      this.$axios({
        method: 'post',
        url: 'login',
        auth: {username: this.username, password: this.password},
        headers: { 'Content-type': 'application/json' }
      }).then(function (response) {
        let data = response.data
        self.$store.commit('auth/SetAuth', data)
        self.$axios.defaults.headers.common['Authorization'] = 'Bearer ' + data.token
        self.fetch_menu()
        LocalStorage.set('user_', data.user)
        LocalStorage.set('token_', data.token)
        self.$router.replace('/')
      }).catch(function (response) {
        let data = response.data
        self.login_fail = true
      })
    }
  }
}
</script>
