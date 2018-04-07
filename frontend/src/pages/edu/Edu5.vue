<template>
  <div>
    <div class="page-intro">
      <img
        src="~assets/img/edu5_background_image.png"
        class="section__background-image" >

      <div class="title--emphasized">
        변화와 성장을 위해, 매일 조금씩 천천히, 위대한 일상을 살다
      </div>

    </div>

    <div class="container">
      <div class="page-name">
        하우의 하루
      </div>
      <hr class="page-name--bottom-border" >
    </div>

    <div class="container">
      <div class="row">

<template v-for="item in items">
        <div class="col-xs-12 col-sm-4 col-md-4 col-lg-4 waglpedia__service"
          @mouseover="item.active = true" 
          @mouseleave="item.active = false">
          <div
            class="waglpedia__service-summary--default"
            :style="{'background-image': item.imgm}"
            style="background-size: cover; height:250px;opacity:0.6;"
            :class="{hidden: item.active}">
            <div class="edu__title3">
              {{ item.title }} 
            </div>
            <p v-if="item.stitle" class="edu__stitle3">
              {{ item.stitle }}
            </p> 
          </div>
          <div
            class="waglpedia__service-summary--active"
            :style="{'background-image': item.img}"
            style="background-size: cover; height:250px;opacity:1;"
            :class="{hidden: !item.active}"/>
        </div>
</template>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  data: function() {
    return {
      items: [
        {title: '아침 돌봄',
         active: false,
         imgm: 'url(assets/img/edu5_1m.jpg)', 
         img: 'url(assets/img/edu5_1.jpg)'}, 
        {title: '등교',
         active: false,
         imgm: 'url(assets/img/edu5_2m.jpg)', 
         img: 'url(assets/img/edu5_2.jpg)'}, 
        {title: '하나님 만나기',
         active: false,
         imgm: 'url(assets/img/edu5_3m.jpg)', 
         img: 'url(assets/img/edu5_3.jpg)'}, 
        {title: '주기 집중',
         active: false,
         imgm: 'url(assets/img/edu5_4m.jpg)', 
         img: 'url(assets/img/edu5_4.jpg)'}, 
        {title: '2~3교시',
         active: false,
         imgm: 'url(assets/img/edu5_5m.jpg)', 
         img: 'url(assets/img/edu5_5.jpg)'}, 
        {title: '점심 식사',
         active: false,
         imgm: 'url(assets/img/edu5_6m.jpg)', 
         img: 'url(assets/img/edu5_6.jpg)'}, 
        {title: '4교시',
         stitle: '(예비초등 닫는말 후 아지트, 돌봄 6시까지)',
         active: false,
         imgm: 'url(assets/img/edu5_7m.jpg)', 
         img: 'url(assets/img/edu5_7.jpg)'}, 
        {title: '5교시',
         stitle: '(초등 닫는말 후 아지트, 돌봄 6시까지)',
         active: false,
         imgm: 'url(assets/img/edu5_8m.jpg)', 
         img: 'url(assets/img/edu5_8.jpg)'}, 
        {title: '아지트와 오후돌봄',
         active: false,
         imgm: 'url(assets/img/edu5_9m.jpg)', 
         img: 'url(assets/img/edu5_9.jpg)'}, 
        ],
    }
  },
}
</script>
