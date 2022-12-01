<template>
  <Page>
    <div v-if="!englishSelected">
      <h1>Privacy</h1>

      <p class="mb-2">
        Deze website maakt alleen gebruik van analytische cookies. Cookies zijn
        kleine tekstbestanden die websites op uw computer opslaan. Daarmee is uw
        computer te herkennen tijdens uw bezoek. Deze informatie helpt ons om de
        site te verbeteren. Analytische cookies geven antwoord op de volgende
        vragen:
        </p>
        <p class="mb-4">
                  <ol>
          <li class="ml-4">
            Is de bezoeker nieuw of heeft de bezoeker de site al eerder bezocht? 
          </li>
          <li class="ml-4">
            Welke pagina's zijn tijdens het bezoek geraadpleegd?
          </li>
          <li class="ml-4">
            Van welke site is de bezoeker gekomen?
          </li>
          <li class="ml-4">
            Heeft de bezoeker de site meteen weer verlaten (het zogenaamde 'bouncing')? 
          </li>
        </ol>
      </p>
      <p class="mb-4">
        Deze cookies worden dus niet gebruikt om een profiel aan te maken of u verder te volgen. Algoritmeregister.overheid.nl plaatst ook geen cookies van derde partijen (zogenaamde third-party cookies). 
        </p>
        <h2>Gegevens via e-mail</h2>
        <p class="mb-4">
          De persoonlijke informatie die je ons verschaft in een e-mail behandelen we vertrouwelijk. Alleen wanneer je ons een vraag stelt, worden je gegevens voor de duur van de behandeling vastgelegd. Nadat je antwoord hebt gekregen, slaan we alleen de vraag en het antwoord op. Op verzoek verwijderen we ook de vraag en het antwoord. Wanneer je ons een bericht stuurt waarop geen antwoord gevraagd wordt, verwijderen wij je persoonlijke gegevens onmiddellijk.
        </p>
    </div>
    <div v-if="englishSelected">
      <h1>Privacy</h1>
      <p class="mb-2">
        This website uses analytical cookies only. Cookies are small text files that websites store on your computer. This makes it possible to recognize your computer during your visit. This information helps us to improve the site. Analytical cookies answer the following questions:
        </p>
        <p class="mb-4">
                  <ol>
          <li class="ml-4">
            Is this a new visitor or has the visitor visited the site before?
          </li>
          <li class="ml-4">
            Which pages were consulted during the visit?
          </li>
          <li class="ml-4">
            Which site was the visitor directed from?
          </li>
          <li class="ml-4">
            Did the visitor immediately leave the site (so-called 'bouncing')?
          </li>
        </ol>
      </p>
      <p class="mb-4">
        These cookies are therefore not used to create a profile or to follow you further. algorithmregister.overheid.nl also does not place third-party cookies.        </p>
        <h2>Data received via email</h2>
        <p class="mb-4">
          We treat any personal information you provide by e-mail as confidential. Should you ask us a question, your personal data will only be kept while we are working on a response. Once we have answered the question only the question and our response will be recorded. On request, we can also delete the question after a response. If you send us a message that does not require a response, we will delete your personal data immediately.        </p>
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
  title: 'Privacyverklaring',
})
</script>
