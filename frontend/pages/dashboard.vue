<template>
  <div v-if="loading">{{ t('dashboard.loadingText') }}</div>
  <div v-else-if="errorMessage">{{ errorMessage }}</div>
  <div v-else>
    <h1>{{ t('dashboard.title') }}</h1>
    <p class="margin-bottom-none font-28px">
      {{ dateStamp }}
    </p>
    <p>{{ t('dashboard.moreInfo') }}</p>
    <button class="button" @click="toggleOverview()">
      {{
        isExpanded
          ? t('dashboard.collapseOverview')
          : t('dashboard.expandOverview')
      }}
    </button>

    <dashboard-tab
      v-for="(data, index) in dashboardData.slice(0, 2)"
      :key="data.title"
      v-model="data.show"
      :title="data.title"
      :count="data.count"
      :description="data.description"
      :icon="data.icon"
      @update:model-value="(value) => handleUpdate(value, data)"
    >
      <button
        v-show="data.show"
        class="button-table"
        @click="data.showTable = !data.showTable"
      >
        {{ displaybuttonName(data.showTable || false) }}
      </button>
      <br />
      <dashboard-table
        v-show="data.showTable"
        :index="index"
        @count="data.count = $event"
      />
      <div v-show="!data.showTable" v-html="data.graph" />
    </dashboard-tab>

    <div class="item-title">{{ t('dashboard.onTheMap') }}</div>

    <dashboard-tab
      v-for="data in dashboardMapData"
      :key="data.title"
      v-model="data.show"
      :title="data.title"
      :count="data.count"
      :description="data.description"
      :click-on="data.clickOn"
      :icon="data.icon"
      @update:model-value="checkIfExpanded()"
    >
      <dashboard-base-map-svg
        :organisation-type="data.organisationType"
        :geojson-file="data.geojsonFile"
        @number-of-organisations="data.count = $event"
      />
    </dashboard-tab>

    <div class="item-title">{{ t('dashboard.andFurther') }}</div>

    <dashboard-tab
      v-for="(data, index) in dashboardData.slice(2)"
      :key="data.title"
      v-model="data.show"
      :title="data.title"
      :count="data.count"
      :description="data.description"
      :icon="data.icon"
      @update:model-value="(value) => handleUpdate(value, data)"
    >
      <button
        v-show="index == 0 && data.show"
        class="button-table"
        @click="data.showTable = !data.showTable"
      >
        {{ displaybuttonName(data.showTable || false) }}
      </button>
      <br />
      <dashboard-table v-show="data.showTable" :index="index + 2" />
      <div v-show="!data.showTable" v-html="data.graph" />
    </dashboard-tab>
  </div>
</template>

<script setup lang="ts">
import iconChart from '@/assets/images/icons/timeline_24dp.svg'
import iconMap from '@/assets/images/icons/icon-maps.svg'
import iconBarChart from '@/assets/images/icons/icon-bar-chart.svg'
import algoritmeService from '@/services/dashboard'
import type { DashboardItem, DashboardMap } from '@/types/dashboard'

const { t, locale } = useI18n()
const loading = ref<boolean>(false)
const isExpanded = ref<boolean>(true)
const dateStamp = ref<string>()
const errorMessage = ref<string>()
const dashboardData = ref<DashboardItem[]>([]) as Ref<DashboardItem[]>
const dashboardMapData = ref<DashboardMap[]>([]) as Ref<DashboardMap[]>

const isDashboardItem = (data: any): data is DashboardItem => {
  return (data as DashboardItem).showTable !== undefined
}

const checkIfExpanded = () => {
  let atLeastOne = false
  for (const item in dashboardData.value) {
    if (dashboardData.value[item].show) {
      atLeastOne = true
    }
  }
  for (const item in dashboardMapData.value) {
    if (dashboardMapData.value[item].show) {
      atLeastOne = true
    }
  }
  if (atLeastOne) {
    isExpanded.value = true
  } else {
    isExpanded.value = false
  }
}

const handleUpdate = (value: boolean, data: DashboardItem) => {
  if (!data.show && isDashboardItem(data)) {
    data.showTable = value
  }
  checkIfExpanded()
}

const displaybuttonName = (showTable: boolean) => {
  if (showTable) {
    return t('dashboard.showGraph')
  } else {
    return t('dashboard.showDatatable')
  }
}

const formatDate = (date: string) => {
  const weekDay = date.split(' ')[0]
  const day = date.split(' ')[1]
  const month = date.split(' ')[2]
  const year = date.split(' ')[3]
  let formattedDate = ''
  if (locale.value === 'en') {
    formattedDate =
      t(`weekDays.${weekDay}`) +
      ' ' +
      t(`months.${month}`) +
      ' ' +
      day +
      ' ' +
      year
  } else {
    formattedDate =
      t(`weekDays.${weekDay}`).charAt(0).toUpperCase() +
      t(`weekDays.${weekDay}`).slice(1) +
      ' ' +
      day +
      ' ' +
      t(`months.${month}`) +
      ' ' +
      year
  }
  return formattedDate
}

