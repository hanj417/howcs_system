<template>
<div>
    <div class="page-intro">
      <img src="~assets/img/login_background_image.png" class="section__background-image" />

      <div class="title--emphasized">
		하우학교에 오신것을 환영합니다!
      </div>
     
    </div>

   <div class="container">
      <div class="page-name">
      회원가입
      </div>
      <hr class="page-name--bottom-border" />
    </div> 

<q-page padding class="row justify-center">
<div style="width: 500px; max-width: 90vw;">
  <q-input v-model="username" float-label="아이디" />
  <q-input v-model="password" type="password" float-label="비밀번호" />
  <q-input v-model="name" float-label="이름" />
  <q-input v-model="email" type="email" float-label="이메일" />
  <q-input v-model="phone" float-label="전화번호" />
  <q-input v-model="church" float-label="출석교회" />
  <q-input v-model="school" float-label="소속학교" />
  <q-datetime v-model="birthday" type="date" float-label="생년월일" />
  <q-input v-model="student_id" float-label="학번" />
  <q-option-group 
    type="radio"
    v-model="gender"
    :options="[
      { label: '남학생', value: 'male' },
      { label: '여학생', value: 'female' },
    ]"
  />
  <q-input v-model="father_name" float-label="부 성명" />
  <q-input v-model="father_rrn" float-label="부 주민등록번호" />
  <q-input v-model="mother_name" float-label="모 성명" />
  <q-input v-model="mother_rrn" float-label="모 주민등록번호 " />
  <q-input v-model="address" float-label="주소" />
  <q-btn @click="store" label="수정" />
</div>
</q-page>
</div>
</template>

