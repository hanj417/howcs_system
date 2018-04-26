<template>
  <div>
    <div>
      <div class="page-intro">
        <img
          src="~assets/img/agit_background_image.png"
          class="section__background-image" >

        <div class="title--emphasized">
          다음세대를 살아갈 하늘빛 닮은 우리 아이들 누구에게나 열린 안전한 공간<br>
          하나님이 사랑하신 것처럼 as God love it

        </div>

      </div>


<!--강좌상세-->

<div class="agit__container">
  <div id="box__blue">
	 <div class="row">
	
		


        <div class="col-xs-12 col-sm-5 col-md-5 col-lg-5">
			 <div id="notice_table5"> 
			    <p align="center"><img src="~assets/img/agit_sample.jpg" width="90%"></p>
			  </div>
		</div><!--end-->

		<div class="col-xs-12 col-sm-7 col-md-7 col-lg-7">
			 <div id="notice_table5"> 
			    <table>
					<tr>
						<td width="17%">강좌명 </td>
						<td class="agit__ftitle_bl">{{ title }}</td>
					</tr>
					<tr>
						<td>길잡이 교사</td>
						<td>{{ teacher.name }}</td>
					</tr>
					<tr>
						<td width="15%">대상</td>
						<td>{{ audience }}</td>
					</tr>
					<tr>
						<td>요일/시간</td>
						<td>{{ weekday_label[time_slot_weekday]}}/{{time_slot_hour}} </td>
					</tr>
					<tr>
						<td>기간</td>
						<td>{{year}}{{semester_label[semester]}}</td>
					</tr>
				</table>
			  </div>
		</div><!--end-->

		<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
			 <div class="mg15" align="center">
<q-btn label="강좌신청하기" @click="apply" />
</div>
		</div><!--end-->


		


      </div>
  </div>
</div>










<div class="agit__container">
  <div id="box__gray">
	 
	 <div class="row">
		<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
			 <p class="agit__title"><span class="glyphicon glyphicon-star" aria-hidden="true" style="font-size:12px"></span> 길잡이 교사 소개<p> 
			 <div class="agit__content">
				<p class="agit__subtitle">{{teacher.name}}</p>
<q-input hide-underline disabled v-model="teacher.agit_teacher_info.career" type="textarea" />
			</div>
		</div><!--end-->

	 </div>



	 <div class="row">
		<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
			 <p class="agit__title"><span class="glyphicon glyphicon-star" aria-hidden="true" style="font-size:12px"></span> 연락처<p> 
			 <div class="agit__content">
{{ teacher.phone }}
			</div>
		</div><!--end-->

	 </div>



	 <div class="row">
		<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
			 <p class="agit__title"><span class="glyphicon glyphicon-star" aria-hidden="true" style="font-size:12px"></span> 개설배경<p> 
			 <div class="agit__content">
{{ background }}
			</div>
		</div><!--end-->

	 </div>
	  



      <div class="row">
		<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
			 <div class="mg15" align="center">
<q-btn label="목록 보기" @click="$router.go(-1)" />
</div>
		</div><!--end-->
	  </div>


  </div>
</div>










    </div>

  </div>
</div>
</template>

<script>
import { LocalStorage } from 'quasar'
export default {
  data: function () {
    return {
      teacher: {name: '' },
      title: '',
      minor_categories: [],
      minor_category: '',
      year: '2018',
      semester: '',
      semester_option : [
        {label: '봄', value: 'spring'},
        {label: '여름', value: 'summer'},
        {label: '가을', value: 'fall'},
        {label: '겨울', value: 'winter'},
        {label: '전체', value: 'year'},
      ],
      time_slot: '',
      time_slot_weekday: '',
      time_slot_hour: '',
      weekday: [
        {label: '월', value: 'mon'},
        {label: '화', value: 'tue'},
        {label: '수', value: 'wed'},
        {label: '목', value: 'thu'},
        {label: '금', value: 'fri'},
        {label: '토', value: 'sat'},
      ],
      google_calendar: '',
      audience: [],
      audience_min: '',
      audience_max: '',
      background: '',
      content: '',
      semester_label: {
        'spring':'봄',
        'summer':'.5.1 ~ 7.31',
        'fall':'가을',
        'winter':'겨울',
        'year':'.1.1 ~ 12.31',
      },
      weekday_label: {
        'mon':'월',
        'tue':'화',
        'wed':'수',
        'thu':'목',
        'fri':'금',
        'sat':'토',
      },
    }
  },
  props: ['id'],
  methods: {
    apply: function() {
      let loggedIn = LocalStorage.has('user_')
      if (!loggedIn) {
        this.$q.notify({message:'로그인이 필요합니다',
          position:'center', timeout:100})
        return
      } 

      var self = this
      self.$axios.post('enrollments/agit', {
        'class_id': self.id,
      }).then(function (response) {
        self.$router.go(-1)
      })
    },
  },
  created: function () {
      var self = this
      self.$axios.get('classes/agit/' + self.id
      ).then(function (response) {
        let data = response.data
        self.teacher = data.teacher
        self.title = data.title
        self.major_category = data.major_category
        self.minor_category = data.minor_category
        self.year = data.year
        self.semester = data.semester
        self.time_slot = data.time_slot
        self.time_slot_weekday = self.time_slot.split(',')[0]
        self.time_slot_hour = self.time_slot.split(',')[1]
        self.google_calendar = data.google_calendar
        self.audience = data.audience
        self.background = data.background
        self.content = data.content

            let aud_arr = self.audience.split(',')
            self.audience = ''
            for (var j = 1; j < 21; j++) {
              if (aud_arr.includes(j.toString())) {
                self.audience = j.toString()
                j++
                break
              }
            }
            for (; j < 21; j++) {
              if (aud_arr.includes(j.toString())) {
                self.audience = self.audience + ', ' + j.toString()
              }
            }
            if (self.audience != '') {
              self.audience = self.audience + '세'
            }
            if (aud_arr.includes('adult')) {
              if (self.audience != '') {
                self.audience = self.audience + ', '
              }
              self.audience = self.audience + '성인'
            }
      })
  },
}
</script>

<style>
* {
  box-sizing: border-box;
}

/* Style the search field */
form.example input[type=text] {
  padding: 7px;
  font-size: 15px;
  border: 2px solid #eee;
  float: left;
  width: 100%;
  background: #f1f1f1;
}

/* Clear floats */
form.example::after {
  content: "";
  clear: both;
  display: table;
}
</style>
