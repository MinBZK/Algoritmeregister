<template>
  <div>
    <div class="row">
      <table v-if="useTableDataNatOrg">
        <thead>
          <tr>
            <th>
              <span>{{ columnName }}</span>
            </th>
            <th>
              {{ columnName2 }}
            </th>
            <th>
              {{ columnName3 }}
            </th>
            <th>
              {{ columnName4 }}
            </th>
            <th>
              {{ columnName5 }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in tableDataNatOrg" :key="row.name">
            <td class="word-break">
              {{ row.name }}
            </td>
            <td>
              <b>
                {{ row.Total }}
              </b>
            </td>
            <td>
              <b>
                {{ row.KD }}
              </b>
            </td>
            <td>
              <b>
                {{ row.Agentschap }}
              </b>
            </td>
            <td>
              <b>
                {{ row.Overig }}
              </b>
            </td>
          </tr>
        </tbody>
      </table>
      <table v-else class="dashboard-table">
        <thead>
          <tr>
            <th>
              <span>{{ columnName }}</span>
            </th>
            <th>
              {{ columnName2 }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in tableData" :key="displayNameOrCategory(row)">
            <td class="word-break">
              {{ displayNameOrCategory(row) }}
            </td>
            <td>
              <b>
                {{ row.count }}
              </b>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import dashboardService from '@/services/dashboard'
import type {
  OrganisationTop20,
  PublicationCategoriesCount,
  MonthlyCount,
  NationalOrganisationsCountDashboard,
} from '@/types/dashboard'
import type { LanguageCode } from '@/types/textLoader'

const props = withDefaults(
  defineProps<{
    index: number
  }>(),
  {
    index: 0,
    title: '',
  }
)
const emit = defineEmits(['count'])
const { t, locale } = useI18n()
const tableData = ref<
  (MonthlyCount | PublicationCategoriesCount | OrganisationTop20)[]
>([])
const tableDataNatOrg = ref<NationalOrganisationsCountDashboard[]>([])
const columnName = ref('' as string)
const columnName2 = ref('' as string)
const columnName3 = ref('' as string)
const columnName4 = ref('' as string)
const columnName5 = ref('' as string)

const useTableDataNatOrg = computed(() => {
  return tableDataNatOrg.value.length > 0
})

const fetchData = async () => {
  if (props.index === 0) {
    const { data } = await dashboardService.getJoinedOrg()
    columnName.value = t('dashboard.month')
    columnName2.value = t('dashboard.numberOfMatches')
    tableData.value = data.value as MonthlyCount[]
    emit('count', data.value?.[data.value.length - 1]?.count)
  }
  if (props.index === 1) {
    const { data } = await dashboardService.getPublishedAlg()
    columnName.value = t('dashboard.month')
    columnName2.value = t('dashboard.numberOfMatches')
    tableData.value = data.value as MonthlyCount[]
    emit('count', data.value?.[data.value.length - 1]?.count)
  }
  if (props.index === 2) {
    const { data } = await dashboardService.getPubCategories(
      mapLocaleName(locale.value as LanguageCode)
    )
    columnName.value = t('dashboard.publicationCategories')
    columnName2.value = t('dashboard.numberOfMatches')
    tableData.value = data.value as PublicationCategoriesCount[]
  }
  if (props.index === 3) {
    const { data } = await dashboardService.getNationalOrgs(
      mapLocaleName(locale.value as LanguageCode)
    )
    columnName2.value = t('dashboard.ministeryTotal')
    columnName3.value = t('dashboard.KD')
    columnName4.value = t('dashboard.AG')
    columnName5.value = t('dashboard.other')
    tableDataNatOrg.value = data.value as NationalOrganisationsCountDashboard[]
  }
}

function displayNameOrCategory(
  row: MonthlyCount | OrganisationTop20 | PublicationCategoriesCount
): string {
  if ('name' in row) {
    return row.name
  }
  if ('date' in row) {
    return row.date
  }
  if ('category' in row) {
    return row.category
  }
  return ''
}

await fetchData()
</script>

<style scoped lang="scss">
.word-break {
  word-break: break-word;
}

.dashboard-table {
  margin-top: 30px;
  min-width: auto;
  width: 30%;

  td,
  th {
    padding: 10px;
  }

  th:nth-child(2),
  td:nth-child(2) {
    width: 80px;
    text-align: right;
  }
}

@media (max-width: 1100px) {
  .dashboard-table {
    width: 100%;
  }
}

@media (max-width: 1000px) {
  .dashboard-map-table {
    min-width: 100% !important;

    td:first-child,
    th:first-child {
      width: 50% !important;
    }
  }
}

.row {
  overflow-x: auto;
  margin-bottom: 0em;
  td,
  th {
    padding: 10px;
  }
}

table {
  min-width: 600px;
  border-collapse: collapse;
  margin-bottom: 0em;
}

@media (max-width: 1000px) {
  .row {
    display: block;
    width: 100%;
  }
}
</style>
