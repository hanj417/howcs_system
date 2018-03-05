<template>
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>아지트 교사 지원</v-toolbar-title>
              </v-toolbar>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click.stop='submit'>신청</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['menu'])
  },
  methods: {
    fetch_menu() {
      this.$http.get('menu')
      .then(({data}) => 
        this.$store.commit('set_menu', data)
      ).catch(function(data) {
        console.log('error')
      })    
    },
    submit() {
      this.$http.post(`agit_teacher_infos`, {
      }).then(({data}) => {
        this.fetch_menu()
        this.$router.replace('/')
      }).catch(({data}) => {
        console.log('error')
      });
    },
  },
}
</script>
