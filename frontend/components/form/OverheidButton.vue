<template>
  <form
    :class="props.alignHorizontally && 'inline-form'"
    :action="action"
    @click="clickButton"
  >
    <button
      :id="buttonId"
      ref="button"
      class="button"
      :class="[
        {
          'button--block': fullWidth,
          disabled: disabled,
        },
        `button--${props.style}`,
      ]"
      type="submit"
      :aria-disabled="disabled ? 'true' : 'false'"
      :aria-label="ariaLabel"
    >
      <span class="button__label"
        >{{ label }} <NuxtIcon v-if="icon" size="0.9em" :name="icon"
      /></span>
    </button>
    <input
      v-for="item in hiddenQuery"
      :key="item.name"
      type="hidden"
      :name="item.name"
      :value="item.value"
    />
  </form>
</template>

<script setup lang="ts">
export interface Query {
  name: string
  value: string
}

const props = withDefaults(
  defineProps<{
    label: string
    icon?: string | null
    fullWidth?: boolean
    style?: 'primary' | 'secondary' | 'tertiary'
    action?: string | undefined
    hiddenQuery?: Query[]
    alignHorizontally?: boolean
    disabled?: boolean
    buttonId?: string | undefined
    ariaLabel?: string | undefined
  }>(),
  {
    icon: null,
    fullWidth: false,
    primary: true,
    action: undefined,
    hiddenQuery: undefined,
    alignHorizontally: false,
    disabled: false,
    style: 'primary',
    buttonId: undefined,
    ariaLabel: undefined,
  }
)

const emit = defineEmits<{
  (e: 'click'): void
}>()

const button = ref<HTMLButtonElement>()

const clickButton = (e: Event) => {
  if (!props.action) {
    e.preventDefault()
    if (!props.disabled) {
      emit('click')
      button.value?.focus()
    }
  }
}
</script>

<style scoped lang="scss">
@use '/assets/styles/colors' as colors;

.button {
  margin-bottom: 0em !important;
}
.inline-form {
  display: inline-block;
  margin-right: 1em;
}

.disabled {
  cursor: not-allowed;
}

.button--primary[aria-disabled='true'] {
  background-color: colors.$primary-darker !important;
  color: white !important;
}
</style>
