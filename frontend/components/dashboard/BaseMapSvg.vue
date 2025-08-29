<template>
  <div>
    <br />
    <button
      class="button-table base-map-button"
      @click="showDatatable = !showDatatable"
    >
      {{ buttonName }}
    </button>
    <br />
    <br />
    <dashboard-map-table v-if="showDatatable" :data="mapData" />
    <br />
    <div v-show="!showDatatable" class="content-map">
      <div class="column-35 float-left">
        <dashboard-tool-tip-map-svg
          v-if="isLargeScreen"
          :tooltip-data="tooltipData"
          :organisation-type="organisationType"
        />
        <br />
        <dashboard-legend-table
          :data="legendData"
          :legend-id="organisationType + '-legenda'"
        />
      </div>
      <div class="column-65 float-right">
        <div
          :class="[
            'svg-container',
            {
              transform: organisationType !== 'environmentalService',
              'transfor-environservice':
                organisationType === 'environmentalService',
            },
          ]"
        >
          <svg :id="'organisationmap-' + organisationType"></svg>
          <div
            :id="'ttcontainer-' + organisationType"
            class="tooltip-container"
            style="display: none"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as d3 from 'd3'
import { useGeotopLegendData } from '@/utils/legendData'
import type {
  DocumentCount,
  DataObject,
  GeoJson,
  ToolTipData,
} from '@/services/aggregates'
import dashboardService from '@/services/dashboard'
import { OrganisationTypes } from '@/services/aggregates'

const props = withDefaults(
  defineProps<{
    organisationType: string
    geojsonFile: string
  }>(),
  {
    organisationType: '',
    geojsonFile: '',
  }
)

const { t } = useI18n()

const emit = defineEmits(['numberOfOrganisations'])
const showDatatable = ref<boolean>(true)
const legendData = useGeotopLegendData()
const mapData = ref<DocumentCount[]>([])
const tooltipData = ref<ToolTipData | void>()
const buttonName = computed(() => {
  return showDatatable.value
    ? t('dashboard.showMap')
    : t('dashboard.showDatatable')
})
let svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>
const isMobile = ref<boolean>(false)
const isLargeScreen = ref<boolean>()
const viewBoxX = ref<string>('50 0 1020 420')

const updateIsMobile = () => {
  isMobile.value = window.innerWidth < 700
  isLargeScreen.value = window.innerWidth > 1100
  updateViewBox()
}

const updateViewBox = () => {
  if (isMobile.value) {
    viewBoxX.value = '300 0 620 420'
  } else if (
    props.organisationType === OrganisationTypes.EnvironmentalService
  ) {
    viewBoxX.value = '70 0 1020 420'
  } else {
    viewBoxX.value = '50 0 1020 420'
  }
  if (svg) {
    svg.attr('viewBox', viewBoxX.value)
  }
}

const fetchData = async () => {
  if (props.organisationType === OrganisationTypes.Municipality) {
    const response = await dashboardService.getMunicipalityData()
    mapData.value = response.data.value as DocumentCount[]
  } else if (props.organisationType === OrganisationTypes.Province) {
    const response = await dashboardService.getProvinceData()
    mapData.value = response.data.value as DocumentCount[]
  } else if (props.organisationType === OrganisationTypes.WaterAuthority) {
    const response = await dashboardService.getWaterAuthorityData()
    mapData.value = response.data.value as DocumentCount[]
  } else if (
    props.organisationType === OrganisationTypes.EnvironmentalService
  ) {
    const response = await dashboardService.getEnvironmentalServiceData()
    mapData.value = response.data.value as DocumentCount[]
  } else if (props.organisationType === OrganisationTypes.SafetyRegion) {
    const response = await dashboardService.getSafetyData()
    mapData.value = response.data.value as DocumentCount[]
  }
  emit('numberOfOrganisations', mapData.value.length)
  createMap(props.organisationType || '', mapData.value)
}

