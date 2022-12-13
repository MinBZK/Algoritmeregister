<template>
  <div>
    <div class="columns">
      <div class="columns column-d-0.5">
        <h1>Dashboard</h1>
      </div>
      <div class="column columnd-d-2">
        <h1>{{ currentDate }}</h1>
      </div>
    </div>
    <div class="row">
      <h3>{{ totalCountText }}:&nbsp; {{ algoCount }}</h3>
    </div>
    <div class="block-cards">
      <DashboardCountPerType :n-algorithms="algoCount!" />
      <DashboardCompleteness :n-algorithms="algoCount!" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import algoritmeService from '@/services/algoritme'

const { t } = useI18n()
const totalCountText = computed(() => t('dashboard.totalCountText'))

const date = new Date()
const currentDate = computed(() => {
  const weekDay: string = t(`weekDays.${date.getDay() + 1}`)
  const month: string = t(`months.${date.getMonth() + 1}`)
  const monthDay: string = date.getDate().toString()
  const year: string = date.getFullYear().toString()

  const isEnglish = t('english?') === 'true'
  if (isEnglish) {
    let monthDayOrdinal = ''
    if (['1', '21', '31'].includes(monthDay)) {
      monthDayOrdinal = 'st'
    } else if (['2', '22'].includes(monthDay)) {
      monthDayOrdinal = 'nd'
    } else if (['3', '23'].includes(monthDay)) {
      monthDayOrdinal = 'rd'
    } else {
      monthDayOrdinal = 'th'
    }
    return (
      weekDay + ', ' + month + ' ' + monthDay + monthDayOrdinal + ' ' + year
    )
  } else if (!isEnglish) {
    return weekDay + ' ' + monthDay + ' ' + month + ' ' + year
  }
})

const { data } = await algoritmeService.getTotalCount()
const algoCount = data
</script>

<style lange="scss">
.block-cards__card {
  margin-right: 20px;
}
</style>
