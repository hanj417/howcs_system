<template>
  <q-page
    padding
    class="row justify-center">
<template v-for="post in table_data">
<q-card inline style="width: 500px">
  <q-card-media>
    <img :src="post.img">
  </q-card-media>
  <q-card-title>
{{ post.title }}
  </q-card-title>
  <q-card-main>
<div v-html="item.ellipsis" />
  </q-card-main>
  <q-card-separator />
  <q-card-actions>
    <q-btn flat color="primary" label="보기" />
  </q-card-actions>
</q-card>
</template>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'

export default {
  data: function() {
    return {
      table_data: [],
      columns: [
        { name: 'id', label: '번호', field: 'id', sortable: true, align: 'left' },
        { name: 'title', label: '제목', field: 'title', sortable: true, align: 'left' },
        { name: 'author_name', label: '글쓴이', field: row => row.author.name, sortable: true, align: 'left' },
        { name: 'date', label: '작성일', field: row => (new Date(row.created_at)).toISOString().slice(0, 10), sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['id', 'title', 'author_name', 'date'],
      item: [],

      major_category: 'homepage',
      is_author: false,
      is_admin: false,
      user: {}
    }
  },
  props: ['minor_category'],
  methods: {
    fetch_data: function() {
      let query = {}
      if (this.minor_category) {
        query['minor_category'] = this.minor_category
      }
      var self = this
      self.$axios.get('posts/homepage', {params: query})
        .then(function(response) { let data = response.data
          self.table_data = data
        })
    }
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
/*
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
*/