function initToolTip() {
  const inverseScaleX =
    props.organisationType === OrganisationTypes.EnvironmentalService
      ? 1 / 1.65
      : 1
  const inverseScaleY = 1 / 1.7
  return d3
    .select('#ttcontainer-' + props.organisationType)
    .append('div')
    .attr('class', 'tooltip')
    .style('transform', `scale(${inverseScaleX}, ${inverseScaleY})`)
}

function initSvg() {
  return d3
    .select('#organisationmap-' + props.organisationType)
    .attr('preserveAspectRatio', 'xMidYMin meet')
    .attr('viewBox', viewBoxX.value)
    .classed('svg-content-responsive', true)
    .attr('aria-label', props.organisationType + ' kaart ')
}

function initPath(data: any) {
  const projection = d3
    .geoIdentity()
    .reflectY(true)
    .reflectX(false)
    .fitSize([1200, 420], data)
  return d3.geoPath(projection)
}

function tooltipHandler(
  d: MouseEvent,
  tooltip: d3.Selection<HTMLDivElement, any, HTMLElement, any>
): ToolTipData | void {
  const target = d.target as any
  if (!target.__data__) {
    return
  }
  const tooltipId = 'ttcontainer-' + props.organisationType
  const closeButtonId = 'close-btn-' + props.organisationType
  const localePath = useLocalePath()
  const orgCode = getOrgCode(target.__data__.properties.tooltips[0])
  const orgId = getOrgId(target.__data__.properties.tooltips[0])
  const isJoined = getJoined(target.__data__.properties.tooltips[0])
  const algoCount = getAlgoCount(target.__data__.properties.tooltips[0])
  const isOrgInfoPage = getOrgInfoPage(target.__data__.properties.tooltips[0])
  const algoKey = getAlgoKey(target.__data__.properties.tooltips[0])

  const orgPageUrl =
    (isJoined && algoCount >= 1) || isOrgInfoPage
      ? localePath('organisatie') + '/' + orgId
      : isJoined
        ? localePath('/map/organisatie-niet-gepubliceerd')
        : localePath('/map/organisatie-niet-aangesloten')

  const orgName =
    target.__data__.properties.statnaam ||
    target.__data__.properties.waterschap ||
    target.__data__.properties.od_naam

  const orgPage =
    !isJoined || algoCount < 1
      ? t('dashboard.moreInfoOrgPage')
      : t('dashboard.seeOrgPage')

  const classificationString = getClassificationString(
    target.__data__.properties.tooltips[0]
  )
  const classificationColour = getColourByTitle(classificationString)
  const colorBox = `<div class="color-box ${classificationColour}" ></div>`
  const algoPublished = algoCount >= 1 ? algoKey : t('dashboard.noPublications')

  let htmlString = '<b>' + orgName + '</b>'
  htmlString = isMobile.value
    ? colorBox +
      htmlString +
      '<hr>' +
      algoPublished +
      `<button id="${closeButtonId}" class="tooltip-close-btn">&times;</button>`
    : colorBox + htmlString + '</br>'

  const leftpx =
    isMobile.value &&
    props.organisationType === OrganisationTypes.EnvironmentalService
      ? -15
      : isMobile.value
        ? -120
        : props.organisationType === OrganisationTypes.EnvironmentalService
          ? 150
          : 60
  const toppx = isMobile.value ? -40 : -12

  tooltip
    .html(htmlString)
    .style('left', leftpx + 'px')
    .style('top', toppx + 'px')
    .attr('aria-live', 'assertive')
  const x = document.getElementById(tooltipId)!
  x.style.display = 'block'

  const closeButton = document.getElementById(closeButtonId)
  closeButton?.addEventListener('click', () => hideTooltip(tooltipId))

  const tooltipData: ToolTipData = {
    orgName,
    algoCount,
    orgPage,
    orgPageUrl,
    classificationColour,
    orgCode,
    joined: isJoined,
    algoKey,
    algoPublished,
    orgId,
  }
  return tooltipData
}

function hideTooltip(tooltipId: string) {
  const tooltip = d3.select('#' + tooltipId)
  tooltip.style('display', 'none')
  const x = document.getElementById(tooltipId)!
  if (x) {
    x.style.display = 'none'
  }
}

