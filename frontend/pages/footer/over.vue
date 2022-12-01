<template>
  <Page>
    <div v-if="!englishSelected">
      <h1>Over het Algoritmeregister van de overheid</h1>
      <p class="mb-4 ml-8">
        De overheid werkt steeds meer digitaal en gebruikt daarvoor steeds meer
        algoritmes. Omdat digitalisering niet automatisch goed gaat, wil de
        overheid werken aan transparante en verantwoorde inzet van die
        algoritmes. Zodat de informatie over de algoritmes van de overheid voor
        iedereen beschikbaar is: burgers, hun belangenbehartigers, media en
        (overheids)professionals.
      </p>
      <h2>Open ontwikkelen</h2>
      <p class="mb-4 ml-8">
        Op algoritme.overheid.nl komen steeds meer algoritmes van de overheid te
        staan. Deze site werkt al, maar is nog volop in ontwikkeling. Het
        ministerie van Binnenlandse Zaken en Koninkrijksrelaties ontwikkelt het
        register op een open manier: iedereen mag meekijken.
      </p>
      <h2>Meedoen</h2>
      <p class="mb-4 ml-8">
        (Overheids)professionals kunnen zich nu al aansluiten. Wat kun je doen? 
        <ul>
          <li>
            Stel de algoritmes van je eigen overheidsorganisaties via het Algoritmeregister van de overheid beschikbaar voor het publiek.
          </li>
          <li>
            Denk mee over de verdere ontwikkeling van het Algoritmeregister. 
          </li>
        </ul>
Doe je mee? Neem dan direct contact op: algoritmeregister@minbzk.nl.

      </p>
      <h2>Open source en toegankelijkheid</h2>
      <p class="mb-4 ml-8">
        Algoritme.overheid.nl wordt ontwikkeld met opensource software (volg ons op Github). Deze site wordt ontwikkeld zodat deze voor zoveel mogelijk mensen bruikbaar is. Dat betekent dat we werken met de eisen voor digitale toegankelijkheid. 
      </p>
      
    </div>

    <div v-if="englishSelected">
      <h1>About the Algorithm register of the government</h1>
      <p class="mb-4 ml-8">
        The government increasingly works digitally and uses more and more algorithms when doing so. Since digitalization not automatically works well, the government wants to provide transparency and responsible use of these algorithms. Information about the algorithms used by the government is available for all: citizens, their advocates, the media and (government) professionals.
      </p>
      <h2>Open development</h2>
      <p class="mb-4 ml-8">
        More and more algorithms used by the Dutch government will be published at algoritme.overheid.nl. This site is live, but is under constant development. The Ministry of the Interior and Kingdom relations is using an open development method to develop the register, meaning everyone can view our progress and join in.
      </p>
      <h2>Joining in</h2>
      <p class="mb-4 ml-8">
        (Government) professionals can join already. How can you contribute?
        <ul>
          <li>
            Make the algorithms of your own government organization available to the public via the algorithm register 
          </li>
          <li>
            Make suggestions for further development of the algorithm register. 
          </li>
        </ul>
        Interested? Contact us via algoritmeregister@minbzk.nl.

      </p>
      <h2>Open source and accessibility</h2>
      <p class="mb-4 ml-8">
        Algoritme.overheid.nl wordt ontwikkeld met opensource software (volg ons op Github). Deze site wordt ontwikkeld zodat deze voor zoveel mogelijk mensen bruikbaar is. Dat betekent dat we werken met de eisen voor digitale toegankelijkheid. 
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
  title: 'Over',
})
</script>
