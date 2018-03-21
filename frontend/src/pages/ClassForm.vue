<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 600px; max-width: 90vw;">
      <div class="col-xs-12 docs-input">
        <q-field
          label="선생님"
          icon="account circle"
          :label-width="3"
          disabled
        >
          <q-input v-model="teacher.name" />
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
          label="대분류"
          icon="create"
          :label-width="3">
          <q-option-group
            type="radio"
            v-model="major_category"
            inline
            :options="major_categories" />
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
          <q-input v-model="semester" />
        </q-field>
        <q-field
          label="수업시간"
          icon="create"
          :label-width="3">
          <q-input v-model="time_slot" />
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
          <q-input v-model="audience" />
        </q-field>
        <q-field
          label="배경"
          icon="create"
          :label-width="3">
          <q-input v-model="background" />
        </q-field>
        <q-field
          label="내용"
          icon="create"
          :label-width="3">
          <q-input v-model="content" />
        </q-field>
      </div>
      <div class="col-xs-12 row justify-end q-mt-lg">
        <div
          v-if="teacher_select"
          class="col-xs-4">
          <q-btn
            @click="search"
            label="선생님 검색" />
        </div>
        <div class="col-xs-2">
          <q-btn
            @click="save"
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
        selection="single"
        :selected.sync="search_item"
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
        <template
          slot="top-selection"
          slot-scope="props">
          <div class="col" />
          <q-btn
            color="negative"
            flat
            round
            icon="add"
            @click="search_select" />
        </template>
      </q-table>
      <div class="row q-ma-md col-xs-12 justify-end">
        <div class="col-xs-2">
          <q-btn
            color="primary"
            @click="search_modal = false"
            label="닫기"
          />
        </div>
      </div>
    </q-modal>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'
import { required, email } from 'vuelidate/lib/validators'

export default {
  data () {
    return {
      teacher_select: false,
      teacher: {name: '' },
      title: '',
      major_categories: [],
      major_category: {},
      minor_categories: [],
      minor_category: '',
      year: '2018',
      semester: '',
      time_slot: '',
      google_calendar: '',
      audience: '',
      background: '',
      content: '',

      search_modal: false,
      search_table_data: [],
      search_columns: [
        { name: 'username', label: '아이디', field: row => row.user.username, sortable: true, align: 'left' },
        { name: 'name', label: '이름', field: row => row.user.name, sortable: true, align: 'left' },
        { name: 'email', label: '이메일', field: row => row.user.email, sortable: true, align: 'left' },
        { name: 'phone', label: '전화번호', field: row => row.user.phone, sortable: true, align: 'left' },
        { name: 'birthday', label: '생년월일', field: row => row.user.birthday, sortable: true, align: 'left' },
        { name: 'school', label: '소속학교', field: row => row.user.school, sortable: true, align: 'left' },
        { name: 'church', label: '출석교회', field: row => row.user.church, sortable: true, align: 'left' }
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
  props: ['action', 'id'],
  watch: {
    'major_category' (val) {
      this.$axios.get(`classes/categories/` + this.major_category
      ).then(({ data }) => {
        this.minor_categories = data
      })
    }
  },
  methods: {
    fetch_data () {
      let query = {
        class: this.id
      }
      this.$axios.get(`enrollments`, {params: query})
        .then(({ data }) => {
          this.items = data
        })
    },
    cancel () {
      this.$router.go(-1)
    },
    save () {
      if (this.action === 'new') {
        this.$axios.post(`classes`, {
          'teacher_id': this.teacher.id,
          'title': this.title,
          'major_category': this.major_category,
          'minor_category': this.minor_category,
          'year': this.year,
          'semester': this.semester,
          'time_slot': this.time_slot,
          'google_calendar': this.google_calendar,
          'audience': this.audience,
          'background': this.background,
          'content': this.content
        }).then(({data}) => {
          this.$router.go(-1)
        })
      } else if (this.action === 'update') {
        if (this.id) {
          this.$axios.put(`classes/` + this.id, {
            'teacher_id': this.teacher.id,
            'title': this.title,
            'major_category': this.major_category,
            'minor_category': this.minor_category,
            'year': this.year,
            'semester': this.semester,
            'time_slot': this.time_slot,
            'google_calendar': this.google_calendar,
            'audience': this.audience,
            'background': this.background,
            'content': this.content
          }).then(({data}) => {
            this.$router.go(-1)
          })
        }
      }
    },
    search () {
      let query = {}
      this.$axios.get(`howcs_teacher_infos`, {params: query})
        .then(({ data }) => {
          this.search_table_data = data
        })
      this.search_modal = true
    },
    search_select () {
      this.teacher = this.search_item[0].user
      this.search_modal = false
    }
  },
  created () {
    let user = LocalStorage.get.item('user_')
    console.log(JSON.parse(user.role))
    console.log(JSON.parse(user.role).includes('admin'))
    if (JSON.parse(user.role).includes('admin')) {
      this.teacher_select = true
    } else {
      this.teacher = user
    }

    this.$axios.get(`classes/categories`
    ).then(({ data }) => {
      this.major_categories = data
    })

    if (this.action === 'update') {
      this.$axios.get(`classes/` + this.id
      ).then(({ data }) => {
        console.log(data)
        this.teacher = data.teacher
        this.teacher_select = false
        this.title = data.title
        this.major_category = data.major_category
        this.minor_category = data.minor_category
        this.year = data.year
        this.semester = data.semester
        this.time_slot = data.time_slot
        this.google_calendar = data.google_calendar
        this.audience = data.audience
        this.background = data.background
        this.content = data.content
      })
    }
  }
}
</script>
