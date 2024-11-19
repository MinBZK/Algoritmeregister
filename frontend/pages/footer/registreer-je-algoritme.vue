<template>
  <div
    class="margin-bottom-6"
    v-html="p('Footer: Registreer je algoritme.content')"
  />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Registreer je algoritme.pageTitle') })
providePageTitle({
  title: 'Footer: Registreer je algoritme.pageTitle',
  labelType: 'preditor-index',
})
</script>
