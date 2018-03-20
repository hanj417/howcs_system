<template>
<q-page padding>
    <q-table
      :data="table_data"
      :columns="columns"
      :filter="filter"
      :visible-columns="visible_columns"
      row-key="name"
      color="secondary"
    >
      <template slot="top-left" slot-scope="props">
        <q-search
          hide-underline
          color="secondary"
          v-model="filter"
          class="col-6"
        />
      </template>
      <template slot="top-right" slot-scope="props">
        <q-table-columns
          color="secondary"
          class="q-mr-sm"
          v-model="visible_columns"
          :columns="columns"
        />
      </template>
      <q-tr slot="body" slot-scope="props" :props="props">
        <template v-for="(key, value) in props.row">
          <q-td :key="key" :props="props">{{ value }}</q-td>
        </template>
      </q-tr>
    </q-table>
</q-page>
</template>

<script>
/*
const get_default_data = () => {
  return {
    loading: false,
    columns: [
      {'text': '선생님', 'value': 'teacher.name'},
      {'text': '제목', 'value': 'title'},
      {'text': '대분류', 'value': 'major_category'},
      {'text': '분류', 'value': 'minor_category'},
    ],
    headers: [
      {'text': '선생님'},
      {'text': '제목'},
      {'text': '대분류'},
      {'text': '분류'},
      {'text': ''},
    ],
    agit_columns: [
      {'text': '분류', 'value': 'minor_category'},
      {'text': '제목', 'value': 'title'},
      {'text': '선생님', 'value': 'teacher.name'},
      {'text': '요일', 'value': 'weekday'},
      {'text': '시간', 'value': 'hour'},
    ],
    agit_headers: [
      {'text': '분류'},
      {'text': '제목', 'width':400},
      {'text': '선생님'},
      {'text': '요일'},
      {'text': '시간'},
      {'text': ''},
    ],
    howcs_teacher_columns: [
      {'text': '분류', 'value': 'minor_category'},
      {'text': '제목', 'value': 'title'},
    ],
    howcs_teacher_headers: [
      {'text': '분류', 'width':200},
      {'text': '제목', 'width':400},
      {'text': '글/출석'},
    ],
    items: [],
    filters: {},
    search_name: '',
    class_form_visible: false,
    attendance_visible: false,
    enrollment_visible: false,
    edit_visible: false,
    delete_visible: false,
    enroll_visible: false,
  }
}
*/

export default {
  data () {
    return {
      table_data: [],
      columns: [
        { name: 'teacher.name', label: '선생님', field: row => row.teacher.name, sortable: true, align: 'left' },
        { name: 'title', label: '제목', field: 'title', sortable: true, align: 'left' },
      ],
      filter: '',
      visible_columns: ['teacher.name', 'title'],
    }
  },
  props: ['major_category', 'id'],
  methods: {
    fetch_data() {
      this.query = {}
      if (this.major_category) {
        this.query['major_category'] = this.major_category
      }
      if (this.id) {
        this.query['teacher_id'] = this.id
      }
      this.$axios.get(`classes`, {params: this.query})
      .then(({ data }) => {
        this.table_data = data
      })
    },
    remove(item) {
      this.$axios.delete(`classes/` + item.id)
      .then(({ data }) => {
        this.fetch_data()
      })
    },
    enroll(item) {
      this.$axios.post(`enrollments`, {
        'class_id': item.id,
      }).then(({ data }) => {
        this.fetch_data()
      })
    },
/*
    set_visibility() {
      if (!!this.$route.params.id) {
        this.filters['teacher_id'] = this.$route.params.id
        this.columns = this.howcs_teacher_columns
        this.headers = this.howcs_teacher_headers
        this.class_form_visible = true
        this.post_visible = true
        this.attendance_visible = true
        this.enrollment_visible = false
        this.edit_visible = false
        this.delete_visible = false
        this.enroll_visible = false
      } else {
        if (this.major_category == 'agit') {
          this.columns = this.agit_columns
          this.headers = this.agit_headers
          this.class_form_visible = false
          this.post_visible = false
          this.attendance_visible = false
          this.enrollment_visible = false
          this.edit_visible = false
          this.delete_visible = false
          this.enroll_visible = true
        } else if (this.major_category == 'howcs') {
          this.class_form_visible = true
          this.post_visible = false
          this.attendance_visible = false
          this.enrollment_visible = true
          this.edit_visible = true
          this.delete_visible = true
          this.enroll_visible = false
        }
      }
    }
*/
  },
  created () {
    //this.set_visibility()
    this.fetch_data()
  }
}
</script>
