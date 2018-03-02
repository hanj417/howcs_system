<template>
    <v-content>
      <v-container fluid fill-height>
        <v-layout justify-center align-center>
          <v-card>
            <v-data-table :headers='columns' :items='items' :total-items="pagination.totalItems" hide-actions :pagination.sync="pagination" :loading="loading">
              <template slot='items' scope='props'>
                <tr>
                  <td v-for='column in columns' v-html="getColumnData(props.item, column)"></td>
                  <td width='160'>
                    <v-btn fab small @click="edit(props.item)">
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
      :to="{name: 'register_student'}"
    >
      <v-icon>add</v-icon>
    </v-btn>
    </v-content>
</template>

<script>
const getDefaultData = () => {
  return {
    form: {
      model: {},
      fields: {},
      rules: {},
      messages: {}
    },
    filters: {
      model: {},
      fields: null
    },
    loading: false,
    columns: [], // fetch grid setup params from server if `columns` is empty
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
    isShowEdit: false,
    currentItem: false,
    items: [],
    dialog: false
  }
}

export default {
  data: getDefaultData,
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
    'dialog' (val) {
      this.fetchData()
    },
  },
  methods: {
    getColumnData (row, field) {
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
    fetchGrid () {
      return new Promise((resolve, reject) => {
        this.$http.get(`students/grid`).then(({ data }) => {
          this.columns = data.columns || {}
          this.actions = data.actions || {}
          this.filters = data.filters || {}
          this.options = data.options || {}

          if (this.options && this.options.sort) {
            let sortData = this.options.sort.split('-')
            let desc = sortData.length > 1
            let sortField = sortData.pop()

            // if (sortField.indexOf('.') < 0) {
            //   sortField = sortField
            // }
            this.pagination.sort = sortField
            this.pagination.descending = desc
          }
          resolve()
        })
      })
    },
    preFetch () {
      let sort = this.pagination.sortBy
      if (this.pagination.descending) {
        sort = '-' + sort
      }
      this.$route.query.query = JSON.stringify(this.filters.model)
      this.$route.query.sort = sort
      this.$route.query.perPage = this.pagination.rowsPerPage
      this.$route.query.page = this.pagination.page
    },
    fetchData () {
      this.preFetch()
      this.$http.get(`students`, {params: this.$route.query}).then(({ data }) => {
        this.items = data.data
        this.pagination.totalItems = data.total
      })
    },
    remove (item) {
      // this.$alert('ok')
      this.$http.post(`students/delete`, {'id': item.id}).then(({ data }) => {
        this.fetchData()
      })
    },
    edit (item) {
      // this.$alert('ok')
    },
    next () {
      // console.log('next')
      this.pagination.page++
    }
  },
  created () {
    this.fetchGrid().then(() => {})
    this.fetchData()
  }
}
</script>
