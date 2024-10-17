<template>
  <div class="margin-bottom-6" v-html="p('Footer: Archief.content')" />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Archief.pageTitle') })
providePageTitle({
  title: 'Footer: Archief.pageTitle',
  labelType: 'preditor-index',
})
</script>
