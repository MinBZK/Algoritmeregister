<template>
  <Page>
    <h1>{{ t('paths./contact') }}</h1>
    <div v-if="!englishSelected">
      <p class="mb-4">
        Contactinformatie is op dit moment niet beschikbaar. Die wordt
        binnenkort toegevoegd.
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
