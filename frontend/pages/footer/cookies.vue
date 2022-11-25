<template>
  <Page>
    <h1>{{ t('paths./cookies') }}</h1>

    <div v-if="!englishSelected">
      <p class="mb-4">
        Deze website maakt alleen gebruik van analytische cookies. Cookies zijn
        kleine tekstbestanden die websites op uw computer opslaan. Daarmee is uw
        computer te herkennen tijdens uw bezoek. Deze informatie helpt ons om de
        site te verbeteren. Analytische cookies geven antwoord op de volgende
        vragen:
      </p>
      <ol class="ml-5 mb-4">
        <li>
          Is de bezoeker nieuw of heeft de bezoeker de site al eerder bezocht?
        </li>
        <li>Welke pagina's zijn tijdens het bezoek geraadpleegd?</li>
        <li>Van welke site is de bezoeker gekomen?</li>
        <li>
          Heeft de bezoeker de site meteen weer verlaten (het zogenaamde
          'bouncing')?
        </li>
      </ol>
      <p class="mb-4">
        Deze cookies worden dus niet gebruikt om een profiel aan te maken of u
        verder te volgen. Rijksictdashboard.nl plaatst ook geen cookies van
        derde partijen (zogenaamde third-party cookies).
      </p>
    </div>
    <div v-if="englishSelected"></div>
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
  title: 'Cookies',
})
</script>
