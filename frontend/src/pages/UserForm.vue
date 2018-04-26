<template>
  <q-page
    padding
    class="row justify-center">
    <div
      style="width: 600px; max-width: 90vw;"
      class="shadow-8">
      <div class="col-xs-12 text-center q-title text-weight-bold q-pa-md">회원 정보</div>
      <div class="col-xs-10 docs-input q-mx-xl">
        <q-field
          label="아이디"
          icon="account circle"
          disabled
          :label-width="3"
          :error="$v.form.username.$error"
          error-label="아이디를 잘못 입력하였습니다."
        >
          <q-input v-model="form.username" />
        </q-field>
        <q-field
          label="비밀번호"
          icon="lock"
          :label-width="3"
          :error="$v.form.password.$error"
          error-label="비밀번호를 잘못 입력하였습니다."
        >
          <q-input
            v-model="form.password"
            type="password" />
        </q-field>
        <q-field
          label="비밀번호 확인"
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
          label="이름"
          icon="format size"
          :label-width="3"
          :error="$v.form.name.$error"
          error-label="이름을 잘못 입력하였습니다."
        >
          <q-input v-model="form.name" />
        </q-field>
        <q-field
          label="이메일"
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
          label="전화번호"
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
          label="생년월일"
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
      <div
        v-if="is_howcs_student"
        class="col-xs-10 docs-input q-mx-xl">
        <hr>
        <q-field
          label="학번"
          icon="create"
          :disabled="!is_admin"
          :label-width="3"
          :error="$v.form.student_id.$error"
          error-label="학번을 잘못 입력하였습니다."
        >
          <q-input v-model="form.student_id" />
        </q-field>
        <q-field
          label="성별"
          icon="wc"
          :label-width="3"
        >
          <q-option-group
            type="radio"
            v-model="form.gender"
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
          :error="$v.form.father_name.$error"
          error-label="이름을 잘못 입력하였습니다."
        >
          <q-input v-model="form.father_name" />
        </q-field>
        <q-field
          label="부 주민번호"
          icon="featured play list"
          :label-width="3"
          :error="$v.form.father_rrn.$error"
          error-label="주민번호를 잘못 입력하였습니다."
        >
          <q-input v-model="form.father_rrn" />
        </q-field>
        <q-field
          label="모 성명"
          icon="face"
          :label-width="3"
          :error="$v.form.mother_name.$error"
          error-label="이름을 잘못 입력하였습니다."
        >
          <q-input v-model="form.mother_name" />
        </q-field>
        <q-field
          label="모 주민번호"
          icon="featured play list"
          :label-width="3"
          :error="$v.form.mother_rrn.$error"
          error-label="주민번호를 잘못 입력하였습니다."
        >
          <q-input v-model="form.mother_rrn" />
        </q-field>
        <q-field
          label="주소"
          icon="home"
          :label-width="3"
          :error="$v.form.address.$error"
          error-label="주소를 잘못 입력하였습니다."
        >
          <q-input v-model="form.address" />
        </q-field>
      </div>
      <div
        v-if="is_agit_teacher"
        class="col-xs-10 docs-input q-mx-xl">
        <hr>
        <q-field
          label="이력"
          icon="create"
          :label-width="3"
          :error="$v.form.career.$error"
          error-label="이력을 잘못 입력하였습니다."
        >
          <q-input v-model="form.career" type="textarea"/>
        </q-field>
        <q-field
          v-if="is_admin"
          label="승인"
          icon="agit_teacher_approval"
          :label-width="3"
          :error="$v.form.agit_teacher_approval.$error"
          error-label="이력을 잘못 입력하였습니다."
        >
          <q-select v-model="form.agit_teacher_approval" type="textarea" :options="agit_teacher_approval_options"/>
        </q-field>
      </div>
      <div class="col-xs-12 row justify-end q-my-lg">
        <div class="col-xs-4">
          <q-btn
            v-if="is_admin && !is_howcs_student"
            @click="convert_student"
            label="하우학교 학생 전환" />
        </div>
        <div
          v-if="is_admin"
          class="col-xs-2">
          <q-btn
            @click="remove"
            label="삭제" />
        </div>
        <div class="col-xs-2">
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
import { required, email, minLength, sameAsPassword, sameAs} from 'vuelidate/lib/validators'

