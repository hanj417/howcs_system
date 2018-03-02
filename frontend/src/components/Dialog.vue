<template>
    <v-dialog v-model="dialog" width="800px">
      <v-card>
        <v-card-title
          class="grey lighten-4 py-4 title"
        >
          회원 가입
        </v-card-title>
        <v-container grid-list-sm class="pa-4">
          <v-layout row wrap>
          <v-form>
            <v-flex xs12 align-center justify-space-between>
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
                type="tel"
                prepend-icon="phone"
                placeholder="전화번호"
                mask="phone"
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
                ref="menu"
                lazy
                :close-on-content-click="false"
                v-model="menu"
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
                @change="save"
                min="1950-01-01"
                :max="new Date().toISOString().substr(0, 10)"
              ></v-date-picker>
              </v-menu>
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
</v-form>
          </v-layout>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat color="primary" @click="dialog = false">Cancel</v-btn>
          <v-btn flat @click="register">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
export default {
  name: 'Dialog',
  props: ['dialog'],
  data () {
    return {
      date: null,
      menu: false,
      valid: true,
      username: '',
      password: '',
      password_confirmation: '',
      name: '',
      email: '',
      phone: '',
      school: '',
      church: '',
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
    menu (val) {
      val && this.$nextTick(() => (this.$refs.picker.activePicker = 'YEAR'))
    }
  },
  methods: {
    cancel() {
        this.dialog = !this.dialog
    },
    register() {
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
        this.dialog = !this.dialog
      })
    },
    save (date) {
      this.$refs.menu.save(date)
    }
  },
}
</script>
