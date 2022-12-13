<template>
  <div v-if="breadcrumbs.length != 0 && !error" class="row row--page-opener">
    <div class="container">
      <div class="breadcrumb">
        <p>{{ t('you-are-here') }}:</p>
        <ClientOnly>
          <ol>
            <li v-for="crumb in breadcrumbsWithLinks" :key="crumb.routeName">
              <a v-if="crumb.routeName != null" :href="`/${crumb.routeName}`">{{
                crumb.label
              }}</a>
              <span v-if="crumb.routeName == null">{{ crumb.label }}</span>
            </li>
            <li>{{ pathTail.label }}</li>
          </ol>
        </ClientOnly>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { navigationItems } from '@/config/config'

const error = useError()

const { algoritme } = useAlgoritme()

const { t } = useI18n()
const currentRoute = useRoute()

const navigationItemsTranslated = computed(() =>
  navigationItems.map((item) => {
    return { label: t(item.localeName), routeName: item.routeName }
  })
)

const ignoredNavigationItems = ['footer']

const breadcrumbs = computed(() => {
  const path = currentRoute.path
  // the added '/ ' is interpreted in the mapping as the link to Home
  let crumbStrings: string[] =
    path !== '/' ? ('/ ' + path).split('/').slice(1) : []

  crumbStrings = crumbStrings.filter(
    (crumb) => !ignoredNavigationItems.includes(crumb)
  )
  return crumbStrings
    .map((crumb: any) => {
      return {
        label:
          // translate path parts with a name matching a navigation item
          navigationItemsTranslated.value.find(
            (item) => item.routeName === crumb
          )?.label || // translate path parts with a name matching an algorithm slug
          algoritme.value?.name ||
          crumb,
        routeName: crumb,
      }
    })
    .filter((bc) => bc.routeName) // remove empty routes when URL has a trailing /
})

const breadcrumbsWithLinks = computed(() => breadcrumbs.value.slice(0, -1))
const pathTail = computed(() => breadcrumbs.value.slice(-1)[0])
</script>

<style scoped lang="scss">
.container {
  width: $page-width;
}
</style>
