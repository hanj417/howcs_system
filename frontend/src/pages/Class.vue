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
        v-if="$route.name == 'class_all' && priv_new"
        round
        color="primary"
        @click="$router.push({name:'class_form_new', params:{major_category:'howcs', role:'admin'}})"
        icon="add" />
      <q-btn
        v-if="$route.name == 'howcs_class_teacher' && priv_new"
        round
        color="primary"
        @click="$router.push({name:'class_form_new', params:{major_category:'howcs', role:'teacher'}})"
        icon="add" />
    </q-page-sticky>
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
        { name: 'teacher_name', label: '선생님', field: function (row) { return row.teacher.name }, sortable: true, align: 'left' },
        { name: 'title', label: '제목', field: 'title', sortable: true, align: 'left' },
        { name: 'major_category', label: '대분류', field: 'major_category', sortable: true, align: 'left' },
        { name: 'minor_category', label: '분류', field: 'minor_category', sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['teacher_name', 'title', 'major_category', 'minor_category'],
      selection: 'none',
      item: []
    }
  },
  watch: {
    '$route.name': function (val) {
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
    },
    'teacher_id': function (val) {
      this.fetch_data()
    }
  },
  props: ['major_category', 'minor_category', 'action', 'teacher_id'],
  methods: {
    check_priv: function () {
      var self = this
      let priv_new_query = {priv: 'howcs_class_new'}
      self.$axios.get('privileges', {params: priv_new_query})
        .then(function (response) {
          let data = response.data
          self.priv_new = data
        })
  
      let priv_update_query = {priv: 'howcs_class_update'}
      self.$axios.get('privileges', {params: priv_update_query})
        .then(function (response) {
          let data = response.data
          self.priv_update = data
        })
  
      let priv_del_query = {priv: 'howcs_class_del'}
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
      let query = {}
      if (this.$route.name === 'class_all') {
        query['major_category'] = this.major_category
      } else if (this.$route.name === 'howcs_class_teacher') {
        query['major_category'] = this.major_category
        query['minor_category'] = this.minor_category
        query['teacher_id'] = this.teacher_id
      } else if (this.$route.name === 'class_teacher') {
        query['major_category'] = this.major_category
        query['teacher_id'] = this.teacher_id
      }
      var self = this
      self.$axios.get('classes', {params: query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
        })
    },
    rowClick: function (row) {
      if (this.action === 'enrollment') {
        this.$router.push({name: 'enrollment_class', params: {class_id: row.id}})
      } else if (this.action === 'attendance') {
        this.$router.push({name: 'attendance_class', params: {class_id: row.id}})
      } else if (this.action === 'post') {
        this.$router.push({name: 'post_class', params: {class_id: row.id}})
      } else if (this.action === 'student_health_record') {
        this.$router.push({name: 'enrollment_class_action', params: {class_id: row.id, action: 'student_health_record'}})
      } else if (this.action === 'student_fruit_record') {
        this.$router.push({name: 'enrollment_class_action', params: {class_id: row.id, action: 'student_fruit_record'}})
      } else if (this.action === 'edit') {
        if (this.$route.name === 'class_all') {
          this.$router.push({name: 'class_form_edit', params: {role: 'admin', class_id: row.id, action: 'edit'}})
        } else if (this.$route.name === 'class_teacher') {
          this.$router.push({name: 'class_form_edit', params: {role: 'teacher', class_id: row.id, action: 'edit'}})
        } else if (this.$route.name === 'howcs_class_teacher') {
          this.$router.push({name: 'class_form_edit', params: {role: 'teacher', class_id: row.id, action: 'edit'}})
        }
      }
    }
  },
  created: function () {
    this.check_priv()
    this.fetch_data()
  }
}
</script>
