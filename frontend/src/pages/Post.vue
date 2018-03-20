<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout justify-center align-center>
        <v-flex xs6 offset-xs1>
          <v-text-field label="검색" single-line hide-details v-model="search_name"></v-text-field>
        </v-flex>
        <v-card>
          <v-data-table :headers='headers' :items='items' :rows-per-page-items='[10, 20, {"text":"All", "value":-1}]' :search="search_name">
            <template slot='items' scope='props'>
              <tr @click="props.expanded = !props.expanded">
                <td v-for='column in columns' v-html="get_column_data(props.item, column)"></td>
                <td v-if='is_author' class="justify-center layout px-0">
                  <v-btn icon class="mx-0" :to="{name: 'post_form', params: {action:'update', id:props.item.id}}">
                    <v-icon>edit</v-icon>
                  </v-btn>
                  <v-btn icon class="mx-0" @click="remove(props.item)">
                    <v-icon>delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </template>
            <template slot="expand" slot-scope="props">
              <v-card flat>
                <v-card-text><span v-html="props.item.body"></span></v-card-text>
              </v-card>
            </template>
          </v-data-table>
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
    :to="{name: 'post_form', params: {action:'new', id:class_id}}"
  >
    <v-icon>add</v-icon>
  </v-btn>
  </v-content>
</template>

<script>
import { mapState } from 'vuex'

const get_default_data = () => {
  return {
    class_id: '',
    is_author: false,
    columns: [
      {'text': '번호', 'value': 'id'},
      {'text': '제목', 'value': 'title', 'width': 400},
      {'text': '글쓴이', 'value': 'author.name'},
      {'text': '작성일', 'value': 'date'},
    ],
    headers: [
      {'text': '번호', 'value': 'id'},
      {'text': '제목', 'value': 'title', 'width': 400},
      {'text': '글쓴이', 'value': 'author.name'},
      {'text': '작성일', 'value': 'date'},
    ],
    filters: {},
    items: [],
    search_name: '',
  }
}

export default {
  data: get_default_data,
  computed: {
    ...mapState(['user'])
  },
  computed: {
    class_id() {
      return this.$route.params.class_id
    }, 
    major_category() {
      return this.$route.params.major_category
    }, 
    minor_category() {
      return this.$route.params.minor_category
    },
    is_category() {
      return !!this.$route.params.minor_category
    }
  },
  methods: {
    get_column_data(row, field) {
      // process fields like `type.name`
      let [l1, l2] = field.value.split('.')
      if (l1 == 'date') {
        let value = new Date(row['created_at'])
        value = value.toISOString().slice(0,10)
        return value
      } 
      if (l1 == 'id') {
console.log(row)
        if (row['properties'] && JSON.parse(row['properties']).includes('notice')) {
          return '공지'
        }
      }

      let value = row[l1]
      let tag = null
      if (l2) { value = row[l1] ? row[l1][l2] : null }
      if (field.type === 'image') { tag = 'img' }
      if (tag) { value = `<${tag} src="${value}" class="crud-grid-thumb" controls />` }
      return value
    },
    fetch_data () {
      this.$route.query.query = JSON.stringify(this.filters)
      this.$axios.get(`posts`, {params: this.$route.query})
      .then(({ data }) => { this.items = data })
    },
    remove (item) {
      this.$axios.delete(`posts/` + item.id)
      .then(({ data }) => { this.fetch_data() })
    },
  },
  created () {
    if (!!this.$route.params.minor_category) {
      this.filters = {
        'major_category': this.$route.params.major_category,
        'minor_category': this.$route.params.minor_category,
      } 
    } else if (!!this.$route.params.class_id) {
      this.filters = {
        'class_id': this.$route.params.class_id,
      } 
      this.class_id = this.$route.params.class_id
    }

    if (this.class_id) {
      var user = JSON.parse(localStorage['user'])
      this.$axios.get(`classes/` + this.class_id)
      .then(({ data }) => { 
        console.log(user)
        if (data.teacher_id == user.id) {
          this.is_author = true
          this.headers.push({'text':'수정/삭제'})
        }
      })
    }

    this.fetch_data()
  }
}
</script>
