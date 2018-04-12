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
    <div
      style="width: 600px; max-width: 90vw;"
      class="no-shadow q-mb-xl q-pb-xl">

      <div class="col-xs-10 docs-input q-mx-xl">
        <q-field
          label="아이디*"
          icon="account circle"
          :label-width="3"
          :error="$v.form.username.$error"
          error-label="아이디를 잘못 입력하였습니다."
        >
          <q-input v-model="form.username" />
        </q-field>
        <q-field
          label="비밀번호*"
          icon="lock"
          :label-width="3"
          :error="$v.form.password.$error"
          error-label="비밀번호는 4자 이상이어야 합니다."
        >
          <q-input
            v-model="form.password"
            type="password" />
        </q-field>
        <q-field
          label="비밀번호 확인*"
          icon="lock"
          :label-width="3"
          :error="$v.form.password_confirm.$error"
          error-label="비밀번호가 일치하지 않습니다."
        >
          <q-input
            v-model="form.password_confirm"
            type="password" />
        </q-field>
        <hr>
        <q-field
          label="이름*"
          icon="format size"
          :label-width="3"
          :error="$v.form.name.$error"
          error-label="이름을 잘못 입력하였습니다."
        >
          <q-input v-model="form.name" />
        </q-field>
        <q-field
          label="이메일*"
          icon="email"
          :label-width="3"
          :error="$v.form.email.$error"
          error-label="이메일을 잘못 입력하였습니다."
        >
          <q-input
            v-model="form.email"
            type="email" />
        </q-field>
        <q-field
          label="전화번호*"
          icon="phone"
          :label-width="3"
          :error="$v.form.phone.$error"
          error-label="전화번호를 잘못 입력하였습니다."
        >
          <q-input v-model="form.phone" />
        </q-field>
        <q-field
          label="출석교회"
          icon="business"
          :label-width="3"
          :error="$v.form.church.$error"
          error-label="출석교회를 잘못 입력하였습니다."
        >
          <q-input v-model="form.church" />
        </q-field>
        <q-field
          label="소속학교"
          icon="school"
          :label-width="3"
          :error="$v.form.school.$error"
          error-label="소속학교를 잘못 입력하였습니다."
        >
          <q-input v-model="form.school" />
        </q-field>
        <q-field
          label="생년월일*"
          icon="cake"
          :label-width="3"
          :error="$v.form.birthday.$error"
          error-label="생년월일을 잘못 입력하였습니다."
        >
          <q-datetime
            v-model="form.birthday"
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
import { required, email, minLength, sameAsPassword, sameAs} from 'vuelidate/lib/validators'

export default {
  data: function () {
    return {
form: {
      username: '',
      password: '',
      password_confirm: '',
      name: '',
      email: '',
      phone: '',
      school: '',
      church: '',
      birthday: null,
},
      conditions: false,
      content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc.',
      terms: false,
      terms_check: false
    }
  },
  validations: {
    form: {
    username: { required, minLength: minLength(4) },
    password: { required, minLength: minLength(4) },
    password_confirm: { sameAsPassword: sameAs('password') },
    name: { required },
    email: { required, email },
    phone: { required },
    school: { },
    church: { },
    birthday: { required }
    }
  },
  methods: {
    store: function () {
      this.$v.form.$touch()
      if (this.$v.form.$error) {
        this.$q.notify('회원 정보가 잘못 되었습니다.')
        return
      }

      let self = this
      self.$axios.post('users', {
        'username': self.form.username,
        'password': self.form.password,
        'name': self.form.name,
        'email': self.form.email,
        'phone': self.form.phone,
        'school': self.form.school,
        'church': self.form.church,
        'birthday': (new Date(self.form.birthday)).toISOString().substr(0,10)
      }).then(function (response) {
        let data = response.data
        self.$router.go(-1)
      })
    }
  }
}
</script>
