<template>
  <div id="content">
    <div class="row">
      <div class="align-right">
        <LanguagePicker />
      </div>
    </div>
    <slot />
  </div>
</template>

<script setup lang="ts">
import LanguagePicker from '@/components/LanguagePicker.vue'
</script>

<style scoped>
#layout {
  margin: 0 auto 10px auto;
}

.row {
  display: flex;
}

.align-right {
  margin-left: auto;
}
</style>
