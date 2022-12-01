<template>
  <Page>
    <h1>{{ t('paths./toegankelijkheid') }}</h1>
    <div v-if="!englishSelected">
      <p class="mb-4">
        Deze site zal de wetten en regels voor toegankelijkheid van de
        Nederlandse overheid volledig volgen. De toegankelijkheid word op dit
        moment getoetst en binnenkort volgt een aanvraag voor de A-status.
      </p>
    </div>

    <div v-if="englishSelected">
      <p class="mb-4">
        This site will fully comply with Dutch government regulations and
        policies concerning accessibility. The site is currently under review
        and will apply for A-status soon.
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
  title: 'Toegankelijkheid',
})
</script>
