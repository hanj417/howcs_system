<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 700px; max-width: 80vw;">
      <q-field
        label="검진일자"
      >
        <q-datetime
          v-model="date"
          type="date" />
      </q-field>
      <q-input
        v-model="internal_medicine"
        float-label="내과/의사명/연락처" />
      <q-input
        v-model="dental_clinic"
        float-label="치과/의사명/연락처" />
      <q-input
        v-model="fluorine_coating"
        float-label="불소도포기관/연락처" />
      <q-input
        v-model="height"
        float-label="신장" />
      <q-input
        v-model="weight"
        float-label="체중" />
      <q-input
        v-model="sight"
        float-label="시력" />
      <q-input
        v-model="internal_medicine_content"
        float-label="내과 비고" />
      <q-input
        v-model="cavity"
        float-label="충치 여부" />
      <q-input
        v-model="dental_clinic_content"
        float-label="치과 비고" />
      <q-input
        v-model="content"
        float-label="비고" />
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
            v-if="$route.name == 'student_health_record_new' && priv_new"
            @click="record_new"
            label="등록" />
          <q-btn
            v-if="$route.name == 'student_health_record_edit' && priv_update"
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
      date: '',
      internal_medicine: '',
      dental_clinic: '',
      fluorine_coating: '',
      height: '',
      weight: '',
      sight: '',
      internal_medicine_content: '',
      cavity: '',
      dental_clinic_content: '',
      content: '',
      student_info_id: '',
    }
  },
  props: ['id'],
  methods: {
    cancel: function () {
      this.$router.go(-1)
    },
    remove: function () {
      let self = this
      self.$axios.delete('student_health_records/' + self.id
      ).then(function (response) {
        let data = response.data
        self.$router.go(-1)
      })
    },
    record_new: function () {
      let self = this
      self.$axios.post('student_health_records', {
        'student_record_id': self.id,
        'date': (new Date(self.date)).toISOString(),
        'internal_medicine': self.internal_medicine,
        'dental_clinic': self.dental_clinic,
        'fluorine_coating': self.fluorine_coating,
        'height': self.height,
        'weight': self.weight,
        'sight': self.sight,
        'internal_medicine_content': self.internal_medicine_content,
        'cavity': self.cavity,
        'dental_clinic_content': self.dental_clinic_content,
        'content': self.content
      }).then(function (response) {
        let data = response.data
        self.$router.go(-1)
      })
    },
    update: function () {
      let self = this
      self.$axios.put('student_health_records/' + self.id, {
        'date': (new Date(self.date)).toISOString(),
        'internal_medicine': self.internal_medicine,
        'dental_clinic': self.dental_clinic,
        'fluorine_coating': self.fluorine_coating,
        'height': self.height,
        'weight': self.weight,
        'sight': self.sight,
        'internal_medicine_content': self.internal_medicine_content,
        'cavity': self.cavity,
        'dental_clinic_content': self.dental_clinic_content,
        'content': self.content
      }).then(function (response) {
        let data = response.data
        self.$router.go(-1)
      })
    }
  },
  created: function () {
    var self = this
    if (this.$route.name === 'student_health_record_edit') {
      self.$axios.get('student_health_records/' + self.id)
        .then(function (response) {
          let data = response.data
          self.student_record_id = data.student_record_id
          self.date = data.date
          self.internal_medicine = data.internal_medicine
          self.dental_clinic = data.dental_clinic
          self.fluorine_coating = data.fluorine_coating
          self.height = data.height
          self.weight = data.weight
          self.sight = data.sight
          self.internal_medicine_content = data.internal_medicine_content
          self.cavity = data.cavity
          self.dental_clinic_content = data.dental_clinic_content
          self.content = data.content
        })
    }

    let priv_new_query = {priv: 'howcs_student_health_record_new'}
    self.$axios.get('privileges', {params: priv_new_query})
      .then(function (response) {
        let data = response.data
        self.priv_new = data
      })

    let priv_update_query = {priv: 'howcs_student_health_record_update'}
    self.$axios.get('privileges', {params: priv_update_query})
      .then(function (response) {
        let data = response.data
        self.priv_update = data
      })

    let priv_del_query = {priv: 'howcs_student_health_record_del'}
    self.$axios.get('privileges', {params: priv_del_query})
      .then(function (response) {
        let data = response.data
        self.priv_del = data
      })
  }
}
</script>
