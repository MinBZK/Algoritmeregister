<template>
  <div class="item default">
    <p :lang="backendContentLanguage">
      <ClientOnly>
        <ParseUrl :key="algoritme.lars">
          <ListifyString :text="description"
        /></ParseUrl>
      </ClientOnly>
    </p>
    <dl class="dl columns--data">
      <div
        v-for="sT in cardGrouping?.subElements"
        :key="sT"
        :class="smallBreakpoint && 'column--fullwidth'"
      >
        <dt>
          {{ t(`algorithmProperties.${helpTextVersion}.${sT}.label`) }}
        </dt>
        <dd class="no-bottom-margin" :lang="backendContentLanguage">
          <ParseUrl :key="sT">
            <ListifyString
              :text="algoritme[sT as keyof Algoritme] || t('ontbreekt')"
            />
          </ParseUrl>
        </dd>
      </div>
    </dl>
  </div>
</template>

<script setup lang="ts">
import { backendContentLanguage, textVersionMapping } from '@/config/config'
import type { Algoritme } from '@/types/algoritme'
import type { headerCardGrouping } from '@/types/layout'

interface Props {
  algoritme: Algoritme
}

const props = defineProps<Props>()

const smallBreakpoint = useMobileBreakpoint().small

const { t } = useI18n()
const shortDescriptionMissing = computed(() => t('short-description-missing'))

const description =
  props.algoritme.description_short || shortDescriptionMissing.value

onMounted(() => {
  getGrouping(props.algoritme.standard_version)
})

const cardGrouping = ref<headerCardGrouping>()
const getGrouping = async (version: string) => {
  const layoutUrl = '/layouts/v' + version.replace(/\./g, '_') + '.json'
  const fetchResponse = await fetch(layoutUrl)
  const layout = await fetchResponse.json()
  cardGrouping.value = layout.headerCardGrouping
}

const helpTextVersion = computed(
  () => textVersionMapping[props.algoritme.standard_version]
)
</script>

<style scoped lang="scss">
.dl.columns--data div {
  padding: 0.5em;
}

.no-bottom-margin {
  margin-bottom: 0;
}

div.default {
  background: $tertiary !important;
  list-style: none;
  padding: 1em;
  margin-bottom: 0.5em;
  border: 0;
}

@media (min-width: 51em) {
  div.default {
    padding: 1.5em 10% !important;
  }
}

.column--fullwidth {
  width: 100% !important;
}
</style>
