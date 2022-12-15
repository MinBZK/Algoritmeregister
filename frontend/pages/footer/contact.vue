<template>
  <div>
    <div v-if="!englishSelected">
      <h1>Neem contact op</h1>
      <p class="mb-4">
        Deze site is volop in ontwikkeling. Heb je vragen over het
        Algoritmeregister? Of ben je een (overheids)professional en wil jij of
        je organisatie meedoen aan de verdere ontwikkeling van het
        Algoritmeregister? Kijk naar de informatie op
        <NuxtLink :to="`/footer/over`" class="link">
          Over deze website</NuxtLink
        >
        en de
        <NuxtLink :to="`/footer/vragen`" class="link">
          Veelgestelde vragen</NuxtLink
        >.
      </p>
      <p class="mb-4">
        Heb je toch nog een vraag? Neem dan contact op met:
        <a href="mailto:algoritmeregister@minbzk.nl">
          algoritmeregister@minbzk.nl</a
        >.
      </p>
    </div>

    <div v-if="englishSelected">
      <h1>Contact us</h1>
      <p class="mb-4">
        This site is under development. Do you have questions about the
        Algorithm Register? Or are you a (government) professional and do you or
        your organisation want to participate in the further development of the
        Algorithm Register? Find more information at

        <NuxtLink :to="`/footer/over`" class="link">
          About this website</NuxtLink
        >
        and

        <NuxtLink :to="`/footer/vragen`" class="link">
          Frequently asked questions</NuxtLink
        >.
      </p>
      <p class="mb-4">
        If you have further questions, then please contact:
        <a href="mailto:algoritmeregister@minbzk.nl">
          algoritmeregister@minbzk.nl</a
        >.
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
  title: 'Contact',
})
</script>
