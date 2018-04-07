<template>
  <q-page
    padding
    class="row justify-center">
    <q-table
      :data="table_data"
      :columns="columns"
      :filter="filter"
      :visible-columns="visible_columns"
      selection="single"
      :selected.sync="item"
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
      <template
        slot="top-selection"
        slot-scope="props">
        <div class="col" />
        <q-btn
          color="negative"
          flat
          round
          delete
          icon="delete"
          @click="remove" />
      </template>
    </q-table>
    <q-page-sticky
      position="bottom-right"
      :offset="[18, 18]">
      <q-btn
        round
        color="primary"
        @click="search"
        icon="add" />
    </q-page-sticky>

    <q-modal
      v-model="search_modal"
      class="row justify-center">
      <q-table
        :data="search_table_data"
        :columns="search_columns"
        :filter="search_filter"
        :visible-columns="search_visible_columns"
        row-key="id"
        color="secondary"
        class="col-xs-12 no-shadow"
      >
        <template
          slot="top-left"
          slot-scope="props">
          <q-search
            hide-underline
            color="secondary"
            v-model="search_filter"
            class="col-6"
          />
        </template>
        <template
          slot="top-right"
          slot-scope="props">
          <q-table-columns
            color="secondary"
            class="q-mr-sm"
            v-model="search_visible_columns"
            :columns="search_columns"
          />
        </template>
        <q-tr slot="body" slot-scope="props" :props="props" @click.native="search_select(props.row)" class="cursor-pointer">
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.value }}
          </q-td>
        </q-tr>
      </q-table>
    </q-modal>
  </q-page>
</template>

<script>
export default {
  data: function() {
    return {
      table_data: [],
      columns: [
        { name: 'username', label: '아이디', field: row => row.user.username, sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: row => row.user.name, sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: row => row.user.email, sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: row => row.user.phone, sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: row => row.user.birthday, sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: row => row.user.school, sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: row => row.user.church, sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['username', 'name', 'email', 'phone'],
      item: [],

      search_modal: false,
      search_table_data: [],
      search_columns: [
        { name: 'username', label: '아이디', field: 'username', sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: 'name', sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: 'email', sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: 'phone', sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: 'birthday', sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: 'school', sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: 'church', sortable: true, align: 'left' }
      ],
      search_filter: '',
      search_visible_columns: ['username', 'name', 'email', 'phone'],
      search_item: []
    }
  },
  methods: {
    fetch_data: function() {
      let query = {}
      var self = this
      self.$axios.get('howcs_teacher_infos', {params: query})
        .then(function(response) { let data = response.data
          self.table_data = data
        })
    },
    remove: function () {
      var self = this
      self.$axios.delete('howcs_teacher_infos/' + self.item[0].id)
        .then(function(response) { let data = response.data
          self.fetch_data()
        })
    },
    howcs_teacher_new: function (row) {
      var self = this
      self.$axios.post('howcs_teacher_infos', {
        'user_id': row.id
      }).then(function(response) { let data = response.data
        self.fetch_data()
      })
    },
    search: function () {
      let query = {}
      var self = this
      self.$axios.get('users', {params: query})
        .then(function(response) { let data = response.data
          self.search_table_data = data
        })
      self.search_modal = true
    },
    search_select: function (row) {
      this.howcs_teacher_new(row)
      this.search_modal = false
    }
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
