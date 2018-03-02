<template>
<v-content>
  <v-container fluid fill-height>
   <v-layout justify-center align-center>
  <v-card>
    <v-card-title
      class="grey lighten-4 py-4 title"
    >
      회원 정보
    </v-card-title>
    <v-container grid-list-sm class="pa-4">
      <v-form v-model="valid" ref="form" lazy-validation>
        <v-layout row wrap>
          <v-flex xs12 align-center>
            <v-layout align-center>
              <v-avatar size="40px" class="mr-3">
                <img
                  src="//ssl.gstatic.com/s2/oz/images/sge/grey_silhouette.png"
                  alt=""
                >
              </v-avatar>
              <v-text-field
                placeholder="선생님"
                v-model="teacher"
                :rules="nameRules"
                required
              ></v-text-field>
            </v-layout>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="학급명"
              v-model="title"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="분류"
              v-model="category"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="해당년도"
              v-model="year"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="학기"
              v-model="semester"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="수업시간"
              v-model="time_slot"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="대상"
              v-model="audience"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="배경"
              v-model="background"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="내용"
              v-model="content"
            ></v-text-field>
          </v-flex>
        </v-layout>
      </v-form>
    </v-container>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn flat color="primary" @click="cancel">취소</v-btn>
      <v-btn flat @click="save">{{ save_btn_text }}</v-btn>
    </v-card-actions>
  </v-card>
</v-layout>
</v-container>
</v-content>
</template>

<script>
export default {
  data () {
    return {
      save_btn_text: '등록',
      valid: true,
      teacher: '',
      title: '',
      category: '',
      year: null,
      semester: '',
      time_slot: '',
      audience: '',
      background: '',
      content: '',
    }
  },
  computed: {
    action() {
      return this.$route.params.action
    }, 
    id() {
      return this.$route.params.id
    }
  },
  methods: {
    cancel() {
      this.$router.replace('/')
    },
    save() {
      if (this.action == 'new') {
          this.$http.post(`classes`, {
              'teacher': this.teacher,
              'title': this.title,
              'category': this.category,
              'year': this.year,
              'semester': this.semester,
              'time_slot': this.time_slot,
              'audience': this.audience,
              'background': this.background,
              'content': this.content,
          }).then(({data}) => {
            this.$router.replace('/')
          })
      } else if (this.action == 'update') {
        if (this.$route.params.hasOwnProperty('id')) {
            this.$http.put(`classes/` + this.$route.params.id, {
              'teacher': this.teacher,
              'title': this.title,
              'category': this.category,
              'year': this.year,
              'semester': this.semester,
              'time_slot': this.time_slot,
              'audience': this.audience,
              'background': this.background,
              'content': this.content,
            }).then(({data}) => {
              this.$router.replace('/')
            })
        }
      }
    },
  },
  created() {
    if (this.$route.params.action == 'update') {
      if (this.$route.params.hasOwnProperty('id')) {
        this.$http.get(`classes/` + this.$route.params.id
        ).then(({ data }) => {
          console.log(data)
          this.teacher = data.teacher
          this.title = data.title
          this.category = data.category
          this.year = data.year
          this.semester = data.semester
          this.time_slot = data.time_slot
          this.audience = data.audience
          this.background = data.background
          this.content = data.content
        })
      }
    }
  }
}
</script>
