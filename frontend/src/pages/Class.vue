<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout justify-center align-center>
        <v-card>
          <v-data-table :headers='headers' :items='items' :total-items="pagination.totalItems" hide-actions :pagination.sync="pagination" :loading="loading">
            <template slot='items' scope='props'>
              <tr>
                <td v-for='column in columns' v-html="get_column_data(props.item, column)"></td>
                <td class="justify-center layout px-0">
                  <v-btn v-if='attendance_visible' small :to="{name: 'post_class', params: {class_id:props.item.id}} " class="mx-0">글</v-btn>
                  <v-btn v-if='attendance_visible' small :to="{name: 'attendance_class', params: {id:props.item.id}} " class="mx-0">출석</v-btn>
                  <v-btn v-if='enrollment_visible' small :to="{name: 'enrollment_class', params: {id:props.item.id}} " class="mx-0">수강생</v-btn>
                  <v-btn v-if='edit_visible' small :to="{name: 'class_form_edit', params: {action:'update', id:props.item.id}} " class="mx-0">수정</v-btn>
                  <v-btn v-if='delete_visible' small @click="remove(props.item)" class="mx-0">삭제</v-btn>
                  <v-btn v-if='enroll_visible' small @click="enroll(props.item)" class="mx-0">신청</v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
          <div class="jc">
            <v-pagination class="ma-3" v-model='pagination.page' :length='pagination.totalPages' circle></v-pagination>
          </div>
        </v-card>
      </v-layout>
    </v-container>
    <v-btn
      fab
      bottom
      right
      color="pink"
      dark
      fixed
      :to="{name: 'class_form_new', params: {major_category: major_category, action:'new'}}"
    >
      <v-icon>add</v-icon>
    </v-btn>
  </v-content>
</template>

<script>
const get_default_data = () => {
  return {
    loading: false,
    columns: [
      {
        'text': '선생님',
        'value': 'teacher.name'
      },
      {
        'text': '제목',
        'value': 'title'
      },
      {
        'text': '대분류',
        'value': 'major_category'
      },
      {
        'text': '분류',
        'value': 'minor_category'
      },
    ],
    headers: [
      {'text': '선생님'},
      {'text': '제목'},
      {'text': '대분류'},
      {'text': '분류'},
      {'text': ''},
    ],
    agit_columns: [
      {
        'text': '선생님',
        'value': 'teacher.name'
      },
      {
        'text': '제목',
        'value': 'title'
      },
      {
        'text': '분류',
        'value': 'minor_category'
      },
      {
        'text': '대상',
        'value': 'audience'
      },
    ],
    agit_headers: [
      {'text': '선생님'},
      {'text': '제목'},
      {'text': '분류'},
      {'text': '대상'},
      {'text': ''},
    ],
    pagination: {
      page: 1,
      rowsPerPage: 10,
      sortBy: 'id',
      descending: true,
      totalItems: 0,
      totalPages: 1
    },
    items: [],
    filters: {},
    attendance_visible: false,
    enrollment_visible: false,
    edit_visible: false,
    delete_visible: false,
    enroll_visible: false,
  }
}

export default {
  data: get_default_data,
  computed: {
    major_category() {
      return this.$route.params.major_category
    }, 
    id() {
      return this.$route.params.id
    }, 
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
      let sort = this.pagination.sortBy
      if (this.pagination.descending) {
        sort = '-' + sort
      }
      this.$route.query.query = JSON.stringify(this.filters)
      this.$route.query.sort = sort
      this.$route.query.perPage = this.pagination.rowsPerPage
      this.$route.query.page = this.pagination.page

      this.$http.get(`classes`, {params: this.$route.query}).then(({ data }) => {
        this.items = data.data
        this.pagination.totalItems = data.total
        this.pagination.totalPages = data.lastPage
      })
    },
    remove(item) {
      this.$http.delete(`classes/` + item.id)
      .then(({ data }) => {
        this.fetch_data()
      })
    },
    enroll(item) {
      this.$http.post(`enrollments`, {
        'class_id': item.id,
      }).then(({ data }) => {
        this.fetch_data()
      })
    },
    next() {
      this.pagination.page++
    },
    set_visibility() {
      this.major_category = this.$route.params.major_category
      this.filters['major_category'] = this.major_category
      if (!!this.$route.params.id) {
        this.filters['teacher_id'] = this.$route.params.id
        this.post_visible = true
        this.attendance_visible = true
        this.enrollment_visible = true
        this.edit_visible = true
        this.delete_visible = true
        this.enroll_visible = false
      } else {
        if (this.major_category == 'agit') {
          this.columns = this.agit_columns
          this.headers = this.agit_headers
          this.post_visible = false
          this.attendance_visible = false
          this.enrollment_visible = false
          this.edit_visible = false
          this.delete_visible = false
          this.enroll_visible = true
        } else if (this.major_category == 'howcs') {
          this.post_visible = false
          this.attendance_visible = false
          this.enrollment_visible = true
          this.edit_visible = true
          this.delete_visible = true
          this.enroll_visible = false
        }
      }
    }
  },
  created () {
    this.set_visibility()
    this.fetch_data()
  }
}
</script>
