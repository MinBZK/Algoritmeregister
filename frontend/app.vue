<template>
  <RijksoverheidHeaderVue
    title="Applicatienaam"
    :pages="['about']"
  />
  <NuxtPage />
</template>

<script setup lang="ts">
import RijksoverheidHeaderVue from "@/components/Header.vue";
</script>
