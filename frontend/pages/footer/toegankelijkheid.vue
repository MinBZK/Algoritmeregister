<template>
  <div v-if="!englishSelected">
    <h1>Toegankelijkheidsverklaring</h1>

    <p class="mb-4">
      Deze website is in ontwikkeling en heeft nog geen
      toegankelijkheidsverklaring. Het bouwteam ontwikkelt de website met de
      eisen voor toegankelijkheid op ons netvlies. Ze zijn getraind in digitale
      toegankelijkheid. Een onafhankelijke toegankelijkheidsexpert levert
      regelmatig advies.
    </p>
    <p class="mb-4">
      In 2023 start de procedure voor een toegankelijkheidsverklaring, en komt
      algoritme.overheid.nl in het
      <a
        class="is-external"
        target="_blank"
        href="https://www.toegankelijkheidsverklaring.nl/register"
      >
        Register van Toegankelijkheidsverklaringen van de overheid </a
      >.
    </p>
  </div>

  <div v-if="englishSelected">
    <h1>Accessibility statement</h1>

    <p class="mb-4">
      This site is under development and does not have an accessibility
      statement yet. This website is being developed with accessibility
      requirements in mind. The team is trained in digital accessibility. An
      independent accessibility expert regularly advises.
    </p>
    <p class="mb-4">
      The procedure for an accessibility statement will start in 2023, and the
      website will be included in the government's
      <a
        class="is-external"
        target="_blank"
        href="https://www.toegankelijkheidsverklaring.nl/register"
      >
        Register van Toegankelijkheidsverklaringen.
      </a>
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const englishSelected = computed(() => {
  return t(`english?`) === 'true'
})
definePageMeta({
  title: 'Toegankelijkheid',
})
</script>