<script>
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
      terms_check: false,
    }
  },
  method: {
    store() {
    },
  },
}
</script>
/*
<v-content>
  <v-container fluid fill-height>
   <v-layout justify-center align-center>
  <v-card>
    <v-card-title
      class="grey lighten-4 py-4 title"
    >
      회원 정보
    </v-card-title>
    <v-container grid-list-sm class="pa-4">
      <v-form @submit.prevent="validateForm" lazy-validation>
        <v-layout row wrap>
          <v-flex xs12 align-center>
            <v-layout align-center>
              <v-avatar size="40px" class="mr-3">
                <img
                  src="//ssl.gstatic.com/s2/oz/images/sge/grey_silhouette.png"
                  alt=""
                >
              </v-avatar>
              <v-text-field
                label="아이디"
                v-model="username"
                data-vv-name="username"
                :error-messages="errors.collect('username')"
                v-validate="'required'"
                required
              ></v-text-field>
              <v-btn v-if="is_admin && !is_howcs_student" @click="convert_student">하우학교 학생 전환</v-btn>
            </v-layout>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              label="이름"
              prepend-icon="chat"
              v-model="name"
              data-vv-name="name"
              :error-messages="errors.collect('name')"
              v-validate="'required'"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              type="password"
              prepend-icon="lock"
              label="비밀번호"
              v-model="password"
              name="password"
              :error-messages="errors.collect('password')"
              v-validate="'required'"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              type="password"
              prepend-icon="lock"
              label="비밀번호 확인"
              name="password_confirmation"
              data-vv-as="password"
              :error-messages="errors.collect('password_confirmation')"
              v-validate="'required|confirmed:password'"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              prepend-icon="mail"
              label="이메일"
              v-model="email"
              autocomplete='email'
              data-vv-name="email"
              :error-messages="errors.collect('email')"
              v-validate="'required'"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              prepend-icon="phone"
              label="전화번호"
              v-model="phone"
              autocomplete='tel'
              data-vv-name="phone"
              :error-messages="errors.collect('phone')"
              v-validate="'required'"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              prepend-icon="business"
              label="출석 교회"
              v-model="church"
              data-vv-name="church"
              :error-messages="errors.collect('church')"
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              prepend-icon="business"
              label="소속 학교"
              v-model="school"
              data-vv-name="school"
              :error-messages="errors.collect('school')"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-menu
              ref="date_menu"
              lazy
              :close-on-content-click="false"
              v-model="date_menu"
              transition="scale-transition"
              offset-y
              full-width
              :nudge-right="40"
              min-width="290px"
            >
            <v-text-field
              slot="activator"
              label="Birthday date"
              v-model="date"
              prepend-icon="event"
              readonly
            ></v-text-field>
            <v-date-picker
              ref="picker"
              v-model="date"
              @change="date_save"
              min="1950-01-01"
              :max="new Date().toISOString().substr(0, 10)"
            ></v-date-picker>
            </v-menu>
          </v-flex>

          <v-flex v-if="is_howcs_student" xs12>
            <v-text-field
              label="학번"
              prepend-icon="chat"
              v-model="student_id"
              required
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs6>
            <v-select
              :items="gender_items"
              v-model="gender"
              label="성별"
              single-line
              bottom
            ></v-select>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs6>
            <v-text-field
              prepend-icon="business"
              label="주민등록번호"
              v-model="rrn"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs6>
            <v-text-field
              prepend-icon="business"
              label="아버지 이름"
              v-model="father_name"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs6>
            <v-text-field
              prepend-icon="business"
              label="아버지 주민등록번호"
              v-model="father_rrn"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs6>
            <v-text-field
              prepend-icon="business"
              label="어머니 이름"
              v-model="mother_name"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs6>
            <v-text-field
              prepend-icon="business"
              label="어머니 주민등록번호"
              v-model="mother_rrn"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs12>
            <v-text-field
              prepend-icon="business"
              label="주소"
              v-model="address"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="action == 'new'" xs12>
            <v-checkbox
              color="green"
              v-model="terms_check"
            >
              <div slot="label" @click.stop="">
                <a href="javascript:;" @click.stop="terms = true">개인정보/수집 및 이용 동의</a>
                와
                <a href="javascript:;" @click.stop="conditions = true">회원 약관</a>
                에 동의합니다.
              </div>
            </v-checkbox>
          </v-flex>
          <v-dialog v-model="terms" width="70%">
            <v-card>
              <v-card-title class="title">Terms</v-card-title>
              <v-card-text v-for="n in 5" :key="n">
                {{ content }}
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  flat
                  color="purple"
                  @click="terms = false"
                >Ok</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="conditions" width="70%">
            <v-card>
              <v-card-title class="title">Conditions</v-card-title>
              <v-card-text v-for="n in 5" :key="n">
                {{ content }}
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  flat
                  color="purple"
                  @click="conditions = false"
                >Ok</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-layout>
      </v-form>
    </v-container>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn flat color="primary" @click="cancel">취소</v-btn>
      <v-btn flat @click="save">{{ save_btn_text }}</v-btn>
    </v-card-actions>
  </v-card>
</v-layout>
</v-container>
</v-content>

import Vue from 'vue'
import VeeValidate from 'vee-validate'
Vue.use(VeeValidate)

export default {
  data () {
    return {
      save_btn_text: '등록',
      is_admin: false,
      is_howcs_student: false,
      user_id: '',
      valid: true,
      username: '',
      password: '',
      password_confirmation: '',
      name: '',
      email: '',
      phone: '',
      school: '',
      church: '',
      date: null,
      date_menu: false,
      student_id: '',
      gender: {},
      gender_items: [{ text: '남성', value:'male'}, {text: '여성', value:'female'}],
      rrn: '',
      father_name: '',
      father_rrn: '',
      mother_name: '',
      mother_rrn: '',
      address: '',
      user: {},
      conditions: false,
      content: `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc.`,
      terms: false,
      terms_check: false,
    }
  },
  watch: {
    date_menu (val) {
      val && this.$nextTick(() => (this.$refs.picker.activePicker = 'YEAR'))
    }
  },
  computed: {
    action() {
      return this.$route.params.action
    }, 
    id() {
      return this.$route.params.id
    }
  },
  methods: {
    cancel() {
      this.$router.go(-1)
    },
    save() {
      if (this.action == 'new') {
        if (this.is_howcs_student == false) {
          this.$axios.post(`users`, {
            'username': this.username,
            'password': this.password, 
            'name': this.name,
            'email': this.email,
            'phone': this.phone,
            'school': this.school,
            'church': this.church,
            'birthday': this.date,
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
            'address': this.address,
          }).then(({data}) => {
            this.$router.go(-1)
          })
        }
      } else if (this.action == 'update') {
        if (this.is_howcs_student == false) {
          this.$axios.put(`users/` + this.user_id, {
            'username': this.username,
            'password': this.password, 
            'name': this.name,
            'email': this.email,
            'phone': this.phone,
            'school': this.school,
            'church': this.church,
            'birthday': this.date,
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
            'address': this.address,
          }).then(({data}) => {
            this.$router.go(-1)
          })
        }
      }
    },
    date_save (date) {
      this.$refs.date_menu.save(date)
    },
    convert_student() {
      this.is_howcs_student = true 
    },
    validateForm() {
      this.$validator.validateAll()
        .then(() => {
          console.log("data");
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  created() {
    if (this.$route.params.action == 'update') {
      if (this.$route.params.hasOwnProperty('id')) {
        this.is_admin = true
        this.user_id = this.$route.params.id
      } else if (localStorage['user']) {
        this.user = JSON.parse(localStorage['user'])
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
        this.date = d.toISOString().substr(0,10)
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
    } else if (this.$route.params.action == 'new_student') {
      this.is_howcs_student = true
    }
  }
}
*/
