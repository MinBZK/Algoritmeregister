<template>
  <div class="form-field-wrapper">
    <div class="toolbar">
      <v-label>
        {{ fieldProperties.title }}
        <span v-if="fieldProperties.required" style="color: red">*</span>
      </v-label>
      <div class="top-right-block">
        <div
          class="explainer-text"
          :class="{ disabled: !!fieldProperties.fixedValue }"
        >
          {{
            fieldProperties.show_always
              ? 'Dit veld wordt altijd getoond'
              : 'Dit veld wordt alleen getoond als het ingevuld is'
          }}
        </div>
        <v-btn
          flat
          variant="outlined"
          rounded="0"
          class="questionmark"
          :class="{ disabled: !!fieldProperties.fixedValue }"
        >
          <v-menu
            activator="parent"
            scroll-strategy="none"
            location="end center"
            offset="10"
            open-on-hover
          >
            <v-card
              rounded="0"
              max-width="300px"
              :text="fieldProperties.instructions"
              color="grey-lighten-2"
              elevation="4"
            />
          </v-menu>
          ?
        </v-btn>
      </div>
    </div>

    <div>
      <v-menu
        v-model="menu"
        min-width="1px"
        class="rule-menu"
        activator="parent"
        :close-on-content-click="false"
        :offset="[-25, -220]"
        scroll-strategy="none"
        transition="none"
      >
        <rule-interface
          :rule-set="ruleSet"
          :text="dataStore.data[fieldKey]"
          @close-menu="menu = false"
        />
      </v-menu>
    </div>
    <form-field-input
      :content="dataStore.data[fieldKey]"
      :type="fieldProperties.type"
      :field-properties="fieldProperties"
      :field-key="fieldKey"
      :unsaved-change="hasUnsavedChanges"
      :editor-id="editorId"
      @update:content="(newValue) => handleUpdatedContent(newValue)"
      @update:focus="focused = !focused"
      @show-c3po-menu="menu = true"
    />
    <!-- @blur="performSentenceCheck"-->
    <v-alert
      v-if="sentenceLengthFeedback"
      icon="mdi-alert-circle"
      variant="tonal"
      type="error"
      :text="sentenceLengthFeedback"
      class="mb-4"
    />
  </div>
</template>

<script setup lang="ts">
import { FormFieldProperties } from '@/types/form'
import { useFormDataStore } from '@/store/form-data'
import { computed, ref, watch } from 'vue'
import FormFieldInput from './FormFieldInput.vue'
import RuleInterface from './RuleInterface.vue'
import { postC3poRequest } from '@/services/c3po'

const dataStore = useFormDataStore()

const props = defineProps<{
  fieldProperties: FormFieldProperties
  fieldKey: string
  ruleSet: string
}>()

const hasUnsavedChanges = ref(false)
const handleUpdatedContent = (content: any) => {
  dataStore.data[props.fieldKey] = content
  dataStore.unsavedChanges = true
  hasUnsavedChanges.value = true
}

const sentenceLengthFeedback = ref<string>('')
const performSentenceCheck = () => {
  const ruleCode = 'SENTENCE_LENGTH'
  const body = { text: dataStore.data[props.fieldKey], ruleSet: ruleCode }
  postC3poRequest(body).then((response) => {
    const ruleResults = response.data?.rules
    if (ruleResults) {
      const ruleFiltered = ruleResults.filter(
        (rule) => rule.rule_code === ruleCode
      )
      sentenceLengthFeedback.value = ruleFiltered[0]?.feedback_message || ''
    }
  })
  // Keep error in console, don't show it to the user
}

const editorId = computed(() => `rich-text-editor-${props.fieldKey}`)

const focused = ref(false)
const menu = ref(false)

const positiveFeedbackWatcher = computed(() => dataStore.feedback.success)
watch(positiveFeedbackWatcher, () => {
  hasUnsavedChanges.value = false
})
</script>

<style scoped lang="scss">
.form-field-wrapper {
  width: 100%;
  padding: 0 0.75em 0 0.75em !important;
  :deep(.v-label) {
    font-weight: bold !important;
  }
}
.toolbar {
  display: flex;
  justify-content: space-between;
}
</style>

<style scoped lang="scss">
.rule-menu {
  div.v-overlay__content {
    border-radius: 10px !important;
    border: 1px solid rgb(200, 200, 200, 1);
  }
}

.top-right-block {
  display: flex;
  min-height: 35px !important;
  max-height: 35px !important;
}

.questionmark {
  min-width: 40px !important;
  max-width: 40px !important;
  min-height: inherit;
  max-height: 35px !important;
  border: 1px solid rgb(172, 172, 172);
  border-bottom-width: 0px !important;

  &.disabled {
    border-color: rgb(223, 223, 223) !important;
  }
}

.explainer-text {
  background-color: white;
  color: rgb(50, 50, 50);
  border: 1px solid rgb(172, 172, 172);
  border-bottom-width: 0;
  border-right-width: 0;

  &.disabled {
    border-color: rgb(223, 223, 223) !important;
  }
}
</style>
