<template>
  <div class="skeleton-content-left">
    <div class="skeleton-header"></div>
    <div class="skeleton-subheader"></div>
    <div class="skeleton-description"></div>
  </div>
  <div
    class="skeleton-content-right"
    :class="smallBreakpoint && 'skeleton-content-right-mobile'"
  >
    <div class="skeleton-description-term"></div>
    <div class="skeleton-description-details"></div>
    <div class="skeleton-description-term"></div>
    <div class="skeleton-description-details"></div>
    <div class="skeleton-description-term"></div>
    <div class="skeleton-description-details"></div>
  </div>
</template>

<script setup lang="ts">
const smallBreakpoint = useMobileBreakpoint().small
</script>
