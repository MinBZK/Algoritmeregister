<template>
  <div
    v-if="showDisclaimer"
    class="info-box"
    :class="{ compact: density == 'compact' }"
  >
    <div v-html="text" />
    <div class="button-row">
      <button class="button dutch-button" @click="goToDutch()">
        <span class="button__label"
          >{{ p('language-disclaimer.goToDutch') }}
        </span>
      </button>
      <button class="button close-button" @click="closeClicked()">
        <span class="button__label"
          >{{ p('language-disclaimer.closeText') }}
        </span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const { p } = useTextLoader()
const { setLocale } = useLocale()

withDefaults(
  defineProps<{
    density: 'default' | 'compact'
  }>(),
  {
    density: 'default',
  }
)

const text = computed(() => {
  return p('language-disclaimer.content')
})

const cookie = useCookie('showDisclaimer')
cookie.value = cookie.value || 'show'

const showDisclaimer = ref<boolean>(true)
showDisclaimer.value = cookie.value === 'show'

const closeClicked = () => {
  showDisclaimer.value = false
  cookie.value = 'hide'
}

const goToDutch = () => {
  setLocale('nl')
}
</script>

<style scoped lang="scss">
.info-box {
  padding: 1em 4em 1em 4em;
  border-width: 1px;
  align-items: center;
  background-color: $tertiary;
}

.compact {
  padding: 1em !important;
}

.button {
  min-width: 8em;
}

.dutch-button {
  background-color: $tertiary;
}

.close-button {
  background-color: $primary-darker;
  color: white;
}

.button-row {
  display: flex;
  justify-content: center;
}
</style>
