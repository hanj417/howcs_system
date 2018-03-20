<template>
<v-content>
  <v-container fluid fill-height>
    <v-layout justify-center align-center>
      <v-card>
        <v-card-title class="grey lighten-4 py-4 title">학급  정보</v-card-title>
        <v-container grid-list-sm class="pa-4">
          <v-form @submit.prevent="validateForm" lazy-validation>
            <v-layout row wrap>
              <v-flex xs12 align-center>
                <v-layout align-center>
                  <v-avatar size="40px" class="mr-3">
                    <img src="//ssl.gstatic.com/s2/oz/images/sge/grey_silhouette.png" alt="">
                  </v-avatar>
                  <v-text-field
                    label="선생님"
                    v-model="teacher.name"
                    data-vv-name="teacher.name"
                    :error-messages="errors.collect('teacher.name')"
                    v-validate="'required'"
                    required
                  ></v-text-field>
                  <v-btn v-if="teacher_select" @click="search"><v-icon>search</v-icon></v-btn>
                </v-layout>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="학급명"
                  v-model="title"
                  data-vv-name="title"
                  :error-messages="errors.collect('title')"
                  v-validate="'required'"
                  required
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-select
                  label="대분류"
                  v-model="major_category"
                  :items="major_categories"
                  single-line
                  bottom
                ></v-select>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="분류"
                  v-model="minor_category"
                  data-vv-name="minor_category"
                  :error-messages="errors.collect('minor_category')"
                  v-validate="'required'"
                  required
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="해당년도"
                  v-model="year"
                  data-vv-name="year"
                  :error-messages="errors.collect('year')"
                  v-validate="'required'"
                  required
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="학기"
                  v-model="semester"
                  data-vv-name="semester"
                  :error-messages="errors.collect('semester')"
                  v-validate="'required'"
                  required
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="수업시간"
                  v-model="time_slot"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="구글 캘린더 ID"
                  v-model="google_calendar"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="대상"
                  v-model="audience"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="배경"
                  v-model="background"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="내용"
                  v-model="content"
                ></v-text-field>
              </v-flex>
            </v-layout>
          </v-form>
          <v-dialog v-model="search_dialog" width="60%">
            <v-card>
              <v-card-title class="title">교사 검색</v-card-title>
              <v-flex xs6 offset-xs1>
                <v-text-field label="검색" single-line hide-details v-model="search_name"></v-text-field>
              </v-flex>
              <v-card-text class="pt-4">
                <v-data-table :headers='search_columns' :items='search_items' :search="search_name">
                  <template slot='items' scope='props'>
                    <tr>
                      <td v-for='column in search_columns' v-html="get_column_data(props.item, column)"></td>
                      <td class="justify-center layout px-0">
                        <v-btn small icon class="mx-0" @click="search_select(props.item)"><v-icon>add</v-icon></v-btn>
                      </td>
                    </tr>
                  </template>
                </v-data-table>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  flat
                  color="purple"
                  @click="search_dialog = false"
                >취소</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
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
      teacher_select: false,
      teacher: '',
      title: '',
      major_categories: [],
      major_category: {},
      minor_category: '',
      year: null,
      semester: '',
      time_slot: '',
      google_calendar: '',
      audience: '',
      background: '',
      content: '',
      save_btn_text: '등록',

      search_dialog: false,
      search_name: '',
      search_items: [],
      filters: {},
      search_columns: [
        {'text': '아이디', 'value': 'username'},
        {'text': '이름', 'value': 'name'},
        {'text': '이메일', 'value': 'email'},
        {'text': '전화번호', 'value': 'phone'},
      ],
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
  watch: {
    'id' (val) {
      this.set_visibility()
      this.fetch_data()
    }
  },
  methods: {
    get_column_data(row, field) {
      // process fields like `type.name`
      let [l1, l2] = field.value.split('.')
      let value = row[l1]
      let tag = null
      if (l2) {
        value = row[l1] ? row[l1][l2] : null
      }
      if (field.type === 'image') {
        tag = 'img'
      }
      if (tag) {
        value = `<${tag} src="${value}" class="crud-grid-thumb" controls />`
      }
      return value
    },
    fetch_data() {
      this.filters = {}
      this.$route.query.query = JSON.stringify(this.filters)
      this.$axios.get(`enrollments`, {params: {class: this.$route.params.id}}).then(({ data }) => {
        this.items = data
      })
    },
    cancel() {
      this.$router.go(-1)
    },
    save() {
      if (this.action == 'new') {
          this.$axios.post(`classes`, {
              'teacher_id': this.teacher.id,
              'title': this.title,
              'major_category': this.major_category,
              'minor_category': this.minor_category,
              'year': this.year,
              'semester': this.semester,
              'time_slot': this.time_slot,
              'google_calendar': this.google_calendar,
              'audience': this.audience,
              'background': this.background,
              'content': this.content,
          }).then(({data}) => {
            this.$router.go(-1)
          })
      } else if (this.action == 'update') {
        if (this.$route.params.hasOwnProperty('id')) {
            this.$axios.put(`classes/` + this.$route.params.id, {
              'teacher_id': this.teacher.id,
              'title': this.title,
              'major_category': this.major_category,
              'minor_category': this.minor_category,
              'year': this.year,
              'semester': this.semester,
              'time_slot': this.time_slot,
              'google_calendar': this.google_calendar,
              'audience': this.audience,
              'background': this.background,
              'content': this.content,
            }).then(({data}) => {
              this.$router.go(-1)
            })
        }
      }
    },
    search() {
      this.filters = {
        'role': 'howcs_teacher',
      }
      this.$route.query.query = JSON.stringify(this.filters)
      this.$axios.get(`users`, {params: this.$route.query}).then(({ data }) => {
        this.search_items = data
      })
      this.search_dialog = true
    },
    search_select(item) {
      this.$axios.get(`users/` + item.id
      ).then(({data}) => {
        this.teacher = data
        this.search_dialog = false
      })
    }
  },
  created() {
    var user = JSON.parse(localStorage['user'])
    if (JSON.parse(user.role).includes('admin')) {
      this.teacher_select = true
    } else {
      this.teacher = user
    }

    this.major_category = this.$route.params.major_category
    this.$axios.get(`classes/major_categories`
    ).then(({ data }) => {
      this.major_categories = data
    })

    if (this.$route.params.action == 'update') {
      this.$axios.get(`classes/` + this.$route.params.id
      ).then(({ data }) => {
        console.log(data)
        this.teacher = data.teacher
        this.teacher_select = false
        this.title = data.title
        this.major_category = data.major_category
        this.minor_category = data.minor_category
        this.year = data.year
        this.semester = data.semester
        this.time_slot = data.time_slot
        this.google_calendar = data.google_calendar
        this.audience = data.audience
        this.background = data.background
        this.content = data.content
      })
    }
  }
}
</script>
