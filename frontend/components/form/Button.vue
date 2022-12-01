<template>
  <v-btn elevation="0" class="btn-dark" :size="props.size">
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
}
const props = withDefaults(defineProps<Props>(), {
  size: 'x-large',
})
</script>

<style scoped lang="scss">
button {
  text-transform: none !important;
  // background-color: $primary-dark !important;
  background-color: #154273;
  color: white;
  font-weight: bold;
}
</style>
