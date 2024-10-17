<template>
  <v-row v-if="archiveStore.loading">
    <v-col cols="12" align="center">
      <v-progress-circular
        indeterminate
        :size="64"
        :width="6"
      />
    </v-col>
  </v-row>
  <v-row v-else>
    <warning-dialog
      v-model="showDialog"
      :title="dialogContent.showArchivedVersion!.title"
      @confirmed="navigateToForm"
    >
      {{ dialogContent.showArchivedVersion!.content }}
    </warning-dialog>
    <v-col v-if="archiveStore.allVersions?.length" class="px-0">
      <v-data-table
        v-if="archiveStore.allVersions.length"
        items-per-page="-1"
        :headers="headers"
        :items="archiveStore.allVersions as AlgorithmWithUser[]"
        item-value="id"
        item-title="name"
        class="py-6 hover"
        hover
        @click:row="handleRowClick"
      >
        <template
          #item.actions="
            // @ts-ignore
            { item }
          "
        >
          <v-tooltip
            text="Dearchiveer"
            location="bottom"
          >
            <template #activator="{ props }">
              <v-btn
                v-if="!item.published"
                v-bind="props"
                icon="mdi-package-up"
                class="mx-auto rounded-lg p-0"
                color="primary"
                variant="tonal"
                size="38"
                rounded="0"
                @click="handleUnarchiveClick($event, item)"
              />
            </template>
          </v-tooltip>
        </template>
        <template #item.create_dt="item">
          {{ formatDateTime(item!.value) }}
        </template>
        <template #item.archive_dt="item">
          {{ formatDateTime(item!.value) }}
        </template>
      </v-data-table>
    </v-col>
    <v-col v-else-if="!authStore.me?.id" class="light-border text-center">
      Je account is nog niet geactiveerd. Neem contact op met de beheerder van
      het Algoritmeregister.
    </v-col>
    <v-col
      v-else-if="authStore.organisations.length === 0"
      class="light-border text-center"
    >
      Je bent nog niet aan een organisatie gekoppeld. Neem contact op met de
      beheerder om rechten tot een organisatie te verkrijgen.
    </v-col>
    <v-col v-else class="light-border text-center mt-8">
      Er zijn nog geen gearchiveerde versies in uw organisatie.
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useArchiveStore } from '@/store/archive'
import { useAuthStore } from '@/store/auth'
import { formatDateTime } from '@/utils/datetime'
import { ref } from 'vue'
import { AlgorithmWithUser } from '@/types/algorithm'
import WarningDialog from '@/components/AlgregWarningDialog.vue'
import { dialogContent } from '../../config/notifications'

const authStore = useAuthStore()
const archiveStore = useArchiveStore()
archiveStore.fetchAlgorithmVersionArchive(authStore.selectedOrg)


const headers = [
  { title: 'Algoritmebeschrijving titel', key: 'name' },
  { title: 'Datum van archivering', key: 'archive_dt' },
  { title: 'Versie aangemaakt op', key: 'create_dt' },
  { title: 'Gearchiveerd door', key: 'user_id' },
  { title: 'Acties', key: 'actions', sortable: false },
]

const router = useRouter()
type ArchiveTableItem = {item: AlgorithmWithUser, [key: string]: any}

const showDialog = ref<boolean>(false)
const selectedVersion = ref<AlgorithmWithUser | null>(null)
const handleRowClick = (_: Event, data: ArchiveTableItem) => {
  selectedVersion.value = data.item
  showDialog.value = true
}

const navigateToForm = () => {
  if (!selectedVersion.value) {
    console.error('selectedVersion is null')
    return
  }
  const lars = selectedVersion.value.lars
  archiveStore.selectedVersion = selectedVersion.value
  router.push({ name: 'algorithm.edit', params: { lars } })
}

const handleUnarchiveClick = (e: Event, item: AlgorithmWithUser) => {
  e.stopPropagation()
  archiveStore.unarchiveVersion(item.lars, item.id)
}
</script>
