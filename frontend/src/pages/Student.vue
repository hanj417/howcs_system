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
        @click.native="rowClick(props.row)"
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
        round
        color="primary"
        @click="$router.push({name: 'user_form', params: {action:'new_student'}})"
        icon="add" />
    </q-page-sticky>
  </q-page>
</template>

<script>

export default {
  data: function () {
    return {
      table_data: [],
      columns: [
        { name: 'username', label: '아이디', field: 'username', sortable: true, align: 'left' },
        { name: 'student_id', label: '학번', field: function (row) { return row.student_info.student_id }, sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: 'name', sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: 'email', sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: 'phone', sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: 'birthday', sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: 'school', sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: 'church', sortable: true, align: 'left' },
        { name: 'father_name', label: '부', field: function (row) { return row.student_info.father_name }, sortable: true, align: 'left' },
        { name: 'mother_name', label: '모', field: function (row) { return row.student_info.mother_name }, sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['student_id', 'name', 'email', 'phone', 'father_name', 'mother_name'],
      item: []
    }
  },
  props: ['action'],
  methods: {
    fetch_data: function () {
      let query = {}
      var self = this
      self.$axios.get('student_infos', {params: self.query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
        })
    },
    remove: function () {
      var self = this
      self.$axios.delete('student_infos/' + self.item[0].id)
        .then(function (response) {
          let data = response.data
          self.fetch_data()
        })
    },
    rowClick: function (row) {
      if (this.action === 'student_record') {
        this.$router.push({name: 'user_form', params: {action: 'update', id: row.id}})
      } else if (this.action === 'student_health_record') {
        this.$router.push({name: 'student_health_record', params: {action: 'edit', id: row.id}})
      }
    }
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
