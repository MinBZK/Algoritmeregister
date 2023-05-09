<template>
  <div v-html="p('Footer: Privacyverklaring.content')" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
const { p, pNoMarkup } = useTextLoader()

definePageMeta({
  title: 'Privacyverklaring',
})

const pageTitle = computed(() =>
  pNoMarkup('Footer: Privacyverklaring.pageTitle')
)
useHead({ title: pageTitle })
providePageTitle({
  title: 'footer.paths.privacyverklaring',
  labelType: 'locale-index',
})
</script>
