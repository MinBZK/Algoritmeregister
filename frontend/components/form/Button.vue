<template>
  <v-btn class="btn-dark" :size="props.size">
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
  size?: string
}
const props = withDefaults(defineProps<Props>(), {
  size: 'x-large',
})
</script>

<style scoped lang="scss">
button {
  text-transform: none !important;
  background-color: $primary-dark !important;
  color: white;
  font-weight: bold;
}
</style>
