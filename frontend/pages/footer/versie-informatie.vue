<template>
  <div
    style="margin-bottom: 6em"
    v-html="p('Footer: Versie-informatie.content')"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'
const { p } = useTextLoader()

definePageMeta({
  title: 'Versie-informatie',
})

const pageTitle = computed(() => p('Footer: Versie-informatie.pageTitle'))
useHead({ title: pageTitle })
providePageTitle({
  title: 'footer.paths.versie-informatie',
  labelType: 'locale-index',
})
</script>
