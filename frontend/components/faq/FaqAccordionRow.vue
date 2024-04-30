<template>
  <div :id="question.anchor">
    <div
      class="question-header"
      :aria-expanded="expanded ? 'true' : 'false'"
      tabindex="0"
      role="button"
      @keydown.enter="toggleQuestion()"
      @keydown.space.prevent="toggleQuestion()"
      @click="toggleQuestion()"
    >
      <img
        v-if="expanded"
        src="@/assets/images/icons/icon-dart-top.svg"
        class="img"
        alt="Pijl omhoog, vraag is uitgeklapt"
      />
      <img
        v-else
        src="@/assets/images/icons/icon-dart-down.svg"
        alt="Pijl omlaag, vraag is ingeklapt"
        class="img"
      />
      <h3 class="question">
        {{ question.question }}
      </h3>
    </div>
    <template v-if="expanded">
      <div class="word-break answer" v-html="question.answer" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { FooterFaqQuestion } from '~~/types/footer'

const props = defineProps<{
  question: FooterFaqQuestion
}>()

const expandedTab = useState<string | undefined>(
  'expandedTabFaq',
  () => undefined
)

const toggleQuestion = () => {
  expandedTab.value = expanded.value ? undefined : props.question.anchor
}

const expanded = computed(() => expandedTab.value === props.question.anchor)
</script>

<style scoped langs="scss">
.question {
  cursor: pointer;
  font-size: 1em !important;
  padding-left: 1em;
  margin-bottom: 0em !important;
}

.answer {
  padding: 1em 1em 0 1em;
}

.question-header {
  padding: 1em 0 1em 1em;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #f3f3f3;
}

.img {
  width: 12px;
  aspect-ratio: 11/7;
}
</style>
