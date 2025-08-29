<template>
  <div class="margin-bottom-6" v-html="p('Footer: Cookies.content')" />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Cookies.pageTitle') })
providePageTitle({
  title: 'Footer: Cookies.pageTitle',
  labelType: 'preditor-index',
})
</script>
