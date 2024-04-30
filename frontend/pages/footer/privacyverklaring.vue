<template>
  <div
    style="margin-bottom: 6em"
    v-html="p('Footer: Privacyverklaring.content')"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'
const { p } = useTextLoader()

definePageMeta({
  title: 'Privacyverklaring',
})

const pageTitle = computed(() => p('Footer: Privacyverklaring.pageTitle'))
useHead({ title: pageTitle })
providePageTitle({
  title: 'footer.paths.privacyverklaring',
  labelType: 'locale-index',
})
</script>
