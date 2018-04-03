<template>
  <div class="row justify-center">
    <div class="page-intro">
      <img
        src="~assets/img/login_background_image.png"
        class="section__background-image" >

      <div class="title--emphasized">
        하우학교에 오신것을 환영합니다!
      </div>

    </div>
      <div class="container col-xs-12">
        <div class="page-name">
          회원가입
        </div>
        <hr class="page-name--bottom-border" >
      </div>
    <div style="width: 600px; max-width: 90vw;" class="no-shadow q-mb-xl q-pb-xl">

        <div class="col-xs-10 docs-input q-mx-xl">
          <q-field
            label="아이디"
            icon="account circle"
            :label-width="3"
            :error="$v.username.$error"
            error-label="아이디를 잘못 입력하였습니다."
          >
            <q-input v-model="username" />
          </q-field>
          <q-field
            label="비밀번호"
            icon="lock"
            :label-width="3"
            :error="$v.password.$error"
            error-label="비밀번호를 잘못 입력하였습니다."
          >
            <q-input
              v-model="password"
              type="password" />
          </q-field>
          <hr>
          <q-field
            label="이름"
            icon="format size"
            :label-width="3"
            :error="$v.name.$error"
            error-label="이름을 잘못 입력하였습니다."
          >
            <q-input v-model="name" />
          </q-field>
          <q-field
            label="이메일"
            icon="email"
            :label-width="3"
            :error="$v.email.$error"
            error-label="이메일을 잘못 입력하였습니다."
          >
            <q-input
              v-model="email"
              type="email" />
          </q-field>
          <q-field
            label="전화번호"
            icon="phone"
            :label-width="3"
            :error="$v.phone.$error"
            error-label="전화번호를 잘못 입력하였습니다."
          >
            <q-input v-model="phone" />
          </q-field>
          <q-field
            label="출석교회"
            icon="business"
            :label-width="3"
            :error="$v.church.$error"
            error-label="출석교회를 잘못 입력하였습니다."
          >
            <q-input v-model="church" />
          </q-field>
          <q-field
            label="소속학교"
            icon="school"
            :label-width="3"
            :error="$v.school.$error"
            error-label="소속학교를 잘못 입력하였습니다."
          >
            <q-input v-model="school" />
          </q-field>
          <q-field
            label="생년월일"
            icon="cake"
            :label-width="3"
            :error="$v.birthday.$error"
            error-label="생년월일을 잘못 입력하였습니다."
          >
            <q-datetime
              v-model="birthday"
              type="date" />
          </q-field>
        </div>
        <div class="col-xs-12 row justify-end">
          <div class="col-xs-4">
            <q-btn
              @click="store"
              label="회원가입"
              class="q-mt-lg" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required, email } from 'vuelidate/lib/validators'

export default {
  data () {
    return {
      username: '',
      password: '',
      password_confirm: '',
      name: '',
      email: '',
      phone: '',
      school: '',
      church: '',
      birthday: null,
      conditions: false,
      content: `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc.`,
      terms: false,
      terms_check: false
    }
  },
  validations: {
    username: { required },
    password: { required },
    name: { required },
    email: { required, email },
    phone: { required },
    school: { required },
    church: { required },
    birthday: { required }
  },
  methods: {
    store () {
          this.$axios.post(`users`, {
            'username': this.username,
            'password': this.password,
            'name': this.name,
            'email': this.email,
            'phone': this.phone,
            'school': this.school,
            'church': this.church,
            'birthday': this.date
          }).then(({data}) => {
            this.$router.go(-1)
          })
    },
  }
}
</script>
