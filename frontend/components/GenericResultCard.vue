<template>
  <div class="card-content-flex">
    <div class="algorithm-main-content">
      <div
        ref="algorithmLink"
        class="item-header"
        :lang="backendContentLanguage"
      >
        <NuxtLink
          :to="localePath(`/algoritme/${algoritme.lars}`)"
          class="result--title focus-border"
        >
          <h2 v-if="!detailedAlgoPage">{{ algoritme.name }}</h2>
        </NuxtLink>
        <h2>{{ algoritme.organization }}</h2>
      </div>
      <p :lang="backendContentLanguage">
        <ParseUrl :key="algoritme.lars">
          <ListifyString :text="description"
        /></ParseUrl>
        <NuxtLink
          v-if="!detailedAlgoPage"
          :to="localePath(`/algoritme/${algoritme.lars}`)"
          >{{ readMore }}
        </NuxtLink>
      </p>
      <div class="read-more-text">
        <div class="font-size-08">
          {{ currentDate }} | {{ publicationStandardVersion }}
        </div>
      </div>
    </div>
    <div
      class="grouping-content-mobile"
      :class="!smallBreakpoint && 'grouping-content'"
    >
      <dl>
        <div
          v-for="sT in cardGrouping?.subElements"
          :key="sT"
          :class="smallBreakpoint && 'row--fullwidth'"
          class="add-padding-bottom"
        >
          <dt>
            {{ t(`algorithmProperties.${helpTextVersion}.${sT}.label`) }}
          </dt>
          <dd class="no-bottom-margin" :lang="backendContentLanguage">
            <DisplayImpacttoetsen
              v-if="sT === 'impacttoetsen_grouping'"
              :text="
                (algoritme[sT] as unknown as ListWithLinks) || t('ontbreekt')
              "
            ></DisplayImpacttoetsen>
            <ParseUrl v-else :key="sT">
              <ListifyString
                :text="algoritme[sT as keyof Algoritme] || t('ontbreekt')"
              />
            </ParseUrl>
          </dd>
        </div>
      </dl>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { AlgoritmeQuery } from '@/types/filter/algoritme'
import { backendContentLanguage, textVersionMapping } from '@/config/config'
import type { Algoritme } from '@/types/algoritme'
import type { genericCardGrouping, ListWithLinks } from '@/types/layout'

interface Props {
  algoritme: Algoritme
  setFocus?: boolean
  query?: AlgoritmeQuery
}

const props = withDefaults(defineProps<Props>(), {
  setFocus: false,
  query: undefined,
})

const emit = defineEmits<{
  (e: 'focusHasBeenSet'): void
}>()

const localePath = useLocalePath()
const smallBreakpoint = useMobileBreakpoint().small
const route = useRoute()
const { t } = useI18n()

const readMore = computed(() => t('genericResultCard.readMore'))
const shortDescriptionMissing = computed(() => t('short-description-missing'))
const publicationStandardVersion = computed(
  () =>
    t('genericResultCard.publicationStandard') +
    ' ' +
    props.algoritme.standard_version
)

const length = 300
const truncatedDescription = computed(() => {
  const truncatedString = (
    props.algoritme.description_short as string | null
  )?.substring(0, length)

  const markedString = props.query?.searchtext
    ? truncatedString?.replace(
        new RegExp(props.query.searchtext, 'gi'),
        (match: string) => `<mark>${match}</mark>`
      )
    : truncatedString
  return truncatedString === props.algoritme.description_short
    ? markedString
    : markedString + '...'
})

const detailedAlgoPage = computed(() => {
  const name = route.name
  if (typeof name === 'string') {
    return name.split('-').includes('slug')
  }
  return false
})
const description = computed(() => {
  return detailedAlgoPage.value
    ? props.algoritme.description_short
    : truncatedDescription.value || shortDescriptionMissing.value
})

const currentDate = computed(() => {
  let dateString = ''
  const dateToConvert = props.algoritme.create_dt
  if (typeof dateToConvert !== 'string') {
    return null
  }
  const date = new Date(dateToConvert)
  const month: string = t(`months.${date.getMonth() + 1}`)
  const monthDay: string = date.getDate().toString()
  const year: string = date.getFullYear().toString()
  const hours: string = date.getHours().toString()
  const minutes: string =
    date.getMinutes() < 10
      ? '0'.concat(date.getMinutes().toString())
      : date.getMinutes().toString()

  const isEnglish = t('english?') === 'true'
  if (isEnglish) {
    let monthDayOrdinal = ''
    if (['1', '21', '31'].includes(monthDay)) {
      monthDayOrdinal = 'st'
    } else if (['2', '22'].includes(monthDay)) {
      monthDayOrdinal = 'nd'
    } else if (['3', '23'].includes(monthDay)) {
      monthDayOrdinal = 'rd'
    } else {
      monthDayOrdinal = 'th'
    }
    dateString =
      monthDay +
      monthDayOrdinal +
      ' of ' +
      month +
      ' ' +
      year +
      ', at ' +
      hours +
      ':' +
      minutes +
      ' (CET)'
  } else if (!isEnglish) {
    dateString =
      monthDay + ' ' + month + ' ' + year + ' om ' + hours + ':' + minutes
  }
  return t('genericResultCard.lastChange') + ' ' + dateString
})

const algorithmLink = ref<HTMLAnchorElement>()

onMounted(() => {
  focusCardLink()
})

const cardGrouping = ref<genericCardGrouping>()
const getGrouping = (version: string) => {
  const layoutVersion = 'v' + version.replace(/\./g, '_')
  const layout = getLayoutConfig(layoutVersion)
  cardGrouping.value = layout.cardGrouping
}

getGrouping(props.algoritme.standard_version)

const focusCardLink = () => {
  if (algorithmLink.value?.firstChild && props.setFocus) {
    ;(algorithmLink.value.firstChild as HTMLElement)?.focus()
    emit('focusHasBeenSet')
  }
}

const helpTextVersion = computed(
  () => textVersionMapping[props.algoritme.standard_version]
)

const setFocusWatcher = computed(() => props.setFocus)
watch(setFocusWatcher, (newValue) => {
  if (newValue) {
    focusCardLink()
  }
})
</script>

<style scoped lang="scss">
h2 {
  font-size: 1.1em;
  margin-bottom: 0.2em;
}

h3 {
  font-size: 0.9em;
  margin-bottom: 0;
}
.add-padding-bottom {
  padding-bottom: 1em;
}

.item-header {
  margin-bottom: 0.2em;
}

.no-bottom-margin {
  margin-bottom: 0;
}

.read-more-text {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
  padding: 0.5em 0 0.5em 0;
}

.card-content-flex {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  height: 100%;
}

.grouping-content {
  flex: 1 0 30%;
  border-left: 1px solid lightgray;
  padding-left: 1.25em;
}

.grouping-content-mobile {
  flex: 1 0 12.5%;
  padding-left: 1.25em;
}

.algorithm-main-content {
  flex: 1 0 70%;
  padding-right: 1em;
  padding-left: 0.25em;
  display: flex;
  flex-direction: column;
}

.font-size-08 {
  font-size: 0.8em;
}
</style>
