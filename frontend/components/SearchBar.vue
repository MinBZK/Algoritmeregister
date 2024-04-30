<template>
  <div class="block-search">
    <label
      v-if="type === 'default'"
      id="search-label"
      class="form__label form__label--accent"
    >
      <i18n-t keypath="searchExplanation" tag="label" scope="global">
        <template #n>
          {{ nAlgorithms }}
        </template>
      </i18n-t>
    </label>
    <div class="columns">
      <div class="column column-d-5">
        <div class="form__row less-bottom-margin">
          <input
            id="input-text-98789"
            v-model="searchValue"
            type="text"
            name="98789"
            class="input input-text"
            :placeholder="p('Zoekbalk.hint')"
            aria-invalid="false"
            aria-labelledby="search-label"
            autocomplete="off"
            @keyup.enter="doSearch()"
          />
          <div
            v-if="suggestionList.length > 0"
            class="autocomplete-suggestions"
          >
            <div>
              <h4>Ga direct naar een algoritmebeschrijving:</h4>
            </div>
            <div v-for="suggestion in suggestionList" :key="suggestion.lars">
              <NuxtLink :to="localePath(`/algoritme/${suggestion.lars}`)">
                {{ suggestion.name }} |
                {{ suggestion.organization }}
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
      <div class="column column-d-0.5">
        <div class="form__row">
          <FormOverheidButton
            class="button--align-to-search-field"
            :label="search"
            icon="ic:round-search"
            :full-width="true"
            @click="doSearch()"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watchDebounced } from '@vueuse/core'
import { Suggestion } from 'types/algoritme'
import algoritmeService, { SearchSuggestionResult } from '@/services/algoritme'

withDefaults(
  defineProps<{
    type?: 'default' | 'no-link'
  }>(),
  {
    type: 'default',
  }
)

const { t, locale } = useI18n()
const { p } = useTextLoader()

const emit = defineEmits<{
  (e: 'input', searchValue: string): void
  (e: 'doSearch', searchValue: string): void
}>()

const searchValue = ref(useRoute().query.searchtext || '')

const suggestionList = ref<Suggestion[]>([])
const suggestionResults = ref<SearchSuggestionResult | null>()

const { data } = await algoritmeService.getTotalCount()
const nAlgorithms = data

const search = computed(() => t('search'))

const localePath = useLocalePath()

const doSearch = () => {
  emit('doSearch', searchValue.value as string)
  suggestionList.value = []
}

async function performSuggestionSearch(searchValue: string) {
  const response = await algoritmeService.getSearchSuggestion(
    searchValue,
    mapLocaleName(locale.value as 'en' | 'nl')
  )
  suggestionResults.value = response.data.value
}

watchDebounced(
  searchValue,
  async () => {
    if (searchValue.value.length > 2) {
      await performSuggestionSearch(searchValue.value as string)
      suggestionList.value = suggestionResults.value?.algorithms || []
    } else {
      suggestionList.value = []
    }
  },
  { debounce: 250 }
)
</script>

<style scoped lang="css">
.form__label {
  margin-bottom: 0.25em !important;
}
.less-bottom-margin {
  margin-bottom: 0.5em !important;
}

.autocomplete-suggestions {
  border: 1px solid #ccc;
  max-height: 200px; /* Set the maximum height for the search results container */
  overflow-y: auto; /* Add a scrollbar when the results exceed the container height */
  background-color: white;
  width: 100%;
  position: absolute;
  z-index: 1;
}
.autocomplete-suggestions div {
  padding: 0.4em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.autocomplete-suggestions h4 {
  font-size: 0.9em;
  margin-bottom: -0.5em;
}
</style>
