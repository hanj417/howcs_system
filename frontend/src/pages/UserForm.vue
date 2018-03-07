<template>
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
              v-model="ssn"
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
              v-model="father_ssn"
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
              v-model="mother_ssn"
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
</template>

<script>
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
      ssn: '',
      father_name: '',
      father_ssn: '',
      mother_name: '',
      mother_ssn: '',
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
      this.$router.replace('/')
    },
    save() {
      if (this.action == 'new') {
        if (this.is_howcs_student == false) {
          this.$http.post(`users`, {
            'username': this.username,
            'password': this.password, 
            'name': this.name,
            'email': this.email,
            'phone': this.phone,
            'school': this.school,
            'church': this.church,
            'birthday': this.date,
          }).then(({data}) => {
            this.$router.replace('/')
          })
        } else {
          this.$http.post(`student_infos`, {
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
            'ssn': this.ssn,
            'father_name': this.father_name,
            'father_ssn': this.father_ssn,
            'mother_name': this.mother_name,
            'mother_ssn': this.mother_ssn,
            'address': this.address,
          }).then(({data}) => {
            this.$router.replace('/')
          })
        }
      } else if (this.action == 'update') {
        if (this.is_howcs_student == false) {
          this.$http.put(`users/` + this.user_id, {
            'username': this.username,
            'password': this.password, 
            'name': this.name,
            'email': this.email,
            'phone': this.phone,
            'school': this.school,
            'church': this.church,
            'birthday': this.date,
          }).then(({data}) => {
            this.$router.replace('/')
          })
        } else {
          this.$http.put(`student_infos/` + this.user_id, {
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
            'ssn': this.ssn,
            'father_name': this.father_name,
            'father_ssn': this.father_ssn,
            'mother_name': this.mother_name,
            'mother_ssn': this.mother_ssn,
            'address': this.address,
          }).then(({data}) => {
            this.$router.replace('/')
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
      this.$http.get(`users/` + this.user_id
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
          this.ssn = data.student_info.ssn
          this.father_name = data.student_info.father_name
          this.father_ssn = data.student_info.father_ssn
          this.mother_name = data.student_info.mother_name
          this.mother_ssn = data.student_info.mother_ssn
          this.address = data.student_info.address
        }
      })
    } else if (this.$route.params.action == 'new_student') {
      this.is_howcs_student = true
    }
  }
}
</script>
