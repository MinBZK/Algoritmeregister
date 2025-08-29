<template>
  <div>
    <editor-field
      :allowed-html-tags="allowedHtmlTags"
      :content="data.about"
      :counter="6000"
      :rules="rules.about"
      @update:content="(e: string) => handleUpdate('about', e)"
    />
    <p>Voeg hier een link toe naar meer informatie op de eigen website:</p>
    <editor-field
      :content="data.contact_info"
      :counter="100"
      :rules="rules.contact_info"
      @update:content="(e: string) => handleUpdate('contact_info', e)"
    />
    <p class="mb-3">
      Sla de wijzigingen op:
    </p>
    <v-btn
      :disabled="!compliant || !dataStore.unsavedChanges"
      class="text-lowercase elevation-0 text-body-1 mb-2"
      :color="showPage ? 'green' : 'blue-darken-2'"
      @click="handleSubmit"
    >
      <span id="btn-title">
        {{ showPage ? 'Opslaan en vrijgeven' : 'Opslaan' }}
      </span>
    </v-btn>
    <v-progress-circular
      v-if="saveLoading"
      class="ml-3"
      indeterminate
      :size="30"
      :width="5"
    />
    <v-icon
      v-if="saveSuccess"
      class="ml-2"
      color="green"
    >
      mdi-check
    </v-icon>
    <span v-if="!compliant" class="color-red">
      Er kan niet opgeslagen worden met verkeerd ingevulde velden</span>
    <span v-if="dataStore.unsavedChanges && compliant" class="color-red">
      Er zijn wijzigingen niet opgeslagen</span>
  </div>
</template>

<script setup lang="ts">
import EditorField from '@/components/editor/EditorField.vue'
import { useAuthStore } from '@/store/auth'
import { ref, computed } from 'vue'
import type { OrganisationDetails } from '@/types/organisationDetails'
import { Language } from '@/types/misc'
import {
  getOrganisationDetails,
  updateOrganisationDetails,
} from '@/services/organisationDetails'
import { useFormDataStore } from '@/store/form-data'
import { countWithoutHTMLTags } from '@/utils/editor'

const authStore = useAuthStore()
const dataStore = useFormDataStore()

const data = ref<OrganisationDetails>({
  contact_info: '',
  about: '',
  organisation_id: 0,
  id: 0,
  create_dt: '',
  language: Language.NLD,
})

const getDetails = async () => {
  try {
    const result = await getOrganisationDetails(authStore.selectedOrg!.org_id)
    data.value = result.data
  } catch (e) {
    console.error(e)
  }
}
getDetails()

const handleUpdate = (key: 'about' | 'contact_info', value: string) => {
  data.value[key] = value
  dataStore.unsavedChanges = true
  saveSuccess.value = false
}

const saveSuccess = ref<boolean>(false)
const saveLoading = ref<boolean>(false)

const showPage = computed(() => authStore.selectedOrg!.show_page)

const handleSubmit = async () => {
  if (!compliant.value) return
  saveLoading.value = true
  try {
    await updateOrganisationDetails(authStore.selectedOrg!.org_id, data.value)
    dataStore.unsavedChanges = false
    saveSuccess.value = true
    saveLoading.value = false
    setTimeout(() => {
      saveSuccess.value = false
    }, 3000)
  } catch (e) {
    console.error(e)
  }
}

const allowedHtmlTags = ['div', 'br', 'p', 'ul', 'ol', 'li']

const compliant = computed(() => {
  const violation = Object.entries(data.value).find(([k, v]) => {
    // Find data in rules, run the rules and report if not compliant
    if (Object.keys(rules).includes(k)) {
      const ruleBroken = rules[k as keyof typeof rules].find((rule) => {
        return rule(v as string) !== true
      })
      return !!ruleBroken
    }
  })
  return !violation
})

const maxLength = 6000
const rules = {
  about: [
    (v: string | null) => {
      return (
        countWithoutHTMLTags(v) <= maxLength ||
        `Maximaal ${maxLength} karakters`
      )
    },
  ],
  contact_info: [
    (v: string | null) => {
      return countWithoutHTMLTags(v) <= 100 || 'Maximaal 100 karakters'
    },
    (v: string | null) => {
      return (
        !v || // can be empty
        (!!v?.match(
          // match with website regex.
          '^<p>https:\/\/(?:[a-zA-Z0-9-]+\.)?([a-zA-Z0-9-]+)\.([a-zA-Z0-9-]{2,4})(\/[a-zA-Z0-9-]+(?:\/[a-zA-Z0-9-]+)*)?\/?<\/p>$'
        ) &&
          v.split(' ').length <= 1) ||
        'Voer alleen een geldige URL in zoals https://algoritmes.overheid.nl'
      )
    },
  ],
}
</script>

<style scoped lang="scss">
h2 {
  margin-top: 0.25em;
  font-size: 1.25em;
}

.color-red {
  color: red;
}
</style>
