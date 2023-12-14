<template>
  <div>
    <div class="skiplinks container">
      <a href="#content" class="no-margin" tabindex="1">Direct naar content</a>
    </div>
    <AppHeader />
    <AppContentBar v-if="false" />
    <AppBreadcrumb />
    <div class="container columns columns--sidebar-left row bottom-margin">
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
const siteTitle = computed(() => t('homepageTitle'))
useHead({
  htmlAttrs: { lang: locale },
  titleTemplate: (pageTitle) => {
    return pageTitle ? `${pageTitle} - ${siteTitle.value}` : siteTitle.value
  },
})

const readAfterLanguageChange = ref<string>()
watch(locale, () => {
  readAfterLanguageChange.value =
    t('currentLanguage') +
    '; ' +
    (pageTitleInfo.value.labelType === 'locale-index'
      ? t(pageTitleInfo.value.title)
      : pageTitleInfo.value.title)
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
