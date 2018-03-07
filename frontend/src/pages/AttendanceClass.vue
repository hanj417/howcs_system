<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-form v-model="valid" ref="form" lazy-validation>
          <v-flex xs12>
            <v-layout>
              <v-menu ref="menu" lazy :close-on-content-click="false" v-model="menu" transition="scale-transition" offset-y full-width :nudge-right="40" min-width="290px" :return-value.sync="date">
                <v-text-field slot="activator" label="Picker in menu" v-model="date" prepend-icon="event" readonly></v-text-field>
                <v-date-picker v-model="date" no-title scrollable>
                  <v-spacer></v-spacer>
                  <v-btn flat color="primary" @click="menu = false">취소</v-btn>
                  <v-btn flat color="primary" @click="$refs.menu.save(date)">결정</v-btn>
                </v-date-picker>
              </v-menu>
            </v-layout>
          </v-flex>
        </v-form>
      </v-layout>
      <v-layout justify-center align-center>
        <v-card>
          <v-data-table :headers='columns' :items='attendance_items' :rows-per-page-items='[10, 20, {"text":"All", "value":-1}]'>
            <template slot='items' scope='props'>
              <tr>
                <td>{{ props.item['name'] }}</td>
                <td v-for='column in columns'>
                  <v-btn small @click="toggle(props.item, column.value)">
                    {{ props.item[column.value].value }}
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
    columns: [],
    filters: {},
    enrollment_items: [],
    attendance_items: [],
    student_id_items: {},

    date: null,
    menu: false,
    first_date: null,
    last_date: null,

    categories: [],
  }
}

export default {
  data: get_default_data,
  watch: {
    date: function(val) {
      console.log(val)
      this.set_date(val)
      this.fetch_data()
    }
  },
  computed: {
    id() {
      return this.$route.params.id
    }
  },
  methods: {
    set_date(date) {
      this.first_date = new Date(date)
      this.last_date = new Date(date)
      this.first_date.setDate(this.first_date.getDate() - this.first_date.getDay() + 1)
      this.last_date.setDate(this.first_date.getDate() + 4)
      console.log(this.first_date.toISOString())
      console.log(this.last_date.toISOString())
      this.fetch_data()
    },
    fetch_attendance_data() {
      // set attendance to default data
      this.attendance_items = []
      for (var i = 0; i < this.enrollment_items.length; i++) {
        this.student_id_items[this.enrollment_items[i].student_id] = i
        var item = {}
        item['id'] = this.enrollment_items[i].student_id
        item['name'] = this.enrollment_items[i].student.name
        for (var d = new Date(this.first_date.getTime()); d <= this.last_date; d.setDate(d.getDate() + 1)) {
          item[d.toISOString().slice(0,10)] = {}
          item[d.toISOString().slice(0,10)]['value'] = '출석'
          item[d.toISOString().slice(0,10)]['id'] = null 
        }
        this.attendance_items.push(item)
      }

      // fetch attendance data
      for (var i = 0; i < this.enrollment_items.length; i++) {
        var student_id = this.enrollment_items[i].student_id
        for (var d = new Date(this.first_date.getTime()); d <= this.last_date; d.setDate(d.getDate() + 1)) {
          this.$http.get(`attendances`, {params: {class_id: this.$route.params.id, student_id:student_id, date:d.toISOString().slice(0,10)}})
          .then(({ data }) => {
            var index = this.student_id_items[student_id]
            if (data.length != 0) {
              var dd = new Date(data[0].date)
              this.attendance_items[index][dd.toISOString().slice(0,10)]['value'] = data[0].category
              this.attendance_items[index][dd.toISOString().slice(0,10)]['id'] = data[0].id
            }
          })
        }
      }
    },
    fetch_data() {
      this.filters = {
        'class_id': this.$route.params.id,
      }
      this.$route.query.query = JSON.stringify(this.filters)
      this.$http.get(`enrollments`, {params: this.$route.query}).then(({ data }) => {
console.log(data)
        this.enrollment_items = data
        this.fetch_attendance_data()
      })

      // column setting
      this.columns = []
      //this.columns = [{'text':'이름', 'value':'name'}]
      for (var d = new Date(this.first_date.getTime()); d <= this.last_date; d.setDate(d.getDate() + 1)) {
        this.columns.push({'text':d.toISOString().slice(0,10), 'value':d.toISOString().slice(0,10)})
      }
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
      value = `<v-btn>${value}</v-btn>`
      return value
    },
    toggle(item, index) {
      var i = this.categories.indexOf(item[index].value)
      i = (i + 1) % this.categories.length
      item[index].value = this.categories[i]

      if (i == 0) {
        this.$http.delete(`attendances/` + item[index].id
        ).then(({data}) => {
          this.fetch_data()
        })
      } else if (i == 1) {
        this.$http.post(`attendances`, {
          'class_id': this.$route.params.id,
          'student_id': item.id,
          'date': index,
          'category': item[index].value,
        }).then(({data}) => {
          item[index].id = data.id
          this.fetch_data()
        })
      } else {
        this.$http.put(`attendances/` + item[index].id, {
          'class_id': this.$route.params.id,
          'student_id': item.id,
          'date': index,
          'category': item[index].value,
        }).then(({data}) => {
          this.fetch_data()
        })
      }
    }
  },
  created () {
    this.$http.get(`attendances/categories`)
    .then(({ data }) => {
      this.categories = data
    })

    this.date = new Date()
    this.date = this.date.toISOString().slice(0,10)
    this.set_date(this.date)
    this.fetch_data()
  }
}
</script>
