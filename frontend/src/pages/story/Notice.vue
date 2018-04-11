<template>
  <div>
    <div class="page-intro">
      <img
        src="~assets/img/story_background_image.png"
        class="section__background-image" >

      <div class="title--emphasized">
        하우학교에서 공지사항을 알려드립니다. <br>꼭 읽어주세요.

      </div>

    </div>

    <div class="container">
      <div class="page-name">
        공지사항
      </div>
      <hr class="page-name--bottom-border" >
    </div>

    <!--
    <div class="row justify-center">
      <div class="col-xs-10">
        <q-tabs
          align="justify"
          two-lines
          color="grey" >
<template v-for="recent in recents">
          <q-tab
            default
            :name="recent.id.toString()"
            slot="title"
            :label="recent.title"
            class="tab"
            style="background-color: inherit;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    transition: 0.3s;
    font-size: 17px;
    width: 33.333%;"/>
</template>

<template v-for="recent in recents">
          <q-tab-pane :name="recent.id.toString()" v-html="recent.body" />
</template>
        </q-tabs>
      </div>
    </div>
-->

    <!--toggle part-->
    <div class="container notice__section">
      <template v-for="recent in recents2">
        <button
          class="enter__collapsible"
          @click="recent.hidden = !recent.hidden">{{ recent.title }}</button>
        <div
          class="enter__content"
          v-html="recent.body"
          :class="{hidden: recent.hidden}"/>
        <div
          v-if="recent.files"
          class="enter__content"
          style="padding: 0px 20px;"
          :class="{hidden: recent.hidden}">첨부파일</div>
        <div
          v-if="recent.files"
          class="enter__content"
          style="padding: 0px 20px 30px 20px;"
          :class="{hidden: recent.hidden}">
          <template v-for="file in recent.files">
            <a :href="'/api/upload/' + file">{{ file }}</a>
          </template>
        </div>
      </template>
    </div><!--container notice__section-->
    <div style="clear:both"/>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      recents: [],
      recents2: []
    }
  },
  methods: {
    fetch_data: function () {
      let query = {}
      query['minor_category'] = 'notice'
      // query['recent'] = '10'
      var self = this
      self.$axios.get('posts/homepage', {params: query})
        .then(function (response) {
          let data = response.data
          /*
          for (let i = 0; i < 3 && i < data.length; i++) {
            self.recents.push(data[i])
          }
          */
          for (let i = 0; i < data.length; i++) {
            self.recents2.push(data[i])
            if (data[i].files) {
              if (data[i].files != '[]') {
                self.recents2[i].files = JSON.parse(data[i].files)
              } else {
                self.recents2[i].files = false
              }
            } else {
              self.recents2[i].files = false
            }
          }
          self.$set(self.recents2[0], 'hidden', false)
          for (let i = 1; i < self.recents2.length; i++) {
            self.$set(self.recents2[i], 'hidden', true)
          }
        })
    }
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
