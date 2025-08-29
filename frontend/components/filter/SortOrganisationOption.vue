<template>
  <div class="sort-org-picker">
    <div class="button-group">
      <button
        class="rotate-sorting-button"
        :title="t('filter.rotateSorting')"
        @click="rotateSortOptions"
      >
        <NuxtIcon name="fluent:arrow-sort-down-lines-24-filled" />
      </button>
      <div class="sort-org-button-wrapper">
        <button
          class="sort-org-button"
          :data-selected="dropdown"
          @click="dropdown = !dropdown"
        >
          {{ buttonText }}
        </button>

        <div class="dropdown-content">
          <button
            v-for="option in sortOptions"
            :key="option.name"
            tab-index="1"
            :class="{
              'sort-org-active': option.name === buttonText,
            }"
            class="sort-org-select-button"
            @click="changeSorting(option.code)"
          >
            {{ option.name }}
          </button>
        </div>
      </div>
    </div>
  </div>
  <hr />
</template>

<script setup lang="ts">
import type { GenericQuery } from '@/types/filter'
import { SortOption } from '@/types/filter/algoritme'

const { t } = useI18n()
const query = computed(() => useRoute().query as GenericQuery)
const dropdown = ref(false)
const currentIndex = ref(1)
const sortOptions = [
  {
    code: SortOption.sortByNumber,
    name: t('filter.sortRegistrationBased'),
  },
  {
    code: SortOption.sortByName,
    name: t('filter.sortAlfabeticalBased'),
  },
]

const changeSorting = (code: string) => {
  const newQuery: GenericQuery = { ...query.value, sort_option: code }
  useRouter().push({ query: newQuery })
  dropdown.value = false
}

const rotateSortOptions = () => {
  const currentCode = query.value.sort_option || sortOptions[1].code
  currentIndex.value =
    (sortOptions.findIndex((option) => option.code === currentCode) + 1) %
    sortOptions.length
  changeSorting(sortOptions[currentIndex.value].code)
}

const buttonText = computed(() => {
  const selectedOption = sortOptions.find(
    (option) => option.code === query.value.sort_option
  )
  return selectedOption
    ? selectedOption?.name
    : `${t('filter.sortAlfabeticalBased')}`
})

const closeDropdownOnClickOutside = (event: MouseEvent) => {
  const dropdownElement = document.querySelector('.sort-org-button-wrapper')

  if (dropdownElement && !dropdownElement.contains(event.target as Node)) {
    dropdown.value = false
  }
}

onMounted(() => {
  nextTick(() => {
    document.addEventListener('click', closeDropdownOnClickOutside)
  })
})

onUnmounted(() => {
  document.removeEventListener('click', closeDropdownOnClickOutside)
})
</script>

<style scoped lang="scss">
@use '/assets/styles/colors' as colors;

.sort-org-picker {
  z-index: 1;
  width: 100%;
  position: relative;
}

.button-group {
  display: flex;
  gap: 0.5em;
  align-items: center;
  width: 100%;
}

.sort-org-button-wrapper {
  position: relative;
  flex: 1;
}

.sort-org-button {
  width: 100%;
  background-color: colors.$primary;
  color: white;
  font-size: 0.85em;
  cursor: pointer;
  height: 1.5em;
  text-align: center;
  border: none;
}

.sort-org-button:hover {
  background-color: colors.$secondary;
  color: colors.$primary-darker;
}

.sort-org-button:hover:after {
  transform: scale(0.5, 0.7);
  content: url('@/assets/images/icons/icon-language-picker-chevron-dark.svg');
}

.sort-org-button:before {
  position: relative;
  right: 0.4em;
  top: 0.2em;
  transform: scale(0.9);
  display: inline-block;
}

.sort-org-button:after {
  float: right;
  transform: scale(0.5, 0.7);
  content: url('@/assets/images/icons/icon-language-picker-chevron.svg');
}

.sort-org-button[data-selected='true']:after {
  transform: scale(0.5, 0.7) rotate(180deg);
  content: url('@/assets/images/icons/icon-language-picker-chevron-dark.svg');
}

.sort-org-button[data-selected='true']:hover:after {
  transform: scale(0.5, 0.7) rotate(180deg);
  content: url('@/assets/images/icons/icon-language-picker-chevron-dark.svg');
}

.sort-org-button[data-selected='true'] {
  background-color: colors.$secondary;
  color: colors.$primary-darker;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: colors.$secondary;
  width: 100%;
  box-shadow: 0px 10px 15px -3px rgba(0, 0, 0, 0.1);
  z-index: 1;
  top: 100%;
  left: 0;
}

.sort-org-select-button {
  text-align: center;
  color: colors.$primary-darker;
  padding: 0.2em;
  font-size: 0.85em;
  text-decoration: none;
  display: block;
  cursor: pointer;
  width: -webkit-fill-available;
  width: -moz-available;
  border: 0;
  background-color: colors.$secondary;
}

.sort-org-select-button:hover {
  background-color: colors.$primary;
  color: white !important;
}
.sort-org-select-button:focus {
  background-color: colors.$primary;
  color: white !important;
}

.sort-org-button[data-selected='true'] ~ .dropdown-content {
  display: block;
}

.sort-org-active {
  background-color: colors.$primary !important;
  color: white !important;
}

.rotate-sorting-button {
  background-color: colors.$primary;
  color: white;
  font-size: 0.85em;
  cursor: pointer;
  height: 1.5em;
  text-align: center;
  border: none;
}

.rotate-sorting-button:hover {
  background-color: colors.$secondary;
  color: colors.$primary-darker;
}
</style>
