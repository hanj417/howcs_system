<template>
  <div/>
</template>
<script>
import { LocalStorage } from 'quasar'

export default {
  created: function () {
    this.$store.commit('auth/SetAuth', {user: {}, token: ''})
    LocalStorage.remove('user_')
    LocalStorage.remove('token_')
    this.$router.go(-1)
  }
}
</script>
