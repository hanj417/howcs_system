<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 500px; max-width: 80vw;">
      <q-input
        v-model="career"
        float-label="경력" />
      <q-btn
        @click="store"
        label="신청" />
    </div>
  </q-page>
</template>

<script>
export default {
  data () {
    return {
      career: ''
    }
  },
  methods: {
    cancel () {
      this.$router.go(-1)
    },
    save () {
      this.$axios.post(`agit_teacher_infos`, {
        'career': this.career
      }).then(({data}) => {
        this.$router.go(-1)
      })
    }
  }
}
</script>
