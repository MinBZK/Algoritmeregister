<template>
  <div>
    <div class="block-info">
      <div class="rows">
        <h3>Mate van compleetheid</h3>
        <div class="row">
          <div v-if="loading" class="loading-text">
            Aan het laden...
          </div>
          <table
            class="table table--condensed"
            aria-label="Mate van compleetheid"
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
              <tr v-for="agg in aggregates" :key="agg.label">
                <td>{{ agg.label }}</td>
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
import { getColumns, getCountWithFilledColumns } from '@/services/algorithms'
import { onMounted, ref } from 'vue'

const props = defineProps<{
  nAlgorithms: number
}>()

const aggregates = ref<{ label: string; value: string; fraction: number }[]>([])
const loading = ref(true)

const getFullyComplete = async () => {
  const result = await getCountWithFilledColumns('*')
  return result.data
}

const setAggregates = async () => {
  const nFullyComplete = await getFullyComplete()
  aggregates.value = [
    {
      label: 'Alle velden ingevuld',
      value: nFullyComplete,
      fraction: Math.floor((nFullyComplete / props.nAlgorithms) * 100),
    },
    {
      label: 'Gedeeltelijk ingevuld',
      value: props.nAlgorithms - nFullyComplete,
      fraction: Math.floor(
        ((props.nAlgorithms - nFullyComplete) / props.nAlgorithms) * 100
      ),
    },
  ]
  loading.value = false
}

onMounted(async () => {
  await getColumns()
  await setAggregates()
})
</script>

<style scoped lang="scss">
.block-info {
  max-width: 100%;
}
.word-break {
  word-break: break-word;
}
.loading-text {
  text-align: center;
}
</style>
