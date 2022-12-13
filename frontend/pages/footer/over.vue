<template>
  <Page>
    <div v-if="!englishSelected">
      <h1>Over het Algoritmeregister van de overheid</h1>
      <p class="mb-4">
        De overheid werkt steeds meer digitaal en gebruikt daarvoor steeds meer
        algoritmes. Omdat digitalisering niet automatisch goed gaat, wil de
        overheid werken aan transparante en verantwoorde inzet van die
        algoritmes. Zodat de informatie over de algoritmes van de overheid voor
        iedereen beschikbaar is: burgers, hun belangenbehartigers, de media en
        (overheids)professionals.
      </p>
      <h2>Open ontwikkelen</h2>
      <p class="mb-4">
        Op algoritme.overheid.nl komen steeds meer algoritmes van de overheid te
        staan. Deze site werkt al, maar is nog volop in ontwikkeling. Het
        ministerie van Binnenlandse Zaken en Koninkrijksrelaties ontwikkelt het
        register op een open manier: iedereen mag meekijken.
      </p>
      <h2>Meedoen</h2>
      <p class="mb-4">
        Ben je (overheids)professional? Dan kan je nu al aansluiten.
      </p>
      <p class="mb-4">
        Wat kan je doen? Stel de algoritmes van je eigen organisaties
        beschikbaar voor het publiek via het Algoritmeregister. Of denk mee over
        de verdere ontwikkeling van het Algoritmeregister.
      </p>
      <p class="mb-4">
        Doe je mee? Neem dan contact op met:
        <a href="mailto:algoritmeregister@minbzk.nl">
          algoritmeregister@minbzk.nl</a
        >.
      </p>
      <h2>Open source software</h2>
      <p class="mb-4">
        algoritme.overheid.nl wordt ontwikkeld met open source software (volg
        ons op
        <a target="_blank" href="https://github.com/MinBZK/Algoritmeregister"
          >Github</a
        >). Deze site wordt ontwikkeld zodat deze voor zoveel mogelijk mensen
        bruikbaar is.
      </p>
    </div>

    <div v-if="englishSelected">
      <h1>About the Algorithm register of the government</h1>
      <p class="mb-4">
        The government increasingly works digitally and uses more and more
        algorithms when doing so. Since digitalisation not automatically works
        well, the government wants to provide transparency and responsible use
        of these algorithms. Information about the algorithms used by the
        government is available for all: citizens, their supporters, the media
        and (government) professionals.
      </p>
      <h2>Open development</h2>
      <p class="mb-4">
        More and more algorithms used by the Dutch government will be published
        at algoritme.overheid.nl. This site is live and under continuous
        development. The Ministry of the Interior and Kingdom relations is using
        an open development method to develop the register, meaning everyone can
        view our progress and join in.
      </p>
      <h2>Joining in</h2>
      <p class="mb-4">
        Are you a (government) professional? Then you can join in. Make the
        algorithms of your own government organisation available to the public
        via the Algorithm register. Or make suggestions for further development
        of the Algorithm register.
      </p>
      <p class="mb-4">
        Please contact us at:
        <a href="mailto:algoritmeregister@minbzk.nl">
          algoritmeregister@minbzk.nl</a
        >.
      </p>
      <h2>Open source software</h2>
      <p class="mb-4">
        algoritme.overheid.nl is developed with open source software (follow us
        on
        <a target="_blank" href="https://github.com/MinBZK/Algoritmeregister"
          >Github</a
        >). This website is being developed to serve as many people as possible.
      </p>
    </div>
  </Page>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const englishSelected = computed(() => {
  return t(`english?`) === 'true'
})
definePageMeta({
  title: 'Over',
})
</script>
