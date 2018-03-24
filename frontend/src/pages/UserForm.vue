<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 600px; max-width: 90vw;" class="shadow-8">
    <div class="col-xs-12 text-center q-title text-weight-bold q-pa-md">회원 정보</div>
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
      <div
        v-if="is_howcs_student"
        class="col-xs-10 docs-input q-mx-xl">
        <hr>
        <q-field
          label="학번"
          icon="create"
          :label-width="3"
          :error="$v.school.$error"
          error-label="소속학교를 잘못 입력하였습니다."
        >
          <q-input v-model="student_id" />
        </q-field>
        <q-field
          label="성별"
          icon="wc"
          :label-width="3"
        >
          <q-option-group
            type="radio"
            v-model="gender"
            inline
            :options="[
              { label: '남학생', value: 'male' },
              { label: '여학생', value: 'female' },
            ]"
          />
        </q-field>
        <q-field
          label="부 성명"
          icon="face"
          :label-width="3"
          :error="$v.school.$error"
          error-label="소속학교를 잘못 입력하였습니다."
        >
          <q-input v-model="father_name" />
        </q-field>
        <q-field
          label="부 주민번호"
          icon="featured play list"
          :label-width="3"
          :error="$v.school.$error"
          error-label="소속학교를 잘못 입력하였습니다."
        >
          <q-input v-model="father_rrn" />
        </q-field>
        <q-field
          label="모 성명"
          icon="face"
          :label-width="3"
          :error="$v.school.$error"
          error-label="소속학교를 잘못 입력하였습니다."
        >
          <q-input v-model="mother_name" />
        </q-field>
        <q-field
          label="모 주민번호"
          icon="featured play list"
          :label-width="3"
          :error="$v.school.$error"
          error-label="소속학교를 잘못 입력하였습니다."
        >
          <q-input v-model="mother_rrn" />
        </q-field>
        <q-field
          label="주소"
          icon="home"
          :label-width="3"
          :error="$v.school.$error"
          error-label="소속학교를 잘못 입력하였습니다."
        >
          <q-input v-model="address" />
        </q-field>
      </div>
      <div class="col-xs-12 row justify-end q-mt-lg">
        <div class="col-xs-4">
          <q-btn
            v-if="is_admin && !is_howcs_student"
            @click="convert_student"
            label="하우학교 학생 전환" />
        </div>
        <div class="col-xs-2 q-ma-xl">
          <q-btn
            @click="store"
            label="수정" />
        </div>
      </div>
    </div>
  </div>
</div>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'
import { required, email } from 'vuelidate/lib/validators'

export default {
  data () {
    return {
      is_admin: false,
      is_howcs_student: false,
      user_id: '',
      username: '',
      password: '',
      password_confirm: '',
      name: '',
      email: '',
      phone: '',
      school: '',
      church: '',
      birthday: null,
      student_id: '',
      gender: {},
      rrn: '',
      father_name: '',
      father_rrn: '',
      mother_name: '',
      mother_rrn: '',
      address: '',
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
  props: ['action', 'id'],
  methods: {
    store () {
      console.log('store')
      console.log(this.id)
      if (this.action === 'new') {
        if (this.is_howcs_student === false) {
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
        } else {
          this.$axios.post(`student_infos`, {
            'username': this.username,
            'password': this.password,
            'name': this.name,
            'email': this.email,
            'phone': this.phone,
            'school': this.school,
            'church': this.church,
            'birthday': this.date,
            'student_id': this.student_id,
            'gender': this.gender,
            'rrn': this.rrn,
            'father_name': this.father_name,
            'father_rrn': this.father_rrn,
            'mother_name': this.mother_name,
            'mother_rrn': this.mother_rrn,
            'address': this.address
          }).then(({data}) => {
            this.$router.go(-1)
          })
        }
      } else if (this.action === 'update') {
        if (this.is_howcs_student === false) {
          this.$axios.put(`users/` + this.user_id, {
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
        } else {
          this.$axios.put(`student_infos/` + this.user_id, {
            'username': this.username,
            'password': this.password,
            'name': this.name,
            'email': this.email,
            'phone': this.phone,
            'school': this.school,
            'church': this.church,
            'birthday': this.date,
            'student_id': this.student_id,
            'gender': this.gender,
            'rrn': this.rrn,
            'father_name': this.father_name,
            'father_rrn': this.father_rrn,
            'mother_name': this.mother_name,
            'mother_rrn': this.mother_rrn,
            'address': this.address
          }).then(({data}) => {
            this.$router.go(-1)
          })
        }
      }
    },
    convert_student () {
      this.is_howcs_student = true
    }
  },
  created () {
    let loggedIn = LocalStorage.has('user_')
    if (this.action === 'update') {
      if (this.id) {
        this.is_admin = true
        this.user_id = this.id
      } else if (loggedIn) {
        this.user = LocalStorage.get.item('user_')
        this.user_id = this.user['id']
      }
      this.$axios.get(`users/` + this.user_id
      ).then(({ data }) => {
        console.log(data)
        this.username = data.username
        this.name = data.name
        this.email = data.email
        this.phone = data.phone
        this.school = data.school
        this.church = data.church
        var d = new Date(data.birthday)
        this.date = d.toISOString().substr(0, 10)
        if (data.hasOwnProperty('student_info')) {
          this.is_howcs_student = true
          this.student_id = data.student_info.student_id
          this.gender = data.student_info.gender
          this.rrn = data.student_info.rrn
          this.father_name = data.student_info.father_name
          this.father_rrn = data.student_info.father_rrn
          this.mother_name = data.student_info.mother_name
          this.mother_rrn = data.student_info.mother_rrn
          this.address = data.student_info.address
        }
      })
    } else if (this.action === 'new_student') {
      this.is_howcs_student = true
    }
  }
}
</script>
