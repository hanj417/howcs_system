<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 600px; max-width: 80vw;" class="q-pa-xl no-shadow">
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
  data: function() {
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
      var self = this
      self.$axios.get('classes/categories/' + self.major_category
      ).then(function(response) { let data = response.data
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
      self.$axios.delete('posts/' + self.id)
        .then(function(response) { let data = response.data 
        self.$router.go(-1) })
    }
  },
  created: function () {
    this.user = LocalStorage.get.item('user_')

    var self = this
    self.$axios.get('posts/categories')
      .then(function(response) { let data = response.data 
        self.major_categories = data })
    self.$axios.get('posts/properties')
      .then(function(response) { let data = response.data})
    self.$axios.get('posts/' + self.id)
      .then(function(response) { let data = response.data
        self.major_category = data.major_category
        self.minor_category = data.minor_category
        self.category_disabled = true
        self.properties = data.properties
        self.date = (new Date(data.created_at)).toISOString().slice(0, 10)
        self.author_name = data.author.name
        if (data.files)
          self.files = JSON.parse(data.files)
        if (self.files == "")
          self.files = []
        
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
