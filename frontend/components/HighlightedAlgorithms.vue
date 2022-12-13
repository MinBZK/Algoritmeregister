<template>
  <div class="bar">
    <b class="highlight-text">
      {{ t('home-highlight-algorithm-text') }}
    </b>
    <div class="bottom-margin"></div>
    <ul class="bar__list">
      <li
        v-for="algo in selectedAlgorithms"
        :key="algo.id"
        class="bar__list__item"
      >
        <p class="bar__list__item-icon">
          <NuxtIcon
            size="0.8em"
            name="material-symbols:arrow-forward-ios-rounded"
          />&nbsp;
          <NuxtLink :to="`/algoritme/${algo.slug}`" class="link">
            {{ algo.name || '' }} | {{ algo.organization || '' }}
          </NuxtLink>
        </p>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import algoritmeService from '@/services/algoritme'
import { AlgNameIdOrg } from '~~/types/algoritme'
const { t } = useI18n()

const { data } = await algoritmeService.getNameIdOrg()
const nameList = ref(data.value as AlgNameIdOrg[])

const selectedAlgorithmSlugs = [
  'public-eye-gemeente-amsterdam',
  'uitrekenen-woz-waarde-gemeente-den-haag',
  'parkeercontrole-gemeente-rotterdam',
]

const selectedAlgorithms = computed(() =>
  nameList.value.filter((algoritme) =>
    selectedAlgorithmSlugs.includes(algoritme.slug)
  )
)
</script>
<style lang="scss">
.bottom-margin {
  padding-bottom: 15px;
}
</style>
