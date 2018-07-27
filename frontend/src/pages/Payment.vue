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
        @click="$router.push({name:'payment_form_new'})"
        icon="add" />
    </q-page-sticky>

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
        { name: 'cost', label: '납부금액', field: function (row) { return row.cost }, sortable: true, align: 'left' },
        { name: 'date', label: '납부일', field: function (row) { return (new Date(row.date)).toISOString().substr(0, 10) }, sortable: true, align: 'left' },
      ],
      filter: '',
      visible_columns: ['username', 'name', 'cost', 'date'],
      item: [],

      payment_modal: false,
    }
  },
  methods: {
    fetch_data: function () {
      let query = {}
      var self = this
      self.$axios.get('payments', {params: query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
        })
    },
    remove: function () {
      var self = this
      self.$axios.delete('payments/' + self.item[0].id)
        .then(function (response) {
          let data = response.data
          self.fetch_data()
        })
    },
    payment_new: function (row) {
      var self = this
      self.$axios.post('payments', {
        'user_id': row.id
      }).then(function (response) {
        let data = response.data
        self.fetch_data()
      })
      self.payment_modal = false
    },
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
