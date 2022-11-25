<template>
  <Page>
    <h1>{{ t('paths./privacyverklaring') }}</h1>
    <div v-if="!englishSelected">
      <p class="mb-4">
        Persoonsgegevens die u opgeeft, gebruikt de Rijksoverheid alleen voor
        het doel waarvoor u ze heeft achtergelaten. Daarmee voldoet de
        Rijksoverheid aan de privacywetgeving.
      </p>
      <p class="mb-4">Hoe gaat de Rijksoverheid om met uw persoonsgegevens?</p>
      <p>
        Wilt u informatie vragen over het ICT-dashboard? Wilt u een opmerking
        achterlaten? Dan kunt u uw persoonsgegevens in een formulier invullen.
        Bijvoorbeeld uw naam en (e-mail)adres. Bij het formulier staat
        aangegeven welke gegevens de Rijksoverheid gebruikt en met welk doel.
      </p>
      <p class="mb-4">
        De Rijksoverheid bewaart deze persoonsgegevens niet langer dan nodig is,
        voor het doel waarvoor u ze heeft achtergelaten.
      </p>
      <p>Wat is de Algemene Verordening Gegevensbescherming (AVG)?</p>

      <p class="mb-4">
        De belangrijkste regels voor de omgang met persoonsgegevens zijn
        vastgelegd in de AVG De Autoriteit Persoonsgegevens is toezichthouder op
        de Algemene Verordening Gegevensbescherming.
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
  title: 'Privacyverklaring',
})
</script>
