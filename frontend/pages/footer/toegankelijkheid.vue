<template>
  <div class="margin-bottom-6" v-html="p('Footer: Toegankelijkheid.content')" />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Toegankelijkheid.pageTitle') })
providePageTitle({
  title: 'Footer: Toegankelijkheid.pageTitle',
  labelType: 'preditor-index',
})
</script>
