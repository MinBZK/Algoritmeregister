<template>
  <div v-if="showBlock">
    <v-card
      elevation="0"
      border
      class="px-3 pt-1 pb-2 mb-3"
    >
      <strong class="card-title">Acties</strong>
      <algreg-button
        v-if="selectableVersions.includes(dataStore.data.standard_version)"
        @confirm="layoutStore.showTemplateDrawer = true"
      >
        <v-icon size="16" color="primary">
          mdi-file-document-edit-outline
        </v-icon>
        Een sjabloon gebruiken
      </algreg-button>
      <algreg-button :disabled="!enablePreview" @confirm="handlePreview(lars)">
        <v-icon color="primary" size="16">
          mdi-eye-outline
        </v-icon> Voorbeeld
        bekijken
      </algreg-button>
    </v-card>
    <v-card
      elevation="0"
      border
      class="px-3 pt-1 pb-2 my-3"
    >
      <strong class="card-title">Status</strong>
      <p class="card-title pt-2">
        Status publicatie
      </p>
      <div class="card-title">
        <status-chip />
      </div>
      <p class="card-title pt-2">
        Status van deze beschrijving
      </p>
      <div class="card-title">
        <template v-if="dataStore.unsavedChanges">
          In bewerking
        </template>
        <template v-else-if="!lars">
          Nieuw
        </template>
        <template v-else>
          Opgeslagen
        </template>
      </div>
      <p class="card-title pt-2 grey-darken-1">
        Laatst opgeslagen wijzigingen
      </p>
      <div v-if="savedDate" class="card-title grey-darken-1">
        {{
          new Date(savedDate).toLocaleDateString() +
            ', ' +
            new Date(savedDate).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })
        }}
      </div>
      <div v-else>
        <p class="card-title grey-darken-1">
          Nog niet opgeslagen!
        </p>
      </div>
      <algreg-button
        v-if="!!lars"
        class="mt-6"
        @confirm="layoutStore.showVersionDrawer = true"
      >
        <v-icon
          class="mr-1"
          color="primary"
          size="20"
        >
          mdi-history
        </v-icon>
        <span id="btn-title"> <strong> Vorige versie ophalen</strong></span>
      </algreg-button>
      <algreg-button
        theme="primary"
        :disabled="!enableSubmit"
        @confirm="handleSubmit(lars)"
      >
        <v-icon class="mr-1" size="20">
          mdi-content-save
        </v-icon>
        <span id="btn-title"> Opslaan</span>
        <v-icon
          v-if="dataStore.saving"
          class="ml-3"
          size="25"
        >
          mdi-loading mdi-spin
        </v-icon>
      </algreg-button>
    </v-card>
    <v-card
      v-if="!!lars && !!dataStore.orgFromData"
      elevation="0"
      border
      class="px-3 pt-1 pb-2 my-3"
    >
      <strong class="card-title">Vrijgeven en publiceren</strong>
      <template v-if="dataStore.availableActions.length > 0">
        <algreg-button
          v-for="action in dataStore.availableActions"
          :key="action.key"
          warn-with-dialog
          :disabled="!action.enabled || dataStore.unsavedChanges"
          :label="action.label"
          :dialog-title="dialogContent[action.key]?.title"
          :dialog-text="dialogContent[action.key]?.content"
          @confirm="dataStore.handleStateChange(lars!, action)"
        />
      </template>
      <div v-else class="card-title">
        Acties worden zichtbaar na het opslaan.
      </div>
    </v-card>
    <v-card
      elevation="0"
      border
      class="px-3 pt-1 pb-2 my-3"
    >
      <strong class="card-title"> Overige </strong>
      <download-dropdown
        :lars="lars"
        class="download-dropdown my-2"
        label="Download deze beschrijving"
      />
      <p class="card-title mt-4">
        Publicatie standaard
      </p>
      <v-select
        v-model="dataStore.data.standard_version"
        :items="selectableVersions"
        hide-details
        variant="outlined"
        rounded="lg"
        density="comfortable"
        class="v-col-12 px-0 py-1"
        @update:model-value="(e: any) => handleSchemaSwap(e)"
      />
    </v-card>
  </div>
</template>

<script setup lang="ts">
import AlgregButton from '@/components/AlgregButton.vue'
import DownloadDropdown from '@/components/DownloadDropdown.vue'
import StatusChip from '@/components/FormSideBlock/StatusChip.vue'
import { useSchemaStore } from '@/store/schema'
import { useFormDataStore } from '@/store/form-data'
import { computed, ref, onMounted } from 'vue'
import { dialogContent } from '@/config/notifications'
import publicationStandard from '@/config/publication-standard'
import router from '@/router'
import { useLayoutStore } from '@/store/layout'

const schemaStore = useSchemaStore()
const dataStore = useFormDataStore()
const layoutStore = useLayoutStore()

const props = defineProps<{
  lars?: string
}>()

const selectableVersions = ref(publicationStandard.availableVersions)

onMounted(() => {
  if (!props.lars) {
    dataStore.data.standard_version = publicationStandard.preferredVersion
  }
})

const showBlock = computed(() => schemaStore.loaded && dataStore.loaded)
const savedDate = computed(() => dataStore.data.create_dt)

const handleSchemaSwap = async (version: string) => {
  const oldVersion = schemaStore.loadedSchema

  dataStore.loaded = false
  dataStore.unsavedChanges = true
  await schemaStore.fetchSchema(version)
  dataStore.handleSchemaSwap(oldVersion, version)
  dataStore.pruneData()
  dataStore.loaded = true
}

const enableSubmit = computed(
  () => dataStore.unsavedChanges && !dataStore.saving
)
const handleSubmit = async (lars?: string) => {
  dataStore.data.name = dataStore.data?.name?.replace(/\r?\n|\r/g, '')
  if (lars) {
    const response = await dataStore.handleUpdate(lars)
    if (response.status == 200) {
      dataStore.data.create_dt = new Date()
    }
    return response
  } else {
    const response = await dataStore.handleCreate()
    if (response.data && response.status == 200) {
      dataStore.data.create_dt = new Date()
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
  const response = await handleSubmit(lars)
  if (response.status == 200) {
    await dataStore.handlePreview(
      lars ? lars : (response.data as { lars_code: string }).lars_code
    )
  }
}
</script>

<style lang="scss">
:deep(.v-field__outline) {
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
}

.card-title {
  font-size: 15px;
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

.grey-darken-1 {
  color: #808080;
}
</style>
