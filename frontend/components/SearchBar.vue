<template>
  <div class="block-search">
    <label
      v-if="type === 'default'"
      id="search-label"
      class="form__label form__label--accent"
    >
      <i18n-t :keypath="keypath" tag="label" scope="global">
        <template #n>
          <span v-if="router.currentRoute.value.meta.title === 'Home'"
            ><NuxtLink :to="localePath(`/algoritme`)">
              {{ totalCount === 0 ? nAlgorithms : totalCount }}
            </NuxtLink>
          </span>
          <span v-else>
            {{ totalCount === 0 ? nAlgorithms : totalCount }}
          </span>
        </template>
      </i18n-t>
    </label>
    <div class="columns">
      <div class="column column-d-5">
        <div ref="searchBarParentDiv" class="form__row less-bottom-margin">
          <input
            id="input-text-98789"
            v-model="searchValue"
            type="text"
            name="98789"
            class="input input-text"
            :placeholder="p(placeholderHint)"
            aria-invalid="false"
            aria-labelledby="search-label"
            autocomplete="off"
            @keyup.enter="doSearch"
            @keydown.esc="clearSuggestionsList"
            @focus="isSuggestionShown = true"
          />
          <div
            v-if="suggestionList.length > 0"
            :class="
              isSuggestionShown
                ? 'autocomplete-suggestions'
                : 'autocomplete-suggestions hidden'
            "
          >
            <div>
              <h4>{{ t('searchSuggestion.title') }}:</h4>
            </div>
            <div v-for="suggestion in suggestionList" :key="suggestion.lars">
              <NuxtLink :to="localePath(`/algoritme/${suggestion.lars}`)">
                {{ suggestion.name }} |
                {{ suggestion.organization }}
              </NuxtLink>
            </div>
          </div>
          <div
            v-if="suggestionOrgSearch?.organisations.length! >= 2"
            :class="
              isSuggestionShown
                ? 'autocomplete-suggestions'
                : 'autocomplete-suggestions hidden'
            "
          >
            <div>
              <h4>{{ t('orgSuggestionSearch.title') }}</h4>
            </div>
            <div
              v-for="org in suggestionOrgSearch!.organisations"
              :key="org.org_id"
            >
              <NuxtLink
                tabindex="0"
                @keydown.enter.prevent="setValueSearchBar(org)"
                @click.prevent="setValueSearchBar(org)"
                >{{ org.name }}</NuxtLink
              >
            </div>
          </div>
          <div
            v-else-if="suggestionOrgSearch?.organisations.length! >= 1"
            :class="
              isSuggestionShown
                ? 'autocomplete-suggestions'
                : 'autocomplete-suggestions hidden'
            "
          >
            <div>
              <h4>{{ t('orgSuggestionSearch.title') }}</h4>
            </div>
            <div>
              <NuxtLink
                :to="localePath('/')"
                @click.prevent="handleSearch(true)"
              >
                {{
                  t('orgSuggestionSearch.OrgSpecificSearch', {
                    organisation: suggestionOrgSearch?.organisations[0].name,
                  })
                }}
              </NuxtLink>
            </div>
            <div>
              <NuxtLink
                :to="localePath('/')"
                @click.prevent="
                  suggestionOrgSearch &&
                  handleRedirectOrgPage(suggestionOrgSearch)
                "
              >
                {{
                  t('orgSuggestionSearch.RedirectToOrgPage', {
                    organisation: suggestionOrgSearch?.organisations[0].name,
                  })
                }}
              </NuxtLink>
            </div>
            <div>
              <NuxtLink
                :to="localePath('/')"
                @click.prevent="handleSearch(false)"
              >
                {{
                  t('orgSuggestionSearch.OrgGenericSearch', {
                    searchQuery: searchValue,
                  })
                }}
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
            @click="doSearch"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watchDebounced } from '@vueuse/core'
import type { Suggestion } from '@/types/algoritme'
import algoritmeService from '@/services/algoritme'
import type { SearchSuggestionResult } from '@/services/algoritme'
import organisationService from '@/services/organisation'
import type {
  OrganisationMappingResult,
  OrganisationSearchSuggestionResponse,
} from '@/types/organisation'