const toggleOverview = () => {
  for (const item in dashboardData.value) {
    dashboardData.value[item].show = !isExpanded.value
    dashboardData.value[item].showTable = false
  }
  for (const item in dashboardMapData.value) {
    dashboardMapData.value[item].show = !isExpanded.value
  }
  isExpanded.value = !isExpanded.value
}

const fetchHtmlFigures = async () => {
  loading.value = true
  await algoritmeService
    .getHtmlFiguresRecent()
    .then((response) => {
      if (response.data.value) {
        const htmlFigures = response.data.value
        dateStamp.value = formatDate(htmlFigures.static_data['date_stamp'])

        const AddItemToDashboard = (
          title: string,
          description: string,
          graphKey: string | undefined,
          icon: string
        ) => {
          const item: DashboardItem = {
            show: true,
            title,
            description,
            showTable: true,
            ...(graphKey !== undefined && {
              graph: htmlFigures.static[graphKey + locale.value],
            }),
            icon,
          }
          dashboardData.value.push(item)
        }

        const AddMapToDashboard = (
          organisationType: string,
          title: string,
          description: string,
          clickOn: string,
          geojsonFile: string
        ) => {
          const item: DashboardMap = {
            show: true,
            organisationType,
            title,
            count: 0,
            description,
            clickOn,
            icon: iconMap,
            geojsonFile,
          }
          dashboardMapData.value.push(item)
        }

        const dashboardDataToAdd = [
          {
            title: t('dashboard.totalJoinedOrganisations'),
            description: t('dashboard.joinedOrganisationsDescription'),
            graphKey: 'graph-joined-organisations-',
            icon: iconChart,
          },
          {
            title: t('dashboard.totalPublishedAlgorithmDescriptions'),
            description: t('dashboard.publishedAlgorithmDescription'),
            graphKey: 'graph-published-algorithmdescriptions-',
            icon: iconChart,
          },
          {
            title: t('dashboard.publicationCategories'),
            description: t('dashboard.publicationCategoriesDescription'),
            graphKey: 'graph-publication-categories-',
            icon: iconBarChart,
          },
        ]

        const dashboardMapDataToAdd = [
          {
            organisationType: 'municipality',
            title: t('dashboard.municipalities'),
            description: t('dashboard.municipalityMapDescription'),
            clickOn: t('dashboard.clickOnMunicipality'),
            geojsonFile: 'gemeentegrenzen.json',
          },
          {
            organisationType: 'province',
            title: t('dashboard.provinces'),
            description: t('dashboard.provinceMapDescription'),
            clickOn: t('dashboard.clickOnProvince'),
            geojsonFile: 'provinciegrenzen.json',
          },
          {
            organisationType: 'waterAuthority',
            title: t('dashboard.waterAuthorities'),
            description: t('dashboard.waterAuthoritiesMapDescription'),
            clickOn: t('dashboard.clickOnWaterAuthority'),
            geojsonFile: 'waterschapsgrenzen.json',
          },
          {
            organisationType: 'environmentalService',
            title: t('dashboard.environmentalServices'),
            description: t('dashboard.environmentalServicesMapDescription'),
            clickOn: t('dashboard.clickOnEnvironmentalService'),
            geojsonFile: 'omgevingsdienstgrenzen.json',
          },
        ]

        for (const item of dashboardDataToAdd) {
          AddItemToDashboard(
            item.title,
            item.description,
            item.graphKey,
            item.icon
          )
        }

        for (const item of dashboardMapDataToAdd) {
          AddMapToDashboard(
            item.organisationType,
            item.title,
            item.description,
            item.clickOn,
            item.geojsonFile
          )
        }
      }
      loading.value = false
    })
    .catch((error) => {
      errorMessage.value = error.message
    })
}
await fetchHtmlFigures()

onMounted(() => {
  toggleOverview()
})
</script>

<style scoped lang="scss">
.margin-bottom-none {
  margin-bottom: 0;
}

.font-28px {
  font-size: 28px;
}

.item-title {
  font-weight: bold;
  margin-top: 20px;
}

:deep(.button-table),
.button-overview {
  all: unset;
  cursor: pointer;
  border-radius: 4px;
  height: 38px;
  padding: 1px 10px;
  font-size: 14px;
  align-content: center;
  text-align: center;
  box-shadow: none !important;
}

:deep(.button-table) {
  color: white;
  float: right;
  background-color: #154273;
}

@media (min-width: 1100px) {
  :deep(.base-map-button) {
    width: 33.5%;
    float: left;
  }
}

.button-overview {
  border: 1px solid #154273;
  font-weight: bold;
  color: #154273;
  margin: 10px 0;
}

@media (max-width: 768px) {
  .button {
    width: 100%;
    box-sizing: inherit;
  }
}
</style>
