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
                placeholder="선생님"
                v-model="teacher.name"
                :rules="nameRules"
                :disabled="teacher_input_disabled"
                required
              ></v-text-field>
              <v-btn @click="search_dialog = true">
                <v-icon>add</v-icon>
              </v-btn>
            </v-layout>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="학급명"
              v-model="title"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-select
              :items="major_categories"
              v-model="major_category"
              label="대분류"
              single-line
              bottom
            ></v-select>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="분류"
              v-model="minor_category"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="해당년도"
              v-model="year"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="학기"
              v-model="semester"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="수업시간"
              v-model="time_slot"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="대상"
              v-model="audience"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="배경"
              v-model="background"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="내용"
              v-model="content"
            ></v-text-field>
          </v-flex>
        </v-layout>
      </v-form>
      <v-dialog v-model="search_dialog" width="50%">
        <v-card>
          <v-card-title class="title">학생 검색</v-card-title>
          <v-spacer></v-spacer>
          <v-text-field
            append-icon="search"
            label="Search"
            single-line
            hide-details
            v-model="search"
          ></v-text-field>
          <v-card-text class="pt-4">
            <v-data-table :headers='search_columns' :items='search_items' :total-items="pagination.totalItems" hide-actions :pagination.sync="pagination" :loading="loading" :search="search">
              <template slot='items' scope='props'>
                <tr>
                  <td v-for='column in search_columns' v-html="get_column_data(props.item, column)"></td>
                  <td width='160'>
                    <v-btn fab small @click="search_select(props.item)">
                      <v-icon>edit</v-icon>
                    </v-btn>
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
export default {
  data () {
    return {
      save_btn_text: '등록',
      valid: true,
      teacher: '',
      teacher_input_disabled: true,
      title: '',
      major_categories: [],
      major_category: {},
      minor_category: '',
      year: null,
      semester: '',
      time_slot: '',
      audience: '',
      background: '',
      content: '',
      search: '',
      search_dialog: false,
      search_name: '',
      search_items: [],
      search_columns: [
        {
          'text': 'ID',
          'value': 'username'
        },
        {
          'text': 'Name',
          'value': 'name'
        },
        {
          'text': 'Email',
          'value': 'email'
        },
        {
          'text': 'Phone',
          'value': 'phone'
        },
        {
          'text': 'School',
          'value': 'school'
        },
        {
          'text': 'Church',
          'value': 'church'
        },
        {
          'text': 'Birthday',
          'value': 'birthday'
        },
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
      let sort = this.pagination.sortBy
      if (this.pagination.descending) {
        sort = '-' + sort
      }
      //this.$route.query.query = JSON.stringify(this.filters.model)
      this.$route.query.sort = sort
      this.$route.query.perPage = this.pagination.rowsPerPage
      this.$route.query.page = this.pagination.page

      this.$http.get(`enrollments`, {params: {class: this.$route.params.id}}).then(({ data }) => {
        this.items = data.data
        this.pagination.totalItems = data.total
      })
    },
    cancel() {
      this.$router.replace('/')
    },
    save() {
      if (this.action == 'new') {
          this.$http.post(`classes`, {
              'teacher_id': this.teacher.id,
              'title': this.title,
              'major_category': this.major_category,
              'minor_category': this.minor_category,
              'year': this.year,
              'semester': this.semester,
              'time_slot': this.time_slot,
              'audience': this.audience,
              'background': this.background,
              'content': this.content,
          }).then(({data}) => {
            this.$router.replace('/')
          })
      } else if (this.action == 'update') {
        if (this.$route.params.hasOwnProperty('id')) {
            this.$http.put(`classes/` + this.$route.params.id, {
              'teacher_id': this.teacher.id,
              'title': this.title,
              'major_category': this.major_category,
              'minor_category': this.minor_category,
              'year': this.year,
              'semester': this.semester,
              'time_slot': this.time_slot,
              'audience': this.audience,
              'background': this.background,
              'content': this.content,
            }).then(({data}) => {
              this.$router.replace('/')
            })
        }
      }
    },
    search() {
      //this.$route.query.query = JSON.stringify(this.filters.model)
      this.$http.get(`users`, {params: {name: this.search_name}}).then(({ data }) => {
        this.search_items = data.data
      })
    },
    search_select(item) {
      this.$http.get(`users/` + item.id
      ).then(({data}) => {
        this.teacher = data
        this.search_dialog = false
      })
    }
  },
  created() {
    this.$http.get(`classes/major_categories`
    ).then(({ data }) => {
      this.major_categories = data
    })
    if (this.$route.params.action == 'update') {
      if (this.$route.params.hasOwnProperty('id')) {
        this.$http.get(`classes/` + this.$route.params.id
        ).then(({ data }) => {
          console.log(data)
          this.teacher = data.teacher
          this.title = data.title
          this.major_category = data.major_category
          this.minor_category = data.minor_category
          this.year = data.year
          this.semester = data.semester
          this.time_slot = data.time_slot
          this.audience = data.audience
          this.background = data.background
          this.content = data.content
        })
      }
    }
  }
}
</script>
