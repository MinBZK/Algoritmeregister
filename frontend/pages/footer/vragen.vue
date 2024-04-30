<template>
  <div style="margin-bottom: 6em">
    <h1>{{ p('Footer: Vragen.pageTitle') }}</h1>
    <FaqAccordions :accordions="questionGroups" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { FooterFaqQuestionGroup, FooterFaqQuestion } from '~~/types/footer'
const { p } = useTextLoader()

const expandedTab = useState<string | undefined>(
  'expandedTabFaq',
  () => undefined
)

const router = useRouter()

// Expands question on internal navigation
router.afterEach((to, _) => {
  if (to.hash) {
    const hash = to.hash.slice(1)
    expandedTab.value = hash
  }
})

definePageMeta({
  title: 'Vragen',
})

const questionGrouping = [
  { groupKey: 1, questionKeys: [1, 2, 3, 4, 5, 6] },
  { groupKey: 2, questionKeys: [7, 8, 9, 10] },
  { groupKey: 3, questionKeys: [11, 12] },
  { groupKey: 4, questionKeys: [13, 14] },
  { groupKey: 5, questionKeys: [15, 16] },
  { groupKey: 6, questionKeys: [17] },
]

const questionGroups = computed<FooterFaqQuestionGroup[]>(() => {
  const result = questionGrouping.map<FooterFaqQuestionGroup>((group) => {
    const questions = group.questionKeys.map<FooterFaqQuestion>(
      (questionKey) => {
        return {
          key: questionKey.toString(),
          anchor: 'question' + questionKey.toString(),
          question: p(`Footer: Vragen.question${questionKey}`),
          answer: p(`Footer: Vragen.answer${questionKey}`),
        }
      }
    )
    const anchor = p(`Footer: Vragen.group${group.groupKey}`)
      .split(' ')
      .slice(1, 2)
      .join('+')
      .toLowerCase()

    return {
      key: group.groupKey.toString(),
      label: p(`Footer: Vragen.group${group.groupKey}`),
      anchor,
      questions,
    }
  })
  return result
})

const pageTitle = computed(() => p('Footer: Vragen.pageTitle'))
useHead({ title: pageTitle })
providePageTitle({ title: 'footer.paths.vragen', labelType: 'locale-index' })
</script>
