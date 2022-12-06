<template>
  <!-- <div class="pagination">
    <div class="pagination__index">
      <ul>
        <li class="prev">
          <a href="#"><span class="">Vorige pagina</span></a>
        </li>
        <li class="">
          <a href="#"><span class="visually-hidden">Pagina: </span>3</a>
        </li>
        <li aria-current="page" class="active">
          <span class="visually-hidden">Pagina: </span>4
        </li>
        <li class="">
          <a href="#"><span class="visually-hidden">Pagina: </span>...</a>
        </li>
        <li class="">
          <a href="#"><span class="visually-hidden">Pagina: </span>102</a>
        </li>
        <li class="next">
          <a href="#"><span class="">Volgende pagina</span></a>
        </li>
      </ul>
    </div>
  </div> -->
  <nav role="navigation" aria-label="Paginering navigatie">
    <div
      class="pagenumber"
      :class="props.currentPage == 1 && 'disabled'"
      :aria-label="
        props.currentPage !== 1
          ? t('pagination.goTo', { n: props.currentPage - 1 })
          : ''
      "
    >
      <NuxtIcon name="mdi:chevron-left" @click="navigate(-1)" />
    </div>
    <div
      class="pagenumber"
      :class="1 == props.currentPage && 'current-page'"
      @click="$emit('setPage', 1)"
      :aria-label="t('pagination.goTo', { n: 1 })"
      :aria-current="1 == props.currentPage && `true`"
    >
      1
    </div>
    <div v-if="range[0] > 2" class="pagenumber-elipsis">...</div>
    <div
      v-for="index in range"
      :class="index == props.currentPage && 'current-page'"
      :aria-current="index == props.currentPage && `true`"
      class="pagenumber"
      @click="$emit('setPage', index)"
      :aria-label="t('pagination.goTo', { n: index })"
    >
      {{ index }}
    </div>
    <div
      class="pagenumber-elipsis"
      v-if="range[range.length - 1] < props.pageLength - 1"
    >
      ...
    </div>
    <div
      class="pagenumber"
      :class="pageLength == props.currentPage && 'current-page'"
      :aria-current="pageLength == props.currentPage && `true`"
      v-if="pageLength > 1"
      @click="$emit('setPage', pageLength)"
      :aria-label="t('pagination.goTo', { n: pageLength })"
    >
      {{ pageLength }}
    </div>
    <div
      class="pagenumber"
      :class="props.currentPage == props.pageLength && 'disabled'"
      @click="navigate(1)"
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

const maxPages = 3
const range = computed(() =>
  [...Array(props.pageLength > maxPages ? maxPages : props.pageLength).keys()]
    .map((r) => {
      let delta
      if (props.currentPage == props.pageLength) {
        delta = 3
      } else if (props.currentPage == 1) {
        delta = 0
      } else {
        delta = 1
      }
      return r + props.currentPage - delta
    })
    .filter((r) => r > 1 && r <= props.pageLength - 1)
)

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
  user-select: none;
  -moz-user-select: none;
  -khtml-user-select: none;
  -webkit-user-select: none;
  -o-user-select: none;
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
}

.pagenumber-elipsis {
  display: inline-block;
}
</style>
