<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 600px; max-width: 90vw;">
      <div
        class="col-xs-12 docs-input">
        <q-field
          label="아이디"
          icon="account circle"
          :label-width="3"
        >
          <q-input
            v-model="user.username"
            class="col-xs-8"
            disabled />
          <q-btn
            class="col-xs-4 float-right"
            @click="search"
            label="검색" />
        </q-field>
      </div>
      <div class="col-xs-12 q-pt-xl docs-input">
        <q-field
          label="이름"
          icon="create"
          :label-width="3"
          disabled>
          <q-input v-model="user.name" />
        </q-field>
        <q-field
          label="분류"
          icon="create"
          :label-width="3">
          <q-option-group
            type="radio"
            v-model="form.major_category"
            inline
            :options="major_categories" />
        </q-field>
        <q-field
          label="해당년도"
          :label-width="3"
          icon="create">
          <q-input v-model="form.year" />
        </q-field>
        <q-field
          label="학기"
          icon="create"
          :label-width="3">
          <q-select v-model="form.semester" :options="semester_option" />
        </q-field>
        <q-field
          label="납부일"
          icon="cake"
          :label-width="3"
          :error="$v.form.date.$error"
          error-label="날짜를 잘못 입력하였습니다."
        >
          <q-datetime
            v-model="form.date"
            type="date" />
        </q-field>
        <q-field
          label="금액"
          icon="create"
          :label-width="3">
          <q-input v-model="form.cost" />
        </q-field>
      </div>
      <div class="col-xs-12 row justify-end q-mt-lg">
        <div class="col-xs-5">
          <q-btn
            @click="$router.go(-1)"
            label="취소" />
          <q-btn
            v-if="$route.name == 'payment_form_edit' && priv_del"
            @click="remove"
            label="삭제" />
          <q-btn
            v-if="$route.name == 'payment_form_new' && priv_new"
            @click="payment_new"
            label="등록" />
          <q-btn
            v-if="$route.name == 'payment_form_edit' && priv_update"
            @click="payment_update"
            label="수정" />
        </div>
      </div>
    </div>
    <q-modal
      v-model="search_modal"
      class="row justify-center">
      <q-table
        :data="search_table_data"
        :columns="search_columns"
        :filter="search_filter"
        :visible-columns="search_visible_columns"
        row-key="id"
        color="secondary"
        class="col-xs-12 no-shadow"
      >
        <template
          slot="top-left"
          slot-scope="props">
          <q-search
            hide-underline
            color="secondary"
            v-model="search_filter"
            class="col-6"
          />
        </template>
        <template
          slot="top-right"
          slot-scope="props">
          <q-table-columns
            color="secondary"
            class="q-mr-sm"
            v-model="search_visible_columns"
            :columns="search_columns"
          />
        </template>
        <q-tr
          slot="body"
          slot-scope="props"
          :props="props"
          @click.native="search_select(props.row)"
          class="cursor-pointer">
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props">
            {{ col.value }}
          </q-td>
        </q-tr>
      </q-table>
    </q-modal>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'
import { required, email } from 'vuelidate/lib/validators'

export default {
  data: function () {
    return {
      priv_new: true,
      priv_update: true,
      priv_del: false,
      user: { username: '', },
form: {
      cost: '',
      date: '',
      major_category: '',
      year: '2018',
      semester: '',
},
      major_categories: [],
      semester_option : [
        {label: '봄', value: 'spring'},
        {label: '여름', value: 'summer'},
        {label: '가을', value: 'fall'},
        {label: '겨울', value: 'winter'},
        {label: '전체', value: 'year'},
      ],

      search_modal: false,
      search_table_data: [],
      search_columns: [
        { name: 'username', label: '아이디', field: function (row) { return row.username }, sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: function (row) { return row.name }, sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: function (row) { return row.email }, sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: function (row) { return row.phone }, sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: function (row) { return row.birthday }, sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: function (row) { return row.school }, sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: function (row) { return row.church }, sortable: true, align: 'left' }
      ],
      search_filter: '',
      search_visible_columns: ['username', 'name', 'email', 'phone'],
      search_item: []
    }
  },
  props: ['id'],
  validations: {
form: {
    cost: { required },
    major_category: { required },
    year: { },
    semester: { },
    date: { },
}
  },
  methods: {
    check_priv: function () {
    },
    fetch_class_categories: function () {
      var self = this
      self.$axios.get('classes/categories')
        .then(function (response) {
          let data = response.data
          self.major_categories = data
        })
    },
    payment_new: function () {
      var self = this

        self.$axios.post('payments', {
          'user_id': self.user.id,
          'cost': self.form.cost,
          'major_category': self.form.major_category,
          'year': self.form.year,
          'semester': self.form.semester,
          'date': (new Date(self.form.date)).toISOString().substr(0, 10)
        }).then(function (response) {
          let data = response.data
          self.$router.go(-1)
        })
    },
    class_update: function () {
      var self = this
      if (!self.priv_update)
        return

      this.time_slot = this.time_slot_weekday + ',' + this.time_slot_hour

        self.$axios.put('classes/' + self.class_id, {
          'teacher_id': self.teacher.id,
          'title': self.title,
          'major_category': self.major_category,
          'minor_category': self.minor_category,
          'year': self.year,
          'semester': self.semester,
          'time_slot': self.time_slot,
          'google_calendar': self.google_calendar,
          'audience': self.audience.toString(),
          'background': self.background,
          'content': self.content,
          'approval': self.approval
        }).then(function (response) {
          let data = response.data
          self.$router.go(-1)
        })
    },
    remove: function () {
      var self = this
      self.$axios.delete('classes/' + self.class_id)
        .then(function (response) {
          let data = response.data
          self.$router.go(-1)
        })
    },
    search: function () {
      let query = {}
      var self = this
      self.$axios.get('users', {params: query})
        .then(function (response) {
          let data = response.data
          self.search_table_data = data
        })
      self.search_modal = true
    },
    search_select: function (row) {
      this.user = row
      this.search_modal = false
    }
  },
  created: function () {
    this.check_priv()
    this.fetch_class_categories()

/*
    if (this.$route.name === 'payment_form_edit') {
      var self = this
      self.$axios.get('payments/' + self.id
      ).then(function (response) {
        let data = response.data
        self.teacher = data.teacher
        self.teacher_select = false
        self.title = data.title
        self.major_category = data.major_category
        self.minor_category = data.minor_category
        self.year = data.year
        self.semester = data.semester
        self.time_slot = data.time_slot
        self.time_slot_weekday = self.time_slot.split(',')[0]
        self.time_slot_hour = self.time_slot.split(',')[1]
        self.google_calendar = data.google_calendar
        self.audience = data.audience.split(',')
        self.background = data.background
        self.content = data.content
        self.approval = data.approval
        if (self.approval) {
          self.approval_str = '승인'
        } else {
          self.approval_str = '대기'
        }
      })
    }
*/
  }
}
</script>
