<template>
  <q-page
    padding
    class="row justify-center">
    <q-table
      :data="table_data"
      :columns="columns"
      :filter="filter"
      :visible-columns="visible_columns"
      selection="single"
      :selected.sync="item"
      row-key="name"
      color="secondary"
      class="col-xs-11"
      dense
    >
      <template
        slot="top-left"
        slot-scope="props">
        <q-search
          hide-underline
          color="secondary"
          v-model="filter"
          class="col-6"
        />
      </template>
      <template
        slot="top-right"
        slot-scope="props">
        <q-table-columns
          color="secondary"
          class="q-mr-sm"
          v-model="visible_columns"
          :columns="columns"
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
          delete
          icon="save"
          @click="save" />
        <q-btn
          color="negative"
          flat
          round
          delete
          icon="delete"
          @click="remove" />
      </template>
      <q-tr slot="body" slot-scope="props" :props="props">
       <q-td auto-width>
        <q-checkbox color="primary" v-model="props.selected" />
       </q-td>
      <template v-for="col in visible_columns">
        <q-td v-if="col == 'label'" :key="col" :props="props">{{ props.row.label }}</q-td>
        <q-td v-else :key="col" :props="props">
          <q-toggle v-model="props.row[col]" />
        </q-td>
      </template>
      </q-tr>
    </q-table>
    <q-page-sticky
      position="bottom-right"
      :offset="[18, 18]">
      <q-btn
        round
        color="primary"
        @click="add_modal = true"
        icon="add" />
    </q-page-sticky>
    <q-modal
      v-model="add_modal"
      class="row justify-center">
      <div class="col-xs-12">
        <q-input v-model="role_label" float-label="권한 이름" />
        <q-input v-model="role_name" float-label="권한 영문 이름" />
      </div> 
      <div class="row q-ma-md col-xs-12 justify-end">
        <div class="col-xs-5">
          <q-btn
            color="primary"
            @click="role_new"
            label="추가"
          />
          <q-btn
            color="primary"
            @click="add_modal = false"
            label="닫기"
          />
        </div>
      </div>
    </q-modal>
  </q-page>
</template>

<script>

