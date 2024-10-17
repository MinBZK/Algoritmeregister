<template>
  <div class="accordion">
    <AlgoritmeAccordionRow
      v-for="p in accordionProperties"
      :key="p.key"
      :group-props="p"
    />
  </div>
</template>

<script setup lang="ts">
import type { AlgorithmDisplay } from '~~/types/algoritme'

defineProps<{
  accordionProperties: AlgorithmDisplay[]
}>()

const expandedTab = useState<string | undefined>('expandedTab', () => undefined)
const selectTabOnMount = () => {
  const hash = useRoute().hash.slice(1)
  expandedTab.value = hash
}
selectTabOnMount()
</script>
