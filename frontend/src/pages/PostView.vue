<template>
  <q-page
    padding
    class="row justify-center">
    <div style="width: 500px; max-width: 80vw;">
      <q-input
        v-model="title"
        float-label="제목" />
      <q-option-group
        label="대분류"
        type="radio"
        v-model="major_category"
        inline
        disabled
        :options="major_categories" />
      <q-option-group
        label="분류"
        type="radio"
        v-model="minor_category"
        inline
        disabled
        :options="minor_categories" />
      <q-editor
        readonly
        :toolbar="[]"
        v-model="body"
        label="본문"
        min-height="400px"
        max-height="400px"/>
        <!--
      <div class="row q-ma-md col-xs-12 justify-end">
      <div class="col-xs-2">
  <q-btn @click="save" label="등록" />
      </div>
      </div>
-->
    </div>
  </q-page>
</template>

<script>
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
      body: ''
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
          'class_id': this.$route.params.id
        }).then(({data}) => {
          this.$router.go(-1)
        })
      } else if (this.action === 'update') {
        this.$axios.put(`posts/` + this.id, {
          'major_category': this.major_category,
          'minor_category': this.minor_category,
          'properties': this.properties,
          'title': this.title,
          'body': this.body
        }).then(({data}) => {
          this.$router.go(-1)
        })
      }
    }
  },
  created () {
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
        /*
      if (JSON.parse(data.properties).includes('notice')) {
        this.notice = true
      }
*/
        this.title = data.title
        this.body = data.body
        this.class_id = data.class_id
      })
  }
}
</script>
