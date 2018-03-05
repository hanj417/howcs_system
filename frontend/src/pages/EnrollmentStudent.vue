<template>
  <v-content>
    <v-container fluid>
      <v-layout justify-center align-center>
        <v-card>
          <v-data-table :headers='columns' :items='items' :total-items="pagination.totalItems" hide-actions :pagination.sync="pagination" :loading="loading">
            <template slot='items' scope='props'>
              <tr>
                <td v-for='column in columns' v-html="get_column_data(props.item, column)"></td>
                <td width='40'>
                  <v-btn fab small @click="remove(props.item)">
                    <v-icon>delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
          <div class="jc">
            <v-pagination class="ma-3" v-model='pagination.page' :length='totalPages' circle></v-pagination>
          </div>
        </v-card>
      </v-layout>
    </v-container>
    <v-container fluid>
      <v-layout justify-center align-center>
        <v-card>
          <v-data-table :headers='all_columns' :items='all_items' :total-items="pagination.totalItems" hide-actions :pagination.sync="pagination" :loading="loading">
            <template slot='items' scope='props'>
              <tr>
                <td v-for='column in all_columns' v-html="get_column_data(props.item, column)"></td>
                <td width='40'>
                  <v-btn fab small @click="enroll(props.item)">
                    <v-icon>delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
          <div class="jc">
            <v-pagination class="ma-3" v-model='pagination.page' :length='totalPages' circle></v-pagination>
          </div>
        </v-card>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
const get_default_data = () => {
  return {
    loading: false,
    columns: [
      {
        'text': '제목',
        'value': 'class.title'
      },
      {
        'text': '분류',
        'value': 'class.minor_category'
      },
    ],
    all_columns: [
      {
        'text': '제목',
        'value': 'title'
      },
      {
        'text': '분류',
        'value': 'minor_category'
      },
      {
        'text': '선생님',
        'value': 'teacher.name'
      },
    ],
    pagination: {
      page: 1,
      rowsPerPage: 10,
      sortBy: 'id',
      descending: true,
      totalItems: 0
    },
    filters: {},
    items: [],
    all_items: [],
  }
}

export default {
  data: get_default_data,
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
  computed: {
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
      if (!!this.$route.params.id) {
        this.filters = {
          'student_id': this.$route.params.id
        }
      }
      let sort = this.pagination.sortBy
      if (this.pagination.descending) {
        sort = '-' + sort
      }
      this.$route.query.query = JSON.stringify(this.filters)
      this.$route.query.sort = sort
      this.$route.query.perPage = this.pagination.rowsPerPage
      this.$route.query.page = this.pagination.page
      this.$route.query.class = this.$route.params.id

      this.$http.get(`enrollments`, {params: this.$route.query}).then(({ data }) => {
        this.items = data.data
        this.pagination.totalItems = data.total
      })


      this.filters = {
        'major_category': 'agit',
      }
      this.$route.query.query = JSON.stringify(this.filters)
      this.$route.query.sort = sort
      this.$route.query.perPage = this.pagination.rowsPerPage
      this.$route.query.page = this.pagination.page
      this.$route.query.class = this.$route.params.id

      this.$http.get(`classes`, {params: this.$route.query}).then(({ data }) => {
        this.all_items = data.data
        this.pagination.totalItems = data.total
      })
    },
    remove(item) {
      this.$http.delete(`enrollments/` + item.class_id + `/` + item.student_id)
      .then(({ data }) => {
        this.fetch_data()
      })
    },
    enroll(item) {
      this.$http.post(`enrollments`, {
        'class_id': item.id,
        'student_id': this.$route.params.id
      }).then(({ data }) => {
        this.fetch_data()
      })
    },
    next() {
      this.pagination.page++
    },
  },
  created () {
    this.fetch_data()
  }
}
</script>
