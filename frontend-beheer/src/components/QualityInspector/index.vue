<template>
  <v-card
    flat
    border
    class="px-9 pb-5"
  >
    <v-card-title> Vulling: </v-card-title>
    <v-row>
      <v-col cols="10">
        <ScoreDisplay :progress="scoreStore.progress" />
      </v-col>
      <v-col>
        <ScoreSummaryBlock
          :variant="scoreStore.summaryVariant"
          :text="`${scoreStore.progress}%`"
        />
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import ScoreSummaryBlock from './ScoreSummaryBlock.vue'
import ScoreDisplay from './ScoreDisplay.vue'
import { useScoreStore } from '@/store/score'

const scoreStore = useScoreStore()
</script>