withDefaults(
  defineProps<{
    type?: 'default' | 'no-link'
    placeholderHint?: string
    keypath?: string
    totalCount?: number | null
  }>(),
  {
    type: 'default',
    placeholderHint: 'Zoekbalk.hint',
    keypath: 'searchExplanation',
    totalCount: 0,
  }
)

const { t, locale } = useI18n()
const { p } = useTextLoader()

const emit = defineEmits<{
  (e: 'input', searchValue: string): void
  (e: 'doSearch', searchValue: string): void
}>()

const searchValue = ref(useRoute().query.searchtext || '')
const isSuggestionShown = ref<boolean>(true)
const suggestionList = ref<Suggestion[]>([])
const suggestionResults = ref<SearchSuggestionResult | null>()
const suggestionOrgSearch = ref<OrganisationSearchSuggestionResponse | null>()
const router = useRouter()

const { data } = await algoritmeService.getTotalCount()
const nAlgorithms = data

const search = computed(() => t('search'))
const localePath = useLocalePath()

const searchBarParentDiv = ref<HTMLDivElement | null>(null)
const handleClickOutsideParentDiv = (event: Event) => {
  if (
    searchBarParentDiv.value &&
    !searchBarParentDiv.value.contains(event.target as Node)
  ) {
    isSuggestionShown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutsideParentDiv)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutsideParentDiv)
})

const doSearch = () => {
  emit('doSearch', searchValue.value as string)
  suggestionList.value = []
  suggestionOrgSearch.value = null
}

const clearSuggestionsList = () => {
  suggestionList.value = []
  suggestionOrgSearch.value = null
}

const setValueSearchBar = (organisation: OrganisationMappingResult) => {
  searchValue.value = organisation.name
}
const handleRedirectOrgPage = (
  suggestionOrgSearch: OrganisationSearchSuggestionResponse
) => {
  const organisation = suggestionOrgSearch.organisations[0]

  let targetPath = '/map/organisatie-niet-gepubliceerd'
  if (organisation.count === 0 && !organisation.show_page) {
    targetPath = '/map/organisatie-niet-aangesloten'
  } else if (organisation.count > 0 || organisation.show_page) {
    targetPath = `/organisatie/${organisation.org_id}`
  }
  router.push(localePath(targetPath))
}

const handleSearch = async (isOrgSpecificSearch: boolean) => {
  const response = await organisationService.getFullNameOrganisation(
    searchValue.value as string,
    mapLocaleName(locale.value as 'en' | 'nl')
  )
  const organisation = response.data.value?.organisations[0]
  const query = isOrgSpecificSearch
    ? {
        organisation: organisation?.name,
      }
    : { searchtext: searchValue.value }

  if (organisation?.count === 0 && !organisation?.show_page) {
    router.push(localePath('/map/organisatie-niet-aangesloten'))
  } else {
    router.push(
      localePath({
        name: 'algoritme',
        query,
      })
    )
  }
  suggestionOrgSearch.value = null
}

async function performSuggestionSearch(searchValue: string) {
  const response = await algoritmeService.getSearchSuggestion(
    searchValue,
    mapLocaleName(locale.value as 'en' | 'nl')
  )
  suggestionResults.value = response.data.value
}

async function performOrganisationSearch(searchValue: string) {
  const response = await organisationService.getFullNameOrganisation(
    searchValue,
    mapLocaleName(locale.value as 'en' | 'nl')
  )
  suggestionOrgSearch.value = response.data.value
}

watchDebounced(
  searchValue,
  async () => {
    if (searchValue.value.length > 2) {
      await performOrganisationSearch(searchValue.value as string)
      if (suggestionOrgSearch.value) {
        suggestionList.value = []
      } else {
        suggestionOrgSearch.value = null
        await performSuggestionSearch(searchValue.value as string)
        suggestionList.value = suggestionResults.value?.algorithms || []
      }
    } else {
      suggestionList.value = []
      suggestionOrgSearch.value = null
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

.hidden {
  visibility: hidden;
}
</style>
