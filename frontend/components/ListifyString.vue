<template>
  <div v-if="isArray" class="listified" :style="listStyle">
    <ul>
      <li v-for="cell in text" :key="cell" class="word-break">
        {{ cell }}
      </li>
    </ul>
  </div>
  <template v-if="!isArray">
    {{ text }}
  </template>
</template>

<script setup lang="ts">
const props = defineProps<{
  text: string | string[]
  listStyle?: string
}>()

const isArray = computed(() => Array.isArray(props.text))
</script>

<style scoped lang="scss">
.listified {
  width: 100% !important;
}
</style>
