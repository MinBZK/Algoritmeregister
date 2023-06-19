<template>
  <ul class="tabs__list" role="tablist">
    <li v-for="(p, index) in tabProperties" :key="p.key" role="presentation">
      <a
        ref="tabHeaders"
        :key="p.key"
        :tabindex="p.key == activeTab ? 0 : -1"
        :aria-selected="p.key == activeTab"
        class="noselect"
        :class="{
          'is-selected': p.key == activeTab,
          'no-focus-border': focusFromClick,
          'focus-border': !focusFromClick,
        }"
        role="tab"
        :aria-controls="`panel-${index + 1}`"
        @click="selectTab({ target: p.key, source: 'click' })"
        @keydown.enter="selectTab({ target: 'selectFocus', source: 'key' })"
        @keydown.left.prevent="navigateTab(-1)"
        @keydown.right.prevent="navigateTab(1)"
      >
        {{ p.keyLabel }}
      </a>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { useActiveElement } from '@vueuse/core'
import { changeHash } from '~~/utils'

const props = defineProps<{
  activeTab: string | undefined
  tabProperties: {
    key: string
    keyLabel: string
  }[]
}>()

const emit = defineEmits<{
  (e: 'update:activeTab', newTab: string): void
}>()

const isMobile = useMobileBreakpoint().medium

const activeElement = useActiveElement()

const focusedTabIndex = computed(() => {
  const currentIndexSelected = props.tabProperties
    .map((sP) => sP.key)
    .indexOf(props.activeTab || '')

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
  focusFromClick.value = false
}

interface SelectTabPayload {
  target: string
  source: 'click' | 'key'
}

const focusFromClick = ref<Boolean>(false)

const selectTab = (payload: SelectTabPayload) => {
  const { target, source } = payload
  if (target === 'selectFocus') {
    emit('update:activeTab', props.tabProperties[focusedTabIndex.value].key)
    changeHash(props.tabProperties[focusedTabIndex.value].key)
  } else {
    emit('update:activeTab', target)
    changeHash(target)
  }
  focusFromClick.value = source === 'click'
}

watch(isMobile, (newValue) => {
  // Closes tabs if the screen is becoming smaller.
  if (newValue) {
    emit('update:activeTab', '')
  } else {
    emit('update:activeTab', props.tabProperties[0].key)
  }
})
</script>

<style lang="scss" scoped>
.tabs__list a {
  cursor: pointer;
}

li a.focus-click:focus {
  box-shadow: 0 0 0 0 #000 !important;
  outline: 0;
}
</style>
