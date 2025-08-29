<template>
  <div class="page">
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
      <div class="result--list result--list__data">
        <ul>
          <li
            v-for="(algoritme, index) in organisation.algoritme_versions"
            :key="algoritme.algoritme_id"
          >
            <GenericResultCard
              :set-focus="index == 0 && newFocusIsRequested"
              :algoritme="algoritme"
              @focus-has-been-set="newFocusIsRequested = false"
            >
            </GenericResultCard>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ParseUrl from '@/components/ParseUrl.vue'
import organisationService from '@/services/organisation'
import type { OrganisationPage } from '@/types/organisation'

const { t, locale } = useI18n()
const route = useRoute()
const params = route.params.params || []
const orgId = params.length === 1 ? params[0] : params.at(-2)!
const { setOrganisation } = useOrganisation()
const newFocusIsRequested = ref<boolean>(false)

const { data } = await organisationService.getOne(
  orgId,
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
.about-section {
  margin-bottom: 3em;
}

.contact-section {
  display: inline-flex;
}

.page {
  margin-bottom: 3em;
}

.margin-bottom-0 :deep(p) {
  margin-bottom: 0em;
}
</style>
