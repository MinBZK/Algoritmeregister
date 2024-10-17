<template>
  <div class="margin-bottom-6" v-html="p('Footer: Contact.content')" />
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Contact.pageTitle') })
providePageTitle({
  title: 'Footer: Contact.pageTitle',
  labelType: 'preditor-index',
})
</script>
