<template>
  <!-- eslint-disable-next-line-->
  <div :class="class">
    <div v-if="variant == 'v-select'" class="flex-container">
      <v-select
        v-model="selectedFormat"
        return-object
        class="select-bar"
        hide-details
        rounded="lg te-0 be-0"
        :label="label"
        variant="outlined"
        density="comfortable"
        :items="downloadOptions"
        :disabled="isDisabled"
      />
      <v-btn
        flat
        class="download-button"
        rounded="lg ts-0 bs-0"
        :disabled="isDisabled || selectedFormat == null"
        @click="downloadFormat(selectedFormat, lars)"
      >
        <template v-if="loading">
          <v-progress-circular
            indeterminate
            :size="21"
            :width="3"
          />
        </template>

        <template v-else>
          <v-icon size="21">
            mdi-download
          </v-icon>
        </template>
      </v-btn>
    </div>
    <div v-else-if="variant == 'v-btn'">
      <v-btn
        size="small"
        variant="tonal"
        class="me-2"
      >
        <v-menu activator="parent">
          <v-card>
            <v-list>
              <v-list-item
                v-for="option in downloadOptions"
                :key="option!.value"
                @click="downloadFormat(option, lars)"
              >
                {{ option!.title }}
              </v-list-item>
            </v-list>
          </v-card>
        </v-menu>
        <template v-if="loading">
          <v-progress-circular
            indeterminate
            :size="21"
            :width="3"
          />
        </template>

        <template v-else>
          <v-icon size="21">
            mdi-download
          </v-icon>
        </template>
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth'
import { ref, computed } from 'vue'
import { useAlgorithmStore } from '@/store/overview'
import { getFileMany, getFileOne } from '@/services/downloads'
import { useFormDataStore } from '@/store/form-data'
import { SnackbarTheme, useSnackbarStore } from '@/store/snackbar'

const authStore = useAuthStore()
const algorithmStore = useAlgorithmStore()
const dataStore = useFormDataStore()
const snackbarStore = useSnackbarStore()

const props = withDefaults(
  defineProps<{
    variant?: 'v-select' | 'v-btn'
    lars?: string
    class?: string
    label?: string
  }>(),
  { variant: 'v-select', lars: undefined, class: '', label: 'Download alles' }
)

const selectedFormat = ref()
const loading = ref(false)

interface DownloadOption {
  title: string
  value: 'excel' | 'pdf' | 'word'
  filetype: string
}

const downloadOptions: DownloadOption[] = [
  {
    title: 'In Excel',
    value: 'excel',
    filetype: '.xlsx',
  },
  {
    title: 'In Word',
    value: 'word',
    filetype: '.docx',
  },
  {
    title: 'In PDF (beta)',
    value: 'pdf',
    filetype: '.pdf',
  },
]

const downloadFormat = async (
  selectedFormat: DownloadOption,
  lars?: string
) => {
  if (!authStore.selectedOrg) return
  loading.value = true

  const date = new Date()
  const dateMark = `${date.getFullYear()}-${
    date.getMonth() + 1
  }-${date.getDate()}`

  let response
  let filename: string
  if (lars) {
    response = await getFileOne(
      authStore.selectedOrg,
      lars,
      selectedFormat.value
    )
    // look for name
    let name = algorithmStore.algorithms.find((a) => a.lars == lars)?.name
    if (!name) {
      name = dataStore.data.name
    }
    filename = `${name} ${dateMark}`
  } else {
    response = await getFileMany(authStore.selectedOrg, selectedFormat.value)
    filename = `Algoritmebeschrijvingen van ${authStore.selectedOrg.name} ${dateMark}`
  }

  loading.value = false
  if (response.status != 200) {
    snackbarStore.add({
      message: response.data as string,
      theme: SnackbarTheme.error,
    })
    return
  }

  const blob = new Blob([response.data as BlobPart])
  const fileURL = window.URL.createObjectURL(blob)
  const fileLink = document.createElement('a')
  fileLink.href = fileURL

  fileLink.setAttribute('download', filename + selectedFormat.filetype)
  fileLink.click()

  URL.revokeObjectURL(fileURL)
}

const isDisabled = computed(() => {
  if (!props.lars) {
    return loading.value || algorithmStore.algorithms.length == 0
  } else {
    return loading.value
  }
})
</script>

<style scoped lang="scss">
:deep(.v-input__control) {
  --v-input-control-height: 40px !important;
}

.flex-container {
  display: flex;
}

.download-button {
  border-width: thin !important;
  border-style: solid !important;
  border-color: rgb(173, 192, 212) !important;
  border-left-width: 0 !important;
  min-height: 48px !important;
  max-width: 48px !important;
  min-width: 48px !important;
}

:deep(.v-btn--disabled) {
  color: white !important;
  border-color: rgb(224, 231, 249) !important;
}
</style>
