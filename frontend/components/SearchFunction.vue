<template>
  <div class="block-search">
    <div class="columns">
      <div class="column column-d-5">
        <div class="form__row">
          <label class="form__label form__label--accent">{{
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
            @keyup.enter="$emit('doSearch')"
          />
        </div>
      </div>
      <div class="column column-d-0.5">
        <div class="form__row">
          <button
            class="button button--primary button--block button--nolabel"
            type="submit"
            @click="$emit('doSearch')"
          >
            <span class="button__label"
              >{{ search }} <NuxtIcon name="ic:round-search"
            /></span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useDisplay } from 'vuetify'

const { t } = useI18n()
const { xs } = useDisplay()

const emit = defineEmits(['input', 'doSearch'])

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
</style>
