<template>
  <Page>
    <div v-if="!englishSelected">
      <h1>Veelgestelde vragen</h1>
      <h2>1. Wat is het Algoritmeregister?</h2>
      <p class="mb-4">
        Op het algoritmeregister staat informatie over algoritmes die de
        overheid gebruikt. Zo is deze informatie vindbaar en beschikbaar voor
        burgers, hun belangenbehartigers, media en professionals.
      </p>
      <h2>2. Wat is het doel van deze website?</h2>
      <p class="mb-4">
        Wanneer algoritmes vindbaar en controleerbaar zijn, kunnen mensen
        daarmee hun recht halen. Bovendien kan iedereen bijdragen aan de
        menselijke maat in digitale overheidsprocessen.
      </p>
      <h2>3.Wat zijn algoritmes?</h2>
      <p class="mb-4">
        Een algoritme is een set van regels en instructies die een computer
        uitvoert. Algoritmes helpen bijvoorbeeld om problemen te analyseren maar
        ook om beslissingen te nemen. Zo kan de overheid grote hoeveelheden
        gegevens (data) combineren en analyseren.
      </p>
      Wil je meer weten over algoritmes?
      <a href="https://www.mediawijsheid.nl/algoritmes/">
        Bekijk de informatie op Mediawijsheid
      </a>
      of bekijk de (gratis)
      <a href="https://ethiek.ai-cursus.nl/home">Nationale AI-cursus. </a>
      <h2>
        4. Ik heb een vraag over een algoritme op deze site, waar kan ik deze
        stellen?
      </h2>
      <p>Vragen zijn welkom via algoritmeregister@minbzk.nl.</p>
      <h2>5. Staan alle algoritmes van de overheid op deze website?</h2>
      <p>
        Voorlopig nog niet. Op dit moment stelt een kopgroep van
        overheidsorganisaties hun algoritmes beschikbaar tijdens de ontwikkeling
        van het register. Samen met hen en toekomstige gebruikers verbeteren we
        zowel de site. als de kwaliteit van de informatie over deze algoritmen.
        Zo is de informatie optimaal bruikbaar. Daarnaast werken we eraan dat
        zoveel mogelijk overheidsorganisaties hun algoritmen via dit register
        publiceren.
      </p>
      <h2>6. Wie werken er aan het register?</h2>
      <p>
        Het ministerie van Binnenlandse Zaken en Koninkrijksrelaties en ICTU
        werkt samen met koploperorganisaties binnen de overheid aan de
        ontwikkeling. Dat zijn op dit moment UWV, RvIG, SVB, en de gemeentes
        Amsterdam, Rotterdam, Den Haag en Utrecht.
      </p>
    </div>

    <div v-if="englishSelected">
      <h1>Frequently asked questions</h1>
      <h2>1. What is the algorithm register?</h2>
      <p class="mb-4">
        algoritmeregister.nl will provide information about the algorithms used
        by the government. This makes the information visible, traceable and
        available to citizens and those who care for their advocacy, the media
        and professionals.
      </p>
      <h2>2. What is the aim of this website?</h2>
      <p class="mb-4">
        When algorithms can be tracked and audited, people can use it to protect
        their rights. It also means everyone can contribute to ensure digital
        government processes have a human dimension.
      </p>
      <h2>3. What are algorithms?</h2>
      <p class="mb-4">
        An algorithm is a set of rules and instructions performed by a computer.
        Algorithms help, for example, to analyse problems, but also to make
        decisions. This allows the government to combine and analyse large
        amounts of data.
      </p>
      Do you want to know more about algorithms? View the information on
      <a href="https://www.mediawijsheid.nl/algoritmes/"> Media Literacy </a>
      or view the (free)
      <a href="https://ethiek.ai-cursus.nl/home">National AI-course. </a>
      <h2>
        4. I have questions about an algorithm on this site, who do I contact?
      </h2>
      <p>Questions are always welcome: algoritmeregister@minbzk.nl.</p>
      <h2>
        5. Are all algorithms used by the government available on this website?
      </h2>
      <p>
        Not yet. At the moment, a leading group of government organizations is
        making their algorithms available during the development of the
        register. In collaboration with them and future users, we can
        continuously improve both the site and the quality of the information on
        these algorithms. This way the information we provide is useful. We are
        working hard to ensure that as many government organizations as possible
        publish their algorithms via this register.
      </p>
      <h2>6. Who develops and maintains the register?</h2>
      <p>
        The Ministry of the Interior and Kingdom Relations and ICTU collaborate
        with leading organizations within the government to develop the website.
        These organizations are UWV, RvIG, SVB, and the municipalities of
        Amsterdam, Rotterdam, The Hague and Utrecht.
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
  title: 'Vragen',
})
</script>
