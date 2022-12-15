<template>
  <div>
    <div v-if="!englishSelected">
      <h1>Toegankelijkheid</h1>

      <p class="mb-4">
        Bij het ontwikkelen van deze website worden de wensen en eisen voor een
        toegankelijke website direct ingebouwd. Het bouwteam van het
        Algoritmeregister is getraind in digitale toegankelijkheid. Een
        onafhankelijke toegankelijkheidsexpert levert regelmatig advies.
      </p>
      <p class="mb-4">
        Deze website is in ontwikkeling en heeft nog geen
        toegankelijkheidsverklaring. In 2023 start de procedure voor een
        toegankelijkheidsverklaring en komt algoritmes.overheid.nl in het
        <a
          class="is-external"
          target="_blank"
          href="https://www.toegankelijkheidsverklaring.nl/register"
        >
          Register van Toegankelijkheidsverklaringen van de overheid</a
        >.
      </p>
    </div>

    <div v-if="englishSelected">
      <h1>Accessibility</h1>

      <p class="mb-4">
        During the development of this website, anything deemed beneficial and
        any requirements to make it accessible are immediately incorporated. The
        development team has been trained in digital accessibility. An
        independent accessibility expert regularly provides advise.
      </p>
      <p class="mb-4">
        This site is under development and does not yet have an accessibility
        statement. The procedure for an accessibility statement will start in
        2023, and the website will be included in the government's
        <a
          class="is-external"
          target="_blank"
          href="https://www.toegankelijkheidsverklaring.nl/register"
        >
          Register van Toegankelijkheidsverklaringen</a
        >.
      </p>
    </div>
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
