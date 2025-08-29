<template>
  <div
    v-if="props.tooltipData"
    class="display-tooltip-data"
    :class="{ highlighted: highlightClass }"
  >
    <div :class="'color-box ' + props.tooltipData.classificationColour"></div>
    <b>{{ props.tooltipData.orgName }}</b>
    <br />
    {{ props.tooltipData.algoPublished }}
    <hr />
    <NuxtLink :to="props.tooltipData.orgPageUrl">{{
      props.tooltipData.orgPage
    }}</NuxtLink>
  </div>
  <div v-else class="display-tooltip-data">
    <div v-if="clickOnMessage">
      {{ clickOnMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ToolTipData } from '@/services/aggregates'
import { OrganisationTypes } from '@/services/aggregates'

const props = defineProps<{
  tooltipData?: ToolTipData | void
  organisationType: string
}>()
const { t } = useI18n()
const highlight = ref<boolean>(false)

const clickOnMessage = computed(() => {
  const messages = {
    [OrganisationTypes.Province]: 'dashboard.clickOnProvince',
    [OrganisationTypes.Municipality]: 'dashboard.clickOnMunicipality',
    [OrganisationTypes.WaterAuthority]: 'dashboard.clickOnWaterAuthority',
    [OrganisationTypes.EnvironmentalService]:
      'dashboard.clickOnEnvironmentalService',
    [OrganisationTypes.SafetyRegion]: 'dashboard.clickOnSafetyRegion',
  }
  return t(messages[props.organisationType as keyof typeof messages])
})

watch(
  () => props.tooltipData?.orgCode,
  (newData, oldData) => {
    if (newData && newData !== oldData) {
      highlight.value = true
      setTimeout(() => {
        highlight.value = false
      }, 500)
    }
  }
)
const highlightClass = computed(() => highlight.value)
</script>

<style scoped lang="scss">
.display-tooltip-data {
  background-color: white;
  border: 1px solid #e6e6e6;
  padding: 1em;
  margin-bottom: 1em;
  transition: box-shadow 0.5s ease-in-out;
}

.display-tooltip-data b {
  vertical-align: middle;
}

.legendgreen-background {
  background-color: rgba(85, 177, 165, 0.8);
}

.legendyellow-background {
  background-color: rgba(237, 208, 136, 0.8);
}

.legendwhite-background {
  background-color: rgba(255, 0, 0, 0);
}

.color-box {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 0.1rem solid grey;
  align-content: center;
  margin-right: 0.5rem;
  vertical-align: middle;
}

.highlighted {
  box-shadow: 0 0 20px rgba(85, 177, 165, 0.6);
}
</style>
