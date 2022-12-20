<template>
  <div>
    <div v-if="!englishSelected">
      <h1>Privacy</h1>

      <p class="mb-2">
        Deze website maakt gebruik van analytische cookies. Cookies zijn kleine
        tekstbestanden die websites op jouw computer opslaan. Daarmee is jouw
        computer te herkennen tijdens uw bezoek. Deze informatie helpt het
        bouwteam om de site te verbeteren. Analytische cookies geven antwoord op
        bijvoorbeeld de volgende vragen:
      </p>
      <ul type="disc" class="ml-4">
        <li>
          Is de bezoeker nieuw of heeft de bezoeker de site al eerder bezocht
        </li>
        <li>Welke pagina's zijn tijdens het bezoek geraadpleegd</li>
        <li>Van welke site is de bezoeker gekomen</li>
        <li>Heeft de bezoeker de site meteen weer verlaten ('bouncing').</li>
      </ul>

      <p class="mb-4 mt-4">
        Deze cookies worden niet gebruikt om een profiel aan te maken of jou
        verder te volgen. Deze website plaatst geen cookies van derde partijen
        (third-party cookies).
      </p>
      <h2>Gegevens via e-mail</h2>
      <p class="mb-4">
        Persoonlijke informatie die via e-mail bij het Algoritmeregister bekend
        wordt, behandelt het team vertrouwelijk. Dergelijke persoonlijke
        gegevens bewaart het team alleen voor de duur van de behandeling van het
        bericht. Nadat je antwoord hebt gekregen of als er geen antwoord
        gevraagd wordt, slaat het team alleen de vraag en het antwoord op. Op
        verzoek verwijdert het team ook de vraag en het antwoord.
      </p>
    </div>
    <div v-if="englishSelected">
      <h1>Privacy</h1>
      <p class="mb-2">
        This website uses analytical cookies only. Cookies are small text files
        that websites store on your computer. This makes it possible to
        recognize your computer during your visit. This information helps the
        development team to improve the site. Analytical cookies answer the
        following questions:
      </p>
      <ul type="disc" class="ml-4">
        <li>
          Is this a new visitor or has the visitor visited the site before
        </li>
        <li>Which pages were consulted during the visit</li>
        <li>Which site was the visitor directed from</li>
        <li>Did the visitor immediately leave the site ('bouncing').</li>
      </ul>
      <p class="mb-4">
        The cookies are not used to create a profile or to follow you further.
        This website does not place third-party cookies.
      </p>
      <h2>Data received via email</h2>
      <p class="mb-4">
        Personal information that becomes known to the Algorithm Register by
        email is treated confidentially by the team. Such personal data will
        only be kept by the team while they work on a response to your message.
        Once the question is answered or if no question is asked, the team will
        only record the question itself and the answer to that question. Upon
        request, the question and answer can also be deleted.
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
  title: 'Privacyverklaring',
})
</script>
