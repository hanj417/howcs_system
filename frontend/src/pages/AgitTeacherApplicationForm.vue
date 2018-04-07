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
  data: function() {
    return {
      career: ''
    }
  },
  methods: {
    cancel: function () {
      this.$router.go(-1)
    },
    save: function () {
      var self = self
      self.$axios.post('agit_teacher_infos', {
        'career': self.career
      }).then(function(response) { let data = response.data
        self.$router.go(-1)
      })
    }
  }
}
</script>
