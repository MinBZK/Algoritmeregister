<template>
  <ul class="tabs__list" role="tablist">
    <li
      v-for="(p, index) in algorithmProperties"
      :key="p.attributeGroupKey"
      role="presentation"
    >
      <a
        ref="tabHeaders"
        :key="p.attributeGroupKey"
        :tabindex="p.attributeGroupKey == activeAttributeKey ? 0 : -1"
        :aria-selected="p.attributeGroupKey == activeAttributeKey"
        class="noselect"
        :class="[
          p.attributeGroupKey == activeAttributeKey ? 'is-selected' : '',
        ]"
        role="tab"
        :aria-controls="`panel-${index + 1}`"
        @click="selectTab(p.attributeGroupKey)"
        @keydown.enter="selectTab('selectFocus')"
        @keydown.left.prevent="navigateTab(-1)"
        @keydown.right.prevent="navigateTab(1)"
        >{{ p.attributeGroupKeyLabel }}</a
      >
    </li>
  </ul>
</template>

<script setup lang="ts">
import { useActiveElement } from '@vueuse/core'
const props = defineProps<{
  algorithmProperties: {
    attributeGroupKey: string
    attributeGroupKeyLabel: string
    properties: {
      attributeKey: string
      attributeValue: string
      attributeKeyDescription: string
      attributeKeyLabel: string
    }[]
  }[]
}>()

const emit = defineEmits<{
  (e: 'focusChanged', activeAttributeKey: string): void
}>()

const isMobile = useMobileBreakpoint()

const activeAttributeKey = ref('')

const activeElement = useActiveElement()

const focusedTabIndex = computed(() => {
  const currentIndexSelected = props.algorithmProperties
    .map((sP) => sP.attributeGroupKey)
    .indexOf(activeAttributeKey.value)

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
  if (newIndex >= 0 && newIndex < props.algorithmProperties.length) {
    tabHeaders.value[newIndex].focus()
  }
}

const selectTab = (key: string) => {
  if (key === 'selectFocus') {
    activeAttributeKey.value =
      props.algorithmProperties[focusedTabIndex.value].attributeGroupKey
  } else {
    activeAttributeKey.value = key
  }
  emit('focusChanged', activeAttributeKey.value)
}

watch(
  isMobile,
  (newValue) =>
    // Closes tabs if the screen is becoming smaller.
    (activeAttributeKey.value = newValue
      ? ''
      : props.algorithmProperties[0].attributeGroupKey)
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
li a:link {
  color: red;
}
</style>
