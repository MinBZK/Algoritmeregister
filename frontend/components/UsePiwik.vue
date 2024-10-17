<template><div></div></template>

<script setup lang="ts">
const { $piwikPRO } = useNuxtApp()
const route = computed(() => useRoute().path)
// @ts-ignore
watch(route, () => $piwikPRO.PageViews.trackPageView())
</script>
