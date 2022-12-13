<template>
  <div class="block-cards__card no-bottom-padding">
    <div class="block-info green-color">
      <p>{{ paragraph1 }}</p>
      <p>{{ paragraph2 }}</p>
      <p>
        <b>
          {{ paragraph3Header }}
        </b>
      </p>
      <p>
        {{ paragraph3part1 }}<b>{{ nAlgorithms }}</b
        >{{ paragraph3part2 }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import algoritmeService from '@/services/algoritme'

const { t } = useI18n()

const paragraph1 = computed(() => t('homePageText.paragraph1'))
const paragraph2 = computed(() => t('homePageText.paragraph2'))
const paragraph3Header = computed(() => t('homePageText.paragraph3Header'))
const paragraph3part1 = computed(() => t('homePageText.paragraph3part1'))
const paragraph3part2 = computed(() => t('homePageText.paragraph3part2'))

const { data } = await algoritmeService.getTotalCount()
const nAlgorithms = data
</script>

<style lang="scss">
.green-color {
  background-color: #f0f8e8;
}
.no-bottom-padding {
  padding-bottom: 0px !important;
  margin-bottom: 0px !important;
}
</style>
