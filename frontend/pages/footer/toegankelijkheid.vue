<template>
  <Page>
    <h1>{{ t('paths./toegankelijkheid') }}</h1>
    <div v-if="!englishSelected">
      <p class="mb-4">
        Rijksoverheid.nl wil dat iedereen deze website kan gebruiken. Komt u
        toch een pagina tegen die niet toegankelijk is? Dan kunt u dit aan ons
        melden.
      </p>
      <h2>Wat is een toegankelijke website?</h2>
      <p class="mb-4">
        Een toegankelijke website is voor alle doelgroepen beter te gebruiken.
        Daarom staat in het Tijdelijk besluit digitale toegankelijkheid overheid
        dat overheidssites moeten voldoen aan toegankelijkheidseisen zoals
        vastgelegd in EN 301 549/WCAG 2.1 en daarover verantwoording moeten
        afleggen in een gepubliceerde toegankelijkheidsverklaring.
      </p>
      <p class="mb-4">
        Wij borgen een goede toegankelijkheid van onze website door diverse
        maatregelen binnen onze (dagelijkse) processen.
      </p>
      <h2>Garanderen toegankelijkheid</h2>

      <p class="mb-4">
        Wij garanderen een goede toegankelijkheid door diverse maatregelen
        binnen onze (dagelijkse) processen:
      </p>
      <ul class="mb-4 ml-5">
        <li>
          Toegankelijkheid ‘by design’: toegankelijkheid is vanaf de start
          onderdeel van alle stappen in het ontwerp-, bouw en redactionele
          proces van onze website.
        </li>
        <li>
          Onderzoek: onafhankelijke deskundigen toetsen regelmatig (onderdelen
          van) de website op toegankelijkheid. Zowel voor de
          functioneel-technische onderdelen als de redactionele aspecten.
          Gevonden knelpunten lossen wij duurzaam op.
        </li>
        <li>
          Kennis medewerkers: onze medewerkers houden hun kennis over
          toegankelijkheid op peil en passen dit toe waar nodig.
        </li>
      </ul>
      <h2>Onderdelen waarop de website niet voldoet</h2>
      <ul class="mb-4 ml-5">
        <li>
          <p>
            Sommige nieuwsvideo’s zijn niet meteen toegankelijk. De
            ondertiteling volgt dan een paar dagen later.
          </p>
          <p>
            Alle toegankelijkheidseisen uit de norm WCAG 2.1 gelden voor de
            pdf-bestanden op Rijksoverheid.nl. Het streven van Rijksoverheid.nl
            is om alle pdf-bestanden volgens de norm WCAG 2.1 aan te bieden.
          </p>
        </li>
        <li>
          Rijksoverheid.nl heeft oude documenten en nieuwsberichten niet
          aangepast aan de toegankelijkheidseisen.
        </li>
      </ul>
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
  title: 'Toegankelijkheid',
})
</script>
