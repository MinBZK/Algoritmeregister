<template>
  <v-row>
    <v-col cols="9">
      <v-progress-circular
        v-if="!schemaStore.loaded || !dataStore.loaded"
        indeterminate
        :size="64"
        :width="6"
      />
      <v-alert
        v-if="dataStore.feedback.error || schemaStore.feedback.error"
        type="error"
        icon="mdi-alert-circle"
        closable
        prominent
        class="floating-alert mb-2"
      >
        <template #text>
          {{ dataStore.feedback.error + ' ' + schemaStore.feedback.error }}
          <div v-for="error in dataStore.feedback.errorList" :key="error">
            - {{ error }}
          </div>
        </template>
      </v-alert>
      <v-alert
        v-else-if="dataStore.feedback.success"
        type="success"
        icon="mdi-check-circle"
        :text="dataStore.feedback.success"
        closable
        prominent
        class="floating-alert mb-2"
      />
      <div
        v-if="schemaStore.loaded && dataStore.loaded"
        class="margin-bottom-1"
      >
        <quality-inspector />
      </div>

      <v-card
        v-if="schemaStore.loaded && dataStore.loaded"
        flat
        border
        class="pa-2"
      >
        <v-card-text>
          <v-form ref="form">
            <form-field-wrapper
              v-for="(fieldProperties, key) in schemaStore.formProperties"
              :key="key"
              :field-properties="fieldProperties"
              :field-key="key as string"
              :rule-set="key as string"
              class="form-field"
            />
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="3" class="sticky">
      <form-side-block :lars="props.lars" />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useSchemaStore } from '@/store/schema'
import { useFormDataStore } from '@/store/form-data'
import FormFieldWrapper from '@/components/FormFieldWrapper.vue'
import FormSideBlock from '@/components/FormSideBlock.vue'
import publicationStandard from '@/config/publication-standard'
import { onBeforeRouteLeave } from 'vue-router'
import QualityInspector from '@/components/QualityInspector/index.vue'

const props = defineProps<{
  lars?: string
}>()

const schemaStore = useSchemaStore()
const dataStore = useFormDataStore()
dataStore.unsavedChanges = false
dataStore.resetFeedback()

if (props.lars) {
  dataStore.fetchData(props.lars)
} else {
  dataStore.data = {}
  dataStore.loaded = true
  schemaStore.fetchSchema(publicationStandard.preferredVersion)
}

const form = ref<any | null>(null)
watch(form, () => {
  if (form.value && props.lars) {
    form.value.validate()
  }
})

// Checks routing within website
onBeforeRouteLeave(() => {
  if (dataStore.unsavedChanges) {
    const answer = window.confirm(
      'Wijzigingen die je hebt aangebracht, worden mogelijk niet opgeslagen.'
    )
    if (!answer) return false
  }
})

// Checks other routing (exit browser, back/forward)
const handleBeforeUnload = (event: any) => {
  event.preventDefault()
  event.returnValue = ''
}

const changeWatcher = computed(() => dataStore.unsavedChanges)
watch(changeWatcher, () => {
  if (dataStore.unsavedChanges) {
    window.addEventListener('beforeunload', handleBeforeUnload, {
      capture: true,
    })
  } else {
    window.removeEventListener('beforeunload', handleBeforeUnload, {
      capture: true,
    })
  }
})
</script>

<style scoped lang="scss">
:deep(.v-progress-circular) {
  display: block;
  margin: 5em auto;
}

.floating-alert {
  position: sticky;
  position: -webkit-sticky; /* Safari */
  z-index: 1;
  left: 50%;
  top: 10px;
}

.form-field {
  padding: 0 0 0 0;
}

.margin-bottom-1 {
  margin-bottom: 1em;
}
</style>
