<template>
  <v-row>
    <v-col>
      <h1 :class="singleOrgOverview ? 'text-h4 px-0' : 'text-h4 px-0 mt-10'">
        Overzicht {{ authStore.selectedOrg.name }}
      </h1>
    </v-col>
    <div class="pt-1" style="display: grid">
      <div
        v-if="authStore.selectedOrg.id && !singleOrgOverview"
        style="justify-self: end; width: 15em"
      >
        <v-label> Organisatie </v-label>
        <v-select
          :value="authStore.selectedOrg.name"
          :items="authStore.organizations"
          item-title="name"
          item-value="id"
          variant="outlined"
          hide-details
          @update:model-value="authStore.selectOrganization($event)"
        />
      </div>
      <v-btn
        class="mt-3 text-lowercase rounded-0 block"
        color="blue-darken-2"
        flat
        @click="navigateToForm"
      >
        <span id="btn-title"> Nieuw algoritme </span>
      </v-btn>
    </div>
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
      v-else-if="!authStore.selectedOrg.id"
      class="light-border text-center"
    >
      Er zijn nog geen organisaties aan dit account gekoppeld
    </v-col>
    <v-col v-else class="light-border text-center">
      Er zijn nog geen algoritmes toegevoegd aan deze organisatie.
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
import { useAuthStore } from '@/store/auth'
import { useAlgorithmStore } from '@/store/overview'
import { computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Algorithm } from '@/types/algorithm'

const router = useRouter()
const authStore = useAuthStore()
const algorithmStore = useAlgorithmStore()
algorithmStore.fetchAlgorithms(authStore.selectedOrg)

const algorithms = computed<Algorithm[]>(() => {
  return algorithmStore.algorithmsFormatted
})
const headers = [
  { title: 'Naam', value: 'name' },
  { title: 'Status', value: 'overviewStatus' },
  { title: 'Laatst bewerkt', value: 'last_update_dt' },
  { title: 'Versie', value: 'schema_version' },
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

const singleOrgOverview = computed(() => authStore.organizations.length == 1)

watch(
  () => authStore.selectedOrg,
  () => algorithmStore.fetchAlgorithms(authStore.selectedOrg)
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

#btn-title:first-letter {
  text-transform: capitalize;
}
</style>
