<template>
  <q-page
    padding
    class="row justify-center">
<!--
    <div
      style="width: 600px; max-width: 90vw;"
      class="shadow-8">
      <div class="col-xs-12 text-center q-title text-weight-bold q-pa-md">하우학교 열매</div>
      <div class="col-xs-10 docs-input q-mx-xl">
-->
<table border="1px">
<!--<tr><th colspan="3"> {{ user.name }}</th></tr>-->
<tr><th colspan="3"> 2018학년도 열매</th></tr>
<template v-for="enrollment in enrollments" v-if="is_subject[enrollment.id]">
<tr><th colspan="3" align="left" bgcolor="#D0D3D4"> [{{ enrollment.class.category }}] {{ enrollment.class.title }}</th></tr>
<tr>
<td></td>
<td>봄학기</td>
<td>여름학기</td>
</tr>
<tr>
<td>교과내용</td>
<template v-if="is_subject[enrollment.id] && contents_length[enrollment.id] == 2">
<td align="left" style="text-align:left">{{ contents[enrollment.id]['spring'] }}</td>
<td align="left" style="text-align:left">{{ contents[enrollment.id]['summer'] }}</td>
</template>
<template v-if="is_subject[enrollment.id] && contents_length[enrollment.id] == 1">
<td colspan="2" align="left" style="text-align:left">{{ contents[enrollment.id]['summer'] }}</td>
</template>
</tr>
<tr>
<td>세부능력<br>및<br>특기사항</td>
<template v-if="is_subject[enrollment.id] && fruits_length[enrollment.id] == 2">
<td align="left" style="text-align:left">{{ fruits[enrollment.id]['spring'].content }}</td>
<td align="left" style="text-align:left">{{ fruits[enrollment.id]['summer'].content }}</td>
</template>
<template v-if="is_subject[enrollment.id] && fruits_length[enrollment.id] == 1">
<td colspan="2" style="text-align:left">{{ fruits[enrollment.id]['summer'].content }}</td>
</template>
</tr>
</template>
</table>
<!--
      </div>
    </div>
  </div>
</div>
-->
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'
import { required, email } from 'vuelidate/lib/validators'

export default {
  data: function () {
    return {
      is_subject: {},
      user: {},
      enrollments: [],
      contents: {},
      contents_length: {},
      fruits: {},
      fruits_length: {},
    }
  },
  props: ['action', 'id'],
  methods: {
  },
  created: function () {
    var self = this
    self.$axios.get('users/' + this.id
    ).then(function (response) {
      let data = response.data
      self.user = data
    })

    let query = {'student_id': this.id}
    self.$axios.get('enrollments', {params: query}
    ).then(function (response) {
      let data = response.data
      self.enrollments = data
      for (let i = 0; i < self.enrollments.length; i++) {
        self.is_subject[self.enrollments[i].id] = true
        if (self.enrollments[i].class.minor_category == 'class') {
          self.is_subject[self.enrollments[i].id] = false
          continue
        }
        let c = JSON.parse(self.enrollments[i].class.content)
        self.contents[self.enrollments[i].id] = c
        self.contents_length[self.enrollments[i].id] = Object.keys(c).length
      }
      for (let i = 0; i < self.enrollments.length; i++) {
        if (self.enrollments[i].class.minor_categories == 'class') {
          continue
        }
        let query = {'enrollment_id': self.enrollments[i].id}
        self.$axios.get('student_fruit_records', {params: query}
        ).then(function (response) {
          let data = response.data
          self.$set(self.fruits, data[0].enrollment_id, {})
          for (let j = 0; j < data.length; j++) {
            self.$set(self.fruits[data[j].enrollment_id], data[j].semester, data[j])
          }
          self.$set(self.fruits_length, data[0].enrollment_id, data.length)
        })
      }
    })
  }
}
</script>
