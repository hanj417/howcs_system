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
  </q-page>
</template>

<script>
export default {
  data: function () {
    return {
      table_data: [],
      columns: [
        { name: 'minor_category', label: '분류', field: function (row) { return row.class.minor_category }, sortable: true, align: 'left' },
        { name: 'title', label: '제목', field: function (row) { return row.class.title }, sortable: true, align: 'left' },
        { name: 'teacher_name', label: '선생님', field: function (row) { return row.class.teacher.name }, sortable: true, align: 'left' }
      ],
      agit_columns: [
        { name: 'title', label: '제목', field: function (row) { return row.class.title }, sortable: true, align: 'left' },
        { name: 'teacher_name', label: '선생님', field: function (row) { return row.class.teacher.name }, sortable: true, align: 'left' },
        { name: 'time_slot', label: '시간', field: function (row) { return row.class.time_slot}, sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['minor_category', 'title', 'teacher_name', 'time_slot'],
      item: [],
      major_categories: [],
      minor_categories: []
    }
  },
  watch: {
    'id': function (val) {
      this.fetch_data()
    },
    'major_category': function (val) {
      this.fetch_data()
    },
    'minor_category': function (val) {
      this.fetch_data()
    },
    'action': function (val) {
      this.fetch_data()
    }
  },
  props: ['id', 'major_category', 'minor_category', 'action'],
  methods: {
    fetch_data: function () {
      let query = {}
      if (this.id) {
        query['student_id'] = this.id
      }
      if (this.major_category) {
        query['major_category'] = this.major_category
      }
      if (this.minor_category) {
        query['minor_category'] = this.minor_category
      }
      query['semester'] = '겨울'
      var self = this
      self.$axios.get('enrollments', {params: query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
        })
    },
    rowClick: function (row) {
      if (this.action === 'post') {
        this.$router.push({name: 'post_class', params: {class_id: row.class.id}})
      } else if (this.action === 'attendance') {
        this.$router.push({name: 'attendance_student', params: {student_id: row.student_id, class_id: row.class_id}})
      } else if (this.action === 'fruit') {
        this.$router.push({name: 'student_fruit_record', params: {action: 'view', id: row.id}})
      }
    }
  },
  created: function () {
    var self = this
    self.$axios.get('classes/categories'
    ).then(function (response) {
      let data = response.data
      self.major_categories = data
      self.$axios.get('classes/categories/' + self.major_category
      ).then(function (response) {
        let data = response.data
        self.minor_categories = data[self.major_category]
        self.fetch_data()
      })
    })
    if (this.major_category === 'agit') {
      this.columns = this.agit_columns
    }
  }
}
</script>
