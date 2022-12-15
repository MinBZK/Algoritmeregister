<template>
  <div>
    <div v-if="!englishSelected">
      <h1>Privacy</h1>

      <p class="mb-2">
        Deze website maakt gebruik van analytische cookies. Cookies zijn kleine
        tekstbestanden die websites op uw computer opslaan. Daarmee is uw
        computer te herkennen tijdens uw bezoek. Deze informatie helpt ons om de
        site te verbeteren. Analytische cookies geven antwoord op de volgende
        vragen:
      </p>
      <ol type="1" class="ml-4">
        <li>
          Is de bezoeker nieuw of heeft de bezoeker de site al eerder bezocht
        </li>
        <li>Welke pagina's zijn tijdens het bezoek geraadpleegd</li>
        <li>Van welke site is de bezoeker gekomen</li>
        <li>Heeft de bezoeker de site meteen weer verlaten ('bouncing').</li>
      </ol>

      <p class="mb-4 mt-4">
        Deze cookies worden niet gebruikt om een profiel aan te maken of u
        verder te volgen. Deze website plaatst geen cookies van derde partijen
        (third-party cookies).
      </p>
      <h2>Gegevens via e-mail</h2>
      <p class="mb-4">
        De persoonlijke informatie die je ons verschaft in een e-mail behandelen
        we vertrouwelijk. Alleen wanneer je ons een vraag stelt, worden je
        gegevens voor de duur van de behandeling vastgelegd. Nadat je antwoord
        hebt gekregen, slaan we alleen de vraag en het antwoord op. Op verzoek
        verwijderen we ook de vraag en het antwoord. Wanneer je ons een bericht
        stuurt waarop geen antwoord gevraagd wordt, verwijderen wij je
        persoonlijke gegevens onmiddellijk.
      </p>
    </div>
    <div v-if="englishSelected">
      <h1>Privacy</h1>
      <p class="mb-2">
        This website uses analytical cookies only. Cookies are small text files
        that websites store on your computer. This makes it possible to
        recognize your computer during your visit. This information helps us to
        improve the site. Analytical cookies answer the following questions:
      </p>
      <ol type="1" class="ml-4">
        <li>
          Is this a new visitor or has the visitor visited the site before
        </li>
        <li>Which pages were consulted during the visit</li>
        <li>Which site was the visitor directed from</li>
        <li>Did the visitor immediately leave the site ('bouncing').</li>
      </ol>
      <p class="mb-4">
        The cookies are not used to create a profile or to follow you further.
        This website does not place third-party cookies.
      </p>
      <h2>Data received via email</h2>
      <p class="mb-4">
        We treat any personal information you provide by e-mail as confidential.
        Should you ask us a question, your personal data will only be kept while
        we are working on a response. Once we have answered the question only
        the question and our response will be recorded. On request, we can also
        delete the question after a response. If you send us a message that does
        not require a response, we will delete your personal data immediately.
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
