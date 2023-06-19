<template>
  <v-row>
    <v-col cols="9">
      <div class="floating-alert mb-0">
        <v-alert
          v-if="dataStore.feedback.error || schemaStore.feedback.error"
          type="error"
          icon="mdi-alert-circle"
          :text="dataStore.feedback.error + ' ' + schemaStore.feedback.error"
          closable
          prominent
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
        />
      </div>
      <div>
        <div v-if="!schemaStore.loaded || !dataStore.loaded" align="center">
          <v-progress-circular
            indeterminate
            :size="64"
            :width="6"
            class="mt-12"
          />
        </div>
        <v-form
          v-if="schemaStore.loaded && dataStore.loaded"
          id="generated-form"
          ref="form"
        >
          <v-row class="mt-5">
            <form-header />
          </v-row>
          <v-row
            v-for="(field, key) in schemaStore.formProperties"
            :key="key"
            class="form-field-form"
          >
            <form-field :field="field" :field-key="key" />
          </v-row>
        </v-form>
      </div>
    </v-col>
    <v-divider v-if="schemaStore.loaded && dataStore.loaded" vertical />
    <v-col cols="3" class="sticky">
      <form-side-block :lars="props.lars" />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useSchemaStore } from '@/store/schema'
import { useFormDataStore } from '@/store/form-data'
import FormField from '@/components/FormField.vue'
import FormSideBlock from '@/components/FormSideBlock.vue'
import FormHeader from '@/components/FormHeader.vue'
import config from '@/app-config'
import { onBeforeRouteLeave } from 'vue-router'

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
  schemaStore.fetchSchema(config.metaDataStandard.preferredVersion)
}

const form = ref<any | null>(null)
watch(form, () => {
  if (form.value && props.lars) {
    form.value.validate()
  }
})

// Checks routing within website
onBeforeRouteLeave((to, from) => {
  console.log(to, from)
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
  return (event.returnValue = '')
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
.floating-alert {
  position: sticky;
  position: -webkit-sticky; /* Safari */
  z-index: 1;
  left: 50%;
  top: 10px;
}
.form-field-form {
  padding-top: 0.3em !important;
  padding-bottom: 0.3em !important;
}
</style>
