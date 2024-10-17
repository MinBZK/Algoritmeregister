<template>
  <div class="filter-buttons">
    <button
      v-for="filter in selectedFilters"
      :key="filter.key"
      class="button"
      @click="removeQueryOnRoute(filter)"
    >
      <span>{{ filter.value }}</span>
      <img src="@/assets/images/icons/icon-cross-primary-darker.svg" alt="" />
    </button>
  </div>
</template>

<script setup lang="ts">
import type { GenericQuery, GenericSelectedFilter } from '~/types/filter'

defineProps<{
  selectedFilters: GenericSelectedFilter[]
}>()

const currentQuery = computed(() => useRoute().query as GenericQuery)
const router = useRouter()
const removeQueryOnRoute = (filter: GenericSelectedFilter) => {
  const query = { ...currentQuery.value }
  if (filter.key in query) {
    delete query[filter.key]
  }
  router.push({ query })
}
</script>

<style scoped lang="scss">
.filter-buttons:first-child {
  margin-left: 0;
}

.button {
  padding: 0.6em;
  display: inline-flex;
  align-items: center;
  border-radius: 8px;

  img {
    margin-top: -0.15em;
    margin-left: 0.5em;
    height: 0.6em;
  }
}
</style>
