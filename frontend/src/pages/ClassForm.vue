<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 600px; max-width: 90vw;">
      <div
        v-if="role == 'admin'"
        class="col-xs-12 docs-input">
        <q-field
          label="선생님"
          icon="account circle"
          :label-width="3"
        >
          <q-input
            v-model="teacher.name"
            class="col-xs-8"
            disabled />
          <q-btn
            class="col-xs-4 float-right"
            @click="search"
            label="교사 입력" />
        </q-field>
      </div>
      <div class="col-xs-12 q-pt-xl docs-input">
        <q-field
          label="제목"
          icon="create"
          :label-width="3"
          :error="$v.title.$error"
          error-label="이름을 잘못 입력하였습니다.">
          <q-input v-model="title" />
        </q-field>
        <q-field
          label="분류"
          icon="create"
          :label-width="3">
          <q-option-group
            type="radio"
            v-model="minor_category"
            inline
            :options="minor_categories" />
        </q-field>
        <q-field
          label="해당년도"
          icon="create"
          :label-width="3"
          :error="$v.year.$error"
          error-label="이름을 잘못 입력하였습니다.">
          <q-input v-model="year" />
        </q-field>
        <q-field
          label="학기"
          icon="create"
          :label-width="3">
          <q-select v-model="semester" :options="semester_option" />
        </q-field>
        <q-field
          label="수업시간"
          icon="create"
          :label-width="3">
          <q-select v-model="time_slot_weekday" :options="weekday" class="col-xs-3" placeholder="요일"/>
          <q-input v-model="time_slot_hour" placeholder="시간" />
        </q-field>
        <q-field
          label="구글캘린더ID"
          icon="create"
          :label-width="3">
          <q-input v-model="google_calendar" />
        </q-field>
        <q-field
          label="대상"
          icon="create"
          :label-width="3">
          <q-select chips multiple v-model="audience" :options="ages" />
        </q-field>
        <q-field
          label="배경"
          icon="create"
          :label-width="3">
          <q-input v-model="background" type="textarea"/>
        </q-field>
        <q-field
          label="내용"
          icon="create"
          :label-width="3">
          <q-input v-model="content" type="textarea"/>
        </q-field>
        <q-field
          label="승인"
          icon="create"
          :label-width="3">
          <q-select :disabled="$route.name != 'class_form_edit' || !priv_del" v-model="approval" :options="approval_options"/>
        </q-field>
      </div>
      <div class="col-xs-12 row justify-end q-mt-lg">
        <div class="col-xs-5">
          <q-btn
            @click="$router.go(-1)"
            label="취소" />
          <q-btn
            v-if="$route.name == 'class_form_edit' && priv_del"
            @click="remove"
            label="삭제" />
          <q-btn
            v-if="$route.name == 'class_form_new' && priv_new"
            @click="class_new"
            label="등록" />
          <q-btn
            v-if="$route.name == 'class_form_edit' && priv_update"
            @click="class_update"
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
      priv_new: false,
      priv_update: false,
      priv_del: false,
      teacher_select: false,
      teacher: {name: '' },
      title: '',
      minor_categories: [],
      minor_category: '',
      year: '2018',
      semester: '',
      semester_option : [
        {label: '봄', value: 'spring'},
        {label: '여름', value: 'summer'},
        {label: '가을', value: 'fall'},
        {label: '겨울', value: 'winter'},
        {label: '전체', value: 'year'},
      ],
      time_slot: '',
      time_slot_weekday: '',
      time_slot_hour: '',
      weekday: [
        {label: '월', value: 'mon'},
        {label: '화', value: 'tue'},
        {label: '수', value: 'wed'},
        {label: '목', value: 'thu'},
        {label: '금', value: 'fri'},
        {label: '토', value: 'sat'},
      ],
      google_calendar: '',
      audience: [],
      audience_min: '',
      audience_max: '',
      background: '',
      content: '',
      save_label: '등록',
      ages: [
        {label: '1세', value: '1'},
        {label: '2세', value: '2'},
        {label: '3세', value: '3'},
        {label: '4세', value: '4'},
        {label: '5세', value: '5'},
        {label: '6세', value: '6'},
        {label: '7세', value: '7'},
        {label: '8세', value: '8'},
        {label: '9세', value: '9'},
        {label: '10세', value: '10'},
        {label: '11세', value: '11'},
        {label: '12세', value: '12'},
        {label: '13세', value: '13'},
        {label: '14세', value: '14'},
        {label: '15세', value: '15'},
        {label: '16세', value: '16'},
        {label: '17세', value: '17'},
        {label: '18세', value: '18'},
        {label: '19세', value: '19'},
        {label: '20세', value: '20'},
        {label: '성인', value: 'adult'},
      ],
      approval: false,
      approval_options: [
        {label: '승인', value: true},
        {label: '대기', value: false},
      ],

      search_modal: false,
      search_table_data: [],
      search_columns: [
        { name: 'username', label: '아이디', field: function (row) { return row.user.username }, sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: function (row) { return row.user.name }, sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: function (row) { return row.user.email }, sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: function (row) { return row.user.phone }, sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: function (row) { return row.user.birthday }, sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: function (row) { return row.user.school }, sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: function (row) { return row.user.church }, sortable: true, align: 'left' }
      ],
      search_filter: '',
      search_visible_columns: ['username', 'name', 'email', 'phone'],
      search_item: []
    }
  },
  validations: {
    title: { required },
    year: { required }
  },
  props: ['role', 'major_category', 'class_id'],
  methods: {
    check_priv: function () {
      var self = this
      let priv_new_query = {priv: this.major_category + '_class_new'}
      self.$axios.get('privileges', {params: priv_new_query})
        .then(function (response) {
          let data = response.data
          self.priv_new = data
        })
  
      let priv_update_query = {priv: this.major_category + '_class_update'}
      self.$axios.get('privileges', {params: priv_update_query})
        .then(function (response) {
          let data = response.data
          self.priv_update = data
        })
  
      let priv_del_query = {priv: this.major_category + '_class_del'}
      self.$axios.get('privileges', {params: priv_del_query})
        .then(function (response) {
          let data = response.data
          self.priv_del = data
        })
    },
    fetch_class_categories: function () {
      var self = this
      self.$axios.get('classes/categories/' + self.major_category)
        .then(function (response) {
          let data = response.data
          self.minor_categories = data
        })
    },
    class_new: function () {
      var self = this
      if (!self.priv_new)
        return

      this.time_slot = this.time_slot_weekday + ',' + this.time_slot_hour
        self.$axios.post('classes', {
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
          'content': self.content
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
    class_approve: function () {
      var self = this
      if (!self.priv_del)
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
          'approval': !self.approval,
        }).then(function (response) {
          let data = response.data
          self.approval = data.approval
        if (self.approval) {
          self.approval_str = '승인'
        } else {
          self.approval_str = '대기'
        }
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
      self.$axios.get('howcs_teacher_infos', {params: query})
        .then(function (response) {
          let data = response.data
          self.search_table_data = data
        })
      self.search_modal = true
    },
    search_select: function (row) {
      this.teacher = row.user
      this.search_modal = false
    }
  },
  created: function () {
    let user = LocalStorage.get.item('user_')
    if (this.role === 'admin') {
      this.teacher_select = true
    } else if (this.role === 'teacher') {
      this.teacher = user
    } else {
      this.$router.go(-1)
    }

    this.check_priv()
    this.fetch_class_categories()

    if (this.$route.name === 'class_form_edit') {
      var self = this
      self.$axios.get('classes/' + self.class_id
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
  }
}
</script>
