import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { AlgorithmWithUser } from '@/types/algorithm'
import {
  getArchive,
  archiveAlgorithmVersion,
  unarchiveAlgorithmVersion,
} from '@/services/algorithms'
import { Organisation } from '@/types/organisation'
import { notifications } from '@/config/notifications'
import { useSnackbarStore } from './snackbar'
import { useAuthStore } from './auth'

export const useArchiveStore = defineStore('archive', () => {
  const snackbarStore = useSnackbarStore()
  const authStore = useAuthStore()

  // State related to all algorithm versions
  const loading = ref(false)
  const allVersions = ref<AlgorithmWithUser[] | null>(null)
  const fetchAlgorithmVersionArchive = async (
    selectedOrg: Organisation | null
  ) => {
    if (!selectedOrg?.code) {
      console.log(
        'No organisation selected, skipped fetching algorithm versions.'
      )
      return
    }

    loading.value = true
    try {
      const response = await getArchive(selectedOrg.code)
      allVersions.value = response.data
    } catch (error) {
      console.error('Failed to fetch algorithm versions:', error)
      snackbarStore.add({
        ...notifications.fetchAlgorithmVersionsError!,
      })
    } finally {
      loading.value = false
    }
  }

  // State related to single algorithm version
  const selectedVersion = ref<AlgorithmWithUser | null>(null)
  const orgCode = computed(() => authStore.selectedOrg?.code)
  const archiveVersion = async (lars: string, versionId: string) => {
    if (!orgCode.value) {
      console.error('No organisation code found, cannot archive version.')
      return
    }

    try {
      await archiveAlgorithmVersion(orgCode.value, lars, versionId)
      snackbarStore.add({
        ...notifications.archiveVersionSuccess!,
      })
    } catch (error) {
      snackbarStore.add({
        ...notifications.archiveVersionError!,
      })
    }
  }

  const unarchiveVersion = async (lars: string, versionId: string) => {
    if (!orgCode.value) {
      console.error('No organisation code found, cannot unarchive version.')
      return
    }
    try {
      await unarchiveAlgorithmVersion(orgCode.value, lars, versionId)
      snackbarStore.add({
        ...notifications.unarchiveVersionSuccess!,
      })
      const version = allVersions.value?.find((v) => v.id === versionId)
      if (version) {
        version.state = 'STATE_1'
        allVersions.value = allVersions.value!.filter((v) => v.id !== versionId)
      }
    } catch (error) {
      snackbarStore.add({
        ...notifications.unarchiveVersionError!,
      })
    }
  }

  return {
    loading,
    allVersions,
    fetchAlgorithmVersionArchive,
    selectedVersion,
    archiveVersion,
    unarchiveVersion,
  }
})
