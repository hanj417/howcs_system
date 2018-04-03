<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 600px; max-width: 80vw;" class="q-pa-xl shadow-10">
    <div class="col-xs-12 text-center q-title text-weight-bold q-pa-md">{{ title }}</div>
    <div class="col-xs-12 text-right q-body-2 text-weight-bold q-px-md">{{ date }}</div>
    <div class="col-xs-12 text-right q-body-2 text-weight-bold q-px-md">{{ author_name }}</div>
    
      <div v-html="body" class="col-xs-12 q-pt-xl"/>
    <div v-if="files" class="col-xs-12 text-left q-body-2 text-weight-bold q-px-md">첨부파일</div>
<div v-if="files" class="col-xs-12 text-left q-body-1">
    <template v-for="file in files">
<a :href="'/api/upload/' + file">{{ file }}</a><br>
    </template>
</div>
      <div class="row q-ma-md col-xs-12 justify-end">
      <div class="col-xs-4">
  <q-btn v-if="is_author" @click="$router.push({name:'post_form', params:{action:'update', id: id}})" label="수정" />
  <q-btn v-if="is_author" @click="remove" label="삭제" />
      </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'

export default {
  data () {
    return {
      class_id: '',
      major_categories: [],
      major_category: {},
      minor_categories: [],
      minor_category: '',
      category_disabled: false,
      properties: '',
      notice: false,
      title: '',
      body: '',
      date: '',
      author_name: '',
      files: [],

      user: {},
      is_author: false,
    }
  },
  props: ['id'],
  watch: {
    'major_category' (val) {
      this.$axios.get(`classes/categories/` + this.major_category
      ).then(({ data }) => {
        this.minor_categories = data
      })
    }
  },
  methods: {
    cancel () {
      this.$router.go(-1)
    },
    remove () {
      this.$axios.delete(`posts/` + this.id)
        .then(({ data }) => { this.$router.go(-1) })
    }
  },
  created () {
    this.user = LocalStorage.get.item('user_')

    this.$axios.get(`posts/categories`)
      .then(({ data }) => { this.major_categories = data })
    this.$axios.get(`posts/properties`)
      .then(({ data }) => {})
    this.$axios.get(`posts/` + this.id)
      .then(({ data }) => {
        this.major_category = data.major_category
        this.minor_category = data.minor_category
        this.category_disabled = true
        this.properties = data.properties
        this.date = (new Date(data.created_at)).toISOString().slice(0, 10)
        this.author_name = data.author.name
        if (data.files)
          this.files = JSON.parse(data.files)
        if (this.files == "")
          this.files = []
        
        /*
      if (JSON.parse(data.properties).includes('notice')) {
        this.notice = true
      }
*/
        this.title = data.title
        this.body = data.body
        this.class_id = data.class_id
        if (this.user.id === data.author_id) {
          this.is_author = true
        }
      })
  }
}
</script>
