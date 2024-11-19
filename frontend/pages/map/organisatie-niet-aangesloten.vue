<template>
  <div
    class="margin-bottom-6"
    v-html="p('Organisatie niet aangesloten.content')"
  />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Organisatie niet aangesloten.pageTitle') })
providePageTitle({
  title: 'Organisatie niet aangesloten.pageTitle',
  labelType: 'preditor-index',
})
</script>
