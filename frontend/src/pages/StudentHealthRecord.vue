<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 600px; max-width: 90vw;" class="shadow-8">
      <div class="col-xs-12 text-center q-title text-weight-bold q-pa-md">건강 기록부</div>
      <div class="col-xs-10 docs-input q-mx-xl">
        <q-table
          :data="health_table_data"
          :columns="health_columns"
          row-key="id"
          color="secondary"
          class="col-xs-12 no-shadow"
          dense
        >
          <q-tr
            slot="body"
            slot-scope="props"
            :props="props"
            @click.native="$router.push({name:'student_health_record_edit', params:{id:props.row.id}})"
            class="cursor-pointer">
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props">
              {{ col.value }}
            </q-td>
          </q-tr>
        </q-table>
        <div v-if="action == 'edit'" class="row q-ma-md col-xs-12 justify-end">
          <div class="col-xs-3">
            <q-btn
              @click="$router.push({name: 'student_health_record_new', params: {id:user.student_info.student_record.id}})"
              label="추가" />
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'
import { required, email } from 'vuelidate/lib/validators'

export default {
  data () {
    return {
      user: {},
      user_id: '',

      health_table_data: [],
      health_columns: [
        { name: 'date', label: '날짜', field: row => (new Date(row.date)).toISOString().slice(0,10), sortable: true, align: 'left' },
        { name: 'height', label: '신장', field: 'height', sortable: true, align: 'left' },
        { name: 'weight', label: '체중', field: 'weight', sortable: true, align: 'left' },
        { name: 'sight', label: '시력', field: 'sight', sortable: true, align: 'left' },
        { name: 'cavity', label: '충치', field: 'cavity', sortable: true, align: 'left' },
      ],
    }
  },
  props: ['action', 'id'],
  methods: {
  },
  created () {
      this.$axios.get(`users/` + this.id
      ).then(({ data }) => {
        console.log(data)
        this.user = data
        if (data.student_info.student_record.student_health_records) {
          this.health_table_data = data.student_info.student_record.student_health_records
        }
      })
  }
}
</script>
