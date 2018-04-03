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
          icon="edit"
          @click="$router.push({name: 'user_form_admin', params: {action:'update', id:item[0].id}})" />
        <q-btn
          color="negative"
          flat
          round
          delete
          icon="delete"
          @click="remove" />
      </template>
      <q-tr slot="body" slot-scope="props" :props="props">
        <q-td key="username" :props="props">{{ props.row.username }}</q-td>
        <q-td key="name" :props="props">{{ props.row.name }}</q-td>
        <q-td key="email" :props="props">{{ props.row.email }}</q-td>
        <q-td key="phone" :props="props">{{ props.row.phone }}</q-td>
        <q-td key="birthday" :props="props">{{ props.row.birthday }}</q-td>
        <q-td key="school" :props="props">{{ props.row.school }}</q-td>
        <q-td key="church" :props="props">{{ props.row.church }}</q-td>
<!--
        <q-td key="calories" :props="props">
          <div class="row items-center justify-between no-wrap">
            <q-btn size="sm" round dense color="secondary" icon="remove" @click="props.row.calories--" class="q-mr-xs" />
            <q-btn size="sm" round dense color="tertiary" icon="add" @click="props.row.calories++" class="q-mr-sm" />
            <div>{{ props.row.calories }}</div>
          </div>
        </q-td>
-->
      </q-tr>
    </q-table>
  </q-page>
</template>

<script>

export default {
  data () {
    return {
      priv: false,
      priv_update: false,
      table_data: [],
      columns: [
        { name: 'username', label: '아이디', field: 'username', sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: 'name', sortable: true, align: 'left' },
        { name: 'role', label: '권한', field: row => {
                JSON.parse(row.role)
            }, sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: 'email', sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: 'phone', sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: 'birthday', sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: 'school', sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: 'church', sortable: true, align: 'left' }
      ],
      filter: '',
      visible_columns: ['username', 'name', 'email', 'phone'],
      item: []
    }
  },
  methods: {
    check_privilege() {
      let query = {priv: 'user'}
      this.$axios.get(`privileges`, {params: query})
        .then(({ data }) => { this.priv = data })

      let update_query = {priv: 'user_update'}
      this.$axios.get(`privileges`, {params: update_query})
        .then(({ data }) => { this.priv_update = data })
    },
    fetch_data () {
      if (this.priv === false) return
      let query = {}
      this.$axios.get(`users`, {params: query})
        .then(({ data }) => { this.table_data = data })
    },
  },
  created () {
    this.check_privilege()
    this.fetch_data()
  }
}
</script>
