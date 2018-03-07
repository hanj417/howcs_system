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
              :disabled="category_disabled"
            ></v-select>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              placeholder="분류"
              v-model="minor_category"
              :disabled="category_disabled"
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
            <v-menu
              ref="menu"
              lazy
              :close-on-content-click="false"
              v-model="menu"
              transition="scale-transition"
              offset-y
              full-width
              :nudge-right="40"
              min-width="290px"
              :return-value.sync="date"
            >
              <v-text-field
                slot="activator"
                label="Picker in menu"
                v-model="date"
                prepend-icon="event"
                readonly
              ></v-text-field>
              <v-date-picker v-model="date" no-title scrollable>
                <v-spacer></v-spacer>
                <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
              </v-date-picker>
            </v-menu>
          </v-flex>
          <v-flex xs12>
            <label> 본문 </label>
            <div class="pt-2">
              {{ body }}
            </div>
          </v-flex>
        </v-layout>
      </v-form>
    </v-container>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn flat color="primary" @click="cancel">Cancel</v-btn>
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
      category_disabled: false,
      switches: [],
      properties: '',
      title: '',
      body: '',
      class_id: '',
      date: null,
    }
  },
  computed: {
    id() {
      return this.$route.params.id
    },
  },
  methods: {
    cancel() {
      this.$router.replace('/')
    },
  },
  created() {
    this.$http.get(`posts/` + this.$route.params.id
    ).then(({ data }) => {
      this.major_category = data.major_category
      this.minor_category = data.minor_category
      this.properties = data.properties
      this.title = data.title
      this.body = data.body
      this.class_id = data.class_id
      this.date = data.date
      this.category_disabled = true
    })
  }
}
</script>
