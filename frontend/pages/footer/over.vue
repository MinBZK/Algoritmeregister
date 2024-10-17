<template>
  <div class="margin-bottom-6" v-html="p('Footer: Over.content')" />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Over.pageTitle') })
providePageTitle({
  title: 'Footer: Over.pageTitle',
  labelType: 'preditor-index',
})
</script>
