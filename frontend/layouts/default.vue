<template>
  <div id="content">
    <h1>{{ route.meta.title }}</h1>
    <slot />
  </div>
</template>

<script setup lang="ts">
import RijksoverheidHeaderVue from "@/components/Header.vue";

const route = useRoute();
</script>
