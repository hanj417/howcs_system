<template>
  <q-page
    padding
    class="row justify-center">
    <q-table
      :data="table_data"
      :columns="columns"
      :filter="filter"
      :visible-columns="visible_columns"
      :pagination.sync="pagination"
      :selection="selection"
      :selected.sync="item"
      row-key="title"
      color="secondary"
      class="col-xs-11"
    >
      <template
        slot="top-left"
        slot-scope="props">
        <q-search
          hide-underline
          color="secondary"
          v-model="filter"
          class="col-6"
        />
      </template>
      <template
        v-if="is_admin"
        slot="top-selection"
        slot-scope="props">
        <div class="col" />
        <q-btn
          color="negative"
          flat
          round
          delete
          icon="delete"
          @click="remove" />
      </template>
      <q-td slot="body-cell-files" slot-scope="props" :props="props">
        <a :href="'/api/upload/' + props.value">{{  props.value }}</a>
      </q-td>
    </q-table>
    <q-page-sticky
      position="bottom-right"
      :offset="[18, 18]">
      <q-btn
        v-if="is_admin"
        round
        color="primary"
        @click="add_modal = true"
        icon="add" />
    </q-page-sticky>
    <q-modal
      v-model="add_modal"
      class="row justify-center">
      <div class="col-xs-12">
        <q-input v-model="resource_name" float-label="이름" />
        <div class="col-xs-12 q-mt-xl q-pt-xl">
        <q-uploader ref="uploader" url="/api/upload" @add="add_file" @remove:done(file)="remove_file" hide-upload-button auto-expand no-thumbnails clearable hide-upload-progress />
        </div>
      </div> 
      <div class="row q-ma-md col-xs-12 justify-end">
        <div class="col-xs-5">
          <q-btn
            color="primary"
            @click="save"
            label="추가"
          />
          <q-btn
            color="primary"
            @click="add_modal = false"
            label="닫기"
          />
        </div>
      </div>
    </q-modal>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'

export default {
  data () {
    return {
      table_data: [],
      columns: [
        { name: 'title', label: '제목', field: 'title', sortable: true, align: 'left' },
        { name: 'files', label: '파일', field: row => JSON.parse(row.files)[0], sortable: true, align: 'left' },
      ],
      filter: '',
      visible_columns: ['title', 'files'],
      item: [],
    pagination: {
      sortBy: null, // String, column "name" property value
      descending: false,
      page: 1,
      rowsPerPage: 0 // current rows per page being displayed
    },

      selection: 'none',
      is_admin: false,
      resource_name: '',
      files: [],
      add_modal: false,
    }
  },
  watch: {
    'minor_category' (value) {
      this.fetch_data()
    },
  },
  props: ['major_category', 'minor_category'],
  methods: {
    fetch_data () {
      let query = {}
      query['major_category'] = this.major_category
      query['minor_category'] = this.minor_category
      this.$axios.get(`posts`, {params: query})
        .then(({ data }) => {
          this.table_data = data
        })
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
    save () {
        this.$axios.post(`posts`, {
          'major_category': this.major_category,
          'minor_category': this.minor_category,
          'properties': '[]',
          'title': this.resource_name,
          'body': '',
          'files': this.files,
        }).then(({data}) => {
          this.fetch_data()
        })
        this.add_modal = false
    },
    remove () {
      this.$axios.delete(`posts/` + this.item[0].id)
        .then(({ data }) => { this.fetch_data() })
    }
  },
  created () {
    let user = LocalStorage.get.item('user_')
    console.log(JSON.parse(user.role))
    console.log(JSON.parse(user.role).includes('admin'))
    if (JSON.parse(user.role).includes('admin')) {
      this.is_admin = true
      this.selection = 'single'
    }

    this.fetch_data()
  }
}
</script>
