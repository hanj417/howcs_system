<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout justify-center align-center>
        <v-card>
          <v-data-table :headers='columns' :items='items' :rows-per-page-items='[10, 20, {"text":"All", "value":-1}]'>
            <template slot='items' scope='props'>
              <tr>
                <td v-for='column in columns' v-html="get_column_data(props.item, column)"></td>
                <td class="justify-center layout px-0">
                  <v-btn icon class="mx-0" :to="{name: 'user_form_admin', params: {action:'update', id:props.item.id}} ">
                    <v-icon>edit</v-icon>
                  </v-btn>
                  <v-btn icon class="mx-0" @click="remove(props.item)">
                    <v-icon>delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-card>
      </v-layout>
    </v-container>
    <v-btn fab bottom right color="pink" dark fixed :to="{name: 'user_form', params: {action:'new'}}">
      <v-icon>add</v-icon>
    </v-btn>
  </v-content>
</template>

<script>
const get_default_data = () => {
  return {
    loading: false,
    columns: [
      {'text': '아이디', 'value': 'username'},
      {'text': '이름', 'value': 'name'},
      {'text': '이메일', 'value': 'email'},
      {'text': '전화번호', 'value': 'phone'},
    ],
    items: [],
    filters: {},
  }
}

export default {
  data: get_default_data,
  methods: {
    get_column_data(row, field) {
      // process fields like `type.name`
      let [l1, l2] = field.value.split('.')
      let value = row[l1]
      let tag = null
      if (l2) { value = row[l1] ? row[l1][l2] : null }
      if (field.type === 'image') { tag = 'img' }
      if (tag) { value = `<${tag} src="${value}" class="crud-grid-thumb" controls />` }
      return value
    },
    fetch_data() {
      this.$route.query.query = JSON.stringify(this.filters)
      this.$http.get(`users`, {params: this.$route.query})
      .then(({ data }) => { this.items = data })
    },
    remove(item) {
      this.$http.delete(`users/` + item.id)
      .then(({ data }) => { this.fetch_data() })
    },
  },
  created () {
    this.fetch_data()
  }
}
</script>
