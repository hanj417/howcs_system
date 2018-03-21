<template>
  <v-content>
    <v-container
      fluid
      fill-height>
      <v-layout
        justify-center
        align-center>
        <v-card>
          <v-card-title
            class="grey lighten-4 py-4 title"
          >
            회원 정보
          </v-card-title>
          <v-container
            grid-list-sm
            class="pa-4">
            <v-form
              v-model="valid"
              ref="form"
              lazy-validation>
              <v-layout
                row
                wrap>
                <v-flex
                  xs12
                  align-center>
                  <v-layout align-center>
                    <v-avatar
                      size="40px"
                      class="mr-3">
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
                      :disabled="is_view"
                    />
                  </v-layout>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    placeholder="이름"
                    prepend-icon="chat"
                    :rules="nameRules"
                    v-model="name"
                    :disabled="is_view"
                    required
                  />
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    placeholder="학번"
                    prepend-icon="chat"
                    v-model="student_id"
                    :disabled="is_view"
                    required
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    type="password"
                    prepend-icon="lock"
                    placeholder="비밀번호"
                    v-model="password"
                    :disabled="is_view"
                    min="4"
                    counter
                    hint="4글자 이상"
                    autocomplete='on'
                    required
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    type="password"
                    prepend-icon="lock"
                    placeholder="비밀번호 확인"
                    v-model="password_confirmation"
                    :disabled="is_view"
                    min="4"
                    counter
                    autocomplete='on'
                    required
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    prepend-icon="mail"
                    placeholder="이메일"
                    :rules="emailRules"
                    v-model="email"
                    :disabled="is_view"
                    autocomplete='email'
                    required
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    prepend-icon="phone"
                    placeholder="전화번호"
                    v-model="phone"
                    :disabled="is_view"
                    autocomplete='tel'
                    required
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    prepend-icon="business"
                    placeholder="출석 교회"
                    v-model="church"
                    :disabled="is_view"
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    prepend-icon="business"
                    placeholder="소속 학교"
                    v-model="school"
                    :disabled="is_view"
                  />
                </v-flex>
                <v-flex xs12>
                  <v-menu
                    ref="date_menu"
                    lazy
                    :close-on-content-click="false"
                    v-model="date_menu"
                    :disabled="is_view"
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
                      :disabled="is_view"
                      prepend-icon="event"
                      readonly
                    />
                    <v-date-picker
                      ref="picker"
                      v-model="date"
                      @change="date_save"
                      min="1950-01-01"
                      :max="new Date().toISOString().substr(0, 10)"
                    />
                  </v-menu>
                </v-flex>

                <v-flex xs6>
                  <v-select
                    :items="gender_items"
                    v-model="gender"
                    :disabled="is_view"
                    label="성별"
                    single-line
                    bottom
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    prepend-icon="business"
                    placeholder="주민등록번호"
                    v-model="ssn"
                    :disabled="is_view"
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    prepend-icon="business"
                    placeholder="아버지 이름"
                    v-model="father_name"
                    :disabled="is_view"
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    prepend-icon="business"
                    placeholder="아버지 주민등록번호"
                    v-model="father_ssn"
                    :disabled="is_view"
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    prepend-icon="business"
                    placeholder="어머니 이름"
                    v-model="mother_name"
                    :disabled="is_view"
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    prepend-icon="business"
                    placeholder="어머니 주민등록번호"
                    v-model="mother_ssn"
                    :disabled="is_view"
                  />
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    prepend-icon="business"
                    placeholder="주소"
                    v-model="address"
                    :disabled="is_view"
                  />
                </v-flex>
              </v-layout>
            </v-form>
          </v-container>
          <v-card-actions v-if="!is_view">
            <v-spacer/>
            <v-btn
              flat
              color="primary"
              @click="cancel">취소</v-btn>
            <v-btn
              flat
              @click="save">{{ save_btn_text }}</v-btn>
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
      is_admin: false,
      is_view: false,
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
      gender_items: [{text: '남성', value: 'male'}, {text: '여성', value: 'female'}],
      ssn: '',
      father_name: '',
      father_ssn: '',
      mother_name: '',
      mother_ssn: '',
      address: '',
      user: {},
      nameRules: [
        v => v.length > 0 || 'Name is required'
      ],
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
      ],
      passwordRules: [
        v => !!v || 'Password is required'
      ],
      passwordConfirmRules: [
        v => !!v || 'Password is required',
        v => this.password_confirmation === this.password || 'Does not match'
      ]
    }
  },
  watch: {
    date_menu (val) {
      val && this.$nextTick(() => (this.$refs.picker.activePicker = 'YEAR'))
    }
  },
  computed: {
    action () {
      return this.$route.params.action
    },
    id () {
      return this.$route.params.id
    }
  },
  methods: {
    cancel () {
      this.$router.go(-1)
    },
    save () {
      if (this.action === 'update') {
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
          'ssn': this.ssn,
          'father_name': this.father_name,
          'father_ssn': this.father_ssn,
          'mother_name': this.mother_name,
          'mother_ssn': this.mother_ssn,
          'address': this.address
        }).then(({data}) => {
          this.$router.go(-1)
        })
      }
    },
    date_save (date) {
      this.$refs.date_menu.save(date)
    }
  },
  created () {
    if (this.$route.params.action === 'update') {
      this.user_id = this.$route.params.id
      this.$axios.get(`students/` + this.user_id
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
        this.student_id = data.student_info.student_id
        this.gender = data.student_info.gender
        this.ssn = data.student_info.ssn
        this.father_name = data.student_info.father_name
        this.father_ssn = data.student_info.father_ssn
        this.mother_name = data.student_info.mother_name
        this.mother_ssn = data.student_info.mother_ssn
        this.address = data.student_info.address
      })
    }
  }
}
</script>
