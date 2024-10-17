<template>
  <v-col cols="12 pr-0">
    <a
      :href="url"
      class="float-right"
    >
      {{ title }}
    </a>
  </v-col>
</template>

<script setup lang="ts">
import content from '@/content.json'
const url = content.metadataManual.url
const title = content.metadataManual.title
</script>