export default {
  data: function () {
    return {
      is_admin: false,
      is_howcs_student: false,
      is_agit_teacher: false,
      user_id: '',
      agit_teacher_info_id: '',
      agit_teacher_approval_options: [
        {label: '승인', value: true},
        {label: '대기', value: false},
      ],
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
      student_id: '',
      gender: {},
      rrn: '',
      father_name: '',
      father_rrn: '',
      mother_name: '',
      mother_rrn: '',
      address: '',
      career: '',
      agit_teacher_approval: '',
},
      conditions: false,
      content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc.',
      terms: false,
      terms_check: false
    }
  },
  validations: {
form: {
    username: { required },
    password: { },
    password_confirm: { sameAsPassword: sameAs('password') },
    name: { required },
    email: { required, email },
    phone: { required },
    school: { },
    church: { },
    birthday: { required },
      student_id: {},
      gender: {},
      rrn: {},
      father_name: {},
      father_rrn: {},
      mother_name: {},
      mother_rrn: {},
      address: {},
      career: {},
      agit_teacher_approval: {},
}
  },
  props: ['action', 'id'],
  methods: {
    store: function () {
      this.$v.form.$touch()
      if (this.$v.form.$error) {
        this.$q.notify('회원 정보가 잘못 되었습니다.')
        return
      }

      var self = this
      if (self.action === 'new') {
        if (self.is_howcs_student === false) {
          self.$axios.post('users', {
            'username': self.form.username,
            'password': self.form.password,
            'name': self.form.name,
            'email': self.form.email,
            'phone': self.form.phone,
            'school': self.form.school,
            'church': self.form.church,
            'birthday': (new Date(self.form.birthday)).toISOString().substr(0, 10)
          }).then(function (response) {
            let data = response.data
            self.$router.go(-1)
          })
        } else {
          self.$axios.post('student_infos', {
            'username': self.form.username,
            'password': self.form.password,
            'name': self.form.name,
            'email': self.form.email,
            'phone': self.form.phone,
            'school': self.form.school,
            'church': self.form.church,
            'birthday': (new Date(self.form.birthday)).toISOString().substr(0, 10),
            'student_id': self.form.student_id,
            'gender': self.form.gender,
            'rrn': self.form.rrn,
            'father_name': self.form.father_name,
            'father_rrn': self.form.father_rrn,
            'mother_name': self.form.mother_name,
            'mother_rrn': self.form.mother_rrn,
            'address': self.form.address
          }).then(function (response) {
            let data = response.data
            self.$router.go(-1)
          })
        }
      } else if (self.action === 'new_student') {
        self.$axios.post('student_infos', {
          'username': self.form.username,
          'password': self.form.password,
          'name': self.form.name,
          'email': self.form.email,
          'phone': self.form.phone,
          'school': self.form.school,
          'church': self.form.church,
          'birthday': (new Date(self.form.birthday)).toISOString().substr(0, 10),
          'student_id': self.form.student_id,
          'gender': self.form.gender,
          'rrn': self.form.rrn,
          'father_name': self.form.father_name,
          'father_rrn': self.form.father_rrn,
          'mother_name': self.form.mother_name,
          'mother_rrn': self.form.mother_rrn,
          'address': self.form.address
        }).then(function (response) {
          let data = response.data
          self.$router.go(-1)
        })
      } else if (self.action === 'update') {
        if (self.is_howcs_student === false) {
          self.$axios.put('users/' + self.user_id, {
            'username': self.form.username,
            'password': self.form.password,
            'name': self.form.name,
            'email': self.form.email,
            'phone': self.form.phone,
            'school': self.form.school,
            'church': self.form.church,
            'birthday': (new Date(self.form.birthday)).toISOString().substr(0, 10)
          }).then(function (response) {
            let data = response.data
            self.$router.go(-1)
          })
        } else {
          self.$axios.put('student_infos/' + self.user_id, {
            'username': self.form.username,
            'password': self.form.password,
            'name': self.form.name,
            'email': self.form.email,
            'phone': self.form.phone,
            'school': self.form.school,
            'church': self.form.church,
            'birthday': (new Date(self.form.birthday)).toISOString().substr(0, 10),
            'student_id': self.form.student_id,
            'gender': self.form.gender,
            'rrn': self.form.rrn,
            'father_name': self.form.father_name,
            'father_rrn': self.form.father_rrn,
            'mother_name': self.form.mother_name,
            'mother_rrn': self.form.mother_rrn,
            'address': self.form.address
          }).then(function (response) {
            let data = response.data
            self.$router.go(-1)
          })
        }
        if (self.is_agit_teacher === true) {
          if (self.is_admin === true) {
            self.$axios.put('agit_teacher_infos/' + self.agit_teacher_info_id, {
              'approval': self.form.agit_teacher_approval,
              'career': self.form.career,
            }).then(function (response) {
            })
          } else {
            self.$axios.put('agit_teacher_infos/' + self.agit_teacher_info_id, {
              'career': self.form.career,
            }).then(function (response) {
            })
          }
        }
      }
    },
    convert_student: function () {
      this.is_howcs_student = true
    },
    remove: function () {
      var self = this
      self.$axios.delete('student_infos/' + self.user_id)
        .then(function (response) {
          let data = response.data
          self.$router.go(-1)
        })
    }
  },
  created: function () {
    let loggedIn = LocalStorage.has('user_')
    if (this.action === 'update') {
      if (this.id) {
        this.is_admin = true
        this.user_id = this.id
      } else if (loggedIn) {
        this.user = LocalStorage.get.item('user_')
        this.user_id = this.user['id']
      }
      var self = this
      self.$axios.get('users/' + self.user_id
      ).then(function (response) {
        let data = response.data
        self.form.username = data.username
        self.form.name = data.name
        self.form.email = data.email
        self.form.phone = data.phone
        self.form.school = data.school
        self.form.church = data.church
        var d = new Date(data.birthday)
        self.form.birthday = d.toISOString().substr(0, 10)
        if (data.hasOwnProperty('student_info')) {
          self.is_howcs_student = true
          self.form.student_id = data.student_info.student_id
          self.form.gender = data.student_info.gender
          self.form.rrn = data.student_info.rrn
          self.form.father_name = data.student_info.father_name
          self.form.father_rrn = data.student_info.father_rrn
          self.form.mother_name = data.student_info.mother_name
          self.form.mother_rrn = data.student_info.mother_rrn
          self.form.address = data.student_info.address
        }
        if (data.hasOwnProperty('agit_teacher_info')) {
          self.is_agit_teacher = true
          self.agit_teacher_info_id = data.agit_teacher_info.id
          self.form.career = data.agit_teacher_info.career
          self.form.agit_teacher_approval = data.agit_teacher_info.approval
        }
      })
    } else if (this.action === 'new_student') {
      this.is_howcs_student = true
    }
  }
}
</script>
