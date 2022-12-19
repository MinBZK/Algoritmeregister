<template>
  <li :class="`item ${mode}`">
    <div v-if="mode === 'compact'" class="item-header">
      <NuxtLink :to="`/algoritme/${algoritme.slug}`" class="result--title">
        <h2>{{ props.algoritme.name }}</h2>
      </NuxtLink>
    </div>
    <p>
      {{ description }}&nbsp;
      <NuxtLink
        v-if="isTruncated && mode === 'compact'"
        :to="`/algoritme/${algoritme.slug}`"
        >{{ readMore }}
      </NuxtLink>
    </p>

    <dl class="dl columns--data">
      <div v-for="sT in summaryTiles" :key="sT">
        <dt>{{ t(`algorithmProperties.${sT}.label`) }}</dt>
        <dd class="no-bottom-margin">
          {{ algoritme[sT as keyof typeof algoritme] }}
        </dd>
      </div>
    </dl>
  </li>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { summaryTiles } from '@/config/config'
import type { Algoritme } from '@/types/algoritme'
interface Props {
  algoritme: Algoritme
  mode?: 'compact' | 'default'
}

const props = withDefaults(defineProps<Props>(), {
  mode: 'default',
})

const { t } = useI18n()
const readMore = computed(() => t('searchResultCard.readMore'))
const shortDescriptionMissing = computed(() => t('short-description-missing'))

const length = 300
const truncatedDescription = computed(() => {
  const truncatedString = props.algoritme.description_short.substring(0, length)
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
    props.algoritme.description_short.substring(0, length)
  )
})
</script>

<style scoped lang="scss">
h2 {
  font-size: 1.1em;
  margin-bottom: 0.2em;
}

.dl.columns--data div {
  padding: 0.5em;
}

.no-bottom-margin {
  margin-bottom: 0;
}
li.default {
  background: $tertiary !important;
  list-style: none;
  padding: 1em;
  margin-bottom: 0.5em;
  border: 0;
}
@media (min-width: 51em) {
  li.default {
    padding: 1.5em 10% !important;
  }
}

li.compact {
  background: #fff;
  list-style: none;
  padding: 1em;
  margin-bottom: 0.5em;
  border: 0;
}
@media (min-width: 51em) {
  li.compact {
    padding: 1.75em 1.25em 1.5em 2em !important;
  }
}
</style>
