<template>
  <div class="row row--page-opener" v-if="breadcrumbs.length != 0">
    <div class="container">
      <div class="breadcrumb">
        <p>{{ t('you-are-here') }}:</p>
        <ol>
          <li v-for="crumb in breadcrumbsWithLinks">
            <a v-if="crumb.routeName != null" :href="`/${crumb.routeName}`">{{
              crumb.label
            }}</a>
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
import { useI18n } from 'vue-i18n'
import algoritmeService from '@/services/algoritme'
import { AlgNameIdOrg } from '~~/types/algoritme'
const { t } = useI18n()
const currentRoute = useRoute()

const { data } = await algoritmeService.getNameIdOrg()
let nameList = ref(data.value as AlgNameIdOrg[])

const navigationItemsTranslated = computed(() =>
  navigationItems.map((item) => {
    console.log(item)
    return { label: t(item.localeName), routeName: item.routeName }
  })
)

const ignoredNavigationItems = ['footer']

const breadcrumbs = computed(() => {
  const path = currentRoute.path
  // the added '/ ' is interpreted in the mapping as the link to Home
  var crumbStrings: string[] =
    path != '/' ? ('/ ' + path).split('/').slice(1) : []

  crumbStrings = crumbStrings.filter(
    (crumb) => !ignoredNavigationItems.includes(crumb)
  )
  return crumbStrings.map((crumb: any) => {
    return {
      label:
        // translate path parts with a name matching a navigation item
        navigationItemsTranslated.value.find((item) => item.routeName == crumb)
          ?.label || // translate path parts with a name matching an algorithm id
        nameList.value.find((alg: any) => alg.id == crumb)?.name ||
        crumb,
      routeName: crumb,
    }
  })
})

const breadcrumbsWithLinks = computed(() => breadcrumbs.value.slice(0, -1))
const pathTail = computed(() => breadcrumbs.value.slice(-1)[0])
</script>
