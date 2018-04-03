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
        <div class="col-xs-4">
          <q-btn
            @click="cancel"
            label="취소" />
          <q-btn
            @click="save"
            label="등록" />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  data () {
    return {
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
    cancel () {
      this.$router.go(-1)
    },
    save () {
      if (this.$route.name === 'student_health_record_new') {
        this.$axios.post(`student_health_records`, {
          'student_record_id': this.id,
          'date': (new Date(this.date)).toISOString(),
          'internal_medicine': this.internal_medicine,
          'dental_clinic': this.dental_clinic,
          'fluorine_coating': this.fluorine_coating,
          'height': this.height,
          'weight': this.weight,
          'sight': this.sight,
          'internal_medicine_content': this.internal_medicine_content,
          'cavity': this.cavity,
          'dental_clinic_content': this.dental_clinic_content,
          'content': this.content,
        }).then(({data}) => {
          this.$router.go(-1)
        })
      } else if (this.$route.name === 'student_health_record_edit') {
        this.$axios.put(`student_health_records/` + this.id, {
          'date': (new Date(this.date)).toISOString(),
          'internal_medicine': this.internal_medicine,
          'dental_clinic': this.dental_clinic,
          'fluorine_coating': this.fluorine_coating,
          'height': this.height,
          'weight': this.weight,
          'sight': this.sight,
          'internal_medicine_content': this.internal_medicine_content,
          'cavity': this.cavity,
          'dental_clinic_content': this.dental_clinic_content,
          'content': this.content,
        }).then(({data}) => {
          this.$router.go(-1)
        })
      }
    },
  },
  created () {
    if (this.$route.name === 'student_health_record_edit') {
      this.$axios.get(`student_health_records/` + this.id)
        .then(({ data }) => {
          this.student_record_id = data.student_record_id
          this.date = data.date
          this.internal_medicine = data.internal_medicine
          this.dental_clinic = data.dental_clinic
          this.fluorine_coating = data.fluorine_coating
          this.height = data.height
          this.weight = data.weight
          this.sight = data.sight
          this.internal_medicine_content = data.internal_medicine_content
          this.cavity = data.cavity
          this.dental_clinic_content = data.dental_clinic_content
          this.content = data.content
        })
    } else if (this.$route.name=== 'student_health_record_new') {
    }
  }
}
</script>
