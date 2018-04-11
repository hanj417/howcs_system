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
          icon="edit"
          @click="$router.push({name: 'user_form_admin', params: {action:'update', id:item[0].id}})" />
        <q-btn
          color="negative"
          flat
          round
          delete
          icon="delete"
          @click="remove" />
      </template>
      <q-td
        slot="body-cell-role"
        slot-scope="props"
        :props="props">
        <template v-for="role in props.value">
          <q-chip
            small
            color="secondary">{{ role_str[role] }}</q-chip>
        </template>
      </q-td>
    </q-table>
  </q-page>
</template>

<script>

export default {
  data: function () {
    return {
      table_data: [],
      role_str: {
        'agit_student': '아지트학생',
        'agit_teacher': '아지트교사',
        'howcs_student': '하우학교학생',
        'howcs_teacher': '하우학교교사',
        'admin': '관리자'
      },
      columns: [
        { name: 'username', label: '아이디', field: 'username', sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: 'name', sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: 'email', sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: 'phone', sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: 'birthday', sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: 'school', sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: 'church', sortable: true, align: 'left' },
        { name: 'role', label: '권한', field: function (row) { return JSON.parse(row.role) }, sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['username', 'name', 'email', 'phone'],
      item: []
    }
  },
  methods: {
    fetch_data: function () {
      let query = {}
      var self = this
      self.$axios.get('users', {params: query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
        })
    },
    remove: function () {
      var self = this
      self.$axios.delete('users/' + self.item[0].id)
        .then(function (response) {
          let data = response.data
          self.fetch_data()
        })
    }
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
