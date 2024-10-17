<template>
  <div v-if="showBlock">
    <v-card
      elevation="0"
      border
      class="pl-3 pa-4"
    >
      <download-dropdown :lars="lars" class="download-dropdown" />
      <v-select
        v-model="dataStore.data.standard_version"
        :items="selectableVersions"
        label="Publicatiestandaard"
        hide-details
        rounded="0"
        outlined
        dense
        variant="outlined"
        class="v-col-12 px-0"
        @update:model-value="(e: any) => handleSchemaSwap(e)"
      />
      <templates-dialog
        v-if="selectableVersions.includes(dataStore.data.standard_version)"
      />
      <v-btn
        class="text-lowercase elevation-0 text-body-1 mb-2"
        block
        color="primary"
        variant="tonal"
        :disabled="!enablePreview"
        @click="handlePreview(lars)"
      >
        <v-icon class="mr-2">
          mdi-eye-outline
        </v-icon>
        <span id="btn-title"> Opslaan en voorbeeld </span>
      </v-btn>
      <div v-if="dataStore.unsavedChanges" class="explainer-text mb-2">
        Let op: er zijn wijzigingen niet opgeslagen.
      </div>
      <v-btn
        class="text-lowercase elevation-0 text-body-1 mb-2"
        block
        color="blue-darken-2"
        :disabled="!enableSubmit"
        @click="handleSubmit(lars)"
      >
        <span id="btn-title"> Opslaan</span>
      </v-btn>
      <v-btn
        class="text-lowercase elevation-0 text-body-1 mb-2"
        block
        color="success"
        :disabled="
          (isPublished && !dataStore.unsavedChanges) || isReleased || !lars
        "
        @click="dialogs.release = true"
      >
        <span id="btn-title">
          {{ isReleased ? 'Vrijgegeven' : 'Opslaan en vrijgeven' }}
        </span>
      </v-btn>
      <warning-dialog
        v-model="dialogs.release"
        color="success"
        @confirmed="handleRelease(lars)"
      >
        {{ content.warningDialog.release.text }}
      </warning-dialog>
      <v-btn
        class="text-lowercase elevation-0 text-body-1 mb-2"
        block
        color="error"
        :disabled="!isPublished"
        @click="dialogs.retract = true"
      >
        <span id="btn-title">
          {{ isPublished ? 'Publicatie intrekken' : 'Niet gepubliceerd' }}
        </span>
      </v-btn>
      <warning-dialog
        v-model="dialogs.retract"
        color="error"
        @confirmed="handleRetract(lars)"
      >
        {{ content.warningDialog.retract.text }}
      </warning-dialog>
      <div v-if="authStore.canPublish">
        <v-btn
          class="text-lowercase elevation-0 text-body-1 mb-2"
          block
          color="warning"
          :disabled="isPublished || !lars"
          @click="dialogs.publish = true"
        >
          <span id="btn-title">
            {{ isPublished ? 'Gepubliceerd' : 'Opslaan en publiceren' }}
          </span>
        </v-btn>
        <warning-dialog
          v-model="dialogs.publish"
          color="warning"
          @confirmed="handlePublish(lars)"
        >
          {{ content.warningDialog.publish.text }}
        </warning-dialog>
      </div>
      <div v-if="authStore.canRemove && lars">
        <v-btn
          class="text-lowercase elevation-0 text-body-1 mb-2"
          block
          color="error"
          :disabled="!lars"
          @click="dialogs.remove = true"
        >
          <span id="btn-title"> Verwijder dit algoritme </span>
        </v-btn>
        <warning-dialog
          v-model="dialogs.remove"
          color="error"
          @confirmed="handleRemove(lars || '')"
        >
          {{ content.warningDialog.remove.text }}
        </warning-dialog>
      </div>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import TemplatesDialog from './TemplatesDialog.vue'
