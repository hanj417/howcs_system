<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout justify-center align-center>
        <v-card>
          <v-data-table :headers='columns' :items='items' :total-items="pagination.totalItems" hide-actions :pagination.sync="pagination" :loading="loading">
            <template slot='items' scope='props'>
              <tr>
                <td v-for='column in columns' v-html="get_column_data(props.item, column)"></td>
                <td width='160'>
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
    <v-btn
      fab
      bottom
      right
      color="pink"
      dark
      fixed
      @click="search_dialog = true"
    >
      <v-icon>add</v-icon>
    </v-btn>
      <v-dialog v-model="search_dialog" width="50%">
        <v-card>
          <v-card-title class="title">학생 검색</v-card-title>
          <v-card-text class="pt-4">
            <v-form>
              <v-text-field name="search_name" label="이름" v-model="search_name" type="text"></v-text-field>
              <v-btn @click.stop='search'>검색</v-btn>
            </v-form>
            <v-data-table :headers='search_columns' :items='search_items' :loading="loading">
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
  </v-content>
</template>

<script>
const get_default_data = () => {
  return {
    loading: false,
    columns: [
      {
        'text': 'Name',
        'value': 'student.name'
      },
      {
        'text': 'Email',
        'value': 'student.email'
      },
      {
        'text': 'Phone',
        'value': 'student.phone'
      },
      {
        'text': 'School',
        'value': 'student.school'
      },
      {
        'text': 'Birthday',
        'value': 'student.birthday'
      },
    ],
    pagination: {
      page: 1,
      rowsPerPage: 10,
      sortBy: 'id',
      descending: true,
      totalItems: 0
    },
    items: [],
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
    remove(item) {
      this.$http.delete(`enrollments/` + item.class_id + `/` + item.student_id)
      .then(({ data }) => {
        this.fetch_data()
      })
    },
    next() {
      this.pagination.page++
    },
    search() {
      //this.$route.query.query = JSON.stringify(this.filters.model)
      this.$http.get(`users`, {params: {name: this.search_name}}).then(({ data }) => {
        this.search_items = data.data
      })
    },
    search_select(item) {
      this.$http.post(`enrollments`, {
        'class_id': this.$route.params.id,
        'student_id': item.id,
      }).then(({data}) => {
        this.$router.replace('/')
      })
    }
  },
  created () {
    this.fetch_data()
  }
}
</script>
