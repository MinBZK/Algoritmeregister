<template>
  <div
    v-for="accordion in accordions"
    :key="accordion.key"
    class="question-accordion"
  >
    <h2 :id="accordion.anchor">{{ accordion.label }}</h2>
    <FaqAccordionRows :questions="accordion.questions" />
  </div>
</template>

<script setup lang="ts">
import type { FooterFaqQuestionGroup } from '@/types/footer'

defineProps<{
  accordions: FooterFaqQuestionGroup[]
}>()

const expandedTab = useState<string | undefined>(
  'expandedTabFaq',
  () => undefined
)
const selectTabOnMount = () => {
  const hash = useRoute().hash.slice(1)
  expandedTab.value = hash
}
selectTabOnMount()
</script>

<style scoped langs="scss">
.question-accordion {
  padding-bottom: 1em;
}

h2 {
  margin-bottom: 0em !important;
  padding-bottom: 0.25em;
}
</style>
