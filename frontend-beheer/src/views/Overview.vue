<template>
  <v-row v-if="selectedOrg?.flow === 'self_publish_two'">
    <v-alert title="Let op!" type="warning">
      Deze organisatie mag zelf algoritmebeschrijvingen publiceren. In verband
      met ontwikkeling is gekozen om dit alleen beschikbaar te maken op de
      nieuwste versie van het webformulier:
      <a href="https://algoritmes.overheid.nl/webformulier2024">
        Deze kan je hier vinden.
      </a>
      Als je dit bericht ziet kan je niet meer werken op deze pagina, en moet je
      het nieuwe webformulier gebruiken om onvoorziene problemen te voorkomen.
    </v-alert>
  </v-row>
  <v-row>
    <v-col class="d-flex align-center mt-10">
      <h1 :class="{ 'text-h4 px-0': true }">
        Overzicht {{ authStore.selectedOrg?.name }}
      </h1>
    </v-col>
    <v-col
      v-if="authStore.organisations.length != 0"
      lg="4"
      md="5"
      cols="12"
    >
      <template v-if="!singleOrgOverview">
        <v-row>
          <v-label> Organisatie </v-label>
        </v-row>
        <v-row>
          <v-autocomplete
            v-model="selectedOrg"
            class="org-selector"
            :items="authStore.organisations"
            density="comfortable"
            placeholder="Organisatie"
            item-title="name"
            rounded="0"
            item-value="org_id"
            variant="outlined"
            hide-details
            @update:model-value="authStore.selectOrganisation($event)"
          />
        </v-row>
      </template>
      <v-row>
        <v-col cols="6" class="pl-0 pt-3 pr-2">
          <download-dropdown />
        </v-col>
        <v-col cols="6" class="pl-2 pt-3 pr-0">
          <v-btn
            class="text-lowercase rounded-0 block new-algorithm-button"
            color="blue-darken-2"
            flat
            block
            @click="navigateToForm"
          >
            <v-icon class="mr-2" size="21">
              mdi-playlist-plus
            </v-icon>
            <span class="btn-title"> Nieuw algoritme </span>
          </v-btn>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
  <v-row v-if="!algorithmStore.loaded || authStore.loading">
    <v-col cols="12" align="center">
      <v-progress-circular
        indeterminate
        :size="64"
        :width="6"
      />
    </v-col>
  </v-row>
  <v-row v-else class="elevation-0 mt-6">
    <v-alert
      v-if="algorithmStore.error"
      type="error"
      variant="tonal"
      class="mb-4"
      icon="mdi-alert-circle"
      :text="algorithmStore.error"
    />
    <v-alert
      v-else-if="algorithmStore.success"
      type="success"
      variant="tonal"
      class="mb-4"
      icon="mdi-check-circle"
      :text="algorithmStore.success"
    />
  </v-row>
  <v-row>
    <v-col v-if="algorithms.length > 0">
      <v-data-table
        items-per-page="-1"
        :headers="headers"
        :items="algorithms"
        item-value="lars"
        item-title="name"
        class="pa-6 hover"
        @click:row="navigateToForm"
      >
        <template #item.actions="{ item }">
          <v-hover>
            <div class="flex-container-align-items">
              <v-btn
                size="small"
                class="me-2"
                color="blue-darken-2"
                variant="tonal"
              >
                <v-icon icon="mdi-lead-pencil" size="20" />
              </v-btn>
              <download-dropdown variant="v-btn" :lars="item.value" />
            </div>
          </v-hover>
        </template>
      </v-data-table>
    </v-col>
    <v-col
      v-else-if="authStore.organisations.length == 0"
      class="light-border text-center"
    >
      Je bent nog niet aan een organisatie gekoppeld. Neem contact op met de
      beheerder om rechten tot een organisatie te verkrijgen.
    </v-col>
    <v-col v-else class="light-border text-center">
      Dit overzicht is nog leeg. Voer een eerste algoritmebeschrijving in.
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
import DownloadDropdown from '@/components/DownloadDropdown.vue'
import { useAuthStore } from '@/store/auth'
import { useAlgorithmStore } from '@/store/overview'
import { computed, watch, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Algorithm } from '@/types/algorithm'
import { Organisation } from '@/types/organisation'
import { useFormDataStore } from '@/store/form-data'

const router = useRouter()
const authStore = useAuthStore()
const algorithmStore = useAlgorithmStore()
const dataStore = useFormDataStore()

dataStore.unsavedChanges = false

const selectedOrg = ref<Organisation>()
if (authStore.selectedOrg) {
  algorithmStore.fetchAlgorithms(authStore.selectedOrg)
  selectedOrg.value = authStore.selectedOrg
}

const algorithms = computed<Algorithm[]>(() => {
  return algorithmStore.algorithmsFormatted
})
const headers = [
  { title: 'Naam', key: 'name', value: 'name' },
  { title: 'Status', key: 'overviewStatus', value: 'overviewStatus' },
  { title: 'Laatst bewerkt', key: 'last_update_dt', value: 'last_update_dt' },
  { title: 'Door', key: 'last_update_by', value: 'last_update_by' },
  { title: 'Standaard', key: 'schema_version', value: 'schema_version' },
  { title: 'ID', key: 'lars', value: 'lars' },
  { title: 'Actie', key: 'actions', sortable: false },
]

const navigateToForm = (event: Event, data: any) => {
  const lars = data?.item.value
  if (lars) {
    router.push({ name: 'algorithm.edit', params: { lars } })
  } else {
    router.push({ name: 'algorithm.create' })
  }
}

const singleOrgOverview = computed(() => authStore.organisations.length == 1)

watch(
  () => authStore.selectedOrg,
  () => algorithmStore.fetchAlgorithms(authStore.selectedOrg!)
)
</script>

<style scoped lang="scss">
:deep(.v-data-table-footer) {
  display: none !important;
}

:deep(.v-table),
.light-border {
  border: 1.3px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  th {
    font-size: 1.45rem;
    color: #333333 !important;
  }
}

.new-algorithm-button {
  min-height: 41px;
}

.can-add-org-style {
  height: 100%;
  max-width: 52px;
  min-width: 52px;
}

.flex-container-align-items {
  display: flex;
  align-items: flex-end;
}

:deep(.org-selector) {
  .v-input__append {
    padding-top: 0px;
  }
}
</style>
