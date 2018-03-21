<template>
  <q-page
    padding
    class="row justify-center">
    <q-table
      :data="table_data"
      :columns="columns"
      :filter="filter"
      :visible-columns="visible_columns"
      row-key="name"
      color="secondary"
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
        <template v-for="(key, value) in props.row">
          <q-td
            :key="key"
            :props="props">{{ value }}</q-td>
        </template>
      </q-tr>
    </q-table>
  </q-page>
</template>

<script>
const get_default_data = () => {
  return {
    columns: [
      {'text': '아이디', 'value': 'user.username'},
      {'text': '이름', 'value': 'user.name'},
      {'text': '이메일', 'value': 'user.email'},
      {'text': '전화번호', 'value': 'user.phone'}
    ],
    items: [],
    filters: {}
  }
}

export default {
  data () {
    return {
      table_data: [],
      columns: [
        { name: 'teacher.name', label: '선생님', field: row => row.teacher.name, sortable: true, align: 'left' },
        { name: 'title', label: '제목', field: 'title', sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['teacher.name', 'title']
    }
  },

  methods: {
    fetch_data () {
      let query = {}
      this.$axios.get(`agit_teacher_infos`, {params: query})
        .then(({ data }) => {
          this.table_data = data
        })
    },
    remove (item) {
      this.$axios.delete(`agit_teacher_infos/` + item.id)
        .then(({ data }) => {
          this.fetch_data()
        })
    },
    toggle_approval (item) {
      this.$axios.put(`agit_teacher_infos/` + item.id, {
        'approval': !item.approval
      }).then(({data}) => {
        this.fetch_data()
      })
    }
  },
  created () {
    this.fetch_data()
  }
}
</script>
