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
                label="이름"
                v-model="user.name"
                :rules="nameRules"
                :disabled="name_input_disabled"
                required
              ></v-text-field>
              <v-btn @click="search_dialog = true">
                <v-icon>add</v-icon>
              </v-btn>
            </v-layout>
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
              label="해당년도"
              v-model="year"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              label="학기"
              v-model="semester"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              label="금액"
              v-model="cost"
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
        </v-layout>
      </v-form>
      <v-dialog v-model="search_dialog" width="50%">
        <v-card>
          <v-card-title class="title">학생 검색</v-card-title>
          <v-flex xs6>
          <v-text-field
            label="이름"
            single-line
            hide-details
            v-model="search_name"
          ></v-text-field>
          </v-flex>
          <v-spacer></v-spacer>
          <v-btn @click="search">검색</v-btn>
          <v-card-text class="pt-4">
            <v-data-table :headers='search_columns' :items='search_items' :total-items="pagination.totalItems" rows-per-page-items="[10, 20, {"text":"All", "value":-1}]" :pagination.sync="pagination" :loading="loading">
              <template slot='items' scope='props'>
                <tr>
                  <td v-for='column in search_columns' v-html="get_column_data(props.item, column)"></td>
                  <td width='160'>
                    <v-btn fab small @click="search_select(props.item)">선택</v-btn>
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
      filters: {},
      user: '',
      user_id: '',
      user_input_disabled: true,
      title: '',
      major_categories: [],
      major_category: {},
      year: null,
      semester: '',
      cost: '',
      date: null,
      pagination: {
        page: 1,
        rowsPerPage: 10,
        sortBy: 'id',
        descending: true,
        totalItems: 0
      },
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
  watch: {
    'pagination.page' (val) {
      this.fetch_data()
    },
    'pagination.sortBy' (val) {
      this.fetch_data()
    },
    'pagination.descending' (val) {
      this.fetch_data()
    },
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
      this.$route.query.query = JSON.stringify(this.filters)
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
        this.$http.post(`payments`, {
            'user_id': this.user_id,
            'major_category': this.major_category,
            'year': this.year,
            'semester': this.semester,
            'cost': this.cost,
            'date': this.date,
        }).then(({data}) => {
          this.$router.replace('/')
        })
      } else if (this.action == 'update') {
        this.$http.put(`payments/` + this.$route.params.id, {
            'user_id': this.user_id,
            'major_category': this.major_category,
            'year': this.year,
            'semester': this.semester,
            'cost': this.cost,
            'date': this.date,
        }).then(({data}) => {
          this.$router.replace('/')
        })
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
        this.user = data
        this.user_id = data.id
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
      this.$http.get(`payments/` + this.$route.params.id
      ).then(({ data }) => {
        console.log(data)
        this.major_category = data.major_category
        this.year = data.year
        this.semester = data.semester
        this.cost = data.cost
        this.date = data.date
      })
    }
  }
}
</script>
