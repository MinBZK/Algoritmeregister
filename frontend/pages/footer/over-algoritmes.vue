<template>
  <div class="margin-bottom-6">
    <div v-html="p('Footer: Over algoritmes.content')" />
    <img
      src="../../assets/images/over-algoritmes.jpeg"
      :alt="p('Footer: Over algoritmes.img_alt')"
    />
    <div v-html="p('Footer: Over algoritmes.content2')" />
  </div>
</template>

<script setup lang="ts">
const { p } = useTextLoader()
useHead({ title: p('Footer: Over algoritmes.pageTitle') })
providePageTitle({
  title: 'Footer: Over algoritmes.pageTitle',
  labelType: 'preditor-index',
})
</script>
