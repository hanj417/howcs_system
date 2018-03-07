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
export default {
  methods: {
    submit() {
      this.$http.post(`agit_teacher_infos`, {
      }).then(({data}) => {
        this.$router.replace('/')
      });
    },
  },
}
</script>
