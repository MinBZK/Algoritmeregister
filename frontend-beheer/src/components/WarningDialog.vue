<template>
  <v-dialog v-model="model" width="475">
    <v-card rounded="lg">
      <v-toolbar :color="color">
        <v-toolbar-title>
          <v-icon icon="mdi-information-outline" class="mr-2" />
          {{ title }}
        </v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <div class="popup-text pa-2">
          <slot>
            <!-- default content -->
            Weet u zeker dat u wilt doorgaan?
          </slot>
        </div>
      </v-card-text>
      <v-divider />
      <v-card-actions class="justify-end">
        <v-btn
          class="text-capitalize"
          @click="emit('update:modelValue', false)"
        >
          Annuleren
        </v-btn>
        <v-btn
          color="primary"
          class="text-capitalize"
          @click="confirm"
        >
          Doorgaan
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: boolean
  title?: string
  color?: string
}
const props = withDefaults(defineProps<Props>(), {
  title: 'Waarschuwing',
  color: 'grey',
})

// Implements component v-model
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'confirmed', value: void): void
}>()
const model = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const confirm = () => {
  emit('update:modelValue', false)
  emit('confirmed')
}
</script>

<style scoped lang="scss">
.popup-text {
  font-size: 1.1rem;
  color: #4b4b4b;
}

:deep(.v-btn) {
  font-size: 1rem;
}
</style>
