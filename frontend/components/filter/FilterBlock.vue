<template>
  <div ref="filterItems" class="filter-block">
    <div v-if="!disableTitle" class="title-show-button">
      <slot name="title">
        <div class="filter-block-title">
          <h2>
            {{ title }}
          </h2>
        </div>
      </slot>
      <slot name="append-title">
        <button
          v-if="!disableDropdown"
          class="show-button"
          :data-selected="open"
          @click="dropdownClicked"
        >
          <img
            :class="open ? 'rotate-up' : 'rotate-down'"
            src="@/assets/images/icons/icon-chevron-left-blue.svg"
            aria-hidden
            alt=""
          />
        </button>
      </slot>
    </div>
    <div v-if="open" class="content">
      <slot />
    </div>
    <div v-if="open && moreOptionsButton" class="read-more-section">
      <button
        v-if="readMoreActive"
        class="show-button"
        :aria-expanded="!readMoreActive"
        @click="readMoreClicked"
      >
        <span>{{ t('filter.moreOptions') }}</span>
        <img
          src="@/assets/images/icons/icon-chevron-left-blue.svg"
          class="rotate-down"
          alt=""
        />
      </button>
      <button
        v-if="readLessActive"
        ref="readLessButton"
        class="show-button"
        :aria-expanded="moreOptionsButton"
        @click="readLessClicked"
      >
        <span>{{ t('filter.lessOptions') }}</span>
        <img
          src="@/assets/images/icons/icon-chevron-left-blue.svg"
          class="rotate-up"
          aria-hidden
          alt=""
        />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title?: string
    disableTitle?: boolean
    disableDropdown?: boolean
    enableReadMore?: boolean
    enableReadLess?: boolean
    readMore?: boolean
    modelValue?: boolean
    moreOptionsButton?: boolean
  }>(),
  {
    title: undefined,
    disableTitle: false,
    disableDropdown: false,
    enableReadMore: false,
    enableReadLess: false,
    readMore: undefined,
    modelValue: undefined,
    moreOptionsButton: false,
  }
)

const { t } = useI18n()

const open = ref<boolean>(props.modelValue || true)
const readMoreActive = ref<boolean>(
  props.modelValue !== undefined ? props.modelValue : props.enableReadMore
)
const readLessActive = ref<boolean>(false)

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
  (e: 'click:dropdown', status: boolean): void
  (e: 'update:readMore', status: boolean): void
}>()

const dropdownClicked = () => {
  if (props.modelValue === undefined) {
    open.value = !open.value
  } else {
    emit('click:dropdown', !open.value)
  }
}

const filterItems = ref<HTMLElement | null>(null)
const readMoreClicked = () => {
  if (props.readMore !== undefined) {
    filterItems.value?.scrollIntoView({
      behavior: 'smooth',
    })
    emit('update:readMore', !props.readMore)
  } else {
    readMoreActive.value = false
  }
  if (props.enableReadLess) {
    readLessActive.value = true
  }
}

const readLessClicked = () => {
  readLessActive.value = false
  filterItems.value?.scrollIntoView({
    behavior: 'smooth',
  })
  if (props.readMore !== undefined) {
    emit('update:readMore', !props.readMore)
  } else if (props.enableReadMore) {
    readMoreActive.value = true
  }
}

watch(
  () => props.modelValue,
  () => {
    open.value = props.modelValue || true
  }
)
watch(
  () => props.readMore,
  () => {
    readMoreActive.value = props.readMore!
  }
)
</script>

<style scoped lang="scss">
.filter-block {
  background-color: $tertiary;
  padding: 0.75em;
  margin-bottom: 0.4em;
}

.title-show-button {
  width: 100%;
  display: inline-flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.4em;
  h2 {
    font-size: 20px;
    margin-bottom: 0;
  }
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

.read-more-section {
  margin-top: 0.5em;
  display: flex;
  justify-content: center;
  button {
    padding: 0.5em;
    font-size: 14pt;
    font-family: inherit;
    color: $primary-darker;
    column-gap: 1em;
    display: flex;
    align-items: center;
  }
}
</style>
