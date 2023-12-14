<template>
  <!-- eslint-disable-next-line-->
  <div :class="class">
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
    <div v-if="variant == 'v-select'" style="display: flex">
      <v-select
        v-model="selectedFormat"
        return-object
        class="select-bar"
        hide-details
        rounded="0"
        label="Download alles"
        variant="outlined"
        density="compact"
        :items="downloadOptions"
        :disabled="isDisabled"
      />
      <v-btn
        flat
        class="rounded-0 download-button"
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

const authStore = useAuthStore()
const algorithmStore = useAlgorithmStore()
const dataStore = useFormDataStore()

const props = withDefaults(
  defineProps<{
    variant?: 'v-select' | 'v-btn'
    lars?: string
    class?: string
  }>(),
  { variant: 'v-select', lars: undefined, class: '' }
)

const selectedFormat = ref()

const loading = ref(false)
const errorMessage = ref('')
const showSnackbar = ref(false)

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
  showSnackbar.value = false
  errorMessage.value = ''

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
    errorMessage.value = response.data as string
    showSnackbar.value = true
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
.btn-title:first-letter {
  text-transform: capitalize;
}

:deep(.v-input__control) {
  --v-input-control-height: 40px !important;
}

.download-button {
  border-width: thin !important;
  border-style: solid !important;
  border-color: rgb(173, 192, 212) !important;
  border-left-width: 0 !important;
  min-height: 41px !important;
  max-width: 41px !important;
  min-width: 41px !important;
}

:deep(.v-btn--disabled) {
  color: white !important;
  border-color: rgb(224, 231, 249) !important;
}
</style>
