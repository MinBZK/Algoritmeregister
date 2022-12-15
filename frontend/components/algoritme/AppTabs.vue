<template>
  <ul class="tabs__list" role="tablist">
    <li v-for="(p, index) in tabProperties" :key="p.key" role="presentation">
      <a
        ref="tabHeaders"
        :key="p.key"
        :tabindex="p.key == activeTab ? 0 : -1"
        :aria-selected="p.key == activeTab"
        class="noselect"
        :class="[p.key == activeTab ? 'is-selected' : '']"
        role="tab"
        :aria-controls="`panel-${index + 1}`"
        @click="selectTab(p.key)"
        @keydown.enter="selectTab('selectFocus')"
        @keydown.left.prevent="navigateTab(-1)"
        @keydown.right.prevent="navigateTab(1)"
        >{{ p.label }}</a
      >
    </li>
  </ul>
</template>

<script setup lang="ts">
import { useActiveElement } from '@vueuse/core'
const props = defineProps<{
  tabProperties: {
    key: string
    label: string
  }[]
}>()

const emit = defineEmits<{
  (e: 'focusChanged', activeTab: string): void
}>()

const isMobile = useMobileBreakpoint()

const activeTab = ref('')

const activeElement = useActiveElement()

const focusedTabIndex = computed(() => {
  const currentIndexSelected = props.tabProperties
    .map((sP) => sP.key)
    .indexOf(activeTab.value)

  const currentIndexWithFocus = activeElement.value
    ? tabHeaders.value.indexOf(activeElement.value as HTMLAnchorElement)
    : -1

  const currentIndex =
    currentIndexWithFocus > -1 ? currentIndexWithFocus : currentIndexSelected

  return currentIndex
})

const tabHeaders = ref<HTMLAnchorElement[]>([])
const navigateTab = (increment: number) => {
  const newIndex = focusedTabIndex.value + increment
  if (newIndex >= 0 && newIndex < props.tabProperties.length) {
    tabHeaders.value[newIndex].focus()
  }
}

const selectTab = (key: string) => {
  if (key === 'selectFocus') {
    activeTab.value = props.tabProperties[focusedTabIndex.value].key
  } else {
    activeTab.value = key
  }
  emit('focusChanged', activeTab.value)
}

watch(
  isMobile,
  (newValue) =>
    // Closes tabs if the screen is becoming smaller.
    (activeTab.value = newValue ? '' : props.tabProperties[0].key)
)
</script>

<style lang="scss">
.tabs__list a {
  cursor: pointer;
}
li a:focus {
  box-shadow: 0 0 0 0 #000 !important;
  outline: 0;
  background-color: $grey;
}
</style>
