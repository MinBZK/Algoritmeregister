<template>
  <div>
    <div class="row">
      <table class="dashboard-map-table">
        <thead>
          <tr>
            <th>
              <span>{{ t('dashboard.name') }}</span>
            </th>
            <th>
              {{ t('dashboard.indication') }}
            </th>
            <th>
              {{ t('dashboard.numberOfMatches') }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in tableData" :key="row.name">
            <td class="word-break">
              {{ row.name }}
            </td>
            <td>
              {{ displayIndication(row) }}
            </td>
            <td>
              <b>
                {{ row.number_of_algorithmdescriptions }}
              </b>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DocumentCount } from '@/services/aggregates'

const props = defineProps({
  data: {
    type: Array as PropType<DocumentCount[]>,
    default: () => [],
  },
})

const { t } = useI18n()
const tableData = ref<DocumentCount[]>(props.data)

function displayIndication(row: DocumentCount) {
  if (row.number_of_algorithmdescriptions > 0 || row.show_page) {
    return t('dashboard.legendGreen')
  } else if (row.number_of_algorithmdescriptions === 0 && row.joined) {
    return t('dashboard.legendYellow')
  } else {
    return t('dashboard.legendWhite')
  }
}
</script>

<style scoped lang="scss">
.word-break {
  word-break: break-word;
}

.dashboard-map-table {
  margin-top: 30px;
  min-width: auto;
  width: 65%;

  td,
  th {
    padding: 10px;
  }

  th:nth-child(2),
  td:nth-child(2) {
    width: 50%;
  }
  th:nth-child(3),
  td:nth-child(3) {
    width: 80px;
    text-align: right;
  }
}

@media (max-width: 1000px) {
  .dashboard-map-table {
    width: 100%;

    th:nth-child(2),
    td:nth-child(2) {
      width: auto !important;
    }
  }
}
</style>