export default {
  data: function() {
    return {
      table_data: [],
      columns: [
        { name: 'label', label: '이름', field: 'label', align: 'center' },
        { name: 'user', label: '회원조회', field: 'user', align: 'center' },
        { name: 'user_new', label: '회원생성', field: 'user_new', align: 'center' },
        { name: 'user_update', label: '회원수정', field: 'user_update', align: 'center' },
        { name: 'user_del', label: '회원삭제', field: 'user_del', align: 'center' },
        { name: 'student', label: '학생조회', field: 'student', align: 'center' },
        { name: 'student_new', label: '학생생성', field: 'student_new', align: 'center' },
        { name: 'student_update', label: '학생수정', field: 'student_update', align: 'center' },
        { name: 'student_del', label: '학생삭제', field: 'student_del', align: 'center' },
        { name: 'howcs_teacher', label: '하우교사조회', field: 'howcs_teacher', align: 'center' },
        { name: 'howcs_teacher_new', label: '하우교사생성', field: 'howcs_teacher_new', align: 'center' },
        { name: 'howcs_teacher_update', label: '하우교사수정', field: 'howcs_teacher_update', align: 'center' },
        { name: 'howcs_teacher_del', label: '하우교사삭제', field: 'howcs_teacher_del', align: 'center' },
        { name: 'howcs_class', label: '하우수업조회', field: 'howcs_class', align: 'center' },
        { name: 'howcs_class_new', label: '하우수업생성', field: 'howcs_class_new', align: 'center' },
        { name: 'howcs_class_update', label: '하우수업수정', field: 'howcs_class_update', align: 'center' },
        { name: 'howcs_class_del', label: '하우수업삭제', field: 'howcs_class_del', align: 'center' },
        { name: 'howcs_enrollment', label: '하우수강조회', field: 'howcs_enrollment', align: 'center' },
        { name: 'howcs_enrollment_new', label: '하우수강생성', field: 'howcs_enrollment_new', align: 'center' },
        { name: 'howcs_enrollment_update', label: '하우수강수정', field: 'howcs_enrollment_update', align: 'center' },
        { name: 'howcs_enrollment_del', label: '하우수강삭제', field: 'howcs_enrollment_del', align: 'center' },
        { name: 'howcs_attendance', label: '하우출결조회', field: 'howcs_attendance', align: 'center' },
        { name: 'howcs_attendance_new', label: '하우출결생성', field: 'howcs_attendance_new', align: 'center' },
        { name: 'howcs_attendance_update', label: '하우출결수정', field: 'howcs_attendance_update', align: 'center' },
        { name: 'howcs_attendance_del', label: '하우출결삭제', field: 'howcs_attendance_del', align: 'center' },
        { name: 'howcs_post', label: '하우게시조회', field: 'howcs_post', align: 'center' },
        { name: 'howcs_post_new', label: '하우게시생성', field: 'howcs_post_new', align: 'center' },
        { name: 'howcs_post_update', label: '하우게시수정', field: 'howcs_post_update', align: 'center' },
        { name: 'howcs_post_del', label: '하우게시삭제', field: 'howcs_post_del', align: 'center' },
        { name: 'homepage_post', label: '홈피게시조회', field: 'homepage_post', align: 'center' },
        { name: 'homepage_post_new', label: '홈피게시생성', field: 'homepage_post_new', align: 'center' },
        { name: 'homepage_post_update', label: '홈피게시수정', field: 'homepage_post_update', align: 'center' },
        { name: 'homepage_post_del', label: '홈피게시삭제', field: 'homepage_post_del', align: 'center' },
      ],
      filter: '',
      visible_columns: [
        'label',
        'user',
        'user_new',
        'user_update',
        'user_del',
        'student',
        'student_new',
        'student_update',
        'student_del',
        'howcs_teacher',
        'howcs_teacher_new',
        'howcs_teacher_update',
        'howcs_teacher_del',
        'howcs_class',
        'howcs_class_new',
        'howcs_class_update',
        'howcs_class_del',
        'howcs_enrollment',
        'howcs_enrollment_new',
        'howcs_enrollment_update',
        'howcs_enrollment_del',
        'howcs_attendance',
        'howcs_attendance_new',
        'howcs_attendance_update',
        'howcs_attendance_del',
        'howcs_post',
        'howcs_post_new',
        'howcs_post_update',
        'howcs_post_del',
        'homepage_post',
        'homepage_post_new',
        'homepage_post_update',
        'homepage_post_del'],
      toggle_columns: [
        'user',
        'user_new',
        'user_update',
        'user_del',
        'student',
        'student_new',
        'student_update',
        'student_del',
        'howcs_teacher',
        'howcs_teacher_new',
        'howcs_teacher_update',
        'howcs_teacher_del',
        'howcs_class',
        'howcs_class_new',
        'howcs_class_update',
        'howcs_class_del',
        'howcs_enrollment',
        'howcs_enrollment_new',
        'howcs_enrollment_update',
        'howcs_enrollment_del',
        'howcs_attendance',
        'howcs_attendance_new',
        'howcs_attendance_update',
        'howcs_attendance_del',
        'howcs_post',
        'howcs_post_new',
        'howcs_post_update',
        'howcs_post_del',
        'homepage_post',
        'homepage_post_new',
        'homepage_post_update',
        'homepage_post_del'],
      item: [],
      add_modal: false,
      role_label: '',
      role_name: '',
    }
  },
  methods: {
    fetch_data: function() {
      let query = {}
      var self = this
      self.$axios.get('privileges', {params: query})
        .then(function(response) { let data = response.data 
        self.table_data = data })
    },
    role_new: function() {
      var self = this
      self.$axios.post('privileges', {
        'name': self.role_name,
        'label': self.role_label,
      }).then(function(response) { let data = response.data
        self.fetch_data()
      })
      this.add_modal = false
    },
    save: function () {
      var self = this
      self.$axios.put('privileges/' + self.item[0].id, self.item[0])
      .then(function(response) { let data = response.data 
        self.fetch_data() })
    },
    remove: function () {
      var self = this
      self.$axios.delete('privileges/' + self.item[0].id)
        .then(function(response) { let data = response.data 
        self.fetch_data() })
    }
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
