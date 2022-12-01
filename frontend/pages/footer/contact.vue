<template>
  <Page>
    <div v-if="!englishSelected">
      <h1>Contact over het algoritmeregister van de overheid</h1>
      <p class="mb-4">Deze site is nog volop in ontwikkeling.</p>
      <p class="mb-4">
        Ben je een (overheids)professionals en wil jij of je organisatie meedoen
        aan de verdere ontwikkeling van het Algoritmeregisteroverheid.nl? Of heb
        je andere vragen over dit project? .Neem dan direct contact op
        algoritmeregister@minbzk.nl.
      </p>
    </div>

    <div v-if="englishSelected">
      <h1>
        How to get in contact about the Dutch Government algorithm register
      </h1>
      <p class="mb-4">This site is continuously developing.</p>
      <p class="mb-4">
        Are you a (government) professional and do you or your organization want
        to contribute to the development of algoritme.overheid.nl? Or do you
        have questions about the project? Please contact algoritme.overheid.nl
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
  title: 'Contact',
})
</script>
