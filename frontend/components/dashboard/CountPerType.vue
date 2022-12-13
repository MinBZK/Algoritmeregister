<template>
  <div class="block-cards__card">
    <div class="block-info">
      <div class="rows">
        <h3>
          {{ title }}
        </h3>
        <div class="row button--block">
          <select aria-describedby="select-helptext-1" v-model="listValue">
            <option v-for="column in columns" :value="column.key">
              {{ column.label }}
            </option>
          </select>
        </div>
        <!-- <div class="row">
          <button
            class="button button--primary button--block button--nolabel"
            @click="selectType()"
          >
            <span class="button__label">{{ select }}</span>
          </button>
        </div> -->
        <div class="row">
          <table class="table table--condensed">
            <thead>
              <tr>
                <th class="u-columnwidth-50p">
                  <span class="notbold">{{ value }} </span>
                </th>
                <th class="u-columnwidth-10p">{{ numberOfMatches }}</th>
                <th class="u-columnwidth-10p borderless-left">
                  <span class="notbold">Percentage</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="org in parsedCountData">
                <td class="word-break">
                  {{ org.descriptor }}
                </td>
                <td>
                  <b>
                    {{ org.count }}
                  </b>
                </td>
                <td class="borderless-left">
                  <span class="small-font"> {{ org.fraction }}% </span>
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
import { useI18n } from 'vue-i18n'
import algoritmeService from '@/services/algoritme'
const props = defineProps<{
  nAlgorithms: number
}>()

const { t } = useI18n()
const title = computed(() => t('dashboard.countPerTypeTitle'))
const value = computed(() => t('dashboard.value'))
const numberOfMatches = computed(() => t('dashboard.numberOfMatches'))

const interestingColumns: string[] = [
  'algoritme.organization',
  'algoritme.department',
  'algoritme.type',
  'algoritme.category',
  'algoritme.status',
  'juridisch.competent_authority',
  'juridisch.dpia',
  'juridisch.iama',
  'metadata.area',
  'metadata.lang',
  'toepassing.mprd',
]

const columnApi = await algoritmeService.getColumns()
const columns = computed(() =>
  columnApi.data.value
    .map((column: any) => {
      return {
        key: `${column.table_name}.${column.column_name}`,
        label: t(`algorithmProperties.${column.column_name}.label`),
      }
    })
    .filter((column: { key: string; label: string }) => {
      return interestingColumns.includes(column.key)
    })
)

var countData = ref<[{ descriptor: string; count: string; fraction: number }]>()
var listValue = ref(interestingColumns[0])
const selectType = async () => {
  await algoritmeService.getCount(listValue.value).then((response) => {
    countData.value = response.data.value?.map((data: any) => {
      const result = {
        descriptor: data.descriptor,
        count: data.count,
        fraction: Math.floor((data.count / props.nAlgorithms) * 100),
      }
      console.log(result)
      return result
    })
  })
}

const parsedCountData = computed(() => {
  return countData.value?.map((data) => {
    const parsedValue = () => {
      if (data.descriptor === '' || data.descriptor === null) {
        return t('ontbreekt')
      } else if (typeof data.descriptor == 'boolean') {
        return data.descriptor == true ? t('yes') : t('no')
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
.notbold {
  font-weight: normal;
}
</style>
