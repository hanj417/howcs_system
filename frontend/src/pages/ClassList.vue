<template>
  <q-page
    padding
    class="row justify-center">
    <q-table
      :data="tableData"
      :columns="columns"
      :filter="filter"
      :visible-columns="visibleColumns"
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
          v-model="visibleColumns"
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
        v-if="$route.name == 'class_all' && privCreate"
        round
        color="primary"
        @click="$router.push({name:'class_form_new', params:{major_category:'howcs', role:'admin'}})"
        icon="add" />
      <q-btn
        v-if="$route.name == 'howcs_class_teacher' && privCreate"
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
      tableData: [],
      columns: [
        { name: 'teacher_name', label: '선생님', field: function (row) { return row.teacher.name }, sortable: true, align: 'left' },
        { name: 'title', label: '제목', field: 'title', sortable: true, align: 'left' },
        { name: 'major_category', label: '대분류', field: 'major_category', sortable: true, align: 'left' },
        { name: 'minor_category', label: '분류', field: 'minor_category', sortable: true, align: 'left' }
      ],
      filter: '',
      visibleColumns: ['teacher_name', 'title', 'major_category', 'minor_category'],
      selection: 'none',
      item: []
    }
  },
  props: ['state', 'major_category', 'minor_category'],
  methods: {
    getData: function () {
      let query = {}
      query['major_category'] = this.major_category
      query['minor_category'] = this.minor_category

      var self = this
      self.$axios.get('resource/classes', {params: query})
        .then(function (response) {
          let data = response.data
          self.tableData = data
        })
    },
    rowClick: function (row) {
/*
      if (this.action === 'enrollment') {
        if (this.major_category == 'agit') {
          this.$router.push({name: 'agit_enrollment_class', params: {class_id: row.id}})
        } else {
          this.$router.push({name: 'enrollment_class', params: {class_id: row.id}})
        }
      } else if (this.action === 'attendance') {
        this.$router.push({name: 'attendance_class', params: {class_id: row.id}})
      } else if (this.action === 'post') {
        this.$router.push({name: 'post_class', params: {class_id: row.id}})
      } else if (this.action === 'student_health_record') {
        this.$router.push({name: 'enrollment_class_action', params: {class_id: row.id, action: 'student_health_record'}})
      } else if (this.action === 'edit') {
        if (this.$route.name === 'class_all') {
          this.$router.push({name: 'class_form_edit', params: {role: 'admin', class_id: row.id, action: 'edit'}})
        } else if (this.$route.name === 'class_teacher') {
          this.$router.push({name: 'class_form_edit', params: {role: 'teacher', class_id: row.id, action: 'edit'}})
        } else if (this.$route.name === 'howcs_class_teacher') {
          this.$router.push({name: 'class_form_edit', params: {role: 'teacher', class_id: row.id, action: 'edit'}})
        }
      }
*/
    }
  },
  created: function () {
    this.getData()
  }
}
</script>