function getClassificationString(dataObject: DataObject): string {
  if (dataObject.count > 0 || dataObject.showPage) {
    return t('dashboard.legendGreen')
  } else if (dataObject.count === 0 && dataObject.joined) {
    return t('dashboard.legendYellow')
  } else {
    return t('dashboard.legendWhite')
  }
}

function getOrgCode(dataObject: DataObject): string {
  return dataObject.code
}

function getJoined(dataObject: DataObject): boolean {
  return dataObject.joined
}

function getAlgoCount(dataObject: DataObject): number {
  return dataObject.count
}

function getOrgInfoPage(dataObject: DataObject): boolean {
  return dataObject.showPage
}

function getAlgoKey(dataObject: DataObject): string {
  return dataObject.key
}

function getOrgId(dataObject: DataObject): string {
  return dataObject.orgId
}

function getColourByTitle(title: string): string | undefined {
  const result = legendData.find((item) => item.title === title)
  return result ? result.className : undefined
}

function objectTypeOverlay(d: any, organisationData: DocumentCount[]): string {
  const code = d.properties.statcode || d.properties.od_code
  const dataObject = organisationData.find((x) => x.identifier === code)
  if (dataObject !== undefined) {
    d.properties.tooltips = [
      {
        key:
          dataObject.number_of_algorithmdescriptions === 1
            ? t('dashboard.singlePublishedAlgorithmDescription', {
                n: dataObject.number_of_algorithmdescriptions,
              })
            : t('dashboard.publishedAlgorithmDescriptions', {
                n: dataObject.number_of_algorithmdescriptions,
              }),
        count: dataObject.number_of_algorithmdescriptions,
        showPage: dataObject.show_page,
        joined: dataObject.joined,
        identifier: dataObject.identifier,
        code: dataObject.code,
        orgId: dataObject.org_id,
      },
    ]
    if (
      dataObject.number_of_algorithmdescriptions > 0 ||
      dataObject.show_page
    ) {
      return 'rgb(85, 177, 165)'
    } else if (
      dataObject.number_of_algorithmdescriptions === 0 &&
      dataObject.joined
    ) {
      return 'rgb(237, 208, 136)'
    }
  }
  return 'rgb(255, 255, 255)'
}
async function createMap(
  organisationType: string,
  organisationData: DocumentCount[]
): Promise<void> {
  const overlayHandler = objectTypeOverlay
  const tooltip = initToolTip()
  const svg = initSvg()
  let path: d3.GeoPath<any, d3.GeoPermissibleObjects> = d3.geoPath()
  let rawFeatures: GeoJson['features'] = []

  const GeoJSONUrl = new URL(
    `../../static/geojson/${props.geojsonFile}`,
    import.meta.url
  ).href
  const { data } = await useFetch(GeoJSONUrl)
  const GeoJSON = data.value as GeoJson

  path = initPath(GeoJSON)
  rawFeatures = GeoJSON.features

  svg
    .selectAll('path')
    .data(rawFeatures)
    .enter()
    .append('path')
    .attr('id', (d: any) => {
      return (
        organisationType + '-' + d.properties.statnaam ||
        d.properties.waterschap ||
        d.properties.od_naam
      )
    })
    .attr('d', (d: any) => path(d))
    .attr('stroke', 'grey')
    .join('path')
    .attr('fill', (d: any) => {
      return overlayHandler(d, organisationData)
    })

  let isAreaClicked = false

  svg
    .selectAll('path')
    .on('click', function (event: MouseEvent) {
      tooltipData.value = tooltipHandler(event, tooltip)
      const x = document.getElementById('ttcontainer-' + organisationType)!
      x.setAttribute('aria-hidden', window.innerWidth > 1100 ? 'true' : 'false')
      x.style.display = 'block'
      isAreaClicked = true
    })
    .on('mouseover', function (event: MouseEvent) {
      if (!isAreaClicked) {
        tooltipHandler(event, tooltip)
        const x = document.getElementById('ttcontainer-' + organisationType)!
        x.style.display = 'block'
        x.setAttribute('aria-hidden', 'false')
      }
    })
    .on('mouseout', function () {
      if (!isAreaClicked) {
        hideTooltip('ttcontainer-' + organisationType)
      }
      isAreaClicked = false
    })
  svg.on('touchend focusout', function () {
    hideTooltip('ttcontainer-' + organisationType)
    isAreaClicked = false
  })
}

