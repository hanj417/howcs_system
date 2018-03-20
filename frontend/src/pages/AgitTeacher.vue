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
                  <v-btn icon class="mx-0" @click="remove(props.item)">
                    <v-icon>delete</v-icon>
                  </v-btn>
                  <v-btn icon class="mx-0" @click="toggle_approval(props.item)">
                    {{ props.item.approval }}
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-card>
      </v-layout>
    </v-container>
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
  }
}

export default {
  data: get_default_data,
  methods: {
    fetch_data() {
      this.$route.query.query = JSON.stringify(this.filters)
      this.$axios.get(`agit_teacher_infos`, {params: this.$route.query})
      .then(({ data }) => {
        this.items = data
      })
    },
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
    remove(item) {
      this.$axios.delete(`agit_teacher_infos/` + item.id)
      .then(({ data }) => {
        this.fetch_data()
      })
    },
    toggle_approval(item) {
      this.$axios.put(`agit_teacher_infos/` + item.id, {
        'approval': !item.approval,
      }).then(({data}) => {
        this.fetch_data()
      })
    },
  },
  created () {
    this.fetch_data()
  }
}
</script>