import DownloadDropdown from './DownloadDropdown.vue'
import { useSchemaStore } from '@/store/schema'
import { useFormDataStore } from '@/store/form-data'
import { computed, reactive, ref, onMounted } from 'vue'
import publicationStandard from '@/config/publication-standard'
import WarningDialog from '@/components/WarningDialog.vue'
import content from '@/content.json'
import { useAuthStore } from '@/store/auth'
import router from '@/router'

const schemaStore = useSchemaStore()
const dataStore = useFormDataStore()
const authStore = useAuthStore()

const props = defineProps<{
  lars?: string
}>()

const selectableVersions = ref(publicationStandard.availableVersions)

const dialogs = reactive({
  publish: false,
  retract: false,
  release: false,
  remove: false,
})

onMounted(() => {
  if (!props.lars) {
    dataStore.data.standard_version = publicationStandard.preferredVersion
  }
})

const showBlock = computed(() => schemaStore.loaded && dataStore.loaded)

const handleSchemaSwap = async (version: string) => {
  const oldVersion = schemaStore.loadedSchema

  dataStore.resetFeedback()
  dataStore.loaded = false
  dataStore.unsavedChanges = true
  await schemaStore.fetchSchema(version)
  dataStore.handleSchemaSwap(oldVersion, version)
  dataStore.pruneData()
  dataStore.loaded = true
}

const enableSubmit = computed(() => dataStore.unsavedChanges)
const handleSubmit = async (lars?: string) => {
  dataStore.data.name = dataStore.data?.name?.replace(/\r?\n|\r/g, '')
  dataStore.resetFeedback()
  if (lars) {
    const response = await dataStore.handleUpdate(lars)
    return response
  } else {
    const response = await dataStore.handleCreate()
    if (response.data && response.status == 200) {
      // Go to 'bewerken' page after creating and submitting a first version.
      router.push({
        name: 'algorithm.edit',
        params: { lars: response.data.lars_code },
      })
    }
    return response
  }
}

const enablePreview = true
const handlePreview = async (lars?: string) => {
  dataStore.resetFeedback()
  const response = await handleSubmit(lars)
  if (response.status == 200) {
    await dataStore.handlePreview(
      lars ? lars : (response.data as { lars_code: string }).lars_code
    )
  }
}

const handleRetract = async (lars?: string) => {
  dataStore.resetFeedback()
  const response = await handleSubmit(props.lars)
  if (response.status == 200) {
    dataStore.handleRetract(
      lars ? lars : (response.data as { lars_code: string }).lars_code
    )
  }
}

const handleRelease = async (lars?: string) => {
  dataStore.resetFeedback()
  const response = await handleSubmit(lars)
  if (response.status == 200) {
    dataStore.handleRelease(
      lars ? lars : (response.data as { lars_code: string }).lars_code
    )
  }
}

const handlePublish = async (lars?: string) => {
  dataStore.resetFeedback()
  const response = await handleSubmit(lars)
  if (response.status == 200) {
    if (!isReleased.value) {
      await dataStore.handleRelease(
        lars ? lars : (response.data as { lars_code: string }).lars_code
      )
    }
    await dataStore.handlePublish(
      lars ? lars : (response.data as { lars_code: string }).lars_code
    )
  }
}

const handleRemove = async (lars: string) => {
  dataStore.resetFeedback()
  const response = await dataStore.handleRemove(lars)
  if (response.status == 200) {
    router.push({ name: 'algorithm.index' })
  }
}

const isPublished = computed(() =>
  props.lars ? dataStore.data.state === 'PUBLISHED' : false
)

const isReleased = computed(() =>
  props.lars ? dataStore.data.state === 'STATE_2' : false
)
</script>

<style lang="scss">
#btn-title:first-letter {
  text-transform: capitalize;
}

.explainer-text {
  background-color: #f2f2f2;
  color: $primary;
  text-align: center;
  font-size: 0.8em;
  padding-bottom: 1em;
  padding-top: 0.5em;
  padding-left: 1.5em;
  padding-right: 1.5em;
  a {
    color: $primary;
  }
}

.download-dropdown {
  .download-button {
    border: 1px solid rgb(171, 171, 171) !important;
    border-left-width: 0px !important;
  }
}
</style>
