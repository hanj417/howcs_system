<template>
<v-content>
  <v-container fluid fill-height>
   <v-layout justify-center align-center>
  <v-card>
    <v-card-title
      class="grey lighten-4 py-4 title"
    >
      회원 정보
    </v-card-title>
    <v-container grid-list-sm class="pa-4">
      <v-form @submit.prevent="validateForm" lazy-validation>
        <v-layout row wrap>
          <v-flex xs12>
            <v-text-field
              label="이름"
              prepend-icon="chat"
              v-model="career"
              data-vv-name="career"
              :error-messages="errors.collect('career')"
              v-validate="'required'"
              required
            ></v-text-field>
          </v-flex>
        </v-layout>
      </v-form>
    </v-container>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn flat color="primary" @click="cancel">취소</v-btn>
      <v-btn flat @click="save">{{ save_btn_text }}</v-btn>
    </v-card-actions>
  </v-card>
</v-layout>
</v-container>
</v-content>
</template>

<script>
import Vue from 'vue'
import VeeValidate from 'vee-validate'
Vue.use(VeeValidate)

export default {
  data () {
    return {
      career: '',
    }
  },
  methods: {
    cancel() {
      this.$router.go(-1)
    },
    save() {
      this.$axios.post(`agit_teacher_infos`, {
      }).then(({data}) => {
        this.$router.go(-1)
      });
    },
    validateForm() {
      this.$validator.validateAll()
        .then(() => {
          console.log("data");
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
}
</script>
