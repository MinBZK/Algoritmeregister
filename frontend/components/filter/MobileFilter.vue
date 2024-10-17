<template>
  <button class="show-filters-button button" @click="modal = true">
    <img src="@/assets/images/icons/icon-adjustment.svg" alt="" />
    <span>{{ t('showFilters') }}</span>
  </button>

  <ModalShell v-model="modal" width="400px" height="80%">
    <slot />
  </ModalShell>
</template>

<script setup lang="ts">
const modal = ref<boolean>(false)
const { t } = useI18n()

const route = useRoute()
watch(
  () => route.fullPath,
  () => {
    modal.value = false
  }
)
</script>

<style scoped lang="scss">
.show-filters-button {
  width: 100%;
  border-radius: 8px;
  font-size: 14pt;
  padding: 1.1em;
  display: flex;
  align-content: center;
  justify-content: center;
  img {
    position: absolute;
    left: 0%;
    margin-top: -0.3em;
    margin-left: 1em;
  }
}
</style>
