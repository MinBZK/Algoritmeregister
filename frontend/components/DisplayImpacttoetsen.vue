<template>
  <div v-if="foundImpactToetsen.length > 0">
    {{ foundImpactToetsen.join(', ') }}
  </div>
  <div v-else>{{ props.text }}</div>
</template>

<script setup lang="ts">
import type { ListWithLinks } from '@/types/layout'

const props = defineProps<{
  text: string | ListWithLinks
}>()

const foundImpactToetsen = computed(() => {
  const impactToetsen: string[] = []
  const displayImpacttoets: string[] = []
  const seen = new Set<string>()
  const maxLength = 60
  let currentLength = 0
  const impactToetsAbbrevations = [
    'AIIA',
    'DEDA',
    'DPIA',
    'FRAIA',
    'IAMA',
    'Uthiek',
  ]

  if (Array.isArray(props.text)) {
    props.text.forEach((item) => {
      if (typeof item.title === 'string') {
        const foundImpactToetsAbbreviation = impactToetsAbbrevations.find(
          (toets) => item.title.includes(toets)
        )
        const impactToetsToAdd =
          foundImpactToetsAbbreviation ?? item.title.trim()
        if (impactToetsToAdd && !seen.has(impactToetsToAdd)) {
          seen.add(impactToetsToAdd)
          impactToetsen.push(impactToetsToAdd)
        }
      }
    })
  }

  for (const item of impactToetsen) {
    const nextItem = displayImpacttoets.length === 0 ? item : ', ' + item
    if (currentLength + nextItem.length > maxLength) {
      displayImpacttoets.push('...')
      break
    }
    displayImpacttoets.push(item)
    currentLength += nextItem.length
  }
  return displayImpacttoets
})
</script>
