<template>
  <div
    class="margin-bottom-6"
    v-html="p('Footer: Privacyverklaring.content')"
  />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Privacyverklaring.pageTitle') })
providePageTitle({
  title: 'Footer: Privacyverklaring.pageTitle',
  labelType: 'preditor-index',
})
</script>
