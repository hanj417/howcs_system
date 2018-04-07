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
<!--
    <v-btn fab bottom right color="pink" dark fixed :to="{name: 'payment_form', params: {action:'new'}}">
      <v-icon>add</v-icon>
    </v-btn>
-->
</template>

<script>
export default {
  data: function() {
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
    fetch_data: function() {
      let query = {}
      var self = this
      self.$axios.get('payments', {params: query})
        .then(function(response) { let data = response.data self.items = data })
    },
    remove: function (item) {
      var self = this
      self.$axios.delete('payments/' + item.id)
        .then(function(response) { let data = response.data self.fetch_data() })
    }
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
/*
const get_default_data = () => {
  return {
    columns: [
      {'text': '이름', 'value': 'user.name'},
      {'text': 'Email', 'value': 'user.email'},
      {'text': '전화번호', 'value': 'user.phone'},
      {'text': '금액', 'value': 'cost'},
      {'text': '분류', 'value': 'major_category'},
    ],
    items: [],
    filters: {},
    search_name: '',
  }
}

*/
