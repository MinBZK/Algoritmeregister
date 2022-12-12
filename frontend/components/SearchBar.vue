<template>
  <div class="block-search">
    <div class="columns">
      <div class="column column-d-5">
        <div class="form__row">
          <label id="search-label" class="form__label form__label--accent">{{
            searchExplanation
          }}</label>

          <input
            type="text"
            id="input-text-98789"
            name="98789"
            class="input input-text"
            :placeholder="searchHint"
            aria-invalid="false"
            v-model="searchValue"
            aria-labelledby="search-label"
            @keyup.enter="$emit('doSearch')"
          />
        </div>
      </div>
      <div class="column column-d-0.5">
        <div class="form__row">
          <button
            class="button button--primary button--block button--nolabel button--align-to-search-field"
            type="submit"
            @click="$emit('doSearch')"
          >
            <span class="button__label"
              >{{ search }} <NuxtIcon size="0.9em" name="ic:round-search"
            /></span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const emit = defineEmits<{
  (e: 'input', searchValue: string): void
  (e: 'doSearch'): void
}>()

const props = defineProps<{
  value: string
}>()

const searchValue = ref(props.value)

const search = computed(() => t('search'))
const searchHint = computed(() => t('searchHint'))
const searchExplanation = computed(() => t('searchExplanation'))

watch(searchValue, () => {
  emit('input', searchValue.value)
})
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
.form__label {
  margin-bottom: 0.5em !important;
}
</style>