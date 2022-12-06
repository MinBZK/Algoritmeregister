<template>
  <li class="item">
    <div class="item-header">
      <a :href="`/algoritme/${props.algoritme.id}`" class="result--title">
        {{ props.algoritme.name }}
      </a>
    </div>
    <p>{{ truncatedDescription }}&nbsp;<a :href="`/algoritme/${props.algoritme.id} `" v-if="isTruncated">lees meer </a></p>

    <p>
    <dl class="dl columns--data">
      <div v-for="sT in summaryTiles">
        <dt>{{
            t(`algorithmProperties.algemeneInformatie.${sT}.label`)
        }}</dt>
        <dd class="word-break">{{ algoritme[sT as keyof typeof algoritme] }}</dd>
      </div>
    </dl>
    </p>
  </li>
</template>

<script setup lang="ts">
import { summaryTiles } from '@/config/config'
import { useI18n } from 'vue-i18n'
import type { Algoritme } from '@/types/algoritme'

const { t } = useI18n()

const props = defineProps<{
  algoritme: Algoritme
}>()

const length = 300
const truncatedDescription = computed(() => {
  const truncatedString = props.algoritme.description_short.substring(0, length)
  return truncatedString == props.algoritme.description_short ? props.algoritme.description_short : truncatedString + '...'
})

const isTruncated = computed(() => {
  return truncatedDescription.value != props.algoritme.description_short.substring(0,length)
})
</script>