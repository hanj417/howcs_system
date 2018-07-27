<template>
  <q-page
    padding
    class="row justify-center">
    <q-table
      :data="table_data"
      :columns="columns"
      :filter="filter"
      :visible-columns="visible_columns"
      :pagination.sync="pagination"
      row-key="name"
      color="secondary"
      class="col-xs-11"
      dense
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
            v-if="col.name == 'category'"
            :key="col.name"
            :props="props">{{ category_label[col.value] }}</q-td>
          <q-td
            v-else
            :key="col.name"
            :props="props">
            <q-toggle v-model="props.row[col.name]" @click.native="save(props.row, col.name)" />
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
      table_data: [],
      columns: [
        { name: 'category', label: '이름', field: 'category', align: 'center' },
        { name: 'view', label: '조회', field: 'view', align: 'center' },
        { name: 'new', label: '생성', field: 'new', align: 'center' },
        { name: 'update', label: '수정', field: 'update', align: 'center' },
        { name: 'del', label: '삭제', field: 'del', align: 'center' },
      ],
      filter: '',
      visible_columns: [
        'category',
        'view',
        'new',
        'update',
        'del'],
      category_label: {
        'user': '사용자',
        'student': '학생',
        'howcs_teacher': '하우학교교사',
        'howcs_class': '하우학교수업',
        'howcs_enrollment': '하우학교수강',
        'howcs_attendance': '하우학교출석',
        'howcs_student_health_record': '하우학교건강기록',
        'howcs_post': '하우학교공지',
        'agit_teacher': '아지트교사',
        'agit_class': '아지트수업',
        'agit_enrollment': '아지트수강',
        'agit_attendance': '아지트출석',
        'homepage_post': '홈페이지게시',
      },
      item: [],
      add_modal: false,
      role_label: '',
      role_name: '',
      pagination: {
        sortBy: null, // String, column "name" property value
        descending: false,
        page: 1,
        rowsPerPage: 0 // current rows per page being displayed
      },

    }
  },
  props: ['id'],
  methods: {
    fetch_data: function () {
      let query = {}
      var self = this
      self.$axios.get('privileges/' + this.id, {params: query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
        })
    },
    save: function (row, col_name) {
      var self = this
      let priv_name = row.category
      if (col_name != 'view') {
        priv_name += "_" + col_name
      } 
      let query = {}
      query[priv_name] = row[col_name]
      self.$axios.put('privileges/' + self.id, query)
        .then(function (response) {
          let data = response.data
          self.fetch_data()
        })
    },
    remove: function () {
      var self = this
      self.$axios.delete('privileges/' + self.item[0].id)
        .then(function (response) {
          let data = response.data
          self.fetch_data()
        })
    }
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
