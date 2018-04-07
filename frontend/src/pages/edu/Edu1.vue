<template>
  <div>
    <div class="page-intro">
      <img
        src="~assets/img/edu1_background_image.png"
        class="section__background-image" >
      <div class="title--emphasized">
        교육은 속도가 아니라 바른 방향입니다
      </div>
    </div>

    <div class="container">
      <div class="page-name">
        교육특징
      </div>
      <hr class="page-name--bottom-border" >
    </div>

    <div class="container">
      <div class="row">
        <template v-for="char in chars">
        <div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 waglpedia__service" 
          @mouseover="char.active = true" 
          @mouseleave="char.active = false">
          <div
            class="waglpedia__service-summary--default"
            style="background-size: cover; opacity:0.5" 
            :style="{'background-image': char.img}"
            :class="{hidden: char.active}">
            <div class="waglpedia__service-name">
{{ char.name }}
            </div>
          </div>
          <div class="waglpedia__service-summary--active" :class="{hidden: !char.active}">
            <p class="text14">{{ char.text }}</p>
          </div>
        </div>
        </template>
        <div style="clear:both;"/>

      </div><!--row-->

    </div><!--container-->

    <div class="container">
      <div class="page-name">
        교육목표
      </div>
      <hr class="page-name--bottom-border" >
    </div>

    <div class="container">
      <div class="row project__list">
<template v-for="purpose in purposes">
        <div class="col-xs-12 col-sm-4 col-md-4 col-lg-4 edu__detail">
          <div class="project__link " :class="[purpose.cl]">
            <div class="edu__title">
             {{ purpose.title }} 
            </div>
            <div class="edu__stitle">
             {{ purpose.stitle }} 
            </div>
            <div class="edu__content">
             <div v-html="purpose.content" />
            </div>
          </div>
        </div>
</template>
      </div>
    </div>

    <div class="hidden-xs">
      <div class="space"/>
      <div class="space"/>
    </div>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      chars: [
        {active: false,
         name: '하나님의 성품을 닮아가는 교육',
         img: 'url(/assets/img/edu1_1.jpg)',
         text: '하우공동체는 기독 공동체로서 교육의 본질은 하나님의 형상대로 빚으시고 그 코에 생기를 넣으신 후 보시기에 참 좋았던 본래의 모습을 회복하게 하는 데 있음을 믿는다.'},
        {active: false,
         name: '기독교세계관에 따른 예수제자 교육',
         img: 'url(assets/img/edu1_2.jpg)',
         text: '하우공동체는 배움이 기독교세계관을 바탕으로 영성, 지성, 인성, 감수성, 사회성, 시민의식, 체력을 조화롭고 균형 있게 갖추는 과정이라고 믿으며, 이를 통해 다음세대를 살아갈 자녀들이 책임 있고 영향력 있는 예수제자로 성장하도록 돕는다.'},
        {active: false,
         name: '주어진 몫을 다할 수 있도록 최선을 다하는 교육',
         img: 'url(assets/img/edu1_3.jpg)',
         text: '하우공동체는 하나님의 자녀들이 저마다 주어진 몫이 있음을 깨닫고 그 몫을 찾기 위해 최선을 다하며 즐겁게 수고하도록 돕는다. 이를 위해 남과 경쟁하지 않고 나를 분주하게 하지 않으며 하나님의 자녀로서 자존감과 정체성을 확립하여 선한 이웃이 되도록 한다.'},
        {active: false,
         name: '부모로서 자녀 양육의 청지기적인 책임을 다하는 교육',
         img: 'url(assets/img/edu1_4.jpg)',
         text: '하우공동체의 부모는 청지기로서 자녀를 양육할 궁극적인 책임이 있으며 자녀와 함께 성장하기 위한 모든 교육과 활동에 적극적으로 참여한다. 또한 ‘나의 아이’만이 아니라 ‘우리의 아이’를 돌보고 양육하는 일에도 기꺼이 함께 하며 다음세대를 위해 ‘지금 여기에서’ 안전한 삶의 공간을 만드는데 힘쓴다. '},
        {active: false,
         name: '나눔과 섬김과 화해와 일치의 교육',
         img: 'url(assets/img/edu1_5.jpg)',
         text: '하우공동체는 나보다 남을 낫게 여기고 내가 가진 것을 나누고 남을 섬기는 일에 인색하지 않는 나눔과 섬김의 삶을 실천하며 언제나 평화를 이루기 위해 화해와 일치의 삶을 우선한다. 또한 매일 삶 속에서 ‘나부터-지금부터-여기부터-작은 것부터-할 수 있는 것부터’ 실천한다'},
        {active: false,
         name: '창조 질서에 따른 결이 있는 교육',
         img: 'url(assets/img/edu1_6.jpg)',
         text: '하우공동체는 하나님의 창조 질서를 지키기 위해 최선을 다하며 가르침과 배움에도 창조 질서에 따른 일정한 주기와 리듬이 있음을 깨닫고 이를 교육과정에 반영한다. 또한 고유한 문화와 기독교 전통에 따른 절기의 의미를 이해하고 삶에 적용하도록 힘쓴다.'},
        {active: false,
         name: '사랑과 이해를 바탕으로 한 자발성의 교육',
         img: 'url(assets/img/edu1_7.jpg)',
         text: '하우공동체는 나와 다른 생각을 가진 이들에 대해 옳고 틀림의 접근이 아니라 서로 다름에 대한 깊은 이해를 바탕으로 이상을 추구하지만 현실을 직시하고, 자율성과 자발성을 추구하지만 책임과 의무의 가치를 존중하며 다양성 안에서 일치를 추구한다.'},
        {active: false,
         name: '',
         img: 'url(assets/img/edu1_8.jpg)',
         text: ''},
        ],
      purposes: [
        {cl: 'edu__bg1',
         title: '초등과정교육목표',
         stitle: '하나님의 성품을 닮아가는 제자',
         content: ' \
              0학년목표(7세과정) : 하나님과 관계 맺기<br> \
              1학년목표 : 하나님의 성품을 알아채다<br> \
              2학년목표 : 하나님의 성품을 알아가다<br> \
              3학년목표 : 사람과 관계 맺으며 능동적으로 행동하다<br> \
              4학년목표 : 창조세계와 관계 맺으며 스스로 만들다<br> \
              5학년목표 : 사회와 관계 맺으며 자신을 표현하다'},
        {cl: 'edu__bg2',
         title: '중등과정목표',
         stitle: '예수님의 삶을 따라가는 제자',
         content: ' \
              7학년목표 : 관계 능력<br> \
              8학년목표 : 자기 발견'},
        {cl: 'edu__bg3',
         title: '고등과정목표',
         stitle: '예수님처럼 살아가는 세상의 문화변혁자',
         content: ' \
              10학년목표 : 협업 능력<br> \
              11학년목표 : 세상 속의 나'},
        {cl: 'edu__bg4',
         title: '하닮과정(초등갭이어)',
         stitle: '교육목표',
         content: ' \
              하나님을 닮아가는 행복한 예수제자 <br> \
              → 캠퍼스이동학습 예정'},
        {cl: 'edu__bg5',
         title: '예삶과정(중등갭이어)',
         stitle: '교육목표',
         content: ' \
              나눔과 섬김을 실천하는 행복한 예수제자 <br> \
              → 캠퍼스이동학습 예정'},
        {cl: 'edu__bg6',
         title: '창업과정',
         stitle: '교육목표',
         content: ' \
              창업 기획자로 행복한 예수제자<br> \
              → 소명주도진학진로중심과정'},
      ],
    }
  }, 
}
</script>
