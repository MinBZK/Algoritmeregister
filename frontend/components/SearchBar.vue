<template>
  <div class="block-search">
    <div class="columns">
      <div class="column column-d-5">
        <div class="form__row less-bottom-margin">
          <label id="search-label" class="form__label form__label--accent">{{
            searchExplanation
          }}</label>

          <input
            id="input-text-98789"
            v-model="searchValue"
            type="text"
            name="98789"
            class="input input-text"
            :placeholder="searchHint"
            aria-invalid="false"
            aria-labelledby="search-label"
            @keyup.enter="doSearch()"
          />
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
const { t } = useI18n()
const localePath = useLocalePath()

const emit = defineEmits<{
  (e: 'input', searchValue: string): void
  (e: 'doSearch'): void
}>()

const searchValue = ref(useRoute().query.search || '')

const search = computed(() => t('search'))
const searchHint = computed(() => t('searchHint'))
const searchExplanation = computed(() => t('searchExplanation'))

const doSearch = () => {
  const router = useRouter()
  // const query = useRoute().query
  router.push(
    localePath({
      name: 'algoritme',
      query: {
        search: searchValue.value,
        // q: query.q,
      },
    })
  )
  emit('doSearch')
}
</script>

<style scoped lang="css">
.wrapper-2 {
  display: flex;
}
.wrapper-1 {
  margin-bottom: 10px;
}
.v-text-field :deep(label) {
  font-size: 1.1em;
}
.button--align-to-search-field {
  margin-top: 1.75em;
}
@media (max-width: 65em) {
  .button--align-to-search-field {
    margin-top: 0.6em;
  }
}
.form__label {
  margin-bottom: 0.5em !important;
}
.less-bottom-margin {
  margin-bottom: 0px !important;
}
</style>
