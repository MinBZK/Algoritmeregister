<template>
  <div v-if="breadcrumbs.length != 0 && !error" class="row row--page-opener">
    <div class="container">
      <div class="breadcrumb">
        <p>{{ t('you-are-here') }}:</p>
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
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { navigationItems } from '@/config/config'

const error = useError()
const localePath = useLocalePath()

const { algoritme } = useAlgoritme()
const { organisation } = useOrganisation()

const { t } = useI18n()
const currentRoute = useRoute()

const navigationItemsTranslated = computed(() =>
  navigationItems.map((item) => {
    return { ...item, label: t(item.localeName) }
  })
)

type Crumb = {
  label: string
  routeName: string
}

const breadcrumbs = computed<Crumb[]>(() => {
  const routeName = currentRoute.name?.toString()

  const crumbStrings: string[] = currentRoute.path.split('/')
  const crumbs: Crumb[] = crumbStrings.reduce(
    (acc: Crumb[], crumb: string): Crumb[] => {
      if (!crumb) return acc
      if (['nl', 'en', 'fy', 'footer'].includes(crumb)) return acc

      let crumbLabel = ''

      const defaultName = navigationItemsTranslated.value.find(
        (item) => item.routeName === crumb
      )?.label
      if (defaultName) crumbLabel = defaultName
      else if (routeName?.includes('algoritme-slug-lars')) {
        // Algoritme detail page. Ignore the slug for the breadcrumb.
        // Checks if path part is a code (minus first character as it can be a C for previews)
        if (isNaN(parseInt(crumb.slice(1)))) return acc
        crumbLabel = algoritme.value?.name || ''
      } else if (routeName?.includes('organisatie-orgCode')) {
        // Organisation detail page
        crumbLabel = organisation.value?.name || ''
      } else return acc
      acc.push({ label: crumbLabel, routeName: crumb })
      return acc
    },
    []
  )

  // Add Home to the start if there is any routing at all.
  if (crumbs.length > 0) crumbs.unshift({ label: 'Home', routeName: '' })
  return crumbs
})

const breadcrumbsWithLinks = computed(() => breadcrumbs.value.slice(0, -1))
const pathTail = computed(() => breadcrumbs.value.slice(-1)[0])
</script>

<style scoped lang="scss">
.container {
  width: $page-width;
}
</style>
