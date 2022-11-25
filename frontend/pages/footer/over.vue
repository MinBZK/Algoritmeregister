<template>
  <Page>
    <h1>{{ t('paths./over') }}</h1>
    <div v-if="!englishSelected">
      <!-- <ol> -->
      <!-- <li> -->
      <h2>1. Wat is het Algoritmeregister?</h2>
      <p class="mb-4 ml-8">
        Op het algoritmeregister vindt u informatie over algoritmes in gebruik
        door de overheid.
      </p>
      <!-- </li> -->
      <!-- <li> -->
      <h2>2. Doel Website</h2>
      <p class="mb-4 ml-8">
        Op het algoritmeregister vindt u informatie over algoritmes in gebruik
        door de overheid. De entiteiten die verantwoordelijk zijn voor deze
        algoritmes leveren de gegevens aan.
      </p>
      <!-- <p class="mb-4 ml-8">
        Het register laat de aantallen, kosten en voortgang van de grote
        ICT-projecten zien. Op de startpagina staat een overzicht van alle
        projecten, een grafische presentatie met rijksbrede informatie en
        trendgegevens en een overzicht van de meest actuele wijzigingen. Zoals
        nieuwe en aangepaste projecten, of grote en kleine aanpassingen in de
        projectgegevens.
      </p> -->
      <p class="mb-4 ml-8">
        Op de algoritmepagina's staan specifieke informatie over de projecten.
      </p>
      <p class="mb-4 ml-8">
        Het algoritmeregister is een website van de rijksoverheid. Het register
        valt onder de verantwoordelijkheid van de minister van Binnenlandse
        Zaken en Koninkrijksrelaties.
      </p>
      <!-- </li> -->
      <!-- <li> -->
      <!-- <h2>3. Grote ICT projecten</h2>
      <p class="mb-4 ml-8">
        Grote ICT-projecten zijn de projecten met een ICT-component van meer dan
        €5 miljoen over de gehele looptijd van het project. Met de meerjarige
        ICT-kosten worden de producten, diensten en resultaten van het project
        gerealiseerd. De ICT-kosten zijn opgenomen in de rijksbegroting, of in
        de begroting van de publieksrechtelijke zelfstandig bestuursorganen
        (zbo’s), en worden hierin verantwoord.
      </p>
      <p class="mb-4 ml-8">
        Ieder jaar staat in de Jaarrapportage Bedrijfsvoering Rijk een overzicht
        van alle in dat jaar actieve projecten, met de belangrijkste data en
        cijfers. Een geactualiseerde versie van dit jaarlijkse overzicht is
        hieronder beschikbaar. Als een project in het geselecteerde jaar nog
        geen wijzigingen heeft doorgevoerd, dan wordt de laatst bekende situatie
        getoond.
      </p>
      <p class="mb-4 ml-8">
        <b
          >Download hieronder het CSV-bestand. Dit bestand is circa 1 MB en kunt
          u openen met een spreadsheetprogramma, zoals Microsoft Excel of
          LibreOffice Calc.</b
        >
      </p> -->
      <!-- </li> -->
      <!-- <li> -->
      <h2>3. Actualiteit</h2>
      <p class="mb-4 ml-8">
        De informatie over de algoritmes op het register werken we regelmatig
        bij; per project minimaal één keer per jaar. Ook als de Tweede Kamer
        over het project wordt geïnformeerd, worden de gegevens geactualiseerd.
      </p>
      <!-- </li> -->
      <!-- <li> -->
      <h2>4. Wijzigingen binnen het algoritme</h2>
      <p class="mb-4 ml-8">
        Er kunnen belangrijke wijzigingen plaatsvinden die gevolgen hebben voor
        de inhoud.
        <!-- De reden van deze wijzigingen wordt altijd aan de
        Tweede Kamer gemeld. -->
      </p>
      <p class="mb-4 ml-8">
        Een wijziging kan om verschillende redenen noodzakelijk zijn. Denk aan
        een nieuwe – politieke – eis of aanpassingen vanwege een uitgevoerde
        kwaliteitstoets.
        <!-- Meer
        informatie over de verschillenden redenen en aanpassingen vindt u op de
        startpagina. -->
      </p>
      <!-- </li> -->
      <!-- <li> -->
      <!-- <h2>5. Open Data</h2>
      <p class="mb-4 ml-8">
        Alle gegevens uit het Algoritmeregister zijn ook als open data
        beschikbaar. Dat geldt voor de lopende en de afgeronde projecten. De
        gegevens vindt u in json-formaat en in xml-formaat.
      </p>
      <p class="mb-4 ml-8">
        Deze datasets van het Algoritmeregister zijn ook vermeld in het Open
        Dataportaal van de rijksoverheid.
      </p>
      <p class="mb-4 ml-8">
        De gegevens van een specifiek project kunt u downloaden. Op de
        projectpagina staat rechtsboven de optie ‘Exporteer project’. Hiermee
        downloadt u het CSV-bestand (met komma-gescheiden waarden). Dit bestand
        is circa 10 kB en kunt u openen met een spreadsheetprogramma, zoals
        Microsoft Excel of LibreOffice Calc.
      </p> -->
      <!-- </li> -->
      <!-- </ol> -->
    </div>

    <div v-if="englishSelected">
      <p class="mb-4">
        This website lists information on algorithms currently used by the Dutch
        government.
      </p>
      <p class="mb-4">
        This site currently is still in its infancy and more information and
        functionality will be added in time.
      </p>
      <p class="mb-4">
        This website is an initiative of the ministry of Interior Affairs and
        Kingdom Relations in close co operation with all parts of central,
        regional and local government of the Netherlands.
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
