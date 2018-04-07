<template>
  <div>
    <div class="page-intro">
      <img
        src="~assets/img/howstory_background_image.png"
        class="section__background-image" >

      <div class="title--emphasized">
        오늘도 하우는 ( &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ) 하다

      </div>

    </div>

    <div class="container">
      <div class="page-name">
        하우하다
      </div>
      <hr class="page-name--bottom-border" >
    </div>

    <div class="container">
      <div class="visible-xs">
        <div class="container story-story__carousel">
          <div
            id="story-story-carousel"
            class="carousel slide"
            data-ride="carousel"
            data-interval="false">
            <ol class="carousel-indicators">
              <li
                data-target="#story-story-carousel"
                data-slide-to="0"
                class="active"/>
              <li
                data-target="#story-story-carousel"
                data-s:ide-to="1"/>
              <li
                data-target="#story-story-carousel"
                data-slide-to="2"/>
                <!-- <li data-target="#story-story-carousel" data-slide-to="3"></li>
              <li data-target="#story-story-carousel" data-slide-to="4"></li>
              <li data-target="#story-story-carousel" data-slide-to="5"></li>
              <li data-target="#story-story-carousel" data-slide-to="6"></li>
              <li data-target="#story-story-carousel" data-slide-to="7"></li>
              <li data-target="#story-story-carousel" data-slide-to="8"></li>
              <li data-target="#story-story-carousel" data-slide-to="9"></li> -->
            </ol>

            <div
              class="carousel-inner"
              role="listbox">
<template v-for="post in posts">
              <a
                :href="'/story/story_view/' + post.id"
                class="item story-story__carousel-item active">
                <img
                  :src="post.img"
                  class="full-width">

                <div class="story-story__title">
{{ post.title }}
                </div>

                <div class="story-story__content">
{{ post.ellipsis }}
                </div>

              </a>
</template>

            </div>

            <a
              class="left carousel-control"
              href="#story-story-carousel"
              role="button"
              data-slide="prev">
              <span
                class="glyphicon glyphicon-chevron-left"
                aria-hidden="true"/>
            </a>
            <a
              class="right carousel-control"
              href="#story-story-carousel"
              role="button"
              data-slide="next">
              <span
                class="glyphicon glyphicon-chevron-right"
                aria-hidden="true"/>
            </a>

          </div>

        </div>
      </div>

      <div class="hidden-xs">
        <div class="row story-story__row">
<template v-for="post in posts">
          <a
            :href="'/story/story_view/' + post.id"
            class="col-sm-4 col-md-4 col-lg-4 story-story__article">
            <img
              :src="post.img"
              class="story-story__image--black" >

            <div class="story-story__title">
{{ post.title }}
            </div>

            <div class="story-story__content">
{{ post.ellipsis }}
            </div>

          </a>
</template>
        </div>

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
      posts: [],
    }
  },
  methods: {
    fetch_data: function () {
      let query = {}
      query['minor_category'] = 'story'
      //query['recent'] = '3'
      var self = this
      self.$axios.get('posts/homepage', {params: query})
        .then(function (response) {
          let data = response.data
          self.posts = data
          for (let i = 0; i < self.posts.length; i++) {
            self.posts[i]['img'] = "/assets/img/howstoryP.jpg"
            let files = JSON.parse(self.posts[i]['files'])
            if (files && files.length > 0) {
              self.posts[i]['img'] = "/api/upload/" + files[0]
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
