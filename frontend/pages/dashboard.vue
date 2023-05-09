<template>
  <div>
    <h1>Dashboard</h1>
    <h2>{{ totalCountText }}:&nbsp; {{ algoCount }}</h2>
    <h2>{{ currentDate }}</h2>
    <div class="block-cards">
      <DashboardCountPerType
        class="block-cards__card"
        :n-algorithms="algoCount!"
      />
      <DashboardDataCompleteness
        class="block-cards__card"
        :n-algorithms="algoCount!"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import algoritmeService from '@/services/algoritme'

const { t } = useI18n()
const totalCountText = computed(() => t('dashboard.totalCountText'))

const date = new Date()
const currentDate = computed(() => {
  const month: string = t(`months.${date.getMonth() + 1}`)
  const monthDay: string = date.getDate().toString()
  const year: string = date.getFullYear().toString()
  const hours: string = date.getHours().toString()
  const minutes: string =
    date.getMinutes() < 10
      ? '0'.concat(date.getMinutes().toString())
      : date.getMinutes().toString()

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
      month +
      ' ' +
      monthDay +
      monthDayOrdinal +
      ' ' +
      year +
      ' | ' +
      hours +
      ':' +
      minutes
    )
  } else if (!isEnglish) {
    return monthDay + ' ' + month + ' ' + year + ' | ' + hours + ':' + minutes
  }
})

const { data } = await algoritmeService.getTotalCount()
const algoCount = data

definePageMeta({
  title: 'Dashboard',
})
useHead({ title: 'Dashboard' })
</script>

<style lang="scss">
.block-cards__card {
  margin-right: 20px;
}
h2 {
  font-size: 1.4rem !important;
  margin-bottom: 0.2em;
}
h1 {
  margin-bottom: 0.4em;
}
.block-cards {
  padding-top: 2em;
}
</style>
