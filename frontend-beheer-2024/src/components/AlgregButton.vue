<template>
  <button
    type="button"
    :class="`${$props.class} algreg-button algreg-button-theme-${theme} `"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot name="default">
      {{ label }}
    </slot>
    <slot name="dialog">
      <warning-dialog
        v-if="warnWithDialog"
        v-model="showDialog"
        :title="dialogTitle"
        @confirmed="$emit('confirm')"
      >
        {{ dialogText }}
      </warning-dialog>
    </slot>
  </button>
</template>

<script setup lang="ts">
import WarningDialog from '@/components/AlgregWarningDialog.vue'
import { ref } from 'vue'

const showDialog = ref<boolean>(false)

const props = withDefaults(
  defineProps<{
    class?: string
    disabled?: boolean
    dialogTitle?: string
    dialogText?: string
    label?: string
    warnWithDialog?: boolean
    theme?: 'primary' | 'default' | 'delete'
    width?: string
  }>(),
  {
    class: '',
    disabled: false,
    dialogTitle: undefined,
    dialogText: undefined,
    label: undefined,
    warnWithDialog: false,
    theme: 'default',
    width: '100%',
  }
)

const emit = defineEmits<{ (e: 'confirm'): void }>()

const handleClick = () => {
  if (props.warnWithDialog) {
    showDialog.value = true
  } else {
    emit('confirm')
  }
}
</script>

<style scoped lang="scss">
.algreg-button {
  font-weight: 400;
  font-size: 0.75em;
  padding: 0.5em;
  border-radius: 8px;
  border: 1px rgb(212, 212, 212) solid;
  width: v-bind(width);
  margin: 0.25em 0;
  &[disabled] {
    cursor: auto;
  }
}

.algreg-button-theme-default {
  background-color: white;
  color: black;
  &:hover {
    background-color: rgb(177, 213, 236);
  }
  &[disabled] {
    background-color: white;
    color: #d1d5db;
  }
}

.algreg-button-theme-primary {
  background-color: $primary;
  color: white;
  &:hover {
    background-color: $primary-dark;
  }
  &[disabled] {
    background-color: rgb(177, 213, 236);
    color: white;
  }
}

.algreg-button-theme-delete {
  background-color: $error;
  color: white;
  &:hover {
    background-color: $error-dark;
  }
  &[disabled] {
    background-color: rgb(194, 128, 128);
    color: white;
  }
}
</style>
