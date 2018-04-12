<template>
  <div>

    <div class="page-intro">
      <img
        src="~assets/img/howstory_background_image.png"
        class="section__background-image" >

      <div class="title--emphasized">
        하우, (사진으로 이야기) 하다

      </div>

    </div>

    <div class="container">
      <div class="page-name">
        하우포토
      </div>
      <hr class="page-name--bottom-border" >
    </div>

    <div class="container">
      <div class="row">

        <template v-for="post in posts">
            <div class="col-sm-4 col-md-3 col-lg-3" >
          <a
            :href="'/story/photo_view/' + post.id">
            <div id="howphoto">

              <div id="howphoto">
                <img
                  :src="post.img"
                  class="image"
                  style="width:100%">
                <div class="middle">
                  <div class="text">{{ post.title }}</div>
                </div>
              </div>

            </div>
          </a>
            </div>
        </template>

      </div>

    </div>

    <div>
      <div class="space"/>
      <div class="space"/>
    </div>

  </div>
</template>

<script>
export default {
  data: function () {
    return {
      posts: []
    }
  },
  methods: {
    fetch_data: function () {
      let query = {}
      query['minor_category'] = 'photo'
      query['recent'] = '4'
      var self = this
      self.$axios.get('posts/homepage', {params: query})
        .then(function (response) {
          let data = response.data
          self.posts = data
          for (let i = 0; i < self.posts.length; i++) {
            self.posts[i]['img'] = '/assets/img/howstoryP.jpg'
            let files = JSON.parse(self.posts[i]['files'])
            if (files && files.length > 0) {
              self.posts[i]['img'] = '/api/upload/' + files[0]
            }
          }
        })
    }
  },
  created: function () {
    this.fetch_data()
  }
}
</script>
