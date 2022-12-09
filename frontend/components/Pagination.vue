<template>
  <nav role="navigation" aria-label="Paginering navigatie">
    <div
      class="pagenumber noselect"
      :tabindex="currentPage == 1 ? -1 : 0"
      :class="currentPage == 1 && 'disabled'"
      aria-role="button"
      :aria-label="
        currentPage !== 1 ? t('pagination.goTo', { n: currentPage - 1 }) : ''
      "
    >
      <NuxtIcon
        name="mdi:chevron-left"
        @click="navigate(-1)"
        @keydown.enter="navigate(-1)"
      />
    </div>
    <template v-for="(pageNumber, index) in range" :key="pageNumber">
      <div
        v-if="index == 1 && pageNumber != 2"
        class="pagenumber-elipsis noselect"
      >
        ...
      </div>
      <div
        :class="pageNumber == currentPage && 'current-page'"
        tabindex="0"
        :aria-current="pageNumber == currentPage && `true`"
        aria-role="button"
        class="pagenumber noselect"
        @keydown.enter="$emit('setPage', pageNumber)"
        @click="$emit('setPage', pageNumber)"
        :aria-label="t('pagination.goTo', { n: pageNumber })"
      >
        {{ pageNumber }}
      </div>
      <div
        v-if="index == range.length - 2 && pageNumber != pageLength - 1"
        class="pagenumber-elipsis noselect"
      >
        ...
      </div>
    </template>
    <div
      class="pagenumber noselect"
      :tabindex="props.currentPage == props.pageLength ? -1 : 0"
      aria-role="button"
      :class="props.currentPage == props.pageLength && 'disabled'"
      @click="navigate(1)"
      @keydown.enter="navigate(1)"
      :aria-label="
        props.currentPage !== props.pageLength
          ? t('pagination.goTo', { n: props.currentPage + 1 })
          : ``
      "
    >
      <NuxtIcon name="mdi:chevron-right" />
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const props = defineProps<{
  currentPage: number
  pageLength: number
}>()

const emit = defineEmits(['setPage'])

const range = computed(() => {
  const maxPages = 3
  const min = 2
  const _windowMin = props.currentPage - (maxPages - 1) / 2

  let windowMin: number = _windowMin
  if (_windowMin < min) {
    windowMin = min
  } else if (_windowMin + maxPages >= props.pageLength) {
    windowMin = props.pageLength - maxPages
  }

  // const windowMin = _windowMin >= min ? _windowMin : min
  const _windowMax = windowMin + maxPages - 1
  const windowMax =
    _windowMax > props.pageLength - 1 ? props.pageLength - 1 : _windowMax

  const arrayLength = 1 + windowMax - windowMin
  const visiblePages: number[] =
    arrayLength > 0
      ? [...Array(arrayLength).keys()].map((v) => v + windowMin)
      : []

  return props.pageLength > 1 ? [1, ...visiblePages, props.pageLength] : [1]
})

const navigate = (delta: number) => {
  const newPage = props.currentPage + delta
  if (newPage >= 1 && newPage <= props.pageLength) {
    emit('setPage', props.currentPage + delta)
  }
}

const { t } = useI18n()
</script>

<style scoped lang="scss">
nav {
  display: inline-block;
}

.pagenumber {
  padding: 0.5em;
  margin: 0.5em;
  background-color: $tertiary;
  cursor: pointer;
  display: inline-block;
}

.pagenumber:hover:not(.disabled) {
  background-color: $secondary;
}

.current-page {
  background-color: $primary;
  color: white;
}

.disabled {
  color: $secondary;
  cursor: not-allowed;
}

.pagenumber-elipsis {
  display: inline-block;
}
</style>
