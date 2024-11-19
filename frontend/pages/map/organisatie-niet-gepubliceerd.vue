<template>
  <div
    class="margin-bottom-6"
    v-html="p('Organisatie niet gepubliceerd.content')"
  />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Organisatie niet gepubliceerd.pageTitle') })
providePageTitle({
  title: 'Organisatie niet gepubliceerd.pageTitle',
  labelType: 'preditor-index',
})
</script>
