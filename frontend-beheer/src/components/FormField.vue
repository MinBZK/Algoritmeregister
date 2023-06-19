<template>
  <v-col
    :class="
      'form-field-form-col' + (fieldHasUnsavedChanges ? ' bold-title' : '')
    "
  >
    <v-textarea
      v-if="fieldKey === 'name'"
      ref="textareaName"
      v-model="dataStore.data['name']"
      class="field-name"
      rows="1"
      auto-grow
      :label="field.title + (field.required ? '*' : '')"
      :counter="field.maxLength"
      :type="field.type"
      :hint="field.instructions"
      :hide-details="!focused && ruleCompliant"
      variant="outlined"
      :rules="field.rules"
      @update:focused="handleFocusUpdate(textareaName)"
      @update:model-value="declareUnsavedChanges"
    />
    <v-text-field
      v-else-if="field.type === 'fixed'"
      v-model="dataStore.data[fieldKey]"
      :label="field.title + (field.required ? '*' : '')"
      :hint="field.instructions ?? ''"
      variant="outlined"
      class="disabled-normal-colour"
      disabled
      hide-details
    />
    <v-textarea
      v-else-if="field.type === 'string'"
      ref="textarea"
      v-model="dataStore.data[fieldKey]"
      rows="1"
      auto-grow
      :label="field.title + (field.required ? '*' : '')"
      :counter="field.maxLength ?? 100"
      :type="field.type"
      :hint="field.instructions ?? ''"
      variant="outlined"
      :rules="field.rules"
      :hide-details="!focused && ruleCompliant"
      @update:focused="handleFocusUpdate(textarea)"
      @update:model-value="declareUnsavedChanges"
    />
    <v-select
      v-else-if="field.type === 'enum'"
      ref="select"
      v-model="dataStore.data[fieldKey]"
      class="v-select-details"
      :items="field.allowedItems!"
      :label="field.title + (field.required ? '*' : '')"
      :hint="field.helpText ?? ''"
      :rules="field.rules"
      clearable
      variant="outlined"
      @click:clear.prevent="select.resetValidation()"
      @update:model-value="declareUnsavedChanges"
    />
    <v-combobox
      v-else-if="field.type === 'array' && field.recommendedItems"
      ref="select"
      v-model="dataStore.data[fieldKey]"
      class="v-select-details"
      :items="field.recommendedItems!"
      :label="field.title + (field.required ? '*' : '')"
      :hint="field.helpText ?? ''"
      :rules="field.rules"
      multiple
      chips
      clearable
      variant="outlined"
      @click:clear.prevent="select.resetValidation()"
      @update:model-value="declareUnsavedChanges"
    />
    <v-select
      v-else-if="field.type === 'array' && field.allowedItems"
      ref="select"
      v-model="dataStore.data[fieldKey]"
      class="v-select-details"
      :items="field.allowedItems!"
      :label="field.title + (field.required ? '*' : '')"
      :hint="field.helpText ?? ''"
      :rules="field.rules"
      multiple
      clearable
      variant="outlined"
      @click:clear.prevent="select.resetValidation()"
      @update:model-value="declareUnsavedChanges"
    />
  </v-col>
  <div style="min-width: 5em; padding-top: 0.5em">
    <div style="float: left; margin-right: 1em">
      <v-tooltip :text="field.helpText" max-width="300px">
        <template #activator="{ props }">
          <v-btn
            size="x-small"
            icon="mdi-help"
            v-bind="props"
            elevation="0"
            variant="outlined"
          />
        </template>
      </v-tooltip>
    </div>
    <div>
      <v-tooltip disabled>
        <template #activator>
          <v-btn
            class="show-as-enabled text-capitalize text-body-3"
            size="x-small"
            icon="mdi-help"
            elevation="0"
            variant="outlined"
            disabled
          >
            {{ field.showAlways ? 'Ja' : 'Nee' }}
          </v-btn>
        </template>
      </v-tooltip>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FormFieldProperties } from '@/types/form'
import { useFormDataStore } from '@/store/form-data'
import { ref, watch, computed } from 'vue'

const dataStore = useFormDataStore()

const props = defineProps<{
  field: FormFieldProperties
  fieldKey: string | number
}>()

const focused = ref(false)

// refs to the individual components
const textareaName = ref<any | null>(null)
const textarea = ref<any | null>(null)
const select = ref<any | null>(null)

const fieldHasUnsavedChanges = ref<boolean>(false)
const declareUnsavedChanges = () => {
  dataStore.unsavedChanges = true
  fieldHasUnsavedChanges.value = true
}

const persistentErrorFeedback = ref(false)
// Used to show the error even outside of focus.
const ruleCompliant = computed(() => {
  if (persistentErrorFeedback.value) {
    if (props.field.rules) {
      const result = props.field.rules.find((rule) => {
        const result = rule(dataStore.data[props.fieldKey]) !== true
        return result
      })
      return !result
    }
  }
  return true
})

const handleFocusUpdate = (component: any) => {
  focused.value = !focused.value
  if (focused.value) {
    persistentErrorFeedback.value = true
  } else {
    // validate on blur
    component.validate()
  }
}

// Make errors persistent on feedback of calls.
const feedbackWatcher = computed(() => dataStore.feedback.error)
watch(feedbackWatcher, () => {
  persistentErrorFeedback.value = true
})

const positiveFeedbackWatcher = computed(() => dataStore.feedback.success)
watch(positiveFeedbackWatcher, () => {
  fieldHasUnsavedChanges.value = false
})
</script>

<style lang="scss">
.form-field-form-col {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

// Give disabled text-fields a grey background color.
.disabled-normal-colour .v-field {
  .v-field__field {
    background-color: #f1f1f1;
  }
}

// Give all field same color scheme, even when disabled.
:root {
  --v-medium-emphasis-opacity: 1;
  --v-disabled-opacity: 1;
}

.v-theme--light {
  --v-medium-emphasis-opacity: 1;
  --v-disabled-opacity: 1;
}

// Show the tooltip as enabled even though it is disabled
.show-as-enabled.v-btn--disabled {
  opacity: 1;
}

// Make the field use a big font size
.field-name .v-field__input {
  font-size: 3em !important;
}

// Make title and text bold
.bold-title {
  .v-field-label {
    font-weight: bold !important;
  }
  .v-field__input {
    font-weight: bold !important;
  }
}

// The v-select has issues as you cannot detect focus.
// This decreases the details, but increases the message size, giving the same effect overall.
.v-select-details > .v-input__details {
  margin-bottom: -2em !important;
}

.v-select-details > .v-input__details > .v-messages > .v-messages__message {
  margin-bottom: 1.5em;
}
</style>
