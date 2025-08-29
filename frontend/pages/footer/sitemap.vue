<template>
  <div>
    <div v-html="p('Footer: Sitemap.content')" />
    <ul>
      <li v-for="(item, routeIndex) in sortedNameAndPath" :key="routeIndex">
        <NuxtLink :v-if="item.name" :href="item.path"
          >{{ item && item.name ? capitalize(t(`sitemap.` + item.name)) : '' }}
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
const { t, locale } = useI18n()
const { p } = useTextLoader()
const router = useRouter()

const allRoutes = router.options.routes

const excludePages = ['/pagina-niet-gevonden', '/sitemap']
const excludeName = ['footer', 'map']

const nameAndPath = computed(() => {
  return allRoutes
    .filter(({ path }) => !path.includes(':'))
    .filter(
      ({ path }) => !excludePages.some((excluded) => path.includes(excluded))
    )
    .filter(({ path }) => path.includes(`/${locale.value}`))
    .map(({ name, path }) => {
      const nameString = String(name)
      const nameParts = nameString?.split(/[-_]/)
      const filteredParts = nameParts.filter(
        (part) =>
          part && part !== `${locale.value}` && !excludeName.includes(part)
      )
      const joinedName = filteredParts.join('-').trim()
      return {
        name: joinedName,
        path,
      }
    })
})

const sortedNameAndPath = computed(() => {
  return nameAndPath.value
    .map((item) => {
      if (item.name.toLowerCase() === 'index') {
        item.name = 'home'
      }
      return item
    })
    .sort((a, b) => a.name.localeCompare(b.name))
})

const capitalize = (string: string) =>
  string.charAt(0).toUpperCase() + string.slice(1)

useHead({ title: p('Footer: Sitemap.pageTitle') })
providePageTitle({
  title: 'Footer: Sitemap.pageTitle',
  labelType: 'preditor-index',
})
</script>
