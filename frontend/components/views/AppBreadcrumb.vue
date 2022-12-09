<template>
  <ClientOnly>
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
  </ClientOnly>
</template>

<script setup lang="ts">
import { navigationItems } from '@/config/config'
import { useI18n } from 'vue-i18n'

const { algoritme } = useAlgoritme()

const { t } = useI18n()
const currentRoute = useRoute()

const navigationItemsTranslated = computed(() =>
  navigationItems.map((item) => {
    return { label: t(item.label), routeName: item.routeName }
  })
)

const navigationItemsWithCustomLink = [
  {
    label: 'footer',
    routeName: ' ',
  },
]

const breadcrumbs = computed(() => {
  const path = currentRoute.path
  const breadCrumbs = path != '/' ? path.split('/').slice(1) : []

  return breadCrumbs.map((crumb) => {
    // console.log(nameList.value.find((alg) => alg.slug == crumb)?.name)
    return {
      label:
        // translate path parts with a name matching a navigation item
        navigationItemsTranslated.value.find((item) => item.routeName == crumb)
          ?.label || // translate path parts with a name matching an algorithm slug
        algoritme.value?.name ||
        crumb,
      routeName:
        navigationItemsWithCustomLink.find((item) => item.label == crumb)
          ?.routeName || crumb,
    }
  })
})

const breadcrumbsWithLinks = computed(() => breadcrumbs.value.slice(0, -1))
const pathTail = computed(() => breadcrumbs.value.slice(-1)[0])
</script>
