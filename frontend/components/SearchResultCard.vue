<template>
  <li class="item">
    <div class="item-header">
      <NuxtLink :to="`/algoritme/${algoritme.slug}`" class="result--title">
        <h2>{{ props.algoritme.name }}</h2>
      </NuxtLink>
    </div>
    <p>
      {{ truncatedDescription }}&nbsp;<NuxtLink
        v-if="isTruncated"
        :to="`/algoritme/${algoritme.slug} `"
        >{{ readMore }}
      </NuxtLink>
    </p>

    <!-- <p> -->
    <dl class="dl columns--data">
      <div v-for="sT in summaryTiles" :key="sT">
        <dt>{{ t(`algorithmProperties.${sT}.label`) }}</dt>
        <dd class="no-bottom-margin">
          {{ algoritme[sT as keyof typeof algoritme] }}
        </dd>
      </div>
    </dl>
    <!-- </p> -->
  </li>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { summaryTiles } from '@/config/config'
import type { Algoritme } from '@/types/algoritme'

const { t } = useI18n()
const readMore = computed(() => t('searchResultCard.readMore'))

const props = defineProps<{
  algoritme: Algoritme
}>()

const length = 300
const truncatedDescription = computed(() => {
  const truncatedString = props.algoritme.description_short.substring(0, length)
  return truncatedString === props.algoritme.description_short
    ? props.algoritme.description_short
    : truncatedString + '...'
})

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
</style>
