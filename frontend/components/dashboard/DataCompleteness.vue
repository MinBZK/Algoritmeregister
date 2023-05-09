<template>
  <div>
    <div class="block-info">
      <div class="rows">
        <h3>
          {{ title }}
        </h3>
        <div class="row">
          <div v-if="loading" class="loading-text">{{ loadingText }}...</div>
          <table v-show="!loading" class="table table--condensed">
            <thead>
              <tr>
                <th class="u-columnwidth-50p">
                  <span>{{ value }} </span>
                </th>
                <th class="u-columnwidth-10p">{{ numberOfMatches }}</th>
                <th class="u-columnwidth-10p borderless-left">
                  <span>Percentage</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="agg in aggregates" :key="agg.label">
                <td>{{ t(agg.label) }}</td>
                <td>
                  <b>{{ agg.value }} </b>
                </td>
                <td class="borderless-left">
                  <span> {{ agg.fraction }}% </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import algoritmeService from '@/services/algoritme'

const { t } = useI18n()
const title = computed(() => t('dashboard.completenessTitle'))
const loadingText = computed(() => t('dashboard.loadingText'))
const value = computed(() => t('dashboard.value'))
const numberOfMatches = computed(() => t('dashboard.numberOfMatches'))

const props = defineProps<{
  nAlgorithms: number
}>()

const getFullyComplete = async () => {
  const result = await algoritmeService.getCountWithFilledColumns('*')
  loading.value = false
  return result.data.value
}

// const getMandatoryComplete = async () => {
//   const notNullableColumns = data.value.filter(
//     (column: any) => column.is_nullable === 'NO'
//   )
//   const columns = notNullableColumns.map(
//     (c: any) => `${c.table_name}.${c.column_name}`
//   )
//   const result = await algoritmeService.getCountWithFilledColumns(columns)
//   loading.value = false
//   return result.data.value
// }

const aggregates = ref<{ label: string; value: string; fraction: number }[]>([])
const setAggregates = async () => {
  const nFullyComplete = await getFullyComplete()
  aggregates.value = [
    {
      label: 'dashboard.fullyComplete',
      value: nFullyComplete,
      fraction: Math.floor((nFullyComplete / props.nAlgorithms) * 100),
    },
    {
      label: 'dashboard.partiallyComplete',
      value: props.nAlgorithms - nFullyComplete,
      fraction: Math.floor(
        ((props.nAlgorithms - nFullyComplete) / props.nAlgorithms) * 100
      ),
    },
  ]
}

const loading = ref(true)
await algoritmeService.getColumns().then((value) => {
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
