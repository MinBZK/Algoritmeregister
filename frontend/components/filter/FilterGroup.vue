<template>
  <div style="margin-bottom: 1em">
    <FilterBlock
      v-if="isMobile"
      v-model="showFiltersMobile"
      title="Filters"
      @dropdown-clicked="toggleShowFilters"
    />
    <h2 v-else>Filters</h2>
    <template v-if="showFilters">
      <FilterBlock
        v-if="selectedFilters?.length || 0 > 0"
        disable-dropdown
        :title="t('filter.selectedFilters')"
      >
        <div v-for="filter in selectedFilters" :key="filter.name">
          <strong>{{ t('filter.' + filter.name) }}:</strong> <br />
          <RouterLink
            class="chosen-filter"
            :to="
              localePath({
                name: 'algoritme',
                query: getQueryWithout(filter.name),
              })
            "
            :aria-label="$t('filter.aria/remove', { what: filter.value }) || ''"
          >
            {{ filter.value }}
            <img
              src="@/assets/images/icons/icon-close.svg"
              alt="Verwijder dit filter"
            />
          </RouterLink>
        </div>
      </FilterBlock>
      <FilterBlock
        v-if="!orgFilterActive"
        :title="t('filter.pickOrgType')"
        :style="!isMobile ? 'margin: 0.5em 0' : ''"
      >
        <OrgTypeSelector
          v-model="selectedOrgType"
          style="margin-top: 0.5em"
          :available-types="filterData?.organisation"
        />
      </FilterBlock>
      <FilterBlock
        v-if="!orgFilterActive && selectedOrgType"
        :title="t('filter.pickOrg')"
      >
        <div v-for="org in orgOptions" :key="org.name">
          <RouterLink
            class="chosen-filter"
            :to="
              localePath({
                name: 'algoritme',
                query: { ...parsedQuery, organisation: org.name },
              })
            "
            :aria-label="$t('filter.aria/remove', { what: org.name }) || ''"
          >
            <span>
              {{ org.name }}
            </span>
            <span class="org-count">
              {{ org.count }}
            </span>
          </RouterLink>
        </div>
      </FilterBlock>
    </template>
  </div>
</template>

<script setup lang="ts">
import { LocationQuery } from 'vue-router'
import OrgTypeSelector from './OrgTypeSelector.vue'
import { FilterData, SelectedFilter } from '@/types/filter'
import { useMobileBreakpoint } from '~~/composables/mobile'
import { OrgType } from 'types/organisation'

const props = defineProps<{
  selectedFilters?: SelectedFilter[]
  filterData?: FilterData
}>()

const { t } = useI18n()

const isMobile = useMobileBreakpoint().medium
const localePath = useLocalePath()

const parsedQuery = computed(() => useRoute().query)

const getQueryWithout = (queryParameter: string): LocationQuery => {
  const query = { ...parsedQuery.value }
  if (queryParameter in query) {
    delete query[queryParameter]
  }
  return query
}

const selectedOrgType = ref<OrgType>()
const orgOptions = computed(
  () =>
    props.filterData?.organisation.find(
      (orgType) => orgType.type === selectedOrgType.value
    )?.organisations
)

const orgFilterActive = computed(() => {
  return props.selectedFilters?.find((filter) => filter.name === 'organisation')
})

// Mobile only.
const showFiltersMobile = ref(false)
const showFilters = computed(() => !isMobile.value || showFiltersMobile.value)
const toggleShowFilters = () =>
  (showFiltersMobile.value = !showFiltersMobile.value)
</script>

<style scoped lang="scss">
.chosen-filter {
  width: 100%;
  display: inline-flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;

  img {
    height: 0.75em;
  }
}

h2 {
  font-size: 1em;
}

.org-count {
  margin-left: 0.5em;
  white-space: nowrap;
}
</style>
