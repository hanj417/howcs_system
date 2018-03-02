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
                  <v-btn fab small :to="{name: 'post_form', params: {action:'update', id:props.item.id}}">
                    <v-icon>edit</v-icon>
                  </v-btn>
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
    :to="{name: 'post_form', params: {action:'new'}}"
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
        'text': '대분류',
        'value': 'major_category'
      },
      {
        'text': '분류',
        'value': 'minor_category'
      },
      {
        'text': '제목',
        'value': 'title'
      },
    ],
    actions: {},
    options: {
      sort: 'id',
      create: false,
      update: true,
      delete: false
    },
    pagination: {
      page: 1,
      rowsPerPage: 10,
      sortBy: 'id',
      descending: true,
      totalItems: 0
    },
    items: [],
  }
}

export default {
  data: get_default_data,
  watch: {
    'pagination.page' (val) {
      this.fetchData()
    },
    'pagination.sortBy' (val) {
      this.fetchData()
    },
    'pagination.descending' (val) {
      this.fetchData()
    },
  },
  methods: {
    get_column_data (row, field) {
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
    fetchData () {
      let sort = this.pagination.sortBy
      if (this.pagination.descending) {
        sort = '-' + sort
      }
      //this.$route.query.query = JSON.stringify(this.filters.model)
      this.$route.query.sort = sort
      this.$route.query.perPage = this.pagination.rowsPerPage
      this.$route.query.page = this.pagination.page
      this.$http.get(`posts`, {params: this.$route.query}).then(({ data }) => {
        this.items = data.data
        this.pagination.totalItems = data.total
      })
    },
    remove (item) {
      // this.$alert('ok')
      this.$http.delete(`posts/` + item.id).then(({ data }) => {
        this.fetchData()
      })
    },
    next () {
      this.pagination.page++
    }
  },
  created () {
    this.fetchData()
  }
}
</script>