<template>
  <div class="block" :class="variant">
    <span class="text"> {{ text }} </span>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    text: string
    variant?: 'orange' | 'yellow' | 'green'
  }>(),
  { variant: 'green' }
)
</script>

<style scoped lang="scss">
.block {
  width: 100%;
  height: 100%;
  text-align: center;
  margin: auto;
}

.text {
  margin: auto;
  font-size: 1.5em;
}

.orange {
  background-color: rgb(255, 123, 0);
  border: 2px solid rgb(211, 102, 0);
}
.yellow {
  background-color: rgb(255, 230, 0);
  border: 2px solid rgb(199, 179, 0);
}

.green {
  background-color: rgb(27, 175, 27);
  border: 2px solid rgb(23, 150, 23);
}
</style>
