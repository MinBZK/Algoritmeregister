<template>
  <div class="margin-bottom-6" v-html="p('Footer: Copyright.content')" />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Copyright.pageTitle') })
providePageTitle({
  title: 'Footer: Copyright.pageTitle',
  labelType: 'preditor-index',
})
</script>
