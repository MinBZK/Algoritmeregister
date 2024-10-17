<template>
  <v-dialog v-model="model" width="400">
    <v-card rounded="xl">
      <v-card-text>
        <strong>Let op: </strong>{{ title }}
        <div class="popup-text pt-4">
          <slot>
            <!-- default content -->
            Weet u zeker dat u wilt doorgaan?
          </slot>
        </div>
      </v-card-text>
      <v-divider />
      <v-card-actions class="justify-end my-2 pr-5">
        <v-btn
          class="text-capitalize rounded-pill"
          @click="emit('update:modelValue', false)"
        >
          Annuleren
        </v-btn>
        <v-btn
          color="purple"
          class="text-capitalize rounded-pill"
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
  font-size: 1rem;
  color: #4b4b4b;
}
</style>
