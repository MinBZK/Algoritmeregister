<template>
  <v-navigation-drawer
    v-model="layoutStore.showVersionDrawer"
    temporary
    location="right"
    :width="475"
    color="grey-background"
  >
    <v-toolbar class="mx-2 pr-3" color="grey-background">
      <v-toolbar-title>
        <strong>Opgeslagen versies</strong>
      </v-toolbar-title>
      <v-btn icon @click.stop="layoutStore.showVersionDrawer = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-container class="pr-8">
      <div class="d-flex justify-space-between">
        <algreg-button
          theme="primary"
          class="half-width"
          :disabled="!selectedVersion"
          @confirm="displayThisVersion"
        >
          Toon geselecteerde versie
        </algreg-button>
        <router-link
          :to="{ name: 'archive.index' }"
          class="text-body-1 half-width align-content-center text-end"
        >
          Naar archiefoverzicht
        </router-link>
      </div>
      <div v-if="loading" class="center-loading-icon">
        <v-progress-circular
          indeterminate
          :size="32"
          :width="4"
          color="primary"
        />
      </div>

      <template v-else-if="versions?.length">
        <version-selection-box
          v-for="version in versions"
          :key="version.id"
          :lars="lars"
          :data="version"
          :focus="version === selectedVersion"
          @click="selectedVersion = version"
          @change="getVersions"
        />
      </template>
      <template v-else>
        <div class="ml-2">
          Er zijn geen oude versies beschikbaar van deze algoritmebeschrijving.
        </div>
      </template>
    </v-container>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { computed, ref, toRefs, watch } from 'vue'
import { getAlgorithmVersions } from '@/services/algorithms'
import { AlgorithmForm, AlgorithmWithUser } from '@/types/algorithm'
import VersionSelectionBox from '@/components/archive/VersionSelectionBox.vue'
import AlgregButton from '@/components/AlgregButton.vue'
import { useFormDataStore } from '@/store/form-data'
import { useLayoutStore } from '@/store/layout'
import { useArchiveStore } from '@/store/archive'
import { useSnackbarStore } from '@/store/snackbar'
import { notifications } from '@/config/notifications'

const layoutStore = useLayoutStore()
const snackbarStore = useSnackbarStore()

const loading = ref<boolean>(false)

const props = defineProps<{
  lars: string
  orgCode: string
}>()

const archiveStore = useArchiveStore()
const { selectedVersion  } = toRefs(archiveStore)
const versions = ref<AlgorithmWithUser[]>([])
const getVersions = async () => {
  if (!props.orgCode || !props.lars) {
    console.error('no org or no lars selected')
    return
  }
  loading.value = true
  try {
    versions.value = (await getAlgorithmVersions(props.orgCode, props.lars, false)).data
  } catch (e) {
    snackbarStore.add({
      ...notifications.unarchiveVersionError!,
    })
  }
  finally {
    loading.value = false
  }
}

const openWatcher = computed(() => layoutStore.showVersionDrawer)
watch(openWatcher, () => {
  if (!!openWatcher.value) {
    getVersions()
  }
})

const displayThisVersion = () => {
  const dataStore = useFormDataStore()
  // Additional attributes (user_id) are passed silently.
  dataStore.data = selectedVersion.value as AlgorithmForm
  dataStore.data.state = 'STATE_1'
  dataStore.unsavedChanges = true
  layoutStore.showVersionDrawer = false
}
</script>

<style scoped lang="scss">
.center-loading-icon {
  width: 100%;
  display: grid;
  justify-content: center;
}

.half-width {
  width: 48% !important;
}
</style>
