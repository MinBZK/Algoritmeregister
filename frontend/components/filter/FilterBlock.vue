<template>
  <div class="filter-block">
    <div v-if="!disableTitle" class="title-show-button">
      <div>
        <strong>
          {{ title }}
        </strong>
      </div>
      <button
        v-if="!disableDropdown"
        class="show-button"
        :data-selected="open"
        @click="dropdownClicked"
      >
        <img
          :class="open ? 'rotate-up' : 'rotate-down'"
          src="@/assets/images/icons/icon-chevron-left-blue.svg"
          :alt="open ? 'Pijltje omhoog' : 'Pijltje omlaag'"
        />
      </button>
    </div>
    <div v-if="open" class="content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title?: string
    disableTitle?: boolean
    disableDropdown?: boolean
    modelValue?: boolean
  }>(),
  {
    title: undefined,
    disableTitle: false,
    disableDropdown: false,
    modelValue: undefined,
  }
)

const open = ref<boolean>(props.modelValue)

const setOpen = () => {
  if (props.disableDropdown || props.disableTitle) {
    open.value = true
  }
  if (typeof props.modelValue === 'undefined') {
    open.value = true
  } else {
    open.value = props.modelValue
  }
}
setOpen()

const emit = defineEmits<{
  (e: 'dropdown-clicked', status: boolean): void
}>()

const dropdownClicked = () => {
  if (props.modelValue === undefined) {
    open.value = !open.value
  } else {
    emit('dropdown-clicked', !open.value)
  }
}

watch(
  () => props.modelValue,
  () => {
    open.value = props.modelValue
  }
)
</script>

<style scoped lang="scss">
.filter-block {
  background-color: $tertiary;
  padding: 0.75em;
}

.title-show-button {
  width: 100%;
  display: inline-flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  font-size: 1.1em;
}

.show-button {
  background-color: rgba(0, 0, 0, 0);
  cursor: pointer;
  border: none;

  img.rotate-down {
    transform: rotate(-90deg);
  }

  img.rotate-up {
    transform: rotate(90deg);
  }
}
</style>
