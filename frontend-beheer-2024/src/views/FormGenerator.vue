<template>
  <v-row>
    <v-col cols="9">
      <v-progress-circular
        v-if="!schemaStore.loaded || !dataStore.loaded"
        indeterminate
        :size="64"
        :width="6"
      />

      <v-card
        v-if="schemaStore.loaded && dataStore.loaded"
        flat
        border
        class="pa-2"
      >
        <quality-inspector class="ma-4" />
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
import { ref, watch, computed, onMounted } from 'vue'
import { useSchemaStore } from '@/store/schema'
import { useFormDataStore } from '@/store/form-data'
import FormFieldWrapper from '@/components/FormFieldWrapper.vue'
import FormSideBlock from '@/components/FormSideBlock/FormSideBlock.vue'
import publicationStandard from '@/config/publication-standard'
import { onBeforeRouteLeave } from 'vue-router'
import QualityInspector from '@/components/QualityInspector/index.vue'
import { useArchiveStore } from '@/store/archive'
import { AlgorithmForm } from '@/types/algorithm'

const props = defineProps<{
  lars?: string
  versionId?: string
}>()

const schemaStore = useSchemaStore()
const dataStore = useFormDataStore()
const archiveStore = useArchiveStore()
dataStore.unsavedChanges = false

onMounted(async () => {
  if (props.lars) {
    await dataStore.fetchData(props.lars)
    const selectedArchiveVersion = archiveStore.selectedVersion
    if (selectedArchiveVersion) {
      dataStore.data = selectedArchiveVersion as AlgorithmForm
      dataStore.data.state = 'STATE_1'
      dataStore.unsavedChanges = true
    }
    await dataStore.fetchAvailableActions(props.lars)
  } else {
    dataStore.data = {}
    dataStore.loaded = true
    await schemaStore.fetchSchema(publicationStandard.preferredVersion)
  }
})

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
  // Reset selected version
  archiveStore.selectedVersion = null
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

:deep(.v-card) {
  border-radius: 16px;
  box-shadow: 0px 0px 8px 0px #f3f4f6 !important;
}
</style>
