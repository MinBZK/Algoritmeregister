<template>
  <div>
    <div class="block-info">
      <div class="rows">
        <h3>
          {{ title }}
        </h3>

        <div class="row button--block">
          <select v-model="listValue" aria-describedby="select-helptext-1">
            <option v-for="column in columns" :key="column" :value="column.key">
              {{ column.label }}
            </option>
          </select>
        </div>

        <div class="row">
          <table class="table table--condensed">
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
              <tr v-for="row in parsedCountData" :key="row.descriptor">
                <td class="word-break">
                  {{ row.descriptor }}
                </td>
                <td>
                  <b>
                    {{ row.count }}
                  </b>
                </td>
                <td class="borderless-left">
                  <span> {{ row.fraction }}% </span>
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
const props = defineProps<{
  nAlgorithms: number
}>()

const { t } = useI18n()
const title = computed(() => t('dashboard.countPerTypeTitle'))
const value = computed(() => t('dashboard.value'))
const numberOfMatches = computed(() => t('dashboard.numberOfMatches'))

const interestingColumns: string[] = [
  'organization',
  'department',
  'type',
  'category',
  'status',
  'competent_authority',
  'dpia',
  'iama',
  'area',
  'lang',
  'mprd',
]

const columnApi = await algoritmeService.getColumns()
const columns = computed(() =>
  columnApi.data.value
    .map((column: any) => {
      return {
        key: column.column_name,
        label: t(`algorithmProperties.${column.column_name}.label`),
      }
    })
    .filter((column: { key: string; label: string }) => {
      return interestingColumns.includes(column.key)
    })
)

const countData =
  ref<[{ descriptor: string; count: string; fraction: number }]>()
const listValue = ref(interestingColumns[0])
const selectType = async () => {
  await algoritmeService.getCount(listValue.value).then((response) => {
    countData.value = response.data.value?.map((data: any) => {
      const result = {
        descriptor: data.descriptor,
        count: data.count,
        fraction: Math.floor((data.count / props.nAlgorithms) * 100),
      }
      return result
    })
  })
}

const parsedCountData = computed(() => {
  return countData.value?.map((data) => {
    const parsedValue = () => {
      if (data.descriptor === '' || data.descriptor === null) {
        return t('ontbreekt')
      } else if (typeof data.descriptor === 'boolean') {
        return data.descriptor === true ? t('yes') : t('no')
      } else {
        return data.descriptor
      }
    }
    return {
      descriptor: parsedValue(),
      count: data.count,
      fraction: data.fraction,
    }
  })
})

selectType()

watch(listValue, () => {
  selectType()
})
</script>

<style lang="scss">
.word-break {
  word-break: break-word;
}
.select-block {
  display: block;
}

.borderless-left {
  border-left: 0 !important;
}
</style>
