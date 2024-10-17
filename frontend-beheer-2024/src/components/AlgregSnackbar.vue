<template>
  <v-snackbar
    :model-value="snackbarStore.show"
    :color="snackbarColour"
    timeout="-1"
    width="800"
  >
    <div class="snackbar">
      <slot name="default">
        {{ snackbarStore.activeItem?.message }}
        <div v-for="message in snackbarStore.activeItem?.list" :key="message">
          - {{ message }}
        </div>
      </slot>
    </div>
    <template #actions>
      <v-btn variant="text" @click="snackbarStore.showNext()">
        sluiten
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup lang="ts">
import { SnackbarTheme, useSnackbarStore } from '@/store/snackbar'
import { computed } from 'vue'

const snackbarStore = useSnackbarStore()

const snackbarColour = computed(() => {
  if (!snackbarStore.activeItem) return 'white'
  if (snackbarStore.activeItem?.theme === SnackbarTheme.error) return 'red'
  else return 'green'
})
</script>

<style scoped lang="scss">
.snackbar {
  font-size: 1.25em;
}
</style>
