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
    return { label: t(item.label), routeName: item.routeName }
  })
)

const navigationItemsWithoutLink = ['footer']

const breadcrumbs = computed(() => {
  const path = currentRoute.path
  const breadCrumbs = path != '/' ? path.split('/').slice(1) : []

  return breadCrumbs.map((crumb) => {
    return {
      label:
        // translate path parts with a name matching a navigation item
        navigationItemsTranslated.value.find((item) => item.routeName == crumb)
          ?.label || // translate path parts with a name matching an algorithm id
        nameList.value.find((alg: any) => alg.id == crumb)?.name ||
        crumb,
      routeName: navigationItemsWithoutLink.includes(crumb) ? null : crumb,
    }
  })
})

const breadcrumbsWithLinks = computed(() => breadcrumbs.value.slice(0, -1))
const pathTail = computed(() => breadcrumbs.value.slice(-1)[0])
</script>
