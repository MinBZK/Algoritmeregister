<template>
  <div>
    <h1 class="text-h4 mb-3 mt-0">
      Dashboard
    </h1>
    <h1 class="text-h5 mb-3 mt-0">
      {{ formatDate(date) }}
    </h1>
  </div>
  <BrokenLinksTable />
  <div class="block-cards">
    <CountPerType class="block-cards__card" :n-algorithms="algoCount!" />
    <br>
    <DataCompleteness class="block-cards__card" :n-algorithms="algoCount!" />
  </div>
</template>

<script setup lang="ts">
import BrokenLinksTable from '@/components/dashboard/BrokenLinksTable.vue'
import CountPerType from '@/components/dashboard/CountPerType.vue'
import DataCompleteness from '@/components/dashboard/DataCompleteness.vue'
import { formatDate } from '@/utils/datetime'
import { getTotalCount } from '@/services/algorithms'
import { ref } from 'vue'

const date = new Date()

const algoCount = ref<number>()
const retrieveTotalCount = async () => {
  const result = await getTotalCount()
  algoCount.value = result.data
}
retrieveTotalCount()
</script>

<style scoped lang="scss">
@media (min-width: 85em) {
  .block-cards__card:first-child {
    padding-right: 2em !important;
  }
  .block-cards__card {
    width: 50% !important;
    height: 100%;
  }
}
.block-cards__card {
  width: 100%;
  margin-bottom: 0em;
  padding-bottom: 1em;
}
.block-cards {
  padding-top: 2em;
}

h2 {
  font-size: 1.4rem !important;
  margin-bottom: 0.2em;
}
h1 {
  margin-bottom: 0.4em;
}
</style>
