<template>
  <q-page
    padding
    class="row justify-center">
    <div
      style="width: 600px; max-width: 90vw;"
      class="shadow-8">
      <div class="col-xs-12 text-center q-title text-weight-bold q-pa-md">회원 정보</div>
      <div class="col-xs-10 docs-input q-mx-xl">
        <q-input v-model="career" type="textarea" float-label="아지트 강좌 관련 이력"/>
      </div>
      <div class="col-xs-12 row justify-end q-my-lg">
        <div
          class="col-xs-2">
          <q-btn
            @click="$router.go(-1)"
            label="취소" />
        </div>
        <div class="col-xs-2">
          <q-btn
            @click="apply"
            label="신청" />
        </div>
      </div>
    </div>
  </div>
</div>
  </q-page>
</template>

<script>
export default {
  data: function () {
    return {
      career: '',
    }
  },
  props: [],
  methods: {
    apply: function () {
      var self = this
      self.$axios.post('agit_teacher_infos', {
        'career': self.career,
      }).then(function (response) {
        let data = response.data
        self.$router.go(-1)
      })
    },
  },
}
</script>
