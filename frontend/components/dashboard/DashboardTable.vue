<template>
  <div>
    <div class="row">
      <table class="dashboard-table">
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
const columnName = ref('' as string)
const columnName2 = ref('' as string)

const fetchData = async () => {
  if (props.index === 0) {
    const { data } = await dashboardService.getJoinedOrg()
    columnName.value = t('dashboard.month')
    tableData.value = data.value as MonthlyCount[]
    emit('count', data.value?.[data.value.length - 1]?.count)
  }
  if (props.index === 1) {
    const { data } = await dashboardService.getPublishedAlg()
    columnName.value = t('dashboard.month')
    tableData.value = data.value as MonthlyCount[]
    emit('count', data.value?.[data.value.length - 1]?.count)
  }
  if (props.index === 2) {
    const { data } = await dashboardService.getPubCategories(
      mapLocaleName(locale.value as LanguageCode)
    )
    columnName.value = t('dashboard.publicationCategories')
    tableData.value = data.value as PublicationCategoriesCount[]
  }
  if (props.index === 3) {
    const { data } = await dashboardService.getOrgTop20(
      mapLocaleName(locale.value as LanguageCode)
    )
    columnName.value = t('organisation')
    tableData.value = data.value as OrganisationTop20[]
  }
  columnName2.value = t('dashboard.numberOfMatches')
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
</style>
