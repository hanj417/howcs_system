<template>
  <q-page
    padding
    class="row justify-center">
    <q-table
      :data="table_data"
      :columns="columns"
      :filter="filter"
      :visible-columns="visible_columns"
      row-key="id"
      color="secondary"
      class="col-xs-11"
    >
      <template
        slot="top-left"
        slot-scope="props">
        <q-search
          hide-underline
          color="secondary"
          v-model="filter"
          class="col-6"
        />
      </template>
      <template
        slot="top-right"
        slot-scope="props">
        <q-table-columns
          color="secondary"
          class="q-mr-sm"
          v-model="visible_columns"
          :columns="columns"
        />
      </template>
      <q-tr
        slot="body"
        slot-scope="props"
        :props="props"
        @click.native="$router.push({name:'post_view', params:{id:props.row.id}})"
        class="cursor-pointer">
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props">
          {{ col.value }}
        </q-td>
      </q-tr>
    </q-table>
    <q-page-sticky
      position="bottom-right"
      :offset="[18, 18]">
      <q-btn
        v-if="is_admin"
        round
        color="primary"
        @click="$router.push({name:'post_form_admin', params:{action:'new'}})"
        icon="add" />
      <q-btn
        v-if="!is_admin && is_author"
        round
        color="primary"
        @click="$router.push({name:'post_form', params:{action:'new', id:class_id}})"
        icon="add" />
    </q-page-sticky>
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

      is_author: false,
      is_admin: false,
      user: {}
    }
  },
  props: ['class_id', 'major_category', 'minor_category'],
  methods: {
    fetch_data: function() {
      let query = {}
      if (this.minor_category) {
        query['major_category'] = this.major_category
        query['minor_category'] = this.major_category
      }
      if (this.class_id) {
        query['class_id'] = this.class_id
      }
      var self = this
      self.$axios.get('posts', {params: query})
        .then(function(response) { let data = response.data
          self.table_data = data
        })
    }
  },
  created: function () {
    let user = LocalStorage.get.item('user_')
    console.log(JSON.parse(user.role))
    console.log(JSON.parse(user.role).includes('admin'))
    if (JSON.parse(user.role).includes('admin')) {
      this.is_admin = true
    }
    if (this.class_id) {
      this.user = LocalStorage.get.item('user_')

      var self = this
      self.$axios.get('classes/' + self.class_id)
        .then(function(response) { let data = response.data
          console.log(self.user)
          if (data.teacher_id === self.user.id) {
            self.is_author = true
          }
        })
    }
    this.fetch_data()
  }
}
</script>
