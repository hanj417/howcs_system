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
      <v-form v-model="valid" ref="form" lazy-validation>
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
                placeholder="아이디"
                v-model="username"
                :rules="nameRules"
                required
              ></v-text-field>
              <v-btn @click="convert_student">
                <v-icon>add</v-icon>
              </v-btn>
            </v-layout>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="이름"
              prepend-icon="chat"
              :rules="nameRules"
              v-model="name"
              required
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs12>
            <v-text-field
              placeholder="학번"
              prepend-icon="chat"
              v-model="student_id"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              type="password"
              prepend-icon="lock"
              placeholder="비밀번호"
              v-model="password"
              min="4"
              counter
              hint="4글자 이상"
              autocomplete='on'
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              type="password"
              prepend-icon="lock"
              placeholder="비밀번호 확인"
              v-model="password_confirmation"
              min="4"
              counter
              autocomplete='on'
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              prepend-icon="mail"
              placeholder="이메일"
              :rules="emailRules"
              v-model="email"
              autocomplete='email'
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              prepend-icon="phone"
              placeholder="전화번호"
              v-model="phone"
              autocomplete='tel'
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              prepend-icon="business"
              placeholder="출석 교회"
              v-model="church"
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              prepend-icon="business"
              placeholder="소속 학교"
              v-model="school"
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
              placeholder="주민등록번호"
              v-model="ssn"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs6>
            <v-text-field
              prepend-icon="business"
              placeholder="아버지 이름"
              v-model="father_name"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs6>
            <v-text-field
              prepend-icon="business"
              placeholder="아버지 주민등록번호"
              v-model="father_ssn"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs6>
            <v-text-field
              prepend-icon="business"
              placeholder="어머니 이름"
              v-model="mother_name"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs6>
            <v-text-field
              prepend-icon="business"
              placeholder="어머니 주민등록번호"
              v-model="mother_ssn"
            ></v-text-field>
          </v-flex>
          <v-flex v-if="is_howcs_student" xs12>
            <v-text-field
              prepend-icon="business"
              placeholder="주소"
              v-model="address"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-checkbox
              color="green"
              v-model="terms_check"
            >
              <div slot="label" @click.stop="">
                Do you accept the
                <a href="javascript:;" @click.stop="terms = true">terms</a>
                and
                <a href="javascript:;" @click.stop="conditions = true">conditions?</a>
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
export default {
  data () {
    return {
      save_btn_text: '등록',
      is_howcs_student: false,
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
      nameRules: [
        v => v.length > 0 || 'Name is required',
      ],
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
      ],
      passwordRules: [
        v => !!v || 'Password is required',
      ],
      passwordConfirmRules: [
        v => !!v || 'Password is required',
        v => this.password_confirmation == this.password || "Does not match"
      ],
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
        } 
/*
        else {
          this.$http.post(`students/update`, {
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
*/
      } else if (this.action == 'update') {
        if (this.$route.params.hasOwnProperty('id')) {
          if (this.is_howcs_student == false) {
            this.$http.put(`users/` + this.$route.params.id, {
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
          }
        } else {
          if (localStorage['user']) {
            this.user = JSON.parse(localStorage['user'])
            if (this.is_howcs_student == false) {
              this.$http.put(`users/` + this.user['id'], {
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
            }
          }
        }
/*
        } else {
          this.$http.post(`students/update/` + this.id, {
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
*/
      }
    },
    date_save (date) {
      this.$refs.date_menu.save(date)
    },
/*
    convert_student() {
      this.is_howcs_student = true 
    }
*/
  },
  created() {
    if (this.$route.params.action == 'update') {
      if (this.$route.params.hasOwnProperty('id')) {
        this.$http.get(`users/` + this.$route.params.id
        ).then(({ data }) => {
          console.log(data)
          this.username = data.username
          this.name = data.name
          this.email = data.email
          this.phone = data.phone
          this.school = data.school
          this.church = data.church
          this.date = data.birthday
        })
      } else {
        if (localStorage['user']) {
          this.user = JSON.parse(localStorage['user'])
          this.$http.get(`users/` + this.user['id']
          ).then(({ data }) => {
            console.log(data)
            this.username = data.username
            this.name = data.name
            this.email = data.email
            this.phone = data.phone
            this.school = data.school
            this.church = data.church
            this.date = data.birthday
          })
        }
      }
    }
  }
}
</script>
