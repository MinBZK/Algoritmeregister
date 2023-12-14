<template>
  <div style="margin-bottom: 6em">
    <div v-html="p('Footer: Over algoritmes.content')" />
    <img
      src="../../assets/images/over-algoritmes.jpeg"
      :alt="p('Footer: Over algoritmes.img_alt')"
    />
    <div v-html="p('Footer: Over algoritmes.content2')" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const { p } = useTextLoader()

definePageMeta({
  title: 'Over algoritmes',
})

const pageTitle = computed(() => p('Footer: Over algoritmes.pageTitle'))
useHead({ title: pageTitle })
providePageTitle({
  title: 'footer.paths.over-algoritmes',
  labelType: 'locale-index',
})
</script>
