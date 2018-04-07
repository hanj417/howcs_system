<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 500px; max-width: 80vw;">
      <q-datetime
        v-model="date"
        type="date"
        float-label="생년월일" />
    </div>
    <q-table
      :data="table_data"
      :columns="columns"
      row-key="name"
      color="secondary"
    >
      <q-tr slot="body" slot-scope="props" :props="props">
      <template v-for="col in columns">
        <q-td v-if="col.name == 'name'" :key="col.name" :props="props">{{ props.row.name }}</q-td>
        <q-td v-else :key="col.name" :props="props">
          <q-btn @click="toggle(props.row, col.name)" :label="props.row[col.name]['category']"/>
        </q-td>
      </template>
      </q-tr>
    </q-table>
  </q-page>
</template>

<script>
import { date } from 'quasar'

export default {
  data: function() {
    return {
      table_data: [],
      columns: [
      ],
      item: [],
      columns_name: { name: 'name', label: '이름', field: 'name', sortable: true, align: 'left' },

      categories: [],
      date: null,
      days: 5,
    }
  },
  watch: {
    '$route.name': function (val) {
      this.fetch_data()
    },
    'date': function (val) {
      this.date = val
      this.fetch_data()
    },
  },
  props: ['class_id'],
  methods: {
    fetch_data: function() {
      let d = new Date(this.date)
      let days = this.days
      this.columns = [this.columns_name]
      while (days) {
        if (date.getDayOfWeek(d) < 1 || date.getDayOfWeek(d) > 5) {
          d = date.addToDate(d, {days: 1})
          continue 
        }
        
        let new_column = {
          name: date.formatDate(d, 'YYYY-MM-DD'),
          label: date.formatDate(d, 'YYYY-MM-DD'),
          field: date.formatDate(d, 'YYYY-MM-DD'),
          align: 'center',
        }
        this.columns.push(new_column)
        d = date.addToDate(d, {days: 1})
        days = days - 1
      }
    
      let query = {
        'class_id': this.class_id,
        'date': (new Date(this.date)).toISOString().slice(0,10),
        'days': this.days,
      }
      var self = this
      self.$axios.get('attendances', {params: query})
      .then(function(response) { let data = response.data
        console.log(data)
        self.table_data = data
      })
    },
    toggle: function (item, index) {
      var i = this.categories.indexOf(item[index]['category'])
      i = (i + 1) % this.categories.length
      item[index]['category'] = this.categories[i]

      var self = this
      if (i === 0) {
        self.$axios.delete('attendances/' + item[index]['id']
        ).then(function(response) { let data = response.data
          self.fetch_data()
        })
      } else if (i === 1) {
        self.$axios.post('attendances', {
          'class_id': self.class_id,
          'student_id': item['id'],
          'date': index,
          'category': item[index]['category']
        }).then(function(response) { let data = response.data
          self.fetch_data()
        })
      } else {
        self.$axios.put('attendances/' + item[index]['id'], {
          'class_id': self.class_id,
          'student_id': item['id'],
          'date': index,
          'category': item[index]['category']
        }).then(function(response) { let data = response.data
          self.fetch_data()
        })
      }
    }
  },
  created: function () {
    var self = this
    self.$axios.get('attendances/categories')
      .then(function(response) { let data = response.data
        self.categories = data
      })

    var today = new Date()
    this.date = today.toISOString().slice(0, 10)
    this.fetch_data()
  }
}
</script>
