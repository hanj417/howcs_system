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
          <v-flex xs12>
            <v-select
              :items="major_categories"
              v-model="major_category"
              label="대분류"
              single-line
              bottom
            ></v-select>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="분류"
              v-model="minor_category"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="제목"
              v-model="title"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <label> 본문 </label>
            <div class="pt-2">
              <vue-editor v-model='body'/>
            </div>
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
      valid: true,
      major_categories: [],
      major_category: {},
      minor_category: '',
      switches: [],
      properties: '',
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
      this.$router.replace('/')
    },
    save() {
      if (this.action == 'new') {
        this.$http.post(`posts`, {
          'major_category': this.major_category,
          'minor_category': this.minor_category,
          'properties': this.properties,
          'title': this.title,
          'body': this.body,
        }).then(({data}) => {
          this.$router.replace('/')
        })
      } else if (this.action == 'update') {
        this.$http.put(`posts/` + this.$route.params.id, {
          'major_category': this.major_category,
          'minor_category': this.minor_category,
          'properties': this.properties,
          'title': this.title,
          'body': this.body,
        }).then(({data}) => {
          this.$router.replace('/')
        })
      } 
    },
  },
  created() {
    this.$http.get(`posts/major_categories`
    ).then(({ data }) => {
      this.major_categories = data
    })
    this.$http.get(`posts/properties`
    ).then(({ data }) => {
    })
    if (this.$route.params.action == 'update') {
      this.$http.get(`posts/` + this.$route.params.id
      ).then(({ data }) => {
        this.major_category = data.major_category
        this.minor_category = data.minor_category
        this.properties = data.properties
        this.title = data.title
        this.body = data.body
      })
    }
  }
}
</script>
