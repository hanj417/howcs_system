<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 700px; max-width: 80vw;">
      <q-input
        v-model="title"
        float-label="제목" />
      <q-option-group
        label="대분류"
        type="radio"
        v-model="major_category"
        inline
        v-if="!category_disabled"
        :options="major_categories" />
      <q-option-group
        label="분류"
        type="radio"
        v-model="minor_category"
        inline
        v-if="!category_disabled"
        :options="minor_categories" />
      <q-field
        label="작성날짜"
      >
        <q-datetime
          v-model="created_at"
          type="date" />
      </q-field>
      <div>
        <quill-editor
          v-model='body'
          style="height: 300px;"/>
      </div>
      <div class="col-xs-12 q-mt-xl q-pt-xl">
        <q-uploader
          ref="uploader"
          url="/api/upload"
          @add="add_file"
          @remove:done(file)="remove_file"
          hide-upload-button
          auto-expand
          no-thumbnails
          clearable
          hide-upload-progress />
      </div>
      <div
        v-if="files"
        class="col-xs-12 text-left q-body-1">
        <template v-for="file in files">
          <a :href="'/api/upload/' + file">{{ file }}</a><br>
        </template>
      </div>
      <div class="row q-ma-md col-xs-12 justify-end">
        <div class="col-xs-4">
          <q-btn
            v-if="(action == 'new' || action == 'update') && (priv_new || priv_update)"
            @click="remove_files"
            label="첨부파일삭제" />
          <q-btn
            v-if="action == 'new' && priv_new"
            @click="post_new"
            label="등록" />
          <q-btn
            v-if="action == 'update' && priv_update"
            @click="post_update"
            label="수정" />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'

export default {
  data: function () {
    return {
      priv_new: false,
      priv_update: false,
      priv_del: false,
      class_id: '',
      major_categories: [],
      major_category: {},
      minor_categories: [],
      minor_category: '',
      category_disabled: true,
      properties: '',
      notice: false,
      title: '',
      created_at: '',
      body: '',
      files: []
    }
  },
  props: ['action', 'id'],
  watch: {
    'major_category': function (val) {
      var self = this
      self.$axios.get('classes/categories/' + self.major_category
      ).then(function (response) {
        let data = response.data
        self.minor_categories = data
      })
    }
  },
  methods: {
    check_priv: function () {
      var self = this
      let priv_new_query = {priv: 'howcs_post_new'}
      self.$axios.get('privileges', {params: priv_new_query})
        .then(function (response) {
          let data = response.data
          self.priv_new = data
        })
  
      let priv_update_query = {priv: 'howcs_post_update'}
      self.$axios.get('privileges', {params: priv_update_query})
        .then(function (response) {
          let data = response.data
          self.priv_update = data
        })
  
      let priv_del_query = {priv: 'howcs_post_del'}
      self.$axios.get('privileges', {params: priv_del_query})
        .then(function (response) {
          let data = response.data
          self.priv_del = data
        })

      let priv_query = {priv: 'howcs_attendance_update'}
      self.$axios.get('privileges', {params: priv_query})
        .then(function (response) {
          let data = response.data
          self.priv = data
      })
    },
    cancel: function () {
      this.$router.go(-1)
    },
    post_new: function () {
      if (!this.priv_new)
        return

      this.properties = []
      if (this.notice) {
        this.properties.push('notice')
      }

      var self = this
        self.$axios.post('posts', {
          'major_category': self.major_category,
          'minor_category': self.minor_category,
          'properties': self.properties,
          'title': self.title,
          'body': self.body,
          'files': self.files,
          'class_id': self.id,
          'created_at': (new Date(self.created_at)).toISOString()
        }).then(function (response) {
          let data = response.data
          self.$router.go(-1)
        })
    },
    post_update: function () {
      if (!this.priv_update)
        return

      this.properties = []
      if (this.notice) {
        this.properties.push('notice')
      }

      var self = this
        self.$axios.put('posts/' + self.id, {
          'major_category': self.major_category,
          'minor_category': self.minor_category,
          'properties': self.properties,
          'title': self.title,
          'body': self.body,
          'files': self.files,
          'created_at': (new Date(self.created_at)).toISOString()
        }).then(function (response) {
          let data = response.data
          self.$router.go(-1)
        })
    },
    add_file: function (files) {
      for (let i = 0; i < files.length; i++) {
        this.files.push(files[i].name)
      }
      this.$refs.uploader.upload()
    },
    remove_file: function (files) {
      for (let i = 0; i < files.length; i++) {
        const index = array.indexOf(files[i].name)
        this.files.splice(index, 1)
      }
    },
    remove_files: function () {
      this.files = []
    }

  },
  created: function () {
    this.check_priv()

    let user = LocalStorage.get.item('user_')
    if (JSON.parse(user.role).includes('admin')) {
      this.category_disabled = false
    }
    this.created_at = Date.now()

    var self = this
    self.$axios.get('posts/categories')
      .then(function (response) {
        let data = response.data
        self.major_categories = data
      })
    self.$axios.get('posts/properties')
      .then(function (response) { let data = response.data })
    if (self.action === 'update') {
      self.$axios.get('posts/' + self.id)
        .then(function (response) {
          let data = response.data
          self.major_category = data.major_category
          self.minor_category = data.minor_category
          // self.category_disabled = true
          self.properties = data.properties
          if (data.properties && JSON.parse(data.properties).includes('notice')) {
            self.notice = true
          }
          self.title = data.title
          self.body = data.body
          if (data.files) { self.files = JSON.parse(data.files) }
          if (self.files == '') { self.files = [] }
          self.class_id = data.class_id
          self.created_at = data.created_at
        })
    } else if (self.action === 'new') {
      if (self.id) {
        self.$axios.get('classes/' + self.id)
          .then(function (response) {
            let data = response.data
            self.major_category = data.major_category
            self.minor_category = data.minor_category
            self.category_disabled = true
          })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .quill-code {
    border: none;
    height: auto;
    > code {
      width: 100%;
      margin: 0;
      padding: 1rem;
      border: 1px solid #ccc;
      border-top: none;
      border-radius: 0;
      height: 10rem;
      overflow-y: auto;
      resize: vertical;
    }
  }
</style>
