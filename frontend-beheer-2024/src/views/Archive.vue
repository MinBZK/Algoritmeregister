<template>
  <h1 class="text-h4 mb-3 mt-0">
    Archiefoverzicht
  </h1>
  <p class="text-body-1 py-3">
    Dit overzicht toont alle gearchiveerde algortimebeschrijvingen van uw organisatie.
    Klik op de blauwe dearchiveer-knop om een versie weer terug te zetten.
  </p>
  <ArchiveTable />
</template>

<script setup lang="ts">
import ArchiveTable from '@/components/archive/ArchiveTable.vue'
</script>
