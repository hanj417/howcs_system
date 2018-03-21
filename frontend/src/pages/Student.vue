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
    </q-table>
    <q-page-sticky
      position="bottom-right"
      :offset="[18, 18]">
      <q-btn
        round
        color="primary"
        @click="$router.push({name: 'user_form', params: {action:'new_student'}})"
        icon="add" />
    </q-page-sticky>
  </q-page>
</template>

<script>

export default {
  data () {
    return {
      table_data: [],
      columns: [
        { name: 'username', label: '아이디', field: 'username', sortable: true, align: 'left' },
        { name: 'student_id', label: '학번', field: row => row.student_info.student_id, sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: 'name', sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: 'email', sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: 'phone', sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: 'birthday', sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: 'school', sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: 'church', sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['student_id', 'name', 'email', 'phone'],
      item: []
    }
  },
  methods: {
    fetch_data () {
      let query = {}
      this.$axios.get(`student_infos`, {params: this.query})
        .then(({ data }) => { this.table_data = data })
    },
    remove () {
      this.$axios.delete(`student_infos/` + this.item[0].id)
        .then(({ data }) => { this.fetch_data() })
    }
  },
  created () {
    this.fetch_data()
  }
}
</script>
