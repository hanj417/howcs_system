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
      <quill-editor v-model='body'  style="height: 300px;"/>
      </div>
      <div class="col-xs-12 q-mt-xl q-pt-xl">
      <q-uploader ref="uploader" url="/api/upload" @add="add_file" @remove:done(file)="remove_file" hide-upload-button auto-expand no-thumbnails clearable hide-upload-progress />
      </div>
<div v-if="files" class="col-xs-12 text-left q-body-1">
    <template v-for="file in files">
<a :href="'/api/upload/' + file">{{ file }}</a><br>
    </template>
</div>
      <div class="row q-ma-md col-xs-12 justify-end">
        <div class="col-xs-4">
          <q-btn
            @click="remove_files"
            label="첨부파일삭제" />
          <q-btn
            @click="save"
            label="등록" />
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
      category_disabled: true,
      properties: '',
      notice: false,
      title: '',
      created_at: '',
      body: '',
      files: [],
    }
  },
  props: ['action', 'id'],
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
    save () {
      this.properties = []
      if (this.notice) {
        this.properties.push('notice')
      }

      console.log(this.files)
      if (this.action === 'new') {
        this.$axios.post(`posts`, {
          'major_category': this.major_category,
          'minor_category': this.minor_category,
          'properties': this.properties,
          'title': this.title,
          'body': this.body,
          'files': this.files,
          'class_id': this.id,
          'created_at': (new Date(this.created_at)).toISOString(),
        }).then(({data}) => {
          this.$router.go(-1)
        })
      } else if (this.action === 'update') {
        this.$axios.put(`posts/` + this.id, {
          'major_category': this.major_category,
          'minor_category': this.minor_category,
          'properties': this.properties,
          'title': this.title,
          'body': this.body,
          'files': this.files,
          'created_at': (new Date(this.created_at)).toISOString(),
        }).then(({data}) => {
          this.$router.go(-1)
        })
      }
    },
    add_file (files) {
      console.log(files)
      for (let i = 0; i < files.length; i++) {
        this.files.push(files[i].name)
      }
      this.$refs.uploader.upload()
    },
    remove_file (files) {
      for (let i = 0; i < files.length; i++) {
        const index = array.indexOf(files[i].name);
        this.files.splice(index, 1);
      }
    },
    remove_files () {
      this.files = []
    },
    
  },
  created () {
    let user = LocalStorage.get.item('user_')
    console.log(JSON.parse(user.role))
    console.log(JSON.parse(user.role).includes('admin'))
    if (JSON.parse(user.role).includes('admin')) {
      this.category_disabled = false
    }
    this.created_at = Date.now()

    this.$axios.get(`posts/categories`)
      .then(({ data }) => { this.major_categories = data })
    this.$axios.get(`posts/properties`)
      .then(({ data }) => {})
    if (this.action === 'update') {
      this.$axios.get(`posts/` + this.id)
        .then(({ data }) => {
          this.major_category = data.major_category
          this.minor_category = data.minor_category
          //this.category_disabled = true
          this.properties = data.properties
          if (data.properties && JSON.parse(data.properties).includes('notice')) {
            this.notice = true
          }
          this.title = data.title
          this.body = data.body
          if (data.files)
            this.files = JSON.parse(data.files)
          if (this.files == "")
            this.files = []
          this.class_id = data.class_id
          this.created_at = data.created_at
        })
    } else if (this.action === 'new') {
      if (this.id) {
        this.$axios.get(`classes/` + this.id)
          .then(({ data }) => {
            this.major_category = data.major_category
            this.minor_category = data.minor_category
            this.category_disabled = true
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
