<template>
  <div style="margin-bottom: 6em" v-html="p('Footer: Webarchief.content')" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
const { p } = useTextLoader()

definePageMeta({
  title: 'Webarchief',
})

const pageTitle = computed(() => p('Footer: Webarchief.pageTitle'))
useHead({ title: pageTitle })
providePageTitle({
  title: 'footer.paths.webarchief',
  labelType: 'locale-index',
})
</script>
