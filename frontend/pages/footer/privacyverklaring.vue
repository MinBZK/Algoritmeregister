<template>
  <Page>
    <h1>{{ t('paths./privacyverklaring') }}</h1>
    <div v-if="!englishSelected">
      <p class="mb-4">
        Deze website slaat geen informatie over u op. Dit kan in de toekomst
        veranderen maar alleen conform de regels van de AVG.
      </p>
    </div>
    <div v-if="englishSelected">
      <p class="mb-4">
        This site does not store information about you. At some point in the
        future this may change but only in compliance with GDPR (AVG)
        regulations.
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
  title: 'Privacyverklaring',
})
</script>
