<template>
  <div class="block-cards__card no-bottom-padding">
    <div class="block-info block-color">
      <div v-html="html" />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  html: string
}>()
</script>

<style scoped lang="scss">
.block-color {
  background-color: $tertiary;
  margin-bottom: 0px !important;
}

:deep(.block-color div p) {
  margin-bottom: 0em;
}

.no-bottom-padding {
  padding-bottom: 0px !important;
  margin-bottom: 0px !important;
}
</style>
