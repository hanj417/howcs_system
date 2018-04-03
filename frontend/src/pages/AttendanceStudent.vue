<template>
  <q-page
    padding
    class="row justify-center">
<full-calendar :events="events" locale="ko-kr" style="width:600px;"></full-calendar>
  </q-page>
</template>

<script>
import { date } from 'quasar'

export default {
  data () {
    return {
events: [],
      table_data: [],
      columns: [
      ],
      item: [],
      columns_name: { name: 'name', label: '이름', field: 'name', sortable: true, align: 'left' },

      categories: [],
      date: null,
      days: 31,
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
  props: ['class_id', 'student_id'],
  methods: {
    fetch_data () {
      let query = {
        'student_id': this.student_id,
        'class_id': this.class_id,
        'date': this.date,
        'days': this.days,
      }
      this.$axios.get(`attendances`, {params: query})
      .then(({ data }) => {
        console.log(data)
        this.table_data = data
        var attendance
        this.events = []
        for (let i = 0; i < data.length; i ++) {
          let event = {
    title     :  data[i].category,
    start     : data[i].date,
    cssClass  : 'family',
    YOUR_DATA : {}
          }
          this.events.push(event)
        }
      })
    },
  },
  created () {
    this.$axios.get(`attendances/categories`)
      .then(({ data }) => {
        this.categories = data
      })

    var today = new Date()
    today = date.startOfDate(today, 'month')
    this.date = today.toISOString().slice(0, 10)
    this.fetch_data()
  }
}
</script>
