<template>
  <div v-if="showBlock">
    <v-card
      elevation="0"
      border
      class="pl-3 pa-4"
    >
      <v-select
        v-model="dataStore.data.standard_version"
        :items="selectableVersions"
        label="Versie"
        outlined
        dense
        variant="outlined"
        class="v-col-12 px-0"
        @update:model-value="(e) => handleSchemaSwap(e)"
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
        :disabled="isReleased || !lars"
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
    <v-card elevation="0">
      <v-row>
        <v-col class="explainer-text mt-6">
          <span>
            Via de knop Opslaan en voorbeeld opent eenmalig het
            Algoritmeregister met deze invoer. Zo kan je het algoritme even in
            de context bekijken en controleren. Let op: deze link verloopt
            direct.
          </span>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="explainer-text mt-4">
          <span>
            * Onder ieder invoerveld staat een <b> instructie </b>, wanneer je
            het veld bewerkt. achter ieder invulveld staat een vraagtekenicoon,
            hier kan je de <b> helptekst </b> bekijken die bezoekers bij het
            Algoritmeregister kunnen lezen. De kolom <b> Zichtbaar </b> geeft
            aan of het betreffende veld in het Algoritmeregister getoond wordt:
            als zo'n veld niet door de organisatie ingevuld word, tonen we dan
            'Veld niet ingevuld' in het Algoritmeregister. Zie de
            <a
              href="https://algoritmes.pleio.nl/groups/view/fc9e6489-91e6-4177-b564-2cbea8e56132/kennisbank/files/6254c700-85ae-48dc-8f3b-31bcf6814cfc"
            >
              handleiding
            </a>
            voor alle informatie.
          </span>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { useSchemaStore } from '@/store/schema'
import { useFormDataStore } from '@/store/form-data'
import { computed, reactive, ref, onMounted } from 'vue'
import config from '@/app-config'
import WarningDialog from '@/components/WarningDialog.vue'
import content from '@/content.json'
import { useAuthStore } from '@/store/auth'
import router from '@/router'
import appConfig from '@/app-config'

const schemaStore = useSchemaStore()
const dataStore = useFormDataStore()
const authStore = useAuthStore()

const props = defineProps<{
  lars?: string
}>()

const selectableVersions = ref(config.metaDataStandard.availableVersions)

const dialogs = reactive({
  publish: false,
  retract: false,
  release: false,
  remove: false,
})

onMounted(() => {
  if (!props.lars) {
    dataStore.data.standard_version =
      appConfig.metaDataStandard.preferredVersion
  }
})

const showBlock = computed(() => schemaStore.loaded && dataStore.loaded)

const handleSchemaSwap = async (version: string) => {
  dataStore.resetFeedback()
  await schemaStore.fetchSchema(version)
  dataStore.pruneData()
}

const enableSubmit = computed(() => dataStore.unsavedChanges)
const handleSubmit = async (lars?: string) => {
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
    dataStore.handlePreview(
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
      dataStore.handleRelease(
        lars ? lars : (response.data as { lars_code: string }).lars_code
      )
    }
    dataStore.handlePublish(
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
  props.lars ? dataStore.data.published : false
)

const isReleased = computed(() =>
  props.lars ? dataStore.data.released : false
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
</style>
