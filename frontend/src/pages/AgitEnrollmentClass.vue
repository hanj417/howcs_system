<template>
  <q-page
    padding
    class="row justify-center">
    <q-table
      :data="table_data"
      :columns="columns"
      :filter="filter"
      :visible-columns="visible_columns"
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
        :props="props">
        <template v-for="col in props.cols">
        <q-td
          v-if="col.name != 'approval'"
          :key="col.name"
          :props="props">
          {{ col.value }}
        </q-td>
        <q-td
          v-else
          :key="col.name"
          :props="props">
          <template v-if="priv_update">
          <q-btn @click.native="rowClick(props.row)" :label="approval_label[col.value]" />
          </template>
          <template v-else>
            {{ approval_label[col.value] }}
          </template>
        </q-td>
        </template>
      </q-tr>
    </q-table>
  </q-page>
</template>

<script>
export default {
  data: function () {
    return {
      approval_label: {
        true: '승인',
        false: '대기',},
      priv_new: false,
      priv_update: false,
      priv_del: false,
      table_data: [],
      columns: [
        { name: 'username', label: '아이디', field: function (row) { return row.student.username }, sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: function (row) { return row.student.name }, sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: function (row) { return row.student.email }, sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: function (row) { return row.student.phone }, sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: function (row) { return row.student.birthday }, sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: function (row) { return row.student.school }, sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: function (row) { return row.student.church }, sortable: true, align: 'left' },
        { name: 'created_at', label: '신청시간', field: function (row) { return (new Date(row.created_at)).toISOString().substr(5, 11) }, sortable: true, align: 'left' },
        { name: 'payment', label: '회비', field: function (row) { if (row.student.payments) return '기납'; return '미납' }, sortable: true, align: 'left' },
        { name: 'approval', label: '승인', field: function (row) { return row.approval }, sortable: true, align: 'left' },
      ],
      filter: '',
      visible_columns: ['username', 'name', 'payment', 'created_at', 'approval'],
      item: [],
    }
  },
  watch: {
    '$route.name': function (val) {
      this.fetch_data()
    }
  },
  props: ['class_id'],
  methods: {
    check_priv: function () {
      var self = this
      let priv_new_query = {priv: 'agit_enrollment_new'}
      self.$axios.get('privileges', {params: priv_new_query})
        .then(function (response) {
          let data = response.data
          self.priv_new = data
        })
  
      let priv_update_query = {priv: 'agit_enrollment_update'}
      self.$axios.get('privileges', {params: priv_update_query})
        .then(function (response) {
          let data = response.data
          self.priv_update = data
        })
  
      let priv_del_query = {priv: 'agit_enrollment_del'}
      self.$axios.get('privileges', {params: priv_del_query})
        .then(function (response) {
          let data = response.data
          self.priv_del = data
        })
      let priv_query = {priv: 'agit_attendance_update'}
      self.$axios.get('privileges', {params: priv_query})
        .then(function (response) {
          let data = response.data
          self.priv = data
      })
    },
    fetch_data: function () {
      let query = {'class_id': this.class_id}
      var self = this
      self.$axios.get('enrollments', {params: query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
        })
    },
    rowClick: function (row) {
      var self = this
      self.$axios.put('enrollments/' + row.class_id + '/' + row.student_id, {
          'approval': !row.approval
        }).then(function (response) {
          self.fetch_data()
        })
      
    }
  },
  created: function () {
    this.check_priv()
    this.fetch_data()
  }
}
</script>
