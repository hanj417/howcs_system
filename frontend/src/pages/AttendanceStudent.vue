<template>
  <q-page
    padding
    class="row justify-center">
    <div>
    <full-calendar
      :events="events"
      locale="ko-kr"
      style="width:600px;"/>
    </div>
  </q-page>
</template>

<script>
import { date } from 'quasar'

export default {
  data: function () {
    return {
      events: [],
      table_data: [],
      columns: [],
      item: [],
      columns_name: { name: 'name', label: '이름', field: 'name', sortable: true, align: 'left' },

      date: null,
      days: 31
    }
  },
  watch: {
    '$route.name': function (val) {
      this.fetch_data()
    },
    'date': function (val) {
      this.fetch_data()
    }
  },
  props: ['class_id', 'student_id'],
  methods: {
    fetch_data: function () {
      let query = {
        'student_id': this.student_id,
        'class_id': this.class_id,
        'date': this.date,
        'days': this.days
      }
      var self = this
      self.$axios.get('attendances', {params: query})
        .then(function (response) {
          let data = response.data
          self.table_data = data
          var attendance
          self.events = []
          for (let i = 0; i < data.length; i++) {
            let event = {
              title: data[i].category,
              start: data[i].date,
              cssClass: 'family',
              YOUR_DATA: {}
            }
            self.events.push(event)
          }
        })
    }
  },
  created: function () {
    let today = new Date()
    today = date.startOfDate(today, 'month')
    this.date = today.toISOString().slice(0, 10)
    this.fetch_data()
  }
}
</script>
