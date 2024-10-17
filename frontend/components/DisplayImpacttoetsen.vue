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
  let hasOtherImpacttoets = false
  const impactToetsenList = ['DPIA', 'IAMA']

  if (Array.isArray(props.text)) {
    props.text.forEach((item) => {
      if (typeof item.title === 'string') {
        const foundImpactToets = impactToetsenList.find((toets) =>
          item.title.includes(toets)
        )
        if (foundImpactToets && !impactToetsen.includes(foundImpactToets)) {
          impactToetsen.push(foundImpactToets)
        } else {
          hasOtherImpacttoets = true
        }
      }
    })
  }
  if (hasOtherImpacttoets && impactToetsen.length === 0) {
    return ['...']
  }

  if (hasOtherImpacttoets) {
    impactToetsen.push('...')
  }

  return impactToetsen
})
</script>
