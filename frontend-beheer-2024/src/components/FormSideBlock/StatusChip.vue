<template>
  <v-chip
    prepend-icon="mdi-information-outline"
    class="chip-colours"
    rounded="pill"
  >
    {{ currentChip.text }}
    <v-menu
      activator="parent"
      scroll-strategy="none"
      location="right center"
      offset="10"
      open-on-hover
    >
      <v-card
        class="rounded-card"
        max-width="300px"
        rounded="lg"
        color="rgba(243, 237, 247)"
      >
        <v-card-text>
          <p class="font-weight-bold my-2">
            {{ currentChip.text }}
          </p>
          {{ currentChip.menuText }}
        </v-card-text>
      </v-card>
    </v-menu>
  </v-chip>
</template>

<script setup lang="ts">
import { useFormDataStore } from '@/store/form-data'
import { computed } from 'vue'

const dataStore = useFormDataStore()
const state = computed(() => dataStore.data.state)

interface Chip {
  text: string
  menuText: string
  backgroundColour: string
  backgroundColourHover: string
}

const currentChip = computed((): Chip => {
  // Show different chips based on the flow
  const flow = dataStore.orgFromData?.flow
  if (flow === 'ictu_last' || flow === 'self_publish_two') {
    if (state.value == 'STATE_1') return chips.notPublished!
    else if (state.value == 'STATE_2') return chips.released!
    else if (state.value == 'PUBLISHED') return chips.published!
  }
  if (state.value === undefined) return chips.notPublished!
  return chips.error!
})

const chips: Record<string, Chip> = {
  notPublished: {
    text: 'Niet gepubliceerd',
    menuText: 'Deze algoritmebeschrijving is nog niet gepubliceerd',
    backgroundColour: '#ffa5a2',
    backgroundColourHover: 'rgb(255, 81, 81)',
  },
  released: {
    text: 'Vrijgegeven, wachten op goedkeuring',
    menuText:
      'Deze algoritmebeschrijving wordt op dit moment beoordeeld door een eindredacteur',
    backgroundColour: '#fffd76',
    backgroundColourHover: 'rgb(246, 250, 24)',
  },
  published: {
    text: 'Gepubliceerd',
    menuText: 'Deze algoritmebeschrijving is gepubliceerd.',
    backgroundColour: '#91ff97',
    backgroundColourHover: 'rgb(82, 255, 30)',
  },
  error: {
    text: 'Er is iets foutgegaan',
    menuText:
      'Deze tekst hoor je niet te zien, neem aub contact op met de beheerder.',
    backgroundColour: 'red',
    backgroundColourHover: 'red',
  },
}

const backgroundColour = computed(() => currentChip.value.backgroundColour)
const hoveredBackground = computed(
  () => currentChip.value.backgroundColourHover
)
</script>

<style scoped lang="scss">
.chip-colours {
  background-color: v-bind(backgroundColour);
  &:hover {
    background-color: v-bind(hoveredBackground);
  }
  cursor: default;
}
</style>
