<template>
  <div v-html="p('Footer: Contact.content')" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
const { p, pNoMarkup } = useTextLoader()

definePageMeta({
  title: 'Contact',
})

const pageTitle = computed(() => pNoMarkup('Footer: Contact.pageTitle'))
useHead({ title: pageTitle })
providePageTitle({ title: 'footer.paths.contact', labelType: 'locale-index' })
</script>
