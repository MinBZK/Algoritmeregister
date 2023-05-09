<template>
  <div class="bar">
    <h2 class="highlight-text">
      {{ t('home-highlight-algorithm-text') }}
    </h2>
    <div class="bottom-margin"></div>
    <ul class="bar__list">
      <li
        v-for="algo in data?.results"
        :key="algo.algoritme_id"
        class="bar__list__item"
      >
        <p class="bar__list__item-icon">
          <NuxtIcon
            size="0.8em"
            name="material-symbols:arrow-forward-ios-rounded"
          />&nbsp;
          <NuxtLink :to="localePath(`/algoritme/${algo.lars}`)" class="link">
            {{ algo.name || '' }} | {{ algo.organization || '' }}
          </NuxtLink>
        </p>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import algoritmeService from '@/services/algoritme'

const { t } = useI18n()
const localePath = useLocalePath()

const selectedAlgorithmIds = ['85816259', '33947772', '97246956']

const { data } = await algoritmeService.getAll({
  filters: [
    {
      attribute: 'lars',
      value: selectedAlgorithmIds,
    },
  ],
  page: 1,
  limit: selectedAlgorithmIds.length,
})
</script>
<style scoped lang="scss">
.bottom-margin {
  padding-bottom: 15px;
}

.highlight-text {
  font-size: 1em;
}
</style>