fetchData()

onMounted(() => {
  if (process.client) {
    isMobile.value = window.innerWidth < 700
    isLargeScreen.value = window.innerWidth > 1100
    window.addEventListener('resize', updateIsMobile)
    updateViewBox()
  }
  svg = d3
    .select('#organisationmap-' + props.organisationType)
    .attr('viewBox', viewBoxX.value)
  showDatatable.value = false
})
</script>

<style scoped>
.hidden-tooltip {
  display: none;
}

.tooltip-container :deep(.tooltip-close-btn) {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: transparent;
  border: none;
  color: red;
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
}

.tooltip-container :deep(.tooltip-close-btn:hover) {
  color: darkred;
}

.transform {
  transform: scaleY(1.7);
}

.transfor-environservice {
  transform: scaleX(1.65) scaleY(1.7);
}

.svg-content-responsive {
  display: inline-block;
  position: absolute;
  top: 10px;
  left: 0;
  box-sizing: initial;
  stroke-width: 0.7;
  outline: none;
  box-shadow: none !important;
}

@media (max-width: 768px) {
  .svg-content-responsive {
    top: 40px;
  }
}

.svg-content-responsive :deep(path:active),
.svg-content-responsive :deep(path:focus),
.svg-content-responsive :deep(path:hover) {
  stroke-width: 2;
  cursor: pointer;
  stroke: rgb(127, 86, 217);
}

.svg-container {
  display: inline-block;
  position: relative;
  width: 100%;
  vertical-align: top;
  outline: none;
}

.tooltip-container :deep(.tooltip) {
  background-color: white;
  border: 1px solid #e6e6e6;
  font-size: 1rem;
  padding: 18px;
  pointer-events: auto;
  position: absolute;
  max-width: 100%;
  margin-left: 120px;
  white-space: normal;
  word-wrap: break-word;
  hyphens: auto;
  transform-origin: left center;
}

.tooltip-container :deep(.tooltip a) {
  pointer-events: auto;
  color: blue;
  text-decoration: underline;
}

.tooltip-container :deep(.color-box) {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 0.1rem solid grey;
  align-content: center;
  margin-right: 0.5rem;
  vertical-align: middle;
}

.tooltip-container :deep(.legendgreen-background) {
  background-color: rgba(85, 177, 165, 0.8);
}

.tooltip-container :deep(.legendyellow-background) {
  background-color: rgba(237, 208, 136, 0.8);
}

.tooltip-container :deep(.legendwhite-background) {
  background-color: rgba(255, 0, 0, 0);
}

.column-35 {
  width: 35%;
  flex: 1;
  height: 50px !important;
}

.column-65 {
  width: 65%;
  flex: 1;
  height: 650px;
}

.float-left {
  float: left;
}

.float-right {
  float: right;
}

.content-map {
  height: 650px;
}

@media (max-width: 1100px) {
  .float-left,
  .float-right {
    float: none;
  }

  .column-35 {
    order: 2;
    width: 60%;
  }

  .column-65 {
    min-height: 750px;
    order: 1;
    width: 100%;
  }

  .content-map {
    display: flex;
    flex-direction: column;
    height: auto;
  }

  .tooltip-container :deep(.tooltip) {
    position: absolute;
    margin-left: 120px;
    max-width: none;
  }
}

@media (max-width: 900px) {
  .column-65 {
    min-height: 600px;
  }
}

@media (max-width: 800px) {
  .column-65 {
    min-height: 550px;
  }
}

@media (max-width: 700px) {
  .column-35 {
    width: 100%;
  }

  .column-65 {
    min-height: 800px;
  }
}

@media (max-width: 600px) {
  .column-65 {
    min-height: 650px;
  }
}

@media (max-width: 500px) {
  .column-65 {
    min-height: 550px;
  }
}

@media (max-width: 400px) {
  .column-65 {
    min-height: 450px;
  }
}
</style>
