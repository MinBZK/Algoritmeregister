<template>
  <div v-html="p('Footer: Over.content')" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
const { p, pNoMarkup } = useTextLoader()

definePageMeta({
  title: 'Over',
})

const pageTitle = computed(() => pNoMarkup('Footer: Over.pageTitle'))
useHead({ title: pageTitle })
providePageTitle({ title: 'footer.paths.over', labelType: 'locale-index' })
</script>
