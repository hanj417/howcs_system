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
        @click.native="view(props.row)"
        class="cursor-pointer">
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props">
          {{ col.value }}
        </q-td>
      </q-tr>
    </q-table>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'

export default {
  data: function () {
    return {
      priv_new: false,
      priv_update: false,
      priv_del: false,
      table_data: [],
      columns: [
        { name: 'id', label: '번호', field: function (row) { return row.post.id }, sortable: true, align: 'left' },
        { name: 'title', label: '제목', field: function (row) { return row.post.title}, sortable: true, align: 'left' },
        { name: 'author_name', label: '글쓴이', field: function (row) { return row.post.author.name }, sortable: true, align: 'left' },
        { name: 'date', label: '작성일', field: function (row) { return (new Date(row.post.created_at)).toISOString().slice(0, 10) }, sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['id', 'title', 'author_name', 'date'],
      item: [],
      user: {}
    }
  },
  props: ['class_id', 'major_category', 'minor_category'],
  methods: {
    fetch_data: function () {
      let query = {}
      var self = this
      self.$axios.get('user_posts', {params: query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
        })
    },
    fetch_menu: function () {
      var self = this
      self.$axios.get('menu')
        .then(function (response) {
          let data = response.data
          self.$store.commit('menu/UpdateMenu', data)
        }).catch(function (error) {
          console.log('error')
        })
    },
    view: function (row) {
      let query = {}
      var self = this
      var post_id = row.post.id
      self.$axios.delete('user_posts/' + row.post.id, {params: query})
        .then(function (response) {
          let data = response.data
          self.fetch_menu()
          self.$router.push({name:'post_view', params:{id:post_id}})
        })
    }
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
