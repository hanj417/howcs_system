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

    <!--toggle part-->
    <div class="container notice__section">
<template v-for="recent in recents2">
      <button class="enter__collapsible" @click="recent.hidden = !recent.hidden">{{ recent.title }}</button>
      <div class="enter__content" v-html="recent.body" :class="{hidden: recent.hidden}"/>
</template>
    </div><!--container notice__section-->
    <div style="clear:both"/>
  </div>
</template>

<script>
export default {
  data () {
    return {
      recents: [],
      recents2: [],
    }
  },
  methods: {
    fetch_data () {
      let query = {}
      query['minor_category'] = 'notice'
      query['recent'] = '10'
      this.$axios.get(`posts/homepage`, {params: query})
        .then(({ data }) => {
          for (let i = 0; i < 3; i++) {
            this.recents.push(data[i]) 
          }
          for (let i = 3; i < data.length; i++) {
            this.recents2.push(data[i]) 
          }
          for (let i = 0; i < this.recents2.length; i++) {
            this.recents2[i]['hidden'] = false 
          }
        })
    }
  },
  created () {
    this.fetch_data()
  }
}
</script>
