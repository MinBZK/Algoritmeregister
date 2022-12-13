<template>
  <Page>
    <div v-if="!englishSelected">
      <h1>Veelgestelde vragen</h1>
      <h2>1. Wat is het Algoritmeregister?</h2>
      <p class="mb-4">
        Op het Algoritmeregister staat informatie over algoritmes die de
        overheid gebruikt. Zo is deze informatie vindbaar en beschikbaar voor
        burgers, hun belangenbehartigers, de media en professionals.
      </p>
      <h2>2. Wat is het doel van deze website?</h2>
      <p class="mb-4">
        Het doel is informatie over algoritmes voor iedereen beschikbaar laten
        zijn. Wanneer algoritmes vindbaar en controleerbaar zijn, kunnen mensen
        daarmee hun recht halen. Bovendien kan iedereen bijdragen aan de
        menselijke maat in digitale overheidsprocessen.
      </p>
      <h2>3. Wat zijn algoritmes?</h2>
      <p class="mb-4">
        Een algoritme is een set van regels en instructies die een computer
        uitvoert. Algoritmes helpen bijvoorbeeld om problemen te analyseren maar
        ook om beslissingen te nemen. Zo kan de overheid grote hoeveelheden
        gegevens (data) combineren en analyseren. (bron: Algemene Rekenkamer).
      </p>
      <p class="mb-4">
        Wil je meer weten over algoritmes?
        <a target="_blank" href="https://www.mediawijsheid.nl/algoritmes/">
          Bekijk de informatie op Mediawijsheid
        </a>
        of bekijk de (gratis)
        <a target="_blank" href="https://ethiek.ai-cursus.nl/home"
          >Nationale AI-cursus.
        </a>
      </p>

      <h2>
        4. Ik heb een vraag over een algoritme op deze site, waar kan ik deze
        stellen?
      </h2>
      <p class="mb-4">
        Vragen? Neem contact op met:
        <a href="mailto:algoritmeregister@minbzk.nl">
          algoritmeregister@minbzk.nl</a
        >.
      </p>
      <h2>5. Staan alle algoritmes van de overheid op deze website?</h2>
      <p class="mb-4">
        Voorlopig nog niet. Op dit moment stelt een kopgroep van
        overheidsorganisaties hun algoritmes al beschikbaar. Samen verbeteren we
        de website en de kwaliteit van de informatie. Zo is de informatie
        optimaal bruikbaar. Daarnaast werken we eraan dat alle
        overheidsorganisaties hun algoritmes via dit register publiceren.
      </p>
      <h2>6. Wie werken er aan het register?</h2>
      <p class="mb-4">
        Het ministerie van Binnenlandse Zaken en Koninkrijksrelaties en ICTU
        werken samen met een kopgroep binnen de overheid aan de ontwikkeling.
        Dat zijn op dit moment UvW, RvIG, SVB, en de gemeentes Amsterdam,
        Rotterdam, Den Haag en Utrecht.
      </p>
    </div>

    <div v-if="englishSelected">
      <h1>Frequently asked questions</h1>
      <h2>1. What is the Algorithm register?</h2>
      <p class="mb-4">
        This website provides information about the algorithms used by the
        government. This makes the information visible, traceable and available
        to citizens and their supporters, the media and professionals.
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
      <p class="mb-4">
        Do you want to know more about algorithms? View the information on
        <a target="_blank" href="https://www.mediawijsheid.nl/algoritmes/">
          Media Literacy
        </a>
        or view the (free)
        <a target="_blank" href="https://ethiek.ai-cursus.nl/home"
          >National AI-course.
        </a>
      </p>

      <h2>
        4. I have questions about an algorithm on this site, who do I contact?
      </h2>
      <p class="mb-4">
        Questions are always welcome at:
        <a href="mailto:algoritmeregister@minbzk.nl">
          algoritmeregister@minbzk.nl</a
        >.
      </p>
      <h2>
        5. Are all algorithms used by the government available on this website?
      </h2>
      <p class="mb-4">
        Not yet. At the moment, a leading group of government organisations is
        making their algorithms available during the development of the
        register. In collaboration with them and future users, we can
        continuously improve both the site and the quality of the information on
        these algorithms. This way the information we provide is useful. We are
        working hard to ensure that as many government organisations as possible
        publish their algorithms via this register.
      </p>
      <h2>6. Who develops and maintains the register?</h2>
      <p class="mb-4">
        The Ministry of the Interior and Kingdom Relations and ICTU collaborate
        with leading organizations within the government to develop the website.
        These organizations are UvW, RvIG, SVB, and the municipalities of
        Amsterdam, Rotterdam, The Hague and Utrecht.
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
  title: 'Vragen',
})
</script>
