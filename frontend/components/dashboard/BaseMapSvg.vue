<template>
  <div>
    <br />
    <button class="button-table" @click="showDatatable = !showDatatable">
      {{ buttonName }}
    </button>
    <br />
    <DashboardMapTable v-if="showDatatable" :data="mapData" />
    <br />
    <div v-show="!showDatatable" class="content-map">
      <div class="column-35 float-left">
        <br />
        <legend-table
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
import LegendTable from '@/components/dashboard/LegendTable.vue'
import { useGeotopLegendData } from '@/utils/legendData'
import type { DocumentCount, DataObject, GeoJson } from '@/services/aggregates'
import dashboardService from '@/services/dashboard'

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

const { t, n } = useI18n()
const emit = defineEmits(['numberOfOrganisations'])
const showDatatable = ref(true)
const legendData = useGeotopLegendData()
const mapData = ref<DocumentCount[]>([])
const buttonName = computed(() => {
  return showDatatable.value
    ? t('dashboard.showMap')
    : t('dashboard.showDatatable')
})
let svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>

const isMobile = ref(false)
const viewBoxX = ref('50 0 1020 420')

const updateIsMobile = () => {
  isMobile.value = window.innerWidth < 700
  updateViewBox()
}

const updateViewBox = () => {
  if (isMobile.value) {
    viewBoxX.value = '300 0 620 420'
  } else if (props.organisationType === 'environmentalService') {
    viewBoxX.value = '70 0 1020 420'
  } else {
    viewBoxX.value = '50 0 1020 420'
  }
  if (svg) {
    svg.attr('viewBox', viewBoxX.value)
  }
}

const fetchData = async () => {
  if (props.organisationType === 'municipality') {
    const response = await dashboardService.getMunicipalityData()
    mapData.value = response.data.value as DocumentCount[]
  } else if (props.organisationType === 'province') {
    const response = await dashboardService.getProvinceData()
    mapData.value = response.data.value as DocumentCount[]
  } else if (props.organisationType === 'waterAuthority') {
    const response = await dashboardService.getWaterAuthorityData()
    mapData.value = response.data.value as DocumentCount[]
  } else if (props.organisationType === 'environmentalService') {
    const response = await dashboardService.getEnvironmentalServiceData()
    mapData.value = response.data.value as DocumentCount[]
  }
  emit('numberOfOrganisations', mapData.value.length)
  createMap(props.organisationType || '', mapData.value)
}

function initToolTip() {
  const inverseScaleX =
    props.organisationType === 'environmentalService' ? 1 / 1.65 : 1
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
  d: FocusEvent,
  tooltip: d3.Selection<HTMLDivElement, any, HTMLElement, any>
): void {
  const target = d.target as any
  if (!target.__data__) {
    return
  }
  let htmlString =
    (target.__data__.properties.statnaam ||
      target.__data__.properties.waterschap ||
      target.__data__.properties.od_naam) + '</br><hr>'

  const classificationString = getClassificationString(
    target.__data__.properties.tooltips[0]
  )
  htmlString += classificationString + '</br></br>'

  if (target.__data__.properties.tooltips !== undefined) {
    target.__data__.properties.tooltips.sort().forEach((x: any) => {
      htmlString += x.key + ': ' + n(x.count) + '</br>'
    })
  }
  const leftpx =
    isMobile.value && props.organisationType === 'environmentalService'
      ? -80
      : isMobile.value
        ? -120
        : props.organisationType === 'environmentalService'
          ? 20
          : -70
  const toppx = isMobile.value ? -70 : 0

  tooltip
    .html(htmlString)
    .style('left', leftpx + 'px')
    .style('top', toppx + 'px')
    .attr('aria-live', 'assertive')
  const x = document.getElementById('ttcontainer-' + props.organisationType)!
  x.style.display = 'block'
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

function objectTypeOverlay(d: any, organisationData: DocumentCount[]): string {
  const code = d.properties.statcode || d.properties.od_code
  const dataObject = organisationData.find((x) => x.identifier === code)
  if (dataObject !== undefined) {
    d.properties.tooltips = [
      {
        key: t('dashboard.publishedAlgorithmDescriptions'),
        count: dataObject.number_of_algorithmdescriptions,
        showPage: dataObject.show_page,
        joined: dataObject.joined,
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
    .attr('stroke', 'black')
    .join('path')
    .attr('fill', (d: any) => {
      return overlayHandler(d, organisationData)
    })
  svg.on('mousemove touchstart focus', (d: FocusEvent) => {
    tooltipHandler(d, tooltip)
    const x = document.getElementById('ttcontainer-' + organisationType)!
    x.setAttribute('aria-hidden', 'false')
  })

  svg.on('mouseout touchend focusout', function () {
    const x = document.getElementById('ttcontainer-' + organisationType)!
    x.style.display = 'none'
  })
}

fetchData()

onMounted(() => {
  if (process.client) {
    isMobile.value = window.innerWidth < 700
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

.svg-content-responsive :deep(path:active),
.svg-content-responsive :deep(path:focus),
.svg-content-responsive :deep(path:hover) {
  stroke-width: 2;
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
  border: 1px solid #cccccc;
  font-size: 1rem;
  padding: 15px;
  pointer-events: none;
  position: absolute;
  max-width: 33%;
  margin-left: 120px;
  white-space: normal;
  word-wrap: break-word;
}

.column-35 {
  width: 35%;
  padding-right: 60px;
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
    padding-right: 0px;
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
