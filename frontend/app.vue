<template>
  <RijksoverheidHeaderVue title="Algoritmeregister" :pages="['algoritme']" />
  <NuxtPage />
</template>

<script setup lang="ts">
import RijksoverheidHeaderVue from "@/components/Header.vue";
</script>

<style>
#content {
  width: 1200px;
  margin: 0 auto;
  padding-top: 0.5em;
}
</style>
