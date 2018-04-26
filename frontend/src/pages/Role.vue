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
      <q-tr
        slot="body"
        slot-scope="props"
        @click.native="$router.push({name:'role_form', params:{id: props.row.id}})"
        :props="props">
        <q-td auto-width>
          <q-checkbox
            color="primary"
            v-model="props.selected" />
        </q-td>
        <template v-for="col in props.cols">
          <q-td
            :key="col.name"
            :props="props">{{ col.value }}</q-td>
          </q-td>
        </template>
      </q-tr>
    </q-table>
    <q-page-sticky
      position="bottom-right"
      :offset="[18, 18]">
      <q-btn
        round
        color="primary"
        @click="add_modal = true"
        icon="add" />
    </q-page-sticky>
    <q-modal
      v-model="add_modal"
      class="row justify-center">
      <div class="col-xs-12">
        <q-input
          v-model="role_label"
          float-label="권한 이름" />
        <q-input
          v-model="role_name"
          float-label="권한 영문 이름" />
      </div>
      <div class="row q-ma-md col-xs-12 justify-end">
        <div class="col-xs-5">
          <q-btn
            color="primary"
            @click="role_new"
            label="추가"
          />
          <q-btn
            color="primary"
            @click="add_modal = false"
            label="닫기"
          />
        </div>
      </div>
    </q-modal>
  </q-page>
</template>

<script>

export default {
  data: function () {
    return {
      table_data: [],
      columns: [
        { name: 'label', label: '이름', field: 'label', align: 'center' },
        { name: 'name', label: '영문이름', field: 'name', align: 'center' },
      ],
      filter: '',
      visible_columns: [
        'label',
        'name'],
      item: [],
      add_modal: false,
      role_label: '',
      role_name: ''
    }
  },
  methods: {
    fetch_data: function () {
      let query = {}
      var self = this
      self.$axios.get('privileges/roles', {params: query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
        })
    },
    role_new: function () {
      var self = this
      self.$axios.post('privileges', {
        'name': self.role_name,
        'label': self.role_label
      }).then(function (response) {
        let data = response.data
        self.fetch_data()
      })
      this.add_modal = false
    },
    save: function () {
      var self = this
      self.$axios.put('privileges/' + self.item[0].id, self.item[0])
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
