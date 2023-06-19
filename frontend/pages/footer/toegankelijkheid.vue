<template>
  <div v-html="p('Footer: Toegankelijkheid.content')" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
const { p } = useTextLoader()

definePageMeta({
  title: 'Toegankelijkheid',
})

const pageTitle = computed(() => p('Footer: Toegankelijkheid.pageTitle'))
useHead({ title: pageTitle })
providePageTitle({
  title: 'footer.paths.toegankelijkheid',
  labelType: 'locale-index',
})
</script>
