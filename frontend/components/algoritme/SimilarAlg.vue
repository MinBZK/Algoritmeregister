<template>
  <div v-if="data && data.results.length">
    <h2>
      {{
        data.results.length === 1
          ? t('similarAlgorithm')
          : t('similarAlgorithms')
      }}
    </h2>
    <div class="result--list result--list__data">
      <ul>
        <li v-for="algoritme in data.results" :key="algoritme.lars">
          <GenericResultCard :algoritme="algoritme" :similar-algo-result="true">
          </GenericResultCard>
        </li>
      </ul>
    </div>
  </div>
</template>
<script setup lang="ts">
import algoritmeService from '@/services/algoritme'
const { t, locale } = useI18n()

const props = defineProps<{
  lars: string
}>()

const { data } = await algoritmeService.getSimilar(
  props.lars,
  mapLocaleName(locale.value as 'en' | 'nl')
)
</script>
<style>
ul {
  list-style-type: none;
}
</style>
