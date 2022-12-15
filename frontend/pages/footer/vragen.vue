<template>
  <div>
    <div v-if="!englishSelected">
      <h1>Veelgestelde vragen</h1>
      <h2>1. Wat is het Algoritmeregister?</h2>
      <p class="mb-4">
        Op het Algoritmeregister staat informatie over algoritmes die de
        overheid gebruikt. Zo is deze informatie vindbaar en beschikbaar voor
        burgers, hun belangenbehartigers, de media en toezichthouders.
      </p>
      <h2>2. Wat is het doel van deze website?</h2>
      <p class="mb-4">
        Het doel is informatie over algoritmes voor iedereen centraal vindbaar
        te laten zijn. Op die manier kan iedereen zien in welke impactvolle
        processen algoritmes gebruikt worden. De informatie geeft de
        mogelijkheid om toezicht te houden op algoritmes. Zo kan gekeken worden
        naar discriminatie en onrechtmatigheid, maar ook de wenselijkheid.
        Wanneer mensen het niet eens zijn met het gebruik van algoritmes, geeft
        het Algoritmeregister aan waar bezwaar gemaakt kan worden.
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
        <a
          target="_blank"
          class="is-external"
          href="https://www.mediawijsheid.nl/algoritmes/"
        >
          Bekijk de informatie op Mediawijsheid</a
        >
        of bekijk de (gratis)
        <a
          target="_blank"
          class="is-external"
          href="https://ethiek.ai-cursus.nl/home"
          >Nationale AI-cursus</a
        >.
      </p>

      <h2>
        4. Ik heb een vraag over een algoritme op deze site, waar kan ik deze
        stellen?
      </h2>
      <p class="mb-4">
        Het kan natuurlijk ook dat je na het lezen van de registratie van een
        algoritme vragen hebt over een specifiek algoritme. Die kun je stellen
        aan de ‘eigenaar’ van het algoritme. De contactgegevens vind je in de
        beschrijving van het algoritme. Alle overige vragen kun je sturen naar:
        <a href="mailto:algoritmeregister@minbzk.nl">
          algoritmeregister@minbzk.nl</a
        >.
      </p>
      <h2>5. Staan alle algoritmes van de overheid op deze website?</h2>
      <p class="mb-4">
        Op dit moment stelt een kopgroep van overheidsorganisaties hun
        algoritmes beschikbaar via deze website. In 2023 publiceren nog meer
        overheidsorganisaties in het Algoritmeregister. Voorlopig gaat het
        aantal algoritmes op deze website dus nog groeien.
      </p>
      <p class="mb-4">
        In de toekomst wordt het wettelijk verplicht algoritmes publiekelijk
        beschikbaar te maken. Daardoor komen de meeste relevante algoritmes in
        het Algoritmeregister. Hierop zullen gerechtvaardigde uitzonderingen
        komen. Denk aan opsporing, rechtshandhaving, defensie of
        inlichtingenverzameling. De exacte kaders worden nog uitgewerkt.
      </p>
      <h2>
        6. Bij sommige algoritmes staat meer informatie dan bij andere
        algoritmes?
      </h2>
      <p class="mb-4">
        Momenteel gebeurt het vullen van het Algoritmeregister vrijwillig door
        overheidsorganisaties. Niet elke organisatie heeft ervoor gekozen alle
        informatie te publiceren. Uiteindelijk wordt er wettelijk vastgelegd
        welke informatie verplicht aangeleverd moet worden, en welke informatie
        optioneel is.
      </p>
      <h2>7. Wie werken er aan het Algoritmeregister?</h2>
      <p class="mb-4">
        De ontwikkeling van het Algoritmeregister is begonnen met het consortium
        Publieke controle op algoritmen. Daarin werkten overheidsorganisaties
        aan beleidsinstrumenten voor een verantwoorde inzet van algoritmen. Een
        van de resultaten is onderzoek naar het Algoritmeregister. Het
        ministerie van Binnenlandse Zaken en Koninkrijksrelaties heeft
        voortgebouwd op deze opgedane kennis om tot dit Algoritmeregister te
        komen. Voor het ontwikkelen van de website werkt het ministerie samen
        met ICTU. In het Algoritmeregister is te zien welke organisaties op dit
        moment algoritmes aangeleverd hebben voor het Algoritmeregister. Kijk
        daarvoor onder het kopje Algoritmes, hier staan alle organisaties die nu
        één of meerdere algoritmes hebben aangeleverd.
      </p>
      <h2>
        8. Hoe verhouden de algoritmeregisters van overheidsorganisaties zich
        tot deze website?
      </h2>
      <p class="mb-4">
        Het Algoritmeregister is de centrale vindplek voor alle algoritmes van
        de overheid. Sommige overheidsorganisaties hebben daarnaast ook een
        eigen algoritmeregister. Organisaties hebben daar de mogelijkheid om
        meer informatie te bieden of op andere wijze. In de huidige versie is de
        informatie handmatig overgenomen. In 2023 wordt gewerkt aan de
        mogelijkheid van automatische uitwisseling.
      </p>
    </div>

    <div v-if="englishSelected">
      <h1>Frequently asked questions</h1>
      <h2>1. What is the Algorithm Register?</h2>
      <p class="mb-4">
        This website provides information about the algorithms used by the
        government. This makes the information visible, traceable and accessible
        to citizens and their representatives, the media and supervisors.
      </p>
      <h2>2. What is the aim of this website?</h2>
      <p class="mb-4">
        The aim is to make all information about algorithms centrally accessible
        for everyone. That allows everyone to see in which impactful processes
        these algorithms are used. The information on this website provides the
        ability to oversee algorithms. For example, discrimination or
        unlawfulness can be exposed, and whether the algorithm provides
        desirable outcomes can be checked. When someone does not agree with the
        use of algorithms, the Algorithm Register indicates how objections can
        be made.
      </p>
      <h2>3. What are algorithms?</h2>
      <p class="mb-4">
        An algorithm is a set of rules and instructions executed by a computer.
        Algorithms help, for example, to analyse problems, but also to make
        decisions. This allows the government to combine and analyse large
        amounts of data. (source: Algemene Rekenkamer)
      </p>
      <p class="mb-4">
        Do you want to know more about algorithms? Find more information on
        <a
          target="_blank"
          class="is-external"
          href="https://www.mediawijsheid.nl/algoritmes/"
        >
          Mediawijsheid</a
        >
        or take the (free)
        <a
          target="_blank"
          class="is-external"
          href="https://ethiek.ai-cursus.nl/home"
          >National AI-course</a
        >.
      </p>

      <h2>
        4. I have questions about an algorithm on this site, who do I contact?
      </h2>
      <p class="mb-4">
        If you have a question about a specific algorithm, please contact the
        ‘owner’ of the algorithm. Contact details can be found in the
        description of the algorithm.
        <p class="mb-4">
          For any other questions please email:
               <a href="mailto:algoritmeregister@minbzk.nl">
          algoritmeregister@minbzk.nl</a
        >.
        </p>
   
      </p>
      <h2>5. Are all algorithms used by the government available on this website? </h2>
      <p class="mb-4">
        A leading group of government organisations is currently making their algorithms available via this website. In 2023, even more government organisations will publish their algorithms in the Algorithm Register. For the time being, the number of algorithms on this website will continue to grow. 
      </p>
      <p class="mb-4">
        In the future, it will become a legal requirement to make algorithms publicly available. As a result, most relevant algorithms will become available in the Algorithm Register. There will be justified exceptions to this. For example, certain algorithms used for investigation, law enforcement, defense or intelligence gathering. The exact framework is still being finalized. 
      </p>
      <h2>
        6. Why do some algorithms contain more information than others? 
      </h2>
      <p class="mb-4">
        Currently, the Algorithm Register is completed voluntarily by government organisations. Not every organisation has chosen to publish all information. Ultimately, it will be legally defined which information is mandatory and which information is optional. 
      </p>
      <h2>7. Who develops and maintains the Algorithm Register? </h2>
      <p class="mb-4">
        The development of the Algorithm Register was started by the Public Control of Algorithms Consortium. In it, government organisations worked on policy instruments for the responsible use of algorithms. One of the outcomes of that work was research into the creation of a register of algorithms. The Ministry of the Interior and Kingdom Relations has built on knowledge gained from this research to create this Algorithm Register. The ministry is working with ICTU to develop this website. All organisations that have currently supplied one or more algorithms to the Algorithm Register can be found under the heading ‘Algorithms’. 
      </p>
      <h2>
        8. How do algorithm registers of individual government organisations relate to this website? 
      </h2>
      <p class="mb-4">
        The Algorithm Register is the central location for all government algorithms. Some government organisations also have their own algorithm register. This gives organisations the opportunity to provide more information or to provide it in a different way. In the current version of this website, information was entered manually. In 2023, the possibility of an automatic upload will be investigated. 
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
  title: 'Vragen',
})
</script>
