<template>
  <div class="margin-bottom-6" v-html="p('Footer: Zelf aan de slag.content')" />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Zelf aan de slag.pageTitle') })
providePageTitle({
  title: 'Footer: Zelf aan de slag.pageTitle',
  labelType: 'preditor-index',
})
</script>
