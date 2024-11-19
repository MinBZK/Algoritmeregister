<template>
  <div class="page">
    <div class="navigation-top">
      <!-- <NuxtLink class="link cta__backwards" :to="localePath(`/organisatie/`)">
        {{ t('orgPage.goBackToOrg') }}
      </NuxtLink> -->
    </div>
    <div class="container row container--centered">
      <h1>{{ organisation.name }}</h1>
      <template v-if="organisation.show_page">
        <div class="about-section">
          <h2>{{ t('orgPage.aboutHeader') }}</h2>
          <div
            v-if="organisation.about"
            class="margin-bottom-0"
            v-html="organisation.about"
          />
          <p v-else>
            {{ t('orgPage.noAbout') }}
          </p>
          <div v-if="organisation.contact_info" class="contact-section">
            <b> {{ t('orgPage.contactInfo') }}&nbsp;</b>
            <ParseUrl>
              <div
                v-if="organisation.contact_info"
                v-html="organisation.contact_info"
              ></div>
            </ParseUrl>
          </div>
        </div>
        <h2 v-if="!!organisation.algoritme_versions.length">
          {{ t('orgPage.algorithmDescriptions') }}
        </h2>
      </template>
      <template v-else>
        <p>{{ t('orgPage.alternativeAlgorithmDescriptions') }}:</p>
      </template>
      <div
        v-for="algo in organisation.algoritme_versions"
        :key="algo.lars"
        class="algo-summary"
      >
        <h3>
          <NuxtLink :to="localePath(`/algoritme/${algo.lars}`)"
            >{{ algo.name }}
          </NuxtLink>
        </h3>
        <div v-if="!isMobile">
          <NuxtLink :to="localePath(`/algoritme/${algo.lars}`)"
            >{{ readMore }}
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ParseUrl from '@/components/ParseUrl.vue'
import organisationService from '@/services/organisation'
import type { OrganisationPage } from '@/types/organisation'
import { useMobileBreakpoint } from '~~/composables/mobile'

const { t, locale } = useI18n()
const isMobile = useMobileBreakpoint().medium

const localePath = useLocalePath()

const route = useRoute()
const orgCode = route.params.orgCode as string

const readMore = computed(() => t('genericResultCard.readMore'))

const { setOrganisation } = useOrganisation()
const { data } = await organisationService.getOne(
  orgCode,
  mapLocaleName(locale.value as 'en' | 'nl')
)
const organisation = ref(data.value as OrganisationPage)
if (!organisation.value) {
  throw createError({
    statusCode: 404,
    fatal: true,
  })
}
setOrganisation(organisation.value)

const { p } = useTextLoader()
const description = computed(() =>
  p('Organisatie-details.meta-description', {
    'org-name': organisation.value.name,
    'algorithm-description-count':
      organisation.value.algoritme_versions.length.toString(),
  })
)
useSeoMeta({
  description: description.value,
  ogDescription: description.value,
})

useHead({ title: organisation.value.name })
providePageTitle({
  title: organisation.value.name,
  labelType: 'plain-text',
})
</script>

<style scoped lang="scss">
.algo-summary {
  width: 100%;
  height: 5em;
  background-color: white;
  border: 0.5em $tertiary solid;

  margin-bottom: -0.5em;

  padding: 1em;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

h3 {
  margin: 0;
  a {
    text-decoration: none !important;
  }
}

.about-section {
  margin-bottom: 3em;
}

.contact-section {
  display: inline-flex;
}

.page {
  margin-bottom: 3em;
}

.navigation-top {
  margin-bottom: 1.5em;
}

.margin-bottom-0 :deep(p) {
  margin-bottom: 0em;
}
</style>
