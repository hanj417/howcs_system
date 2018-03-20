<template>
<v-content>
  <v-container fluid fill-height>
   <v-layout justify-center align-center>
  <v-card>
    <v-card-title
      class="grey lighten-4 py-4 title"
    >
      글쓰기
    </v-card-title>
    <v-container grid-list-sm class="pa-4">
      <v-form @submit.prevent="validateForm" lazy-validation>
        <v-layout row wrap>
          <v-flex xs12>
            <v-text-field
              label="제목"
              v-model="title"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-checkbox :label="`공지`" v-model="notice"></v-checkbox>
          </v-flex>
          <v-flex xs12>
            <label> 본문 </label>
            <div class="pt-2">
              <vue-editor v-model='body'/>
            </div>
          </v-flex>
          <v-flex v-if="!category_disabled" xs12>
            <v-select
              label="대분류"
              v-model="major_category"
              :disabled="category_disabled"
              :items="major_categories"
              single-line
              bottom
            ></v-select>
          </v-flex>
          <v-flex v-if="!category_disabled" xs12>
            <v-text-field
              label="분류"
              v-model="minor_category"
              :disabled="category_disabled"
              required
            ></v-text-field>
          </v-flex>
        </v-layout>
      </v-form>
    </v-container>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn flat color="primary" @click="cancel">Cancel</v-btn>
      <v-btn flat @click="save">Save</v-btn>
    </v-card-actions>
  </v-card>
</v-layout>
</v-container>
</v-content>
</template>

<script>
import { VueEditor } from 'vue2-quill-editor'

export default {
  components: { VueEditor },
  data () {
    return {
      class_id: '',
      major_categories: [],
      major_category: {},
      minor_category: '',
      category_disabled: false,
      properties: '',
      notice: false,
      title: '',
      body: '',
    }
  },
  computed: {
    action() {
      return this.$route.params.action
    }, 
    id() {
      return this.$route.params.id
    },
  },
  methods: {
    cancel() {
      this.$router.go(-1)
    },
    save() {
      this.properties = []
      if (this.notice) {
        this.properties.push('notice')
      }
      if (this.action == 'new') {
        this.$axios.post(`posts`, {
          'major_category': this.major_category,
          'minor_category': this.minor_category,
          'properties': this.properties,
          'title': this.title,
          'body': this.body,
          'class_id': this.$route.params.id,
        }).then(({data}) => {
          this.$router.go(-1)
        })
      } else if (this.action == 'update') {
        this.$axios.put(`posts/` + this.$route.params.id, {
          'major_category': this.major_category,
          'minor_category': this.minor_category,
          'properties': this.properties,
          'title': this.title,
          'body': this.body,
        }).then(({data}) => {
          this.$router.go(-1)
        })
      } 
    },
  },
  created() {
    this.$axios.get(`posts/major_categories`)
    .then(({ data }) => { this.major_categories = data })
    this.$axios.get(`posts/properties`)
    .then(({ data }) => {})
    if (this.$route.params.action == 'update') {
      this.$axios.get(`posts/` + this.$route.params.id)
      .then(({ data }) => {
        this.major_category = data.major_category
        this.minor_category = data.minor_category
        this.category_disabled = true
        this.properties = data.properties
        if (JSON.parse(data.properties).includes('notice')) {
          this.notice = true
        }
        this.title = data.title
        this.body = data.body
        this.class_id = data.class_id
      })
    } else if (this.$route.params.action == 'new') {
      this.$axios.get(`classes/` + this.$route.params.id)
      .then(({ data }) => {
        this.major_category = data.major_category
        this.minor_category = data.minor_category
        this.category_disabled = true
      })
    }
  }
}
</script>
