<template>
  <div>
    <div class="skiplinks container">
      <a href="#content" class="no-margin" tabindex="1">Direct naar content</a>
    </div>
    <AppHeader />
    <AppContentBar v-if="false" />
    <AppBreadcrumb />
    <div class="container columns columns--sidebar-left bottom-margin">
      <div id="content">
        <slot />
      </div>
    </div>
    <AppFooter />
    <div class="visually-hidden" disabled aria-live="polite">
      {{ readAfterLanguageChange }}
    </div>
  </div>
</template>

<script setup lang="ts">
import AppContentBar from '@/components/views/AppContentBar.vue'
import AppHeader from '@/components/views/AppHeader.vue'
import AppBreadcrumb from '@/components/views/AppBreadcrumb.vue'
import AppFooter from '@/components/views/AppFooter.vue'
import { pageTitleInfo } from '~~/utils'

const { t, locale } = useI18n()
const { p } = useTextLoader()

useHead({
  htmlAttrs: { lang: locale },
})

// On every update of this variable, it is read by the screenreader.
const readAfterLanguageChange = ref<string>()
watch(locale, () => {
  let head
  switch (pageTitleInfo.value.labelType) {
    case 'locale-index':
      head = t(pageTitleInfo.value.title)
      break
    case 'preditor-index':
      head = p(pageTitleInfo.value.title)
      break
    case 'plain-text':
      head = pageTitleInfo.value.title
      break
  }
  readAfterLanguageChange.value = t('currentLanguage') + '; ' + head
})
</script>

<style scoped>
#layout {
  margin: 0 auto 10px auto;
}

.bottom-margin {
  padding-bottom: 1.5em;
}

.row {
  display: flex;
}

.align-right {
  margin-left: auto;
}

#content {
  margin: 0;
}
</style>
