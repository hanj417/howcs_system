<template>
  <div>
<!--
    <div class="page-intro">
      <img
        src="~assets/img/howstory_background_image.png"
        class="section__background-image" >

      <div class="title--emphasized">
        오늘도 하우는 ( &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ) 하다

      </div>

    </div>
-->

    <div class="container">
      <div class="page-name">
        하우하다
      </div>
      <hr class="page-name--bottom-border" >
    </div>


  <div
    class="row justify-center">
    <div style="width: 800px; max-width: 80vw;" class="q-pa-xl shadow-10">
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
<!--
      <div class="row q-ma-md col-xs-12 justify-end">
      <div class="col-xs-4">
  <q-btn v-if="is_author" @click="$router.push({name:'post_form', params:{action:'update', id: id}})" label="수정" />
  <q-btn v-if="is_author" @click="remove" label="삭제" />
      </div>
      </div>
-->
    </div>
  </div>



  </div>
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
    'major_category': function (val) {
      var self = this
      self.$axios.get(`classes/categories/` + self.major_category
      ).then(function (response) {
        let data = response.data
        self.minor_categories = data
      })
    }
  },
  methods: {
    cancel: function () {
      this.$router.go(-1)
    },
    remove: function () {
      var self = this
      self.$axios.delete(`posts/` + self.id)
        .then(function (response) {  self.$router.go(-1) })
    }
  },
  created: function () {
    this.user = LocalStorage.get.item('user_')

    var self = this
    self.$axios.get(`posts/categories`)
      .then(function (response) { self.major_categories = response.data })
    self.$axios.get(`posts/homepage/` + self.id)
      .then(function (response) {
        let data = response.data
        self.major_category = data.major_category
        self.minor_category = data.minor_category
        self.category_disabled = true
        self.properties = data.properties
        self.date = (new Date(data.created_at)).toISOString().slice(0, 10)
        self.author_name = data.author.name
        self.files = JSON.parse(data.files)
        
        /*
      if (JSON.parse(data.properties).includes('notice')) {
        self.notice = true
      }
*/
        self.title = data.title
        self.body = data.body
        self.class_id = data.class_id
        if (self.user.id === data.author_id) {
          self.is_author = true
        }
      })
  }
}
</script>
