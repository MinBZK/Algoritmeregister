<template>
  <Page>
    <h1>{{ t('paths./kwetsbaarheid') }}</h1>
    <div v-if="!englishSelected">
      <p class="mb-4">
        Ontdekt u een zwakke plek of kwetsbaarheid op deze website, meld dit dan
        aan het Nationaal Cyber Security Centrum (NCSC). Het maken van zo'n
        melding heet Coordinated Vulnerability Disclosure (CVD).
      </p>
      <p class="mb-4">
        <a
          target="_blank"
          href="https://www.ncsc.nl/contact/kwetsbaarheid-melden"
        >
          Klik hier om een kwetsbaarheid te melden.
        </a>
      </p>

      <p class="mb-4">
        Wij bekijken samen met het NCSC het probleem en lossen dit zo snel
        mogelijk op.
      </p>
    </div>

    <div v-if="englishSelected">
      <p class="mb-4">
        If you discover any weaknesses or vulnerabilities on this website,
        please report this to the National Cyber Security Centre (NCSC). A
        report like this is called a Coordinated Vulnerability Disclosure (CVD).
      </p>
      <p class="mb-4">
        We will discuss the issue with the NCSC and resolve it as soon as
        possible.
      </p>
      <p class="mb-4">
        <a
          target="_blank"
          href="https://www.ncsc.nl/contact/kwetsbaarheid-melden"
        >
          Report vulnerability
        </a>
      </p>
    </div>
  </Page>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const englishSelected = computed(() => {
  return t(`english?`) == 'true'
})

definePageMeta({
  title: 'Kwetsbaarheid',
})
</script>
