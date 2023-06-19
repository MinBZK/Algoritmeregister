<template>
  <div :class="`item ${mode}`">
    <div
      v-if="mode === 'compact'"
      ref="algorithmLink"
      class="item-header"
      :lang="backendContentLanguage"
    >
      <NuxtLink
        :to="localePath(`/algoritme/${algoritme.lars}`)"
        class="result--title focus-border"
      >
        <h2>{{ algoritme.name }}</h2>
      </NuxtLink>
    </div>

    <p :lang="backendContentLanguage">
      <ParseUrl :key="algoritme.lars"> {{ description }}</ParseUrl
      >&nbsp;
      <NuxtLink
        v-if="isTruncated && mode === 'compact'"
        :to="localePath(`/algoritme/${algoritme.lars}`)"
        >{{ readMore }}
      </NuxtLink>
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
    <div v-if="mode === 'compact'" class="read-more-text">
      <b>
        <NuxtLink
          v-if="mode === 'compact'"
          :to="localePath(`/algoritme/${algoritme.lars}`)"
          >{{ readMore }}
        </NuxtLink>
      </b>
    </div>
  </div>
</template>

<script setup lang="ts">
import { backendContentLanguage, textVersionMapping } from '@/config/config'
import type { Algoritme } from '@/types/algoritme'
import type { headerCardGrouping } from '@/types/layout'

interface Props {
  algoritme: Algoritme
  mode?: 'compact' | 'default'
  setFocus?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  mode: 'default',
  setFocus: false,
})

const emit = defineEmits<{
  (e: 'focusHasBeenSet'): void
}>()

const localePath = useLocalePath()

const smallBreakpoint = useMobileBreakpoint().small

const { t } = useI18n()
const readMore = computed(() => t('searchResultCard.readMore'))
const shortDescriptionMissing = computed(() => t('short-description-missing'))

const length = 300
const truncatedDescription = computed(() => {
  const truncatedString = (
    props.algoritme.description_short as string | null
  )?.substring(0, length)
  return truncatedString === props.algoritme.description_short
    ? props.algoritme.description_short
    : truncatedString + '...'
})

const description =
  props.mode === 'compact'
    ? truncatedDescription
    : props.algoritme.description_short || shortDescriptionMissing

const isTruncated = computed(() => {
  return (
    truncatedDescription.value !==
    (props.algoritme.description_short as string | null)?.substring(0, length)
  )
})

const algorithmLink = ref<HTMLAnchorElement>()

onMounted(() => {
  focusCardLink()
  getGrouping(props.algoritme.standard_version)
})

const cardGrouping = ref<headerCardGrouping>()
const getGrouping = async (version: string) => {
  const layoutUrl = '/layouts/v' + version.replace(/\./g, '_') + '.json'
  const fetchResponse = await fetch(layoutUrl)
  const layout = await fetchResponse.json()
  cardGrouping.value = layout.headerCardGrouping
}

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
  margin-bottom: 0;
}

.item-header {
  margin-bottom: 0.2em;
}

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

div.compact {
  background: #fff;
  list-style: none;
  padding: 1em;
  margin-bottom: 0.5em;
  border: 0;
}

@media (min-width: 51em) {
  div.compact {
    padding: 1.75em 1.25em 1.5em 2em !important;
  }
}

.read-more-text {
  text-align: right;
  padding-right: 0.75em;
}
</style>
