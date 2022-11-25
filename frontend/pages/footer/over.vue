<template>
  <Page>
    <h1>{{ t('paths./over') }}</h1>
    <div v-if="!englishSelected">
      <!-- <ol> -->
      <!-- <li> -->
      <h2>1. Wat is het Rijks ICT-dashboard?</h2>
      <p class="mb-4 ml-8">
        Op dit Rijks ICT-dashboard vindt u informatie over alle projecten van de
        rijksoverheid met een ICT-component van tenminste €5 miljoen, over de
        gehele looptijd van het project. Dit worden de ‘grote ICT-projecten’
        genoemd.
      </p>
      <!-- </li> -->
      <!-- <li> -->
      <h2>2. Doel Website</h2>
      <p class="mb-4 ml-8">
        Op het Rijks ICT-dashboard staat informatie over alle grote
        ICT-projecten van de rijksoverheid. De ministeries die verantwoordelijk
        zijn voor deze projecten leveren de gegevens aan.
      </p>
      <p class="mb-4 ml-8">
        Het dashboard laat de aantallen, kosten en voortgang van de grote
        ICT-projecten zien. Op de startpagina staat een overzicht van alle
        projecten, een grafische presentatie met rijksbrede informatie en
        trendgegevens en een overzicht van de meest actuele wijzigingen. Zoals
        nieuwe en aangepaste projecten, of grote en kleine aanpassingen in de
        projectgegevens.
      </p>
      <p class="mb-4 ml-8">
        Op de projectpagina’s staat specifieke informatie over de projecten.
      </p>
      <p class="mb-4 ml-8">
        Het Rijks ICT-dashboard is een website van de rijksoverheid. Het
        dashboard valt onder de verantwoordelijkheid van de minister van
        Binnenlandse Zaken en Koninkrijksrelaties.
      </p>
      <!-- </li> -->
      <!-- <li> -->
      <h2>3. Grote ICT projecten</h2>
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
      </p>
      <!-- </li> -->
      <!-- <li> -->
      <h2>4. Actualiteit</h2>
      <p class="mb-4 ml-8">
        De informatie over de projecten op het Rijks ICT-dashboard werken we
        regelmatig bij; per project minimaal één keer per jaar. Ook als de
        Tweede Kamer over het project wordt geïnformeerd, worden de gegevens
        geactualiseerd.
      </p>
      <!-- </li> -->
      <!-- <li> -->
      <h2>5. Wijzigingen binnen het project</h2>
      <p class="mb-4 ml-8">
        Tijdens een project kunnen belangrijke wijzigingen (‘herijkingen’)
        plaatsvinden die gevolgen hebben voor de inhoud, de doorlooptijd en de
        kostenschatting. De reden van deze wijzigingen wordt altijd aan de
        Tweede Kamer gemeld.
      </p>
      <p class="mb-4 ml-8">
        Een wijziging kan om verschillende redenen noodzakelijk zijn. Denk aan
        een nieuwe – politieke – eis, of aanpassingen vanwege een uitgevoerde
        kwaliteitstoets, of een veranderde looptijd van het project. Meer
        informatie over de verschillenden redenen en aanpassingen vindt u op de
        startpagina.
      </p>
      <!-- </li> -->
      <!-- <li> -->
      <h2>6. Open Data</h2>
      <p class="mb-4 ml-8">
        Alle gegevens uit het Rijks ICT-dashboard zijn ook als open data
        beschikbaar. Dat geldt voor de lopende en de afgeronde projecten. De
        gegevens vindt u in json-formaat en in xml-formaat.
      </p>
      <p class="mb-4 ml-8">
        Deze datasets van het Rijks ICT-dashboard zijn ook vermeld in het Open
        Dataportaal van de rijksoverheid.
      </p>
      <p class="mb-4 ml-8">
        De gegevens van een specifiek project kunt u downloaden. Op de
        projectpagina staat rechtsboven de optie ‘Exporteer project’. Hiermee
        downloadt u het CSV-bestand (met komma-gescheiden waarden). Dit bestand
        is circa 10 kB en kunt u openen met een spreadsheetprogramma, zoals
        Microsoft Excel of LibreOffice Calc.
      </p>
      <!-- </li> -->
      <!-- </ol> -->
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
  title: 'Over',
})
</script>
