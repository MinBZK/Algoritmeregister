<template>
  <Page>
    <h1>{{ t('paths./over') }}</h1>
    <div v-if="!englishSelected">
      <p class="mb-4">
        Deze website toont informatie over algoritmes die op dit moment door de
        Nederlandse overheid worden gebruikt.
      </p>
      <p class="mb-4">
        De website is op dit moment nog in ontwikkeling. Meer informatie en
        functionaliteit zal worden toegevoegd in de toekomst.
      </p>
      <p>
        Deze website is een initiatief van het ministerie van Binnenlandse Zaken
        en Koninklijksrelaties in nauwe samenwerking met alle centrale,
        regionale en lokale overheden van Nederland.
      </p>
    </div>

    <div v-if="englishSelected">
      <p class="mb-4">
        This website lists information on algorithms currently used by the Dutch
        government.
      </p>
      <p class="mb-4">
        This site currently is still in its infancy and more information and
        functionality will be added in time.
      </p>
      <p class="mb-4">
        This website is an initiative of the ministry of Interior Affairs and
        Kingdom Relations in close co operation with all parts of central,
        regional and local government of the Netherlands.
      </p>
    </div>
  </Page>
</template>

<script setup lang="ts">
import Page from '~~/components/PageWrapper.vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const englishSelected = computed(() => {
  return t(`english?`) == 'true'
})
definePageMeta({
  title: 'Over',
})
</script>
