<template>
  <div class="block-cards__card">
    <div class="block-info">
      <div class="rows">
        <h3>
          {{ title }}
        </h3>
        <div class="row">
          <div v-if="loading" class="loading-text">{{ loadingText }}...</div>
          <table v-show="!loading" class="table">
            <thead>
              <tr>
                <th class="u-columnwidth-50p">{{ tableHeader }}:</th>
                <th class="u-columnwidth-10p"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="agg in aggregates" :key="agg.label">
                <td>{{ agg.label }}</td>
                <td>{{ agg.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import algoritmeService from '@/services/algoritme'

const { t } = useI18n()
const title = computed(() => t('dashboard.completenessTitle'))
const tableHeader = computed(() => t('dashboard.tableHeader'))
const loadingText = computed(() => t('dashboard.loadingText'))

const props = defineProps<{
  nAlgorithms: number
}>()

const getFullyComplete = async () => {
  const result = await algoritmeService.getCountWithFilledColumns('*')
  return result.data.value
}

const getMandatoryComplete = async () => {
  const notNullableColumns = data.value.filter(
    (column: any) => column.is_nullable === 'NO'
  )
  const columns = notNullableColumns.map(
    (c: any) => `${c.table_name}.${c.column_name}`
  )
  const result = await algoritmeService.getCountWithFilledColumns(columns)
  loading.value = false
  return result.data.value
}

const getMandatoryMissing = async () => {
  return (
    props.nAlgorithms -
    (await getFullyComplete()) -
    (await getMandatoryComplete())
  )
}

const aggregates = ref<{ label: string; value: string }[]>([])
const setAggregates = async () => {
  aggregates.value = [
    {
      label: t('dashboard.fullyComplete'),
      value: await getFullyComplete(),
    },
    {
      label: t('dashboard.mandatoryComplete'),
      value: await getMandatoryComplete(),
    },
    {
      label: t('dashboard.mandatoryMissing'),
      value: await getMandatoryMissing(),
    },
  ]
}

const loading = ref(true)
const { data } = await algoritmeService.getColumns().then((value) => {
  setAggregates()
  return value
})
</script>

<style lang="scss">
.word-break {
  word-break: break-word;
}
.loading-text {
  text-align: center;
}
</style>
