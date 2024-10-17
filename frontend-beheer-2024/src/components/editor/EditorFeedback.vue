<template>
  <!-- Feedback modelled after Vuetify's v-textarea component -->
  <div class="v-input__details">
    <v-messages
      v-if="anyErrorMessages"
      :messages="errorMessages!"
      :active="anyErrorMessages"
      color="error"
    />
    <v-messages
      v-else
      :messages="helpText ? [helpText] : []"
      :active="active"
      color="grey-darken-1"
    />
    <v-counter
      v-if="maxCharCount && charCount !== undefined"
      :max="maxCharCount"
      :value="charCount"
      :active="active"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{
  helpText?: string
  errorMessages?: string[]
  maxCharCount?: number
  charCount?: number
  active: boolean
}>()

const anyErrorMessages = computed(() => !!props.errorMessages?.length)
</script>

<style scoped lang="scss">
:deep(.v-messages) {
  opacity: 1;
}
</style>
