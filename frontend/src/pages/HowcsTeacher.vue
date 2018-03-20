<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout justify-center align-center>
        <v-card>
          <v-data-table :headers='columns' :items='items'>
            <template slot='items' scope='props'>
              <tr>
                <td v-for='column in columns' v-html="get_column_data(props.item, column)"></td>
                <td class="justify-center layout px-0">
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
    <v-btn fab bottom right color="pink" dark fixed @click="search">
      <v-icon>add</v-icon>
    </v-btn>
      <v-dialog v-model="search_dialog" width="60%">
        <v-card>
          <v-card-title class="title">학생 검색</v-card-title>
          <v-flex xs6 offset-xs2>
            <v-text-field label="검색" single-line hide-details v-model="search_name"></v-text-field>
          </v-flex>
          <v-card-text class="pt-4">
            <v-data-table :headers='search_columns' :items='search_items' :search="search_name">
              <template slot='items' scope='props'>
                <tr>
                  <td v-for='column in search_columns' v-html="get_column_data(props.item, column)"></td>
                  <td class="justify-center layout px-0">
                    <v-btn small icon class="mx-0" @click="search_select(props.item)"><v-icon>add</v-icon></v-btn>
                  </td>
                </tr>
              </template>
            </v-data-table>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              flat
              color="purple"
              @click="search_dialog = false"
            >취소</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-content>
</template>

<script>
const get_default_data = () => {
  return {
    columns: [
      {'text': '아이디', 'value': 'user.username'},
      {'text': '이름', 'value': 'user.name'},
      {'text': '이메일', 'value': 'user.email'},
      {'text': '전화번호', 'value': 'user.phone'},
    ],
    items: [],
    filters: {},
    search_dialog: false,
    search_name: '',
    search_items: [],
    search_columns: [
      {'text': '아이디', 'value': 'username'},
      {'text': '이름', 'value': 'name'},
      {'text': '이메일', 'value': 'email'},
      {'text': '전화번호', 'value': 'phone'},
    ],
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
      if (l2) {
        value = row[l1] ? row[l1][l2] : null
      }
      if (field.type === 'image') {
        tag = 'img'
      }
      if (tag) {
        value = `<${tag} src="${value}" class="crud-grid-thumb" controls />`
      }
      return value
    },
    fetch_data() {
      this.$route.query.query = JSON.stringify(this.filters)
      this.$axios.get(`howcs_teacher_infos`, {params: this.$route.query})
      .then(({ data }) => {
        this.items = data
      })
    },
    remove(item) {
      this.$axios.delete(`howcs_teacher_infos/` + item.id)
      .then(({ data }) => {
        this.fetch_data()
      })
    },
    howcs_teacher_new(item) {
      this.$axios.post(`howcs_teacher_infos`, {
        'user_id': item.id
      }).then(({ data }) => {
        this.fetch_data()
      })
    },
    search() {
      this.$route.query.query = JSON.stringify(this.filters)
      this.$axios.get(`users`, {params: this.$route.query})
      .then(({ data }) => {
        this.search_items = data
      })
      this.search_dialog = true
    },
    search_select(item) {
      this.howcs_teacher_new(item)
    }
  },
  created () {
    this.fetch_data()
  }
}
</script>
