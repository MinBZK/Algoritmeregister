<template>
  <div>
    <div class="block-info">
      <div class="rows">
        <h3>Algoritmes in het register per informatietype</h3>
        <div class="row button--block">
          <div>
            <select
              v-model="listValue"
              class="width-100"
              aria-describedby="select-helptext-1"
            >
              <option
                v-for="column in columns"
                :key="column.key"
                :value="column.key"
              >
                {{ column.label }}
              </option>
            </select>
          </div>
        </div>
        <div class="row">
          <table
            class="table table--condensed"
            aria-label="Samenvatting per informatietype"
          >
            <thead>
              <tr>
                <th class="u-columnwidth-50p">
                  <span>Waarde</span>
                </th>
                <th class="u-columnwidth-10p">
                  Aantal
                </th>
                <th class="u-columnwidth-10p borderless-left">
                  <span>Percentage</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in parsedCountData" :key="index">
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
import { getColumns, getCount } from '@/services/algorithms'
import { computed, ref, watch } from 'vue'
const props = defineProps<{
  nAlgorithms: number
}>()

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
  'standard_version',
]

const labelMap: { [key: string]: string } = {
  organization: 'Organisatie',
  department: 'Afdeling',
  type: 'Type algoritme',
  category: 'Beleidsterrein',
  status: 'Status',
  competent_authority: 'Bevoegde autoriteit',
  dpia: 'Data Protection Impact Assessment (DPIA)',
  iama: 'Impact Assessment Mensenrechten en Algoritmes (IAMA)',
  area: 'Geografisch gebied',
  lang: 'Taal',
  mprd: 'Koppelingen met basisregistraties',
  standard_version: 'Schema',
}

const columnApi = ref<any>()
const retrieveColumns = async () => {
  const result = await getColumns()
  columnApi.value = result.data
}
retrieveColumns()

const columns = computed(() => {
  if (columnApi.value) {
    return columnApi.value
      .filter((column: any) => {
        return interestingColumns.includes(column.column_name)
      })
      .map((column: any) => {
        return {
          key: column.column_name,
          label: labelMap[column.column_name],
        }
      })
  }
  return []
})

const countData =
  ref<Array<{ descriptor: string; count: string; fraction: number }>>()

const listValue = ref(interestingColumns[0])
const selectType = async () => {
  const response = await getCount(listValue.value || 'organisation')

  countData.value = response.data.map((data: any) => {
    const result = {
      descriptor: data.descriptor,
      count: data.count,
      fraction: Math.floor((data.count / props.nAlgorithms) * 100),
    }
    return result
  })
}

const parsedCountData = computed(() => {
  return countData.value?.map((data) => {
    const parsedValue = () => {
      if (data.descriptor === '' || data.descriptor === null) {
        return 'Veld niet ingevuld'
      } else if (typeof data.descriptor === 'boolean') {
        return data.descriptor === true ? 'Ja' : 'Nee'
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

<style scoped lang="scss">
.block-info {
  max-width: 100%;
}
.word-break {
  word-break: break-word;
}
.select-block {
  display: block;
}

.borderless-left {
  border-left: 0 !important;
}

.width-100 {
  width: 100%;
}
/* Style the select element to hide default dropdown arrow */
select {
  -webkit-appearance: none; /* For Safari */
  -moz-appearance: none; /* For Firefox */
  appearance: none; /* Standard */
  background-color: white;
  background-image: url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 5"><path fill="%23666" d="M0 0h4L2 5z"/></svg>');
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 10px;
  padding: 8px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Optional hover/focus effect */
select:hover,
select:focus {
  border-color: #888;
}
</style>
