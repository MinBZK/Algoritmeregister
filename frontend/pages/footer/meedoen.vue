<template>
  <div style="margin-bottom: 6em" v-html="p('Footer: Meedoen.content')" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
const { p } = useTextLoader()

definePageMeta({
  title: 'Meedoen',
})

const pageTitle = computed(() => p('Footer: Meedoen.pageTitle'))
useHead({ title: pageTitle })
providePageTitle({ title: 'footer.paths.meedoen', labelType: 'locale-index' })
</script>
