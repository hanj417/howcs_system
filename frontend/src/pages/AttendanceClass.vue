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
  data () {
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
    '$route.name' (val) {
      this.fetch_data()
    },
    'date' (val) {
      this.date = val
      this.fetch_data()
    },
  },
  props: ['class_id'],
  methods: {
    fetch_data () {
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
      this.$axios.get(`attendances`, {params: query})
      .then(({ data }) => {
        console.log(data)
        this.table_data = data
      })
    },
    toggle (item, index) {
      var i = this.categories.indexOf(item[index]['category'])
      i = (i + 1) % this.categories.length
      item[index]['category'] = this.categories[i]

      if (i === 0) {
        this.$axios.delete(`attendances/` + item[index]['id']
        ).then(({data}) => {
          this.fetch_data()
        })
      } else if (i === 1) {
        this.$axios.post(`attendances`, {
          'class_id': this.class_id,
          'student_id': item['id'],
          'date': index,
          'category': item[index]['category']
        }).then(({data}) => {
          this.fetch_data()
        })
      } else {
        this.$axios.put(`attendances/` + item[index]['id'], {
          'class_id': this.class_id,
          'student_id': item['id'],
          'date': index,
          'category': item[index]['category']
        }).then(({data}) => {
          this.fetch_data()
        })
      }
    }
  },
  created () {
    this.$axios.get(`attendances/categories`)
      .then(({ data }) => {
        this.categories = data
      })

    var today = new Date()
    this.date = today.toISOString().slice(0, 10)
    this.fetch_data()
  }
}
</script>
