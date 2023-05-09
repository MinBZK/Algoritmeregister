<template>
  <div v-if="breadcrumbs.length != 0 && !error" class="row row--page-opener">
    <div class="container">
      <div class="breadcrumb">
        <p>{{ t('you-are-here') }}:</p>
        <ClientOnly>
          <ol>
            <li v-for="crumb in breadcrumbsWithLinks" :key="crumb.routeName">
              <NuxtLink
                v-if="crumb.routeName !== null"
                :to="localePath(`/${crumb.routeName}`)"
                >{{ crumb.label }}</NuxtLink
              >
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
import { navigationItems } from '@/config/config'

const error = useError()
const localePath = useLocalePath()

const { algoritme } = useAlgoritme()

const { t } = useI18n()
const currentRoute = useRoute()

const navigationItemsTranslated = computed(() =>
  navigationItems.map((item) => {
    return { label: t(item.localeName), routeName: item.routeName }
  })
)

const ignoredNavigationItems = ['footer', 'en', 'nl']

type Crumb = {
  label: string
  routeName: string
}

const breadcrumbs = computed<Crumb[]>(() => {
  const path = currentRoute.path
  // the added '/ ' is interpreted in the mapping as the link to Home
  const crumbStrings: string[] =
    path !== '/' ? ('/' + path).split('/').slice(1) : []

  const crumbs: Crumb[] = crumbStrings
    .filter((crumb) => {
      // crumb must be truthy, otherwise trailing slashes will be parsed as a route
      return crumb && !ignoredNavigationItems.includes(crumb)
    })
    .map((crumb: any) => {
      return {
        label:
          // translate path parts with a name matching a navigation item
          navigationItemsTranslated.value.find(
            (item) => item.routeName === crumb
          )?.label || // translate path parts with a name matching an algorithm id
          algoritme.value?.name ||
          crumb,
        routeName: crumb,
      }
    })

  return crumbs.length > 0
    ? [
        {
          label: 'Home',
          routeName: '',
        },
        ...crumbs,
      ]
    : []
})

const breadcrumbsWithLinks = computed(() => breadcrumbs.value.slice(0, -1))
const pathTail = computed(() => breadcrumbs.value.slice(-1)[0])
</script>

<style scoped lang="scss">
.container {
  width: $page-width;
}
</style>
