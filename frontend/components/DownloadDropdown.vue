<template>
  <div v-if="isLoading" class="spinner-container">
    <span class="spinner"></span>
  </div>
  <div class="download-dropdown">
    <button
      :id="buttonId"
      ref="dropdownButton"
      class="button"
      :class="[
        {
          'button--block': fullWidth,
          disabled: isLoading,
        },
        `button--secondary`,
      ]"
      :aria-disabled="isLoading ? 'true' : 'false'"
      @click="displayDropdown = !displayDropdown"
    >
      <span class="button__label">
        {{ label }}
        <NuxtIcon size="1.2em" name="mdi:chevron-down" />
      </span>
    </button>
    <div v-if="displayDropdown" class="dropdown-content">
      <form
        ref="formElement"
        :action="action.currentPublished"
        @submit.prevent="
          handleDownload(action.currentPublished!, 'csv', 'recent')
        "
      >
        <button
          ref="csvButton"
          class="download-button"
          :aria-disabled="isLoading ? 'true' : 'false'"
          :disabled="!!isLoading"
        >
          <span class="button__label"> {{ t('RecentAlgorithms') }} CSV </span>
        </button>
      </form>
      <form
        v-if="action.allPublished"
        ref="formElement"
        :action="action.allPublished"
        @submit.prevent="handleDownload(action.allPublished!, 'csv', 'history')"
      >
        <button
          ref="csvButton"
          class="download-button"
          :aria-disabled="isLoading ? 'true' : 'false'"
          :disabled="!!isLoading"
        >
          <span class="button__label">
            {{ t('AlgorithmsWithHistory') }} CSV</span
          >
        </button>
      </form>
      <form
        ref="formElement"
        :action="action.currentPublished"
        @submit.prevent="
          handleDownload(action.currentPublished!, 'excel', 'recent')
        "
      >
        <button
          ref="xlsxButton"
          class="download-button"
          :aria-disabled="isLoading ? 'true' : 'false'"
          :disabled="!!isLoading"
        >
          <span class="button__label"> {{ t('RecentAlgorithms') }} XLSX</span>
        </button>
      </form>
      <form
        v-if="action.allPublished"
        ref="formElement"
        :action="action.allPublished"
        @submit.prevent="
          handleDownload(action.allPublished!, 'excel', 'history')
        "
      >
        <button
          ref="xlsxButton"
          class="download-button"
          :aria-disabled="isLoading ? 'true' : 'false'"
          :disabled="!!isLoading"
        >
          <span class="button__label">
            {{ t('AlgorithmsWithHistory') }} XLSX</span
          >
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string
    fullWidth?: boolean
    buttonId?: string | undefined
    action: {
      currentPublished: string | undefined
      allPublished?: string | undefined
    }
  }>(),
  {
    fullWidth: false,
    buttonId: undefined,
  }
)

const { t } = useI18n()
const dropdownButton = ref<HTMLButtonElement>()
const csvButton = ref<HTMLButtonElement>()
const xlsxButton = ref<HTMLButtonElement>()
const displayDropdown = ref<boolean>(false)
const isLoading = ref<boolean>(false)

const downloadSpecifiedFile = async (url: string, filetype: string) => {
  try {
    const result = await useFetch<Blob>(url + `?filetype=` + filetype, {
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      method: 'GET',
      responseType: 'blob',
    })
    return result
  } catch {
    isLoading.value = false
  }
}

const handleDownload = async (
  action: string,
  filetype: string,
  label: 'recent' | 'history'
) => {
  isLoading.value = true
  const result = await downloadSpecifiedFile(action, filetype)
  if (result && result.data) {
    const blobData = result.data.value
    const url = URL.createObjectURL(blobData!)
    const fileLink = document.createElement('a')
    fileLink.href = url
    const fileExtension = computed(() =>
      filetype === 'excel' ? 'xlsx' : filetype
    )
    const fileName =
      label === 'recent' ? t('RecentAlgorithms') : t('AlgorithmsWithHistory')
    const date = getCurrentDate()
    fileLink.setAttribute(
      'download',
      `${fileName} ${date}.` + fileExtension.value
    )
    document.body.appendChild(fileLink)
    fileLink.click()
    document.body.removeChild(fileLink)
    window.URL.revokeObjectURL(url)
    isLoading.value = false
  }
}

const getCurrentDate = (): string => {
  const dateObj = new Date()
  const year = dateObj.getFullYear()
  const month = dateObj.getMonth() + 1
  const day = dateObj.getDate()
  return `${year}-${month}-${day}`
}
</script>

<style scoped lang="scss">
@use '/assets/styles/colors' as colors;

.button {
  margin-bottom: 0em !important;
}
.inline-form {
  display: inline-block;
  margin-right: 1em;
}

.disabled {
  cursor: not-allowed;
}

.button--primary[aria-disabled='true'] {
  background-color: colors.$primary-darker !important;
  color: white !important;
}

.download-dropdown {
  position: relative;
  //display: inline-block;
}

.dropdown-content {
  position: absolute;
  left: 49.8%;
  transform: translateX(-50%);
  width: 100%;
  box-shadow:
    -8px 8px 8px -8px rgba(0, 0, 0, 0.2),
    8px 8px 8px -8px rgba(0, 0, 0, 0.2); /* Modify this line */
  z-index: 1;
  top: 2.9em;
  text-align: left;
  background: white;
  padding: 0.3em 1em;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
  border: 1px solid colors.$primary;
  border-top: none;
  padding-bottom: 0.5em;
}

.download-button {
  width: 100%;
  background-color: white;
  border: none;
  padding: 1em;
  margin: 1px;
}

.download-button:hover {
  background-color: colors.$secondary;
}

.spinner-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.5em;
}

.spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 4px solid #ccc;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
