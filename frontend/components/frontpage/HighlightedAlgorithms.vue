<template>
  <div class="bar highlighted-bar">
    <h2 class="highlight-text">
      {{ p('Home.highlightTextTop') }}
    </h2>
    <ul class="bar__list">
      <li v-for="algo in data" :key="algo.lars" class="bar__list__item">
        <div class="bar__list__item-icon highlighted-truncated-link">
          <div class="highlight-icon-fix">
            <NuxtIcon
              size="0.8em"
              name="material-symbols:arrow-forward-ios-rounded"
            />&nbsp;
          </div>
          <NuxtLink :to="localePath(`/algoritme/${algo.lars}`)" class="link">
            {{ algo.name || '' }} | {{ algo.organization || '' }}
          </NuxtLink>
        </div>
      </li>
    </ul>
    <div v-html="p('Home.highlightTextBottom')" />
  </div>
</template>

<script setup lang="ts">
import algoritmeService from '@/services/algoritme'
import { mapLocaleName } from '@/utils'
const { p } = useTextLoader()
const { locale } = useI18n()

const localePath = useLocalePath()

const language = mapLocaleName(locale.value as 'nl' | 'en')
const { data } = await algoritmeService.getHighlighted(language)
</script>

<style scoped lang="scss">
.highlighted-bar {
  padding: 0.5em 0.5em 0.5em 0.5em;
}
.highlight-icon-fix {
  width: 1.2em;
  display: flex;
  align-items: center;
}

.highlight-text {
  font-size: 1em;
  margin-bottom: 0.6em;
}

.highlighted-truncated-link {
  display: flex;
  align-items: center;
}

.bar__list__item {
  margin: 0 0 0.6em 0;
  // width: 25em;
}

// .highlighted-truncated-link a {
// overflow: hidden;
// text-overflow: ellipsis;
// white-space: nowrap;
// }

.highlighted-truncated-link svg {
  margin-right: 0.2em;
}
</style>
