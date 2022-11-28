<template>
  <div id="content">
    <v-row>
      <v-col class="align-right">
        <LanguagePicker class="align-right"> </LanguagePicker>
      </v-col>
    </v-row>
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
