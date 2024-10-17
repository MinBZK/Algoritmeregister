<template>
  <div class="margin-bottom-6" v-html="p('Footer: Meedoen.content')" />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Meedoen.pageTitle') })
providePageTitle({
  title: 'Footer: Meedoen.pageTitle',
  labelType: 'preditor-index',
})
</script>
