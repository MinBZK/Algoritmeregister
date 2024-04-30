<template>
  <button class="button" :class="style" :disabled="style === 'disabled'">
    <span class="button-text">
      {{ value }}
    </span>
    <img
      src="@/assets/images/icons/icon-close-white.svg"
      alt="Maak selectie ongedaan"
    />
  </button>
</template>

<script setup lang="ts">
defineProps<{
  value?: string
  style: 'active' | 'open' | 'disabled'
}>()
</script>

<style scoped lang="scss">
.button {
  display: flex;
  align-items: center;
  max-width: 75%;
  margin-left: 0em;
  font-size: 0.8em;

  .button-text {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.button img {
  height: 0.6em !important;
  margin-left: 0.4em;
}

.active {
  background-color: $primary-darker !important;
  color: white;
}

.open {
  background-color: rgb(0, 0, 0, 0);
  img {
    display: none;
  }
}

.disabled {
  background-color: rgb(0, 0, 0, 0);
  color: rgb(176, 176, 176);
  border-color: rgb(200, 213, 226);

  img {
    display: none;
  }
}
</style>
