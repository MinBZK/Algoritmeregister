<template>
  <div>
    <template v-for="question in questions" :key="question.key">
      <FaqAccordionRow :question="question" />
    </template>
  </div>
</template>

<script setup lang="ts">
import type { FooterFaqQuestion } from '@/types/footer'

defineProps<{
  questions: FooterFaqQuestion[]
}>()
</script>
