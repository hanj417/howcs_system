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
<!--
      <q-editor v-model="body"
        :toolbar="[
        ['bold', 'italic', 'strike', 'underline', 'subscript', 'superscript'],
        ['token', 'hr', 'link', 'custom_btn'],
        ['print', 'fullscreen'],
        [
          {
            label: $q.i18n.editor.formatting,
            icon: $q.icon.editor.formatting,
            list: 'no-icons',
            options: ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'code']
          },
          {
            label: $q.i18n.editor.fontSize,
            icon: $q.icon.editor.fontSize,
            fixedLabel: true,
            fixedIcon: true,
            list: 'no-icons',
            options: ['size-1', 'size-2', 'size-3', 'size-4', 'size-5', 'size-6', 'size-7']
          },
          {
            label: $q.i18n.editor.defaultFont,
            icon: $q.icon.editor.font,
            fixedIcon: true,
            list: 'no-icons',
            options: ['default_font', 'arial', 'arial_black', 'comic_sans', 'courier_new', 'impact', 'lucida_grande', 'times_new_roman', 'verdana']
          },
          'removeFormat'
        ],
        ['quote', 'unordered', 'ordered', 'outdent', 'indent'],
        [
          {
            label: $q.i18n.editor.align,
            icon: $q.icon.editor.align,
            fixedLabel: true,
            list: 'only-icons',
            options: ['left', 'center', 'right', 'justify']
          },
          {
            label: $q.i18n.editor.align,
            icon: $q.icon.editor.align,
            fixedLabel: true,
            options: ['left', 'center', 'right', 'justify']
          }
        ],
        ['undo', 'redo']
      ]"
      :fonts="{
        arial: 'Arial',
        arial_black: 'Arial Black',
        comic_sans: 'Comic Sans MS',
        courier_new: 'Courier New',
        impact: 'Impact',
        lucida_grande: 'Lucida Grande',
        times_new_roman: 'Times New Roman',
        verdana: 'Verdana'
      }"/>
-->
      <div>
      <quill-editor v-model='body'  style="height: 300px;"/>
      </div>
      <div class="col-xs-12 q-mt-xl q-pt-xl">
      <q-uploader ref="uploader" url="/api/upload" @add="added" @uploaded="uploaded" />
      </div>
      <div class="row q-ma-md col-xs-12 justify-end">
        <div class="col-xs-2">
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
      body: '',
      files: '',
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
      if (this.action === 'new') {
        this.$axios.post(`posts`, {
          'major_category': this.major_category,
          'minor_category': this.minor_category,
          'properties': this.properties,
          'title': this.title,
          'body': this.body,
          'files': this.files,
          'class_id': this.id
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
        }).then(({data}) => {
          this.$router.go(-1)
        })
      }
    },
added (files) {
        console.log(files)
this.files = []
for (let i = 0; i < files.length; i++) {
this.files.push(files[i].name)
}
        this.$refs.uploader.upload()
      },
uploaded (files) {
    },
    
  },
  created () {
    let user = LocalStorage.get.item('user_')
    console.log(JSON.parse(user.role))
    console.log(JSON.parse(user.role).includes('admin'))
    if (JSON.parse(user.role).includes('admin')) {
      this.category_disabled = false
    }

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
          if (JSON.parse(data.properties).includes('notice')) {
            this.notice = true
          }
          this.title = data.title
          this.body = data.body
          this.files = data.files
          this.class_id = data.class_id
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
