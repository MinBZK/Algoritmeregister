<template>
  <div class="margin-bottom-6" v-html="p('Footer: Release-notes.content')" />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Release-notes.pageTitle') })
providePageTitle({
  title: 'Footer: Release-notes.pageTitle',
  labelType: 'preditor-index',
})
</script>
