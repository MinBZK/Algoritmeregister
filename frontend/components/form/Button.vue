<template>
  <v-btn elevation="0" :class="[baseClass, isAttachedClass]" :size="props.size">
    {{ label
    }}<template v-if="icon"
      >&nbsp;<v-icon right dark> {{ icon }} </v-icon></template
    >
  </v-btn>
</template>

<script setup lang="ts">
type Props = {
  label: string
  icon?: string
  size?: string | number
  isAttached?: string
}
const props = withDefaults(defineProps<Props>(), {
  size: '56',
})

const isAttachedClass =
  props.isAttached == 'left'
    ? 'rounded-s-0'
    : props.isAttached == 'top'
    ? 'rounded-t-0'
    : ''

const baseClass = 'btn-dark'
</script>

<style scoped lang="scss">
button {
  text-transform: none !important;
  background-color: $primary-darker !important;
  color: white;
  font-weight: bold;
  min-width: 150px;
  font-size: 1.5rem;
}
</style>
