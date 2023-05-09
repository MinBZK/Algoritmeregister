<template>
  <div class="accordion">
    <ClientOnly>
      <AlgoritmeAccordionRow
        v-for="p in accordionProperties"
        :key="p.groupKey"
        :group-props="p"
      />
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  accordionProperties: {
    groupKey: string
    properties: {
      key: string
      value: string
      keyDescription: string
      keyLabel: string
    }[]
  }[]
}>()

const expandedTab = useState<string | undefined>('expandedTab', () => undefined)
const selectTabOnMount = () => {
  const hash = useRoute().hash.slice(1)
  expandedTab.value = hash
}
selectTabOnMount()
</script>
