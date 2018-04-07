<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 600px; max-width: 90vw;">
      <div v-if="role == 'admin'" class="col-xs-12 docs-input">
        <q-field
          label="선생님"
          icon="account circle"
          :label-width="3"
        >
          <q-input v-model="teacher.name"  class="col-xs-8" disabled />
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
        <div v-if="$route.name == 'class_form_edit'" class="col-xs-2">
          <q-btn
            @click="remove"
            label="삭제" />
        </div>
        <div class="col-xs-4">
          <q-btn
            @click="$router.go(-1)"
            label="취소" />
          <q-btn
            @click="save"
            :label="save_label" />
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
        <q-tr slot="body" slot-scope="props" :props="props" @click.native="search_select(props.row)" class="cursor-pointer">
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
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
  data: function() {
    return {
      teacher_select: false,
      teacher: {name: '' },
      title: '',
      minor_categories: [],
      minor_category: '',
      year: '2018',
      semester: '',
      time_slot: '',
      google_calendar: '',
      audience: '',
      background: '',
      content: '',
      save_label: '등록',

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
  props: ['role', 'major_category', 'class_id'],
  methods: {
    save: function () {
      var self = this
      if (this.$route.name === 'class_form_new') {
        self.$axios.post('classes', {
          'teacher_id': self.teacher.id,
          'title': self.title,
          'major_category': self.major_category,
          'minor_category': self.minor_category,
          'year': self.year,
          'semester': self.semester,
          'time_slot': self.time_slot,
          'google_calendar': self.google_calendar,
          'audience': self.audience,
          'background': self.background,
          'content': self.content
        }).then(function(response) { let data = response.data
          self.$router.go(-1)
        })
      } else if (self.$route.name === 'class_form_edit') {
        self.$axios.put('classes/' + self.class_id, {
          'teacher_id': self.teacher.id,
          'title': self.title,
          'major_category': self.major_category,
          'minor_category': self.minor_category,
          'year': self.year,
          'semester': self.semester,
          'time_slot': self.time_slot,
          'google_calendar': self.google_calendar,
          'audience': self.audience,
          'background': self.background,
           'content': self.content
        }).then(function(response) { let data = response.data
          self.$router.go(-1)
        })
      }
    },
    remove: function () {
      var self = this
      self.$axios.delete('classes/' + self.class_id)
      .then(function(response) { let data = response.data
        self.$router.go(-1)
      })
    },
    search: function () {
      let query = {}
      var self = this
      self.$axios.get('howcs_teacher_infos', {params: query})
      .then(function(response) { let data = response.data
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

    var self = this
    self.$axios.get('classes/categories/' + self.major_category
    ).then(function(response) { let data = response.data
      self.minor_categories = data
    })
    if (self.$route.name === 'class_form_new') {
      self.save_label = '등록'
    } else if (self.$route.name === 'class_form_edit') {
      self.save_label = '수정'
      self.$axios.get('classes/' + self.class_id
      ).then(function(response) { let data = response.data
        console.log(data)
        self.teacher = data.teacher
        self.teacher_select = false
        self.title = data.title
        self.major_category = data.major_category
        self.minor_category = data.minor_category
        self.year = data.year
        self.semester = data.semester
        self.time_slot = data.time_slot
        self.google_calendar = data.google_calendar
        self.audience = data.audience
        self.background = data.background
        self.content = data.content
      })
    } else {
      self.$router.go(-1)
    }
  }
}
</script>
