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
          v-if="priv_del"
          color="negative"
          flat
          round
          delete
          icon="delete"
          @click="remove" />
      </template>
      <q-tr
        slot="body"
        slot-scope="props"
        :props="props"
        @click.native="rowClick(props.row)"
        class="cursor-pointer">
        <q-td auto-width>
          <q-checkbox
            color="primary"
            v-model="props.selected" />
        </q-td>
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
        v-if="priv_new"
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
        row-key="name"
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
        <q-tr
          slot="body"
          slot-scope="props"
          :props="props"
          @click.native="search_select(props.row)"
          class="cursor-pointer">
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props">
            {{ col.value }}
          </q-td>
        </q-tr>
      </q-table>
    </q-modal>
  </q-page>
</template>

<script>

export default {
  data: function () {
    return {
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
        { name: 'church', label: '출석교회', field: function (row) { return row.student.church }, sortable: true, align: 'left' }
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
  watch: {
    '$route.name': function (val) {
      this.fetch_data()
    }
  },
  props: ['action', 'class_id'],
  methods: {
    check_priv: function () {
      var self = this
      let priv_new_query = {priv: 'howcs_enrollment_new'}
      self.$axios.get('privileges', {params: priv_new_query})
        .then(function (response) {
          let data = response.data
          self.priv_new = data
        })
  
      let priv_update_query = {priv: 'howcs_enrollment_update'}
      self.$axios.get('privileges', {params: priv_update_query})
        .then(function (response) {
          let data = response.data
          self.priv_update = data
        })
  
      let priv_del_query = {priv: 'howcs_enrollment_del'}
      self.$axios.get('privileges', {params: priv_del_query})
        .then(function (response) {
          let data = response.data
          self.priv_del = data
        })

      let priv_query = {priv: 'howcs_attendance_update'}
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
    remove: function () {
      var self = this
      if (!self.priv_del)
        return

      self.$axios.delete('enrollments/' + self.item[0].class_id + '/' + self.item[0].student_id)
        .then(function (response) {
          let data = response.data
          self.fetch_data()
        })
    },
    search: function () {
      let query = {}
      var self = this
      self.$axios.get('student_infos', {params: self.query})
        .then(function (response) {
          let data = response.data
          self.search_table_data = data
        })
      self.search_modal = true
    },
    search_select: function (row) {
      var self = this
      self.$axios.post('enrollments', {
        'class_id': self.class_id,
        'student_id': row.id
      }).then(function (response) {
        let data = response.data
        self.search_modal = false
        self.fetch_data()
      })
    },
    rowClick: function (row) {
      if (this.action === 'student_health_record') {
        this.$router.push({name: 'student_health_record', params: {id: row.student.id, action: 'edit'}})
      } else if (this.action === 'student_fruit_record') {
        this.$router.push({name: 'student_fruit_record', params: {id: row.id, action: 'edit'}})
      }
    }
  },
  created: function () {
    this.check_priv()
    this.fetch_data()
  }
}
</script>
