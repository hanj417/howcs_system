<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 700px; max-width: 80vw;">
      <q-input
        v-model="semester"
        float-label="학기" />
      <q-input
        v-model="content"
        float-label="세부 내용" />
      <div class="row q-ma-md col-xs-12 justify-end">
        <div class="col-xs-6">
          <q-btn
            @click="cancel"
            label="취소" />
          <q-btn
            v-if="priv_del"
            @click="remove"
            label="삭제" />
          <q-btn
            v-if="$route.name == 'student_fruit_record_new' && priv_new"
            @click="record_new"
            label="등록" />
          <q-btn
            v-if="$route.name == 'student_fruit_record_edit' && priv_update"
            @click="update"
            label="수정" />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  data: function () {
    return {
      priv_new: false,
      priv_update: false,
      priv_del: false,
      semester: '',
      content: '',
      enrollment_id: '',
      student_annual_info_id: '',
      student_fruit_record_id: '',
    }
  },
  props: ['id'],
  methods: {
    cancel: function () {
      this.$router.go(-1)
    },
    remove: function () {
      let self = this
      self.$axios.delete('student_fruit_records/' + self.id
      ).then(function (response) {
        let data = response.data
        self.$router.go(-1)
      })
    },
    record_new: function () {
      let self = this
      self.$axios.post('student_fruit_records', {
        'enrollment_id': self.enrollment_id,
        'semester': self.semester,
        'content': self.content
      }).then(function (response) {
        let data = response.data
        self.$router.go(-1)
      })
    },
    update: function () {
      let self = this
      self.$axios.put('student_fruit_records/' + self.id, {
        'semester': self.semester,
        'content': self.content
      }).then(function (response) {
        let data = response.data
        self.$router.go(-1)
      })
    }
  },
  created: function () {
    var self = this
    if (this.$route.name === 'student_fruit_record_edit') {
      self.$axios.get('student_fruit_records/' + self.id)
        .then(function (response) {
          let data = response.data
          self.enrollment_id = data.enrollment_id
          self.student_annual_record_id = data.student_annual_record_id
          self.semester = data.semester
          self.content = data.content
        })
    }
    if (this.$route.name === 'student_fruit_record_new') {
      self.enrollment_id = self.id
    }

    let priv_new_query = {priv: 'howcs_student_fruit_record_new'}
    self.$axios.get('privileges', {params: priv_new_query})
      .then(function (response) {
        let data = response.data
        self.priv_new = data
      })

    let priv_update_query = {priv: 'howcs_student_fruit_record_update'}
    self.$axios.get('privileges', {params: priv_update_query})
      .then(function (response) {
        let data = response.data
        self.priv_update = data
      })

    let priv_del_query = {priv: 'howcs_student_fruit_record_del'}
    self.$axios.get('privileges', {params: priv_del_query})
      .then(function (response) {
        let data = response.data
        self.priv_del = data
      })
  }
}
</script>
