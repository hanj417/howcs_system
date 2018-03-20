<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout justify-center align-center>
        <v-card>
          <v-data-table :headers='headers' :items='items' :rows-per-page-items='[10, 20, {"text":"All", "value":-1}]'>
            <template slot='items' scope='props'>
              <tr>
                <td v-for='column in columns' v-html="get_column_data(props.item, column)"></td>
                <td class="justify-center layout px-0">
                  <v-btn icon class="mx-0" :to="{name: 'post_class', params: {class_id: props.item.id}}">
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
  </v-content>
</template>

<script>
const get_default_data = () => {
  return {
    columns: [
      {'text': '분류', 'value': 'class.minor_category'},
      {'text': '제목', 'value': 'class.title'},
      {'text': '선생님', 'value': 'class.teacher.name'},
      {'text': '요일', 'value': 'class.weekday'},
      {'text': '시간', 'value': 'class.hour'},
    ],
    headers: [
      {'text': '분류'},
      {'text': '제목', 'width':400},
      {'text': '선생님'},
      {'text': '요일'},
      {'text': '시간'},
      {'text': ''},
    ],
    filters: {},
    items: [],
  }
}

export default {
  data: get_default_data,
  computed: {
    id() {
      return this.$route.params.id
    }
  },
  methods: {
    get_column_data(row, field) {
      // process fields like `type.name`
      let [l1, l2, l3] = field.value.split('.')
      let value = row[l1]
      let tag = null
      if (l2) {
        value = row[l1] ? row[l1][l2] : null
      }
      if (l3) {
        value = row[l1] ? (row[l1][l2] ? row[l1][l2][l3] : null) : null
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
      if (!!this.$route.params.id) {
        this.filters = {
          'student_id': this.$route.params.id
        }
      }
      this.$route.query.query = JSON.stringify(this.filters)
      this.$axios.get(`enrollments`, {params: this.$route.query})
      .then(({ data }) => {
        this.items = data
      })
    },
    remove(item) {
      this.$axios.delete(`enrollments/` + item.class_id + `/` + item.student_id)
      .then(({ data }) => {
        this.fetch_data()
      })
    },
  },
  created () {
    this.fetch_data()
  }
}
</script>
