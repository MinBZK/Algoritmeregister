<template>
  <div v-html="p('Footer: Vragen.content')" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
const { p, pNoMarkup } = useTextLoader()

definePageMeta({
  title: 'Vragen',
})

const pageTitle = computed(() => pNoMarkup('Footer: Vragen.pageTitle'))
useHead({ title: pageTitle })
providePageTitle({ title: 'footer.paths.vragen', labelType: 'locale-index' })
</script>
