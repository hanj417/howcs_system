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
      <v-form @submit.prevent="validateForm" lazy-validation>
          <v-flex xs12>
            <v-select
              label="대분류"
              v-model="major_category"
              :disabled="category_disabled"
              :items="major_categories"
              single-line
              bottom
            ></v-select>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              label="분류"
              v-model="minor_category"
              :disabled="category_disabled"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              label="제목"
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
                label="날짜"
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
export default {
  data () {
    return {
      class_id: '',
      major_categories: [],
      major_category: {},
      minor_category: '',
      category_disabled: false,
      properties: '',
      date: null,
      title: '',
      body: '',
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
