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
          icon="group add"
          @click="$router.push({name:'enrollment_class', params: {id: item[0].id}})" />
        <q-btn
          color="negative"
          flat
          round
          icon="assignment"
          @click="$router.push({name:'post_class', params: {class_id: item[0].id}})" />
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
        @click="$router.push({name:'class_form_admin', params:{major_category:'howcs', action:'new'}})"
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
        { name: 'teacher_name', label: '선생님', field: row => row.teacher.name, sortable: true, align: 'left' },
        { name: 'title', label: '제목', field: 'title', sortable: true, align: 'left' },
        { name: 'major_category', label: '대분류', field: 'major_category', sortable: true, align: 'left' },
        { name: 'minor_category', label: '분류', field: 'minor_category', sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['teacher_name', 'title', 'major_category', 'minor_category'],
      item: []
    }
  },
  props: ['major_category', 'id'],
  methods: {
    fetch_data () {
      let query = {}
      if (this.major_category) {
        query['major_category'] = this.major_category
      }
      if (this.id) {
        query['teacher_id'] = this.id
      }
      this.$axios.get(`classes`, {params: query})
        .then(({ data }) => {
          this.table_data = data
        })
    },
    remove () {
      this.$axios.delete(`classes/` + this.item[0].id)
        .then(({ data }) => {
          this.fetch_data()
        })
    },
    enroll () {
      this.$axios.post(`enrollments`, {
        'class_id': this.item.id
      }).then(({ data }) => {
        this.fetch_data()
      })
    }
    /*
    set_visibility() {
      if (this.id) {
        this.filters['teacher_id'] = this.id
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
        if (this.major_category === 'agit') {
          this.columns = this.agit_columns
          this.headers = this.agit_headers
          this.class_form_visible = false
          this.post_visible = false
          this.attendance_visible = false
          this.enrollment_visible = false
          this.edit_visible = false
          this.delete_visible = false
          this.enroll_visible = true
        } else if (this.major_category === 'howcs') {
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
    // this.set_visibility()
    this.fetch_data()
  }
}
</script>

/*
    class_form_visible: false,
    attendance_visible: false,
    enrollment_visible: false,
    edit_visible: false,
    delete_visible: false,
    enroll_visible: false,
  }
}
*/
