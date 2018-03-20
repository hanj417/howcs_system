<template>
  <q-page class="flex flex-center">
    <q-breadcrumbs
      separator="->"
      active-color="secondary"
      color="light"
    >
      <q-breadcrumbs-el label="Home" to="/" />
      <q-breadcrumbs-el label="Components" to="/components" />
      <q-breadcrumbs-el label="Breadcrumbs" to="/components/breadcrums" />
      <q-breadcrumbs-el label="Bogus" to="/components/breadcrums/bogus" />
    </q-breadcrumbs>
    <img alt="Quasar logo" src="~assets/quasar-logo-full.svg">
    <img alt="Quasar logo" src="~assets/quasar-logo-full.svg">
    <img alt="Quasar logo" src="~assets/quasar-logo-full.svg">
    <img alt="Quasar logo" src="~assets/quasar-logo-full.svg">
    <img alt="Quasar logo" src="~assets/quasar-logo-full.svg">
  </q-page>
</template>

<style>
</style>

<script>
export default {
  name: 'PageIndex'
}
</script>
