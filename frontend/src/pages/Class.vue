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
      <q-tr slot="body" slot-scope="props" :props="props" @click.native="rowClick(props.row)" class="cursor-pointer">
        <q-td v-for="col in props.cols" :key="col.name" :props="props">
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
        @click="$router.push({name:'class_form_new', params:{major_category:'howcs', role:'admin'}})"
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
      selection: 'none',
      item: [],
    }
  },
  watch: {
    '$route.name' (val) {
      this.fetch_data()
    },
  },
  watch: {
    'major_category' (val) {
      this.fetch_data()
    },
    'minor_category' (val) {
      this.fetch_data()
    },
    'action' (val) {
      this.fetch_data()
    },
    'teacher_id' (val) {
      this.fetch_data()
    },
  },
  props: ['major_category', 'minor_category', 'action', 'teacher_id'],
  methods: {
    fetch_data () {
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
    },
    rowClick (row) {
      if (this.action === 'enrollment') {
        this.$router.push({name:'enrollment_class', params: {class_id: row.id}})
      } else if (this.action === 'attendance') {
        this.$router.push({name:'attendance_class', params: {class_id: row.id}})
      } else if (this.action === 'post') {
        this.$router.push({name:'post_class', params: {class_id: row.id}})
      } else if (this.action === 'edit') {
        if (this.$route.name === 'class_all') {
          this.$router.push({name:'class_form_edit', params: {role: 'admin', class_id: row.id, action:'edit'}})
        } else if (this.$route.name === 'class_teacher') {
          this.$router.push({name:'class_form_edit', params: {role: 'teacher', class_id: row.id, action:'edit'}})
        }
      }
    }, 
  },
  created () {
    if (this.$route.name === 'class_all') {
    } else if (this.$route.name === 'class_teacher') {
    }
    this.fetch_data()
  }
}
</script>

