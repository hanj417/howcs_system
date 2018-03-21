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
        @click.native="$router.push({name:'post_class', params:{class_id:props.row.class.id}})"
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
  data () {
    return {
      table_data: [],
      columns: [
        { name: 'minor_category', label: '분류', field: row => row.class.minor_category, sortable: true, align: 'left' },
        { name: 'title', label: '제목', field: row => row.class.title, sortable: true, align: 'left' },
        { name: 'teacher_name', label: '선생님', field: row => row.class.teacher.name, sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['minor_category', 'title', 'teacher_name'],
      item: [],
      major_categories: [],
      minor_categories: []
    }
  },
  props: ['id', 'major_category'],
  methods: {
    fetch_data () {
      let query = {}
      if (this.id) {
        query['student_id'] = this.id
      }
      if (this.major_category) {
        query['major_category'] = this.major_category
      }
      this.$axios.get(`enrollments`, {params: query})
        .then(({ data }) => {
          this.table_data = data
        })
    },
    remove () {
      this.$axios.delete(`enrollments/` +
        this.item[0].class_id + `/` + this.item[0].student_id)
        .then(({ data }) => {
          this.fetch_data()
        })
    }
  },
  created () {
    this.$axios.get(`classes/categories`
    ).then(({ data }) => {
      this.major_categories = data
    })

    this.$axios.get(`classes/categories/` + this.major_category
    ).then(({ data }) => {
      this.minor_categories = data[this.major_category]
      this.fetch_data()
    })
  }
}
</script>
