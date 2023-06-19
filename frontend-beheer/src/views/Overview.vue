<template>
  <v-snackbar
    v-model="showSnackbar"
    color="red"
    location="top"
    class="mt-8"
  >
    {{ errorMessage }}
    <template #actions>
      <v-btn icon @click=";[(errorMessage = ''), (showSnackbar = false)]">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
  <v-row>
    <v-col>
      <h1 :class="{ 'text-h4 px-0': true, 'mt-10': !singleOrgOverview }">
        Overzicht {{ authStore.selectedOrg?.name }}
      </h1>
    </v-col>
    <v-col
      v-if="authStore.organizations.length != 0"
      lg="4"
      md="5"
      cols="12"
    >
      <template v-if="!singleOrgOverview">
        <v-row>
          <v-label> Organisatie </v-label>
        </v-row>
        <v-row>
          <v-select
            :value="authStore.selectedOrg?.name"
            :items="authStore.organizations"
            item-title="name"
            item-value="id"
            variant="outlined"
            hide-details
            @update:model-value="authStore.selectOrganization($event)"
          />
        </v-row>
      </template>
      <v-row>
        <v-col cols="6" class="pl-0 pt-3 pr-2">
          <v-btn
            v-if="authStore.selectedOrg?.id"
            class="text-lowercase rounded-0 block btn-title"
            color="blue-darken-2"
            flat
            block
            :disabled="loading || algorithmStore.algorithms.length === 0"
            @click="downloadExcel"
          >
            <template v-if="loading">
              <v-progress-circular
                indeterminate
                class="mr-4"
                :size="21"
                :width="3"
              />
              <span class="btn-title">Even geduld ...</span>
            </template>
            <template v-else>
              <v-icon class="mr-2" size="21">
                mdi-microsoft-excel
              </v-icon>
              <span class="btn-title"> Download Excel </span>
            </template>
          </v-btn>
        </v-col>
        <v-col cols="6" class="pl-2 pt-3 pr-0">
          <v-btn
            v-if="!(authStore.organizations.length == 0)"
            class="text-lowercase rounded-0 block"
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
  <v-row v-if="!algorithmStore.loaded">
    <v-col cols="12" align="center">
      <v-progress-circular
        indeterminate
        :size="64"
        :width="6"
      />
    </v-col>
  </v-row>
  <v-row v-if="algorithmStore.loaded" class="elevation-0 mt-6">
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
    <v-data-table
      v-else-if="algorithms.length > 0"
      items-per-page="-1"
      :headers="headers"
      :items="algorithms"
      item-value="lars"
      item-title="name"
      class="pa-6 hover"
      @click:row="navigateToForm"
    >
      <template #item.actions>
        <v-hover>
          <v-btn
            size="small"
            class="me-2"
            color="blue-darken-2"
            variant="tonal"
          >
            <v-icon icon="mdi-lead-pencil" size="20" />
          </v-btn>
        </v-hover>
      </template>
    </v-data-table>
    <v-col
      v-else-if="!authStore.selectedOrg?.id"
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
import { useAuthStore } from '@/store/auth'
import { useAlgorithmStore } from '@/store/overview'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Algorithm } from '@/types/algorithm'
import { getExcelFile } from '@/services'

const router = useRouter()
const authStore = useAuthStore()
const algorithmStore = useAlgorithmStore()
if (authStore.selectedOrg) {
  algorithmStore.fetchAlgorithms(authStore.selectedOrg)
}

const algorithms = computed<Algorithm[]>(() => {
  return algorithmStore.algorithmsFormatted
})
const headers = [
  { title: 'Naam', value: 'name' },
  { title: 'Status', value: 'overviewStatus' },
  { title: 'Laatst bewerkt', value: 'last_update_dt' },
  { title: 'Publicatiestandaard', value: 'schema_version' },
  { title: 'ID', value: 'lars' },
  { title: '', key: 'actions', sortable: false },
]

const navigateToForm = (event: Event, data: any) => {
  const lars = data?.item.value
  if (lars) {
    router.push({ name: 'algorithm.edit', params: { lars } })
  } else {
    router.push({ name: 'algorithm.create' })
  }
}

const loading = ref(false)
const errorMessage = ref('')
const showSnackbar = ref(false)
const downloadExcel = async () => {
  const organization = authStore.selectedOrg
  if (!organization) {
    return
  }
  loading.value = true
  showSnackbar.value = false
  errorMessage.value = ''
  await getExcelFile(organization)
    .then((response) => {
      const blob = new Blob([response.data as BlobPart], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      })
      const fileURL = window.URL.createObjectURL(blob)
      const fileLink = document.createElement('a')
      fileLink.href = fileURL
      fileLink.setAttribute('download', 'overzicht_algoritmes.xlsx')
      document.body.appendChild(fileLink)
      fileLink.click()
    })
    .catch((error) => {
      errorMessage.value = error.data
      showSnackbar.value = true
    })
    .finally(() => (loading.value = false))
}

const singleOrgOverview = computed(() => authStore.organizations.length == 1)

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

.btn-title:first-letter {
  text-transform: capitalize;
}
</style>
