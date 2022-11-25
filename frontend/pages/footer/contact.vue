<template>
  <Page>
    <h1>{{ t('paths./contact') }}</h1>
    <div v-if="!englishSelected">
      <p class="mb-4">
        Inhoudelijke vragen, zoals beleidsvragen over projecten, kunt u via het
        contactformulier op rijksoverheid.nl sturen.
      </p>
      <!-- <p class="mb-4">
        Vragen, opmerkingen en/of suggesties over de werking en vormgeving van
        het ICT-dashboard zijn van harte welkom. U kunt deze sturen naar
        Postbus.ICTdashboard@minbzk.nl. Wij nemen uw reactie mee bij de
        ontwikkeling van onze website.
      </p> -->
      <p class="mb-4">
        Uw persoonsgegevens worden alleen gebruikt voor het beantwoorden van uw
        verzoek. De gegevens worden dus niet langer bewaard dan nodig is.
        Informatie hierover vindt u in onze privacyverklaring.
      </p>
      <p class="mb-4">
        Uw vraag handelen wij af conform de e-mailgedragslijn voor overheden.
        Daarin staat beschreven hoe de overheid omgaat met het afhandelen en
        bewaren van e-mail.
      </p>
    </div>

    <div v-if="englishSelected">
      <p>
        Contact information is not available at this time. It will be added
        soon.
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
  title: 'Contact',
})
</script>
