<template>
<v-content>
  <v-container fluid fill-height>
   <v-layout justify-center align-center>
  <v-card>
    <v-card-title
      class="grey lighten-4 py-4 title"
    >
      회원 가입
    </v-card-title>
    <v-container grid-list-sm class="pa-4">
      <form @submit.prevent="validateForm">
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
                v-model="form.username"
                :rules="rules.name"
                v-validate="'required'"
              ></v-text-field>
            </v-layout>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              label="이름"
              :rules="rules.name"
              v-model="name"
              v-validate="'required'"
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              type="password"
              label="비밀번호"
              v-model="form.password"
              min="4"
              counter
              hint="4글자 이상"
              autocomplete='on'
              v-validate="'required'"
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              type="password"
              label="비밀번호 확인"
              v-model="form.password_confirmation"
              min="4"
              counter
              autocomplete='on'
              v-validate="'required'"
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              label="이메일"
              :rules="rules.email"
              v-model="form.email"
              autocomplete='email'
              v-validate="'required'"
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              type="tel"
              label="전화번호"
              mask="phone"
              v-model="form.phone"
              autocomplete='tel'
              v-validate="'required'"
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              label="출석 교회"
              v-model="form.church"
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              label="소속 학교"
              v-model="form.school"
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
              label="생년월일"
              v-model="form.date"
              readonly
            ></v-text-field>
            <v-date-picker
              ref="picker"
              v-model="form.date"
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
              v-validate="'required'"
            >
              <div slot="label" @click.stop="">
                <a href="javascript:;" @click.stop="terms = true">terms</a>
                와 
                <a href="javascript:;" @click.stop="conditions = true">conditions?</a>
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
      <v-btn flat color="primary" @click="cancel">Cancel</v-btn>
      <v-btn flat @click="register">Save</v-btn>
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
      form: {
        username: '',
        password: '',
        password_confirmation: '',
        name: '',
        email: '',
        phone: '',
        school: '',
        church: '',
        date: null,
      },
      rules: {
        username: [],
        password: [],
        name: [],
        email: [],
        phone: [],
        school: [],
        church: [],
        date: [],
      },
      menu: false,
      conditions: false,
      content: `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc.`,
      terms: false,
      terms_check: false,
    }
  },
  watch: {
    menu (val) {
      val && this.$nextTick(() => (this.$refs.picker.activePicker = 'YEAR'))
    },
    errors: {
      handler: function(val, oldVal) {
        _.forEach(this.rules, (val, key) => {
          this.rules[key] = [() => (this.errors.has(key) ? this.errors.first(key) : true)];
        });
      },
      deep: true
    },
  },
  methods: {
    cancel() {
      this.$router.replace('/')
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
        this.$router.replace('/')
      })
    },
    save (date) {
      this.$refs.menu.save(date)
    },
    validateForm() {
      this.$validator.validateAll()
        .then(() => {
          console.log("data", this.form);
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
}
</script>
