<template>
  <Page>
    <div v-if="!englishSelected">
      <h1>Toegankelijkheidverklaring</h1>

      <p class="mb-4">
        Deze site is nog in ontwikkeling en heeft nog geen
        toegankelijkheidsverklaring. We ontwikkelen de site met de eisen voor
        toegankelijkheid op ons netvlies. Ons team is getraind in digitale
        toegankelijkheid. En we vragen regelmatig advies aan een onafhankelijke
        toegankelijkheidsexpert.
      </p>
      <p class="mb-4">
        In 2023 start de procedure voor een toegankelijkheidsverklaring, en komt
        de algoritmen.overheid.nl in het
        <a href="https://www.toegankelijkheidsverklaring.nl/register">
          Register van Toegankelijkheidsverklaringen van de overheid
        </a>
      </p>
    </div>

    <div v-if="englishSelected">
      <h1>Accessibility statement</h1>

      <p class="mb-4">
        This site is under development and does not have an accessibility
        statement yet. We are developing the site with accessibility
        requirements in mind. Our team is trained in digital accessibility. And
        we regularly seek advice from an independent accessibility expert.
      </p>
      <p class="mb-4">
        The procedure for an accessibility statement will start in 2023, and
        algorithms.overheid.nl will be included in the government's
        <a href="https://www.toegankelijkheidsverklaring.nl/register">
          Register van Toegankelijkheidsverklaringen.
        </a>
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
