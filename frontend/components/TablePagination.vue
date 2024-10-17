<template>
  <div>
    <nav
      role="navigation"
      aria-label="Paginering navigatie"
      :class="isMobile && 'pagination-mobile'"
    >
      <div
        class="pagenumber noselect"
        :tabindex="currentPage == 1 ? -1 : 0"
        :class="currentPage == 1 && 'disabled'"
        role="button"
        :aria-label="currentPage !== 1 ? t('pagination.goToPreviousPage') : ''"
        @click="navigate(-1)"
        @keydown.enter="navigate(-1)"
        @keydown.space.prevent="navigate(-1)"
      >
        <NuxtIcon name="mdi:chevron-left" />
      </div>
      <template v-for="(pageNumber, index) in range" :key="pageNumber">
        <div
          v-if="index == 1 && pageNumber != 2"
          class="pagenumber-elipsis noselect"
        >
          ...
        </div>
        <NuxtLink
          :to="
            localePath({
              path: '/' + route.path?.split('/')[2],
              query: { page: pageNumber.toString() },
            })
          "
          :class="pageNumber == currentPage && 'current-page'"
          :aria-label="t('pagination.goTo', { n: pageNumber })"
          tabindex="0"
          :aria-current="pageNumber == currentPage && `true`"
          role="button"
          class="pagenumber noselect"
          @click=";[$emit('setPage', pageNumber), announcePage(pageNumber)]"
          @keydown.enter="
            ;[$emit('setPage', pageNumber), announcePage(pageNumber)]
          "
          @keydown.space.prevent="
            ;[$emit('setPage', pageNumber), announcePage(pageNumber)]
          "
        >
          {{ pageNumber }}
        </NuxtLink>
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
        :aria-label="
          props.currentPage !== props.pageLength
            ? t('pagination.goToNextPage')
            : ``
        "
        role="button"
        :class="props.currentPage == props.pageLength && 'disabled'"
        @click="navigate(1)"
        @keydown.enter="navigate(1)"
        @keydown.space.prevent="navigate(1)"
      >
        <NuxtIcon name="mdi:chevron-right" />
      </div>
    </nav>
    <div class="visually-hidden" disabled aria-live="polite">
      {{ pageAnnouncer }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMobileBreakpoint } from '~~/composables/mobile'

const props = defineProps<{
  currentPage: number
  pageLength: number
}>()

const isMobile = useMobileBreakpoint().medium
const localePath = useLocalePath()
const route = useRoute()

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

const pageAnnouncer = ref()
const navigate = (delta: number) => {
  const newPage = props.currentPage + delta
  if (newPage >= 1 && newPage <= props.pageLength) {
    emit('setPage', props.currentPage + delta)
    pageAnnouncer.value = t('pagination.page') + ' ' + newPage.toString()
  }
}

const announcePage = (pageNumber: number) => {
  pageAnnouncer.value = t('pagination.page') + ' ' + pageNumber.toString()
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
  text-decoration: none;
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

.pagination-mobile {
  font-size: 91%;
}
</style>
