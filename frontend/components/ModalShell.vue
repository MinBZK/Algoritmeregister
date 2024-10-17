<template>
  <div
    v-if="modelValue"
    class="modal-background"
    role="dialog"
    :aria-labelledby="
      modalTitle === 'faqQuestionTitle'
        ? 'faqQuestionTitle'
        : 'onderwerpenTitle-' + indexModalTitle
    "
    @click.self="$emit('update:modelValue', false)"
  >
    <div class="modal-view">
      <button
        ref="closeButton"
        class="close-button"
        :aria-label="t('closeSubjectTile')"
        @click="$emit('update:modelValue', false)"
      >
        <NuxtIcon name="mdi:close-thick" />
      </button>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

const props = withDefaults(
  defineProps<{
    modelValue: boolean
    height?: string
    width?: string
    maxHeight?: string
    modalTitle?: string
    indexModalTitle?: number
  }>(),
  {
    width: 'auto',
    height: 'auto',
    maxHeight: 'auto',
    modalTitle: '',
    indexModalTitle: 0,
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', modelValue: boolean): void
}>()
const closeButton = ref<HTMLElement | null>(null)

onMounted(() => {
  const escListener = (event: any) => {
    if (event.key === 'Escape') {
      emit('update:modelValue', false)
    }
  }
  window.addEventListener('keydown', escListener)
  onBeforeUnmount(() => {
    window.removeEventListener('keydown', escListener)
  })
})

watch(
  () => props.modelValue,
  (modelValue) => {
    nextTick(() => {
      const focusableElements = document.querySelectorAll(
        'button:not(.close-button, .show-button), a:not(.items, .is-external-icon.external-link.exclusive-modal-mobile), input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      if (modelValue) {
        closeButton.value?.focus()
        document.body.style.overflow = 'hidden'
        focusableElements.forEach((el) => el.setAttribute('tabindex', '-1'))
      } else {
        document.body.style.overflow = ''
        focusableElements.forEach((el) => el.removeAttribute('tabindex'))
      }
    })
  }
)

onBeforeUnmount(() => {
  document.body.style.overflow = ''
})
</script>

<style scoped lang="scss">
.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 10;
  padding: 1em;
  border: 10em;

  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-view {
  position: relative;
  padding: 0.8em;
  background-color: $tertiary;
  border: 10px white solid;
  border-radius: 8px;
  overflow-y: auto;
  width: v-bind('width');
  height: v-bind('height');
  max-height: v-bind('maxHeight');
}

.close-button {
  background: none;
  border: none;
  color: var(--primary-darker, #154273);
  cursor: pointer;
  font-size: 1em;
  position: absolute;
  right: 10px;
  top: 10px;
}
</style>
