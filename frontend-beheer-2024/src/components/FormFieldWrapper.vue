<template>
  <div class="form-field-wrapper">
    <div class="toolbar">
      <v-label>
        {{ fieldProperties.title }}
        <span v-if="fieldProperties.required" class="color-red">*</span>
      </v-label>
      <div class="top-right-block">
        <div
          class="explainer-text"
          :class="{
            disabled:
              !!fieldProperties.fixedValue ||
              !!(fieldProperties.type === 'fixed'),
          }"
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
          :class="{
            disabled:
              !!fieldProperties.fixedValue ||
              !!(fieldProperties.type === 'fixed'),
          }"
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
            />
          </v-menu>
          <v-icon> mdi-help </v-icon>
        </v-btn>
      </div>
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
      @blur="performLanguageChecks"
    />
    <v-row v-if="languageCheckInProgress" class="mb-3 text-grey-darken-2">
      <v-progress-circular
        indeterminate
        color="primary"
        size="24"
        class="ma-0 v-col-1"
      />
      Taalcontroles uitvoeren ...
    </v-row>
    <div class="px-10">
      <v-expansion-panels
        v-if="
          ignoredRuleCodes && !languageCheckInProgress && failedRules?.length
        "
        class="mb-12 rounded"
      >
        <v-expansion-panel
          v-for="failedRule in failedRules"
          :key="failedRule.rule_code"
          flat
        >
          <v-expansion-panel-title
            class="text-orange font-weight-bold"
            :class="
              failedRule.severity_level === 'warning'
                ? 'text-warning'
                : 'text-error'
            "
          >
            <v-icon
              :color="
                failedRule.severity_level === 'warning'
                  ? 'warning'
                  : 'error'
              "
              :icon="
                failedRule.severity_level === 'warning'
                  ? 'mdi-alert'
                  : 'mdi-alert-circle'
              "
              class="mr-4"
            />
            {{ failedRule.title }}
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <span v-html="applyStyling(failedRule.feedback_message)" />
            <v-row class="mt-6">
              <v-col v-if="failedRule.result?.suggestion">
                <v-label class="font-weight-bold mr-4">
                  Verbetervoorstel
                </v-label>
              </v-col>
              <v-spacer />
              <v-col class="align-content-end d-flex justify-end">
                <v-btn
                  v-if="failedRule.result?.suggestion"
                  color="success"
                  variant="tonal"
                  class="text-lowercase mr-4 justify-end"
                  @click="insertSuggestion"
                >
                  <v-icon
                    icon="mdi-check-circle"
                    class="mr-2"
                    size="24"
                  />
                  <span class="btn-title">Accepteren</span>
                </v-btn>
                <v-btn
                  v-if="failedRule.severity_level !== 'fout'"
                  color="error"
                  variant="tonal"
                  class="text-lowercase btn-title"
                  @click="ignoreRule(failedRule.rule_code)"
                >
                  <v-icon
                    icon="mdi-close-circle"
                    class="mr-2"
                    size="24"
                  />
                  <span class="btn-title">Negeren</span>
                </v-btn>
              </v-col>
            </v-row>
            <v-row v-if="failedRule.result?.suggestion" class="mt-1">
              <v-col v-if="suggestion" cols="12">
                <div class="pa-5 border rounded-lg">
                  {{ suggestion }}
                </div>
              </v-col>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FormFieldProperties } from '@/types/form'
import { useFormDataStore } from '@/store/form-data'
import { computed, ref, watch } from 'vue'
import FormFieldInput from './FormFieldInput.vue'
import { postC3poRequest } from '@/services/c3po'
import { LanguageRule } from '@/types/c3po'

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

const ignoredRuleCodes = ref(new Set<string>())
const failedRules = ref<LanguageRule[] | null>(null)
const suggestion = computed(() => {
  const langLevelRule = failedRules.value?.find(
    (rule) => rule.rule_code === 'B1_LANGUAGE_LEVEL'
  )
  return langLevelRule?.result?.suggestion || null
})
const languageCheckInProgress = ref(false)
const performLanguageChecks = () => {
  if (!hasUnsavedChanges.value) {
    return
  }
  let text = dataStore.data[props.fieldKey]
  if (typeof text === 'object') {
    text = JSON.stringify(text)
  }
  if (!text) {
    failedRules.value = null
    return
  }
  languageCheckInProgress.value = true
  postC3poRequest(text)
    .then((response) => {
      const ruleResults = response.data?.rules
      if (!ruleResults?.length) {
        failedRules.value = null
        return
      }
      failedRules.value =
        ruleResults.filter((rule: LanguageRule) => {
          const passed = rule.passed === false
          const ignored = ignoredRuleCodes.value.has(rule.rule_code)
          return passed && !ignored
        }) || null
      failedRules.value?.sort((a, b) => a.title.localeCompare(b.title))
    })
    .finally(() => {
      languageCheckInProgress.value = false
    })
}

const ignoreRule = (ruleCode: string) => {
  ignoredRuleCodes.value.add(ruleCode)
  if (failedRules.value) {
    failedRules.value = failedRules.value.filter(
      (rule) => rule.rule_code !== ruleCode
    )
  }
}

const insertSuggestion = () => {
  handleUpdatedContent(suggestion.value)
  ignoreRule('B1_LANGUAGE_LEVEL')
  performLanguageChecks()
}

const applyStyling = (text: string) => {
  if (!text) {
    return ''
  }

  const pattern =
    /\b(https?:\/\/[a-zA-Z0-9\-._~:\/?#[\]@!$&'()*+,;=%]+|www\.[a-zA-Z0-9\-._~:\/?#[\]@!$&'()*+,;=%]+)\b/g
  return text.replace(pattern, (match) => {
    // Extract the URL part without trailing punctuation
    const urlPart = match.match(pattern)?.[0]
    if (!urlPart) {
      return match
    }
    const punctuation = match.slice(urlPart.length)

    // Ensure the URL starts with http:// or https://
    const url = urlPart.startsWith('www.') ? `https://${urlPart}` : urlPart

    // Return the anchor tag with the URL, followed by any punctuation
    return `<a href="${url}" target="_blank">${urlPart}</a>${punctuation}`
  })
}

const editorId = computed(() => `rich-text-editor-${props.fieldKey}`)

const focused = ref(false)
const menu = ref(false)

const positiveFeedbackWatcher = computed(() => dataStore.unsavedChanges)
watch(positiveFeedbackWatcher, (oldValue, newValue) => {
  // Going from unsaved to saved, should reset all the local unsavedChanges
  if (!!newValue && !oldValue) {
    hasUnsavedChanges.value = false
  }
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
.color-red {
  color: red;
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
  border-bottom-width: 0 !important;

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

:deep(.v-expansion-panel__shadow) {
  box-shadow: 0 0.3px 6px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.1);
}
</style>
