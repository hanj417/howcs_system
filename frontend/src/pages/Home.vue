<template>
  <div>
    <div class="landing__intro">
      <div class="hidden-xs hidden-sm">
        <video
          class="intro__background-video"
          poster="~assets/img/landingbg.png"
          muted
          autoplay
          loop>
          <source
            src="~assets/img/movie_intro.mp4"
            type="video/mp4" >
        </video>
      </div>
      <div class="hidden-md hidden-lg">
        <img
          src="~assets/img/landingbg.png"
          class="intro__background-video--replacement" >
      </div>
      <div class="container">
        <div class="intro__name">
          하늘빛우리학교
        </div>
        <div class="intro__fullname">
          하나님의 꿈을 함께 이루어가는 행복한 교육공동체
        </div>
        <div class="intro__vision">
          <div class="visible-xs">
            기독교세계관을 바탕으로 한 기독교교육을 통하여 <span class="intro__vision--emphasized">영성과 인성과 실력을 통합한</span> 행복한 예수 제자로서 하나님을 영화롭게 하며 이웃에 사랑을 실천하고 세상을 충만하게 하여 <span class="intro__vision--emphasized">하나님의 꿈</span>을 함께 이루어가는 책임 있는 그리스도인으로 살아갈 수 있도록 돕는다

          </div>
          <div class="hidden-xs">
            기독교세계관을 바탕으로 한 기독교교육을 통하여<br>
            <span class="intro__vision--emphasized">영성과 인성과 실력을 통합한</span> 행복한 예수 제자로서<br>
            하나님을 영화롭게 하며 이웃에 사랑을 실천하고<br>
            세상을 충만하게 하여 <span class="intro__vision--emphasized">하나님의 꿈</span>을 함께 이루어가는<br>
            책임 있는 그리스도인으로 살아갈 수 있도록 돕는다
          </div>
        </div>

      </div>
    </div>

    <div class="container landing__section">
      <div class="section__title">
        핵심가치
      </div>

      <div class="section__subtitle">
        핵심가치에 따른 교육적인 기초
      </div>

      <div class="row project__list">

        <div class="col-xs-12 col-sm-6 col-md-3 col-lg-3 project__detail">
          <a
            href="/about/worth"
            class="project__link worthbg1">
            <div class="worth__category">
              <img
                src="~assets/img/about_ic1.png"
                width="50%">
            </div>

            <div class="worth__explain">
              하나님이 불어넣어 주신 생생하고 기운찬 숨을 쉬며 하나님의 성품을 닮아가는 교육 창2:7
            </div>

            <button class="worth__more-btn">
              +
          </button></a>
        </div>

        <div class="col-xs-12 col-sm-6 col-md-3 col-lg-3 project__detail">
          <a
            href="/about/worth"
            class="project__link worthbg2">
            <div class="worth__category">
              <img
                src="~assets/img/about_ic2.png"
                width="50%">
            </div>

            <div class="worth__explain">
              공동의 이익을 위해 하나님이 주신 선물인 저마다의 몫(소명)이 주도하는 자발성 교육 고전 12:7
            </div>

            <button class="worth__more-btn">
              +
          </button></a>
        </div>

        <div class="col-xs-12 col-sm-6 col-md-3 col-lg-3 project__detail">
          <a
            href="/about/worth"
            class="project__link worthbg3">
            <div class="worth__category">
              <img
                src="~assets/img/about_ic3.png"
                width="50%">
            </div>

            <div class="worth__explain">
              예수님처럼 영성과 인성과 실력을 통합한 역량을 갖춰 세상의 문화를 변혁하는 교육 골1:15
            </div>

            <button class="worth__more-btn">
              +
          </button></a>
        </div>

        <div class="col-xs-12 col-sm-6 col-md-3 col-lg-3 project__detail">
          <a
            href="/about/worth"
            class="project__link worthbg4">
            <div class="worth__category">
              <img
                src="~assets/img/about_ic4.png"
                width="50%">
            </div>

            <div class="worth__explain">
              세상을 충만케 하려는 하나님의 꿈 하나님 나라를 위해 우리의 최선을 드리는 교육 요3:16
            </div>

            <button class="worth__more-btn">
              +
          </button></a>
        </div>

      </div>
    </div><!-- container landing__section-->

    <div class="container landing__section">
      <div class="section__title">
        추천의 글
      </div>

      <div class="section__subtitle">
        하우학교를 추천하는 사람들
      </div>

      <div class="visible-xs">
        <div class="container waglpedia__carousel">
          <div
            id="waglpedia-carousel"
            class="carousel slide"
            data-ride="carousel"
            data-interval="false">
            <ol class="carousel-indicators">
              <li
                data-target="#waglpedia-carousel"
                data-slide-to="0"
                class="active"/>
              <li
                data-target="#waglpedia-carousel"
                data-slide-to="1"/>
              <li
                data-target="#waglpedia-carousel"
                data-slide-to="2"/>
              <li
                data-target="#waglpedia-carousel"
                data-slide-to="3"/>
              <li
                data-target="#waglpedia-carousel"
                data-slide-to="4"/>
              <li
                data-target="#waglpedia-carousel"
                data-slide-to="5"/>
              <li
                data-target="#waglpedia-carousel"
                data-slide-to="6"/>
                <!--  <li data-target="#waglpedia-carousel" data-slide-to="7"></li>
              <li data-target="#waglpedia-carousel" data-slide-to="8"></li> -->
            </ol>

            <div
              class="carousel-inner"
              role="listbox">

              <template v-for="item in items">
                <div
                  class="item"
                  :class="{ active: item.active }">
                  <a
                    href="#"
                    class="row man--mobile">
                    <div class="col-xs-6 man__text-container--mobile">
                      <div class="man__text">
                        <span class="man__text--emphasized">{{ item.name }}</span><br>{{ item.desc }}<br>
                        {{ item.title }}
                      </div>

                    </div>
                    <div
                      class="col-xs-6 man__image-container--mobile "
                      :class="item.cl"/>
                  </a>
                </div>
              </template>

              <div class="item">
                <a
                  href="#"
                  class="row man--mobile">
                  <div class="col-xs-6 man__text-container--mobile">
                    <div class="man__text">
                      <span class="man__text--emphasized">임규석</span><br>(하늘빛우리교회 장로 양성초․중학교장)<br>
                      하나님이 하신 일, 하나님이 하실 일
                    </div>

                  </div>
                  <div class="col-xs-6 man__image-container--mobile manbg2"/>
                </a>
              </div>

              <div class="item">
                <a
                  href="#"
                  class="row man--mobile">
                  <div class="col-xs-6 man__text-container--mobile">
                    <div class="man__text">
                      <span class="man__text--emphasized">정명진</span><br>(하늘빛우리교회 장로 을지대학교 보건환경안전학과 교수)<br>
                      인성과 영성과 실력을 통합하는 교육
                    </div>

                  </div>
                  <div class="col-xs-6 man__image-container--mobile manbg3"/>
                </a>
              </div>

              <div class="item">
                <a
                  href="#"
                  class="row man--mobile">
                  <div class="col-xs-6 man__text-container--mobile">
                    <div class="man__text">
                      <span class="man__text--emphasized">박현수</span><br>(별무리학교장)<br>
                      이 시대의 어두움을 밝히는 빛이 되는 학교
                    </div>

                  </div>
                  <div class="col-xs-6 man__image-container--mobile manbg4"/>
                </a>
              </div>

              <div class="item">
                <a
                  href="#"
                  class="row man--mobile">
                  <div class="col-xs-6 man__text-container--mobile">
                    <div class="man__text">
                      <span class="man__text--emphasized">임종화</span><br>(좋은교사운동 공동대표)<br>
                      ‘하늘빛우리학교’의 첫걸음을 축하하며
                    </div>

                  </div>
                  <div class="col-xs-6 man__image-container--mobile manbg5"/>
                </a>
              </div>

              <div class="item">
                <a
                  href="#"
                  class="row man--mobile">
                  <div class="col-xs-6 man__text-container--mobile">
                    <div class="man__text">
                      <span class="man__text--emphasized">한은경</span><br>(두란노어머니학교 본부장)<br>
                      새벽같이 영롱한 다음 세대가 양육되기를
                    </div>

                  </div>
                  <div class="col-xs-6 man__image-container--mobile manbg6"/>
                </a>
              </div>

              <div class="item">
                <a
                  href="#"
                  class="row man--mobile">
                  <div class="col-xs-6 man__text-container--mobile">
                    <div class="man__text">
                      <span class="man__text--emphasized">김성천</span><br>(교육정책디자인연구소장 혁신학교란 무엇인가 저자)<br>
                      하늘빛 우리 학교의 성장을 기대하며
                    </div>

                  </div>
                  <div class="col-xs-6 man__image-container--mobile manbg7"/>
                </a>
              </div>

            </div>

            <a
              class="left carousel-control"
              href="#waglpedia-carousel"
              role="button"
              data-slide="prev">
              <span
                class="glyphicon glyphicon-chevron-left"
                aria-hidden="true"/>
            </a>
            <a
              class="right carousel-control"
              href="#waglpedia-carousel"
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
        <div class="container">
          <div class="row">

            <template v-for="item in items">
              <a
                href="#"
                class="col-sm-4 col-md-3 col-lg-3 man__item"
                @mouseover="item.desktop_active = true"
                @mouseleave="item.desktop_active = false">
                <div
                  class="man__image-container--desktop"
                  :class="{hidden: item.desktop_active}">
                  <div
                    class="man__textl"
                    v-html="item.desktop_title"/>

                  <div
                    class="man__texts"
                    v-html="item.desktop_desc"/>
                </div>

                <div
                  class="man__text-container--desktop"
                  :class="[item.desktop_active? '':'hidden', item.cl]">
                  <div class="man__text--desktop">
                    {{ item.text }}
                  </div>

                </div>
              </a>
            </template>

            <a
              href="#"
              class="col-sm-4 col-md-3 col-lg-3 man__item">
              <!-- <div class="man__see-more">
                <span class="hidden">더보기</span>
              </div> -->
            </a>

          </div>
        </div>
      </div>
    </div>

    <div class="container landing__section landing__section--how-story">
      <div class="section__title">
        하우 스토리
      </div>

      <div class="section__subtitle">
        위대한 일상을 살아가는 하우학교 이야기
      </div>

      <div class="row">

        <a
          href="/story/notice"
          target="_blank"
          class="col-xs-12 col-sm-4 col-md-4 col-lg-4 how-story">
          <div class="how-story__summary">
            <img
              :src="recent_notice.img"
              class="how-story__background-image" >
            <span class="how-story__title">{{ recent_notice.title }}</span>
          </div>
          <div class="how-story__detail">
            <div class="how-story__content">{{ recent_notice.ellipsis }}...
            </div>
            <div class="how-story__created: function-at">
              {{ recent_notice.date }}
            </div>
            <div class="how-story__author">
              하우학교
            </div>
          </div>
        </a>

        <a
          href="/story/story"
          target="_blank"
          class="col-xs-12 col-sm-4 col-md-4 col-lg-4 how-story">
          <div class="how-story__summary">
            <img
              :src="recent_story.img"
              class="how-story__background-image" >
            <span class="how-story__title">{{ recent_story.title }}</span>
          </div>
          <div class="how-story__detail">
            <div class="how-story__content">{{ recent_story.ellipsis }}...</div>
            <div class="how-story__created: function-at">
              {{ recent_story.date }}
            </div>
            <div class="how-story__author">
              하우학교
            </div>
          </div>
        </a>

        <a
          href="/story/photo"
          target="_blank"
          class="col-xs-12 col-sm-4 col-md-4 col-lg-4 how-story">
          <div class="how-story__summary">
            <img
              :src="recent_photo.img"
              class="how-story__background-image" >
            <span class="how-story__title">{{ recent_photo.title }}</span>
          </div>
          <div class="how-story__detail">
            <div class="how-story__content">
              {{ recent_photo.ellipsis }}...
            </div>
            <div class="how-story__created: function-at">
              {{ recent_photo.date }}
            </div>
            <div class="how-story__author">
              하우학교
            </div>
          </div>
        </a>

      </div>
    </div>

    <div class="hidden-xs">
      <div class="space"/>
      <div class="space"/>
    </div>

    <div class="landing__section">
      <div class="section__title">
        하우학교와 함께하는 사람들
      </div>

      <div class="section__subtitle">
        하우학교의 철학과 가치를 공유하며 협력하는 교회와 단체와 사람들
      </div>

      <div class="container">

        <div class="social-media__icon-container--big">
          <p align="center">
            <a
              href="#"
              target="_blank"><img
                src="~assets/img/logoshow1.jpg"
                class="social-media__icon--big" ></a>
            <a
              href="#"
              target="_blank"><img
                src="~assets/img/logoshow2.jpg"
                class="social-media__icon--big" ></a>
            <a
              href="#"
              target="_blank"><img
                src="~assets/img/logoshow3.jpg"
                class="social-media__icon--big" ></a>
          </p>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      recent_notice: {},
      recent_story: {},
      recent_photo: {},
      items: [
        {title: '한국교회와 이 땅을 위해 쓰임 받는 학교',
          desktop_title: '한국교회와 이 땅을 위해<br> 쓰임 받는 학교',
          mobile_active: true,
          desktop_active: true,
          name: '이찬수',
          desc: '(분당우리교회 담임목사)',
          desktop_desc: '분당우리교회 담임목사<br>이찬수',
          text: '교회 안의 인재만 아니라 교회 바깥에서도 통할 수 있는 인재의 요람으로 하늘빛우리학교가 한국교회와 이 땅을 위해 쓰임 받게 되기를 소망합니다.',
          cl: 'manbg1'},
        {title: '한국교회와 이 땅을 위해 쓰임 받는 학교',
          desktop_title: '하나님이 하신 일<br>하나님이 하실 일',
          mobile_active: false,
          desktop_active: false,
          name: '임규석',
          desc: '(하늘빛우리교회 장로 양성초․중학교장)',
          desktop_desc: '하늘빛우리교회 장로<br>양성초․중학교장<br>임규석',
          text: '모두가 한 마음으로 준비해온 기도의 응답이었고 하나님이 하신 일을 체험하는 순간이었습니다. 그래서 앞으로 하우학교을 통해 하나님이 하실 일들이 기대가 됩니다.',
          cl: 'manbg2'},
        {title: '인성과 영성과 실력을 통합하는 교육',
          desktop_title: '인성과 영성과 실력을<br>통합하는 교육',
          mobile_active: false,
          desktop_active: false,
          name: '정명진',
          desc: '(하늘빛우리교회 장로 을지대학교 보건환경안전학과 교수)',
          desktop_desc: '하늘빛우리교회 장로<br>을지대학교 보건환경안전학과 교수<br>정명진',
          text: '신앙과 성품, 학업이 서로 분리되지 않고 연결되는 기독교 교육을 실천하기 위해 세워진 하우학교를 통해 건강한 하나님의 사람들이 배출되어 하나님 나라가 아름답게 확장되기를 기대합니다.',
          cl: 'manbg3'},
        {title: '이 시대의 어두움을 밝히는 빛이 되는 학교',
          desktop_title: '이 시대의 어두움을 밝히는<br>빛이 되는 학교',
          mobile_active: false,
          desktop_active: false,
          name: '박현수',
          desc: '(별무리학교장)',
          desktop_desc: '별무리학교장<br>박현수',
          text: '하나님께서 주신 꿈을 품고 그 길을 기꺼이 가려고 하는 모든 교직원들의 열정에 더해 학부모님들과 후원자들이 동참하여 이 시대의 어두움을 밝히는 빛이 되는 학교가 되시기를 기도드립니다.',
          cl: 'manbg4'},
        {title: '‘하늘빛우리학교’의 첫걸음을 축하하며',
          desktop_title: '‘하늘빛우리학교’의 첫걸음을 축하하며',
          mobile_active: false,
          desktop_active: false,
          name: '임종화',
          desc: '(좋은교사운동 공동대표)',
          desktop_desc: '좋은교사운동 공동대표<br>임종화',
          text: '하늘빛우리학교가 만들어가는 새로운 교육의 길을 많은 사람들이 따라가게 될 것입니다. 이를 위해 함께 동역하며 기도하겠습니다.',
          cl: 'manbg5'},
        {title: '새벽같이 영롱한 다음 세대가 양육되기를',
          desktop_title: '새벽같이 영롱한 다음 세대가 양육되기를',
          mobile_active: false,
          desktop_active: false,
          name: '한은경',
          desc: '(두란노어머니학교 본부장)',
          desktop_desc: '두란노어머니학교 본부장<br>한은경',
          text: '황무한 이 시대에 여름 비 같이 해갈해 주는 학교로 우뚝 서길 한 마음으로 기도합니다.',
          cl: 'manbg6'},
        {title: '새하늘빛 우리 학교의 성장을 기대하며',
          desktop_title: '새하늘빛 우리 학교의 성장을 기대하며',
          mobile_active: false,
          desktop_active: false,
          name: '김성천',
          desc: '(교육정책디자인연구소장 혁신학교란 무엇인가 저자)',
          desktop_desc: '교육정책디자인연구소장<br>혁신학교란 무엇인가 저자<br>김성천',
          text: '시대의 고통에 대답할 수 있는 기독교인을 길러내는 학교를, 공교육에 신선한 자극을 줄 수 있는 모델링 학교를, 아이들과 학생과 학부모가 행복한 학교를… 그 학교가 바로 하늘빛 우리학교이기를 기대하고 응원합니다.',
          cl: 'manbg7'}
      ]
    }
  },
  methods: {
    fetch_data: function () {
      let query = {}
      query['minor_category'] = 'notice'
      query['recent'] = '1'
      var self = this
      self.$axios.get('posts/homepage', {params: query})
        .then(function (response) {
          let data = response.data
          if (data.length > 0) {
            self.recent_notice = data[0]
          } else {
            self.recent_notice = {title: '', ellipsis: ''}
          }
          self.recent_notice['date'] = (new Date(self.recent_notice.created_at)).toISOString().substr(0, 10)
          self.recent_notice['img'] = '/assets/img/how_notice.png'
          let files = JSON.parse(self.recent_notice['files'])
          if (files && files.length > 0) {
            let extensions = ['jpg', 'png', 'gif', 'jpeg', 'JPG', 'PNG', 'GIF', 'JPEG']
            if (extensions.indexOf(files[0].split('.').pop()) !== -1) {
              self.recent_notice['img'] = '/api/upload/' + files[0]
            }
          }
        })

      let query_story = {}
      query_story['minor_category'] = 'story'
      query_story['recent'] = '1'
      self.$axios.get('posts/homepage', {params: query_story})
        .then(function (response) {
          let data = response.data
          if (data.length > 0) {
            self.recent_story = data[0]
          } else {
            self.recent_story = {title: '', ellipsis: ''}
          }
          self.recent_story['date'] = (new Date(self.recent_story.created_at)).toISOString().substr(0, 10)
          self.recent_story['img'] = '/assets/img/how_story.png'
          let files = JSON.parse(self.recent_story['files'])
          if (files && files.length > 0) {
            let extensions = ['jpg', 'png', 'gif', 'jpeg', 'JPG', 'PNG', 'GIF', 'JPEG']
            if (extensions.indexOf(files[0].split('.').pop()) !== -1) {
              self.recent_story['img'] = '/api/upload/' + files[0]
            }
          }
        })

      let query_photo = {}
      query_photo['minor_category'] = 'photo'
      query_photo['recent'] = '1'
      self.$axios.get('posts/homepage', {params: query_photo})
        .then(function (response) {
          let data = response.data
          if (data.length > 0) {
            self.recent_photo = data[0]
          } else {
            self.recent_photo = {title: '', ellipsis: ''}
          }
          self.recent_photo['date'] = (new Date(self.recent_photo.created_at)).toISOString().substr(0, 10)
          self.recent_photo['img'] = '/assets/img/how_photo.png'
          let files = JSON.parse(self.recent_photo['files'])
          if (files && files.length > 0) {
            let extensions = ['jpg', 'png', 'gif', 'jpeg', 'JPG', 'PNG', 'GIF', 'JPEG']
            if (extensions.indexOf(files[0].split('.').pop()) !== -1) {
              self.recent_photo['img'] = '/api/upload/' + files[0]
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
