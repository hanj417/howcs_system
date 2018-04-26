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
<!--
        <q-tr
          slot="body"
          slot-scope="props"
          :props="props">
          <template v-for="col in columns">
            <q-td
              v-if="visible_columns.includes(col.name) && col.name != 'approval'"
              :key="col.name"
              :props="props">{{ col.field(props.row) }}</q-td>
            <q-td
              v-else-if="col.name == 'approval'"
              :key="col.name"
              :props="props">
              <q-btn 
                @click="toggle(props.row)"
                :label="col.field(props.row)" />
            </q-td>
          </template>
        </q-tr>
-->
    </q-table>
  </q-page>
</template>

<script>
export default {
  data: function () {
    return {
      table_data: [],
      columns: [
        { name: 'username', label: '아이디', field: function (row) { return row.user.username }, sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: function (row) { return row.user.name }, sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: function (row) { return row.user.email }, sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: function (row) { return row.user.phone }, sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: function (row) { return row.user.birthday }, sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: function (row) { return row.user.school }, sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: function (row) { return row.user.church }, sortable: true, align: 'left' },
        { name: 'approval', label: '승인', field: function (row) { if (row.approval) { return "승인"} return "대기" }, sortable: true, align: 'left' },
        { name: 'career', label: '이력', field: function (row) { return row.career }, sortable: true, align: 'left' },
      ],
      filter: '',
      visible_columns: ['username', 'name', 'email', 'career', 'approval'],
      item: [],
    }
  },
  methods: {
    fetch_data: function () {
      let query = {}
      var self = this
      self.$axios.get('agit_teacher_infos', {params: query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
        })
    },
    rowClick: function (row) {
      this.$router.push({name: 'user_form_admin', params: {id: row.user_id, action: 'update'}})
    },
    toggle: function (item) {
      var self = this
      self.$axios.put('agit_teacher_infos/' + item.id, {
          'approval': !item.approval
        }).then(function (response) {
          let data = response.data
          self.fetch_data()
        })
    },
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
