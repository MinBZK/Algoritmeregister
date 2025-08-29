<template>
  <div class="d-flex justify-space-between align-center">
    <h2 v-if="currentOrg" class="my-3">
      Overzicht van {{ orgUpdate?.name }}
    </h2>
    <h2 v-else class="my-3">
      Nieuwe organisatie
    </h2>
    <algreg-button
      width="200px"
      @confirm="$router.push({ name: 'beheer.organisation' })"
    >
      Terug naar overzicht
    </algreg-button>
  </div>
  <v-row>
    <v-col cols="6">
      <v-form
        ref="form"
        v-model="valid"
        @submit.prevent="save"
      >
        <v-card
          flat
          border
          class="pa-4"
        >
          <v-select
            v-model="orgUpdate.name"
            :items="altOrgNames"
            label="Organisatienaam (Zichtbaar door gehele website)"
            variant="outlined"
            :rules="[requiredRule]"
            class="mt-2"
          />
          <!-- <v-text-field
            v-model="orgUpdate.name"
            variant="outlined"
            label="Organisatienaam"
            :rules="[requiredRule]"
            class="mt-2"
          /> -->
          <v-text-field
            v-model="orgUpdate.code"
            variant="outlined"
            label="Technische naam (gebruik door API)"
            :rules="[requiredRule, nameNewNotAllowedRule]"
          />
          <v-select
            v-model="orgUpdate.flow"
            :items="flowOptions"
            label="Gekozen publicatieproces"
            class="mb-5"
            return-object
            variant="outlined"
            hide-details
            :rules="[requiredRule]"
          />
          <v-select
            v-model="orgUpdate.type"
            :items="orgTypes"
            label="Organisatietype"
            class="mb-4"
            variant="outlined"
            hide-details
            :rules="[requiredRule]"
          />
          Uniek ID: {{ currentOrg?.id || '-' }}

          <div class="d-inline-flex w-100 mt-4">
            <AlgregButton
              type="submit"
              class="mr-2"
              :disabled="!valid"
            >
              {{ !!currentOrg ? 'Opslaan' : 'Aanmaken' }}
            </AlgregButton>
            <AlgregButton
              :disabled="!currentOrg"
              theme="delete"
              warn-with-dialog
              dialog-text="Weet je zeker dat je deze organisatie wilt verwijderen?"
              dialog-title="Dit kan niet ongedaan gemaakt worden."
              @confirm="remove(currentOrg?.org_id!)"
            >
              Verwijderen
            </AlgregButton>
          </div>
        </v-card>
      </v-form>
    </v-col>
    <v-col cols="6">
      <v-card
        flat
        border
        class="pa-4"
      >
        <flow-checker :flow="currentOrg?.flow" :org-id="currentOrg?.org_id" />
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import FlowChecker from '@/components/FlowChecker.vue'
import AlgregButton from '@/components/AlgregButton.vue'
import { useAuthStore } from '@/store/auth'
import { OrgType, Organisation, OrganisationUpdate } from '@/types/organisation'
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { requiredRule, nameNewNotAllowedRule } from '@/utils/rules'
import {
  createOrganisation,
  deleteOrganisation,
  updateOrganisation,
  getAltOrganisationNames,
} from '@/services/organisation'
import { SnackbarTheme, useSnackbarStore } from '@/store/snackbar'
import { notifications } from '@/config/notifications'
import router from '@/router'

const currentOrg = ref<Organisation>()
const orgUpdate = ref<OrganisationUpdate>({
  name: '',
  code: '',
  org_id: '',
  flow: 'ictu_last',
  type: OrgType.gemeente,
})

const valid = ref<boolean>(true)

const { add: addNotification } = useSnackbarStore()
const loading = ref<boolean>(false)
const route = useRoute()
const flowOptions = ['ictu_last', 'self_publish_two']
const altOrgNames = ref<string[]>([])

const fetchAltOrgNames = async (orgName: string) => {
  const response = await getAltOrganisationNames(orgName)
  altOrgNames.value = response.data
}

const authStore = useAuthStore()
const assignOrg = () => {
  const existingOrg = authStore.organisations.find(
    (org) => route.params.orgCode == org.code
  )
  if (existingOrg) {
    fetchAltOrgNames(existingOrg.code)
    currentOrg.value = { ...existingOrg }
    orgUpdate.value = {
      name: existingOrg.name,
      code: existingOrg.code,
      org_id: existingOrg.org_id,
      flow: existingOrg.flow,
      type: existingOrg.type,
    }
  }
}
assignOrg()

const orgTypes = Object.values(OrgType).filter(
  (value) => typeof value !== 'number'
)

const save = async () => {
  if (currentOrg.value) {
    await update(orgUpdate.value, currentOrg.value.org_id)
  } else {
    await add(orgUpdate.value)
  }
}

const add = async (org: OrganisationUpdate) => {
  loading.value = true
  await createOrganisation(org)
    .then(async (response) => {
      currentOrg.value = response.data
      await authStore.fetchMe()
      addNotification(notifications.addOrgSuccess!)
      router.push({ name: 'orgView', params: { orgCode: response.data.org_id } })
    })
    .catch((error) => {
      if (error.data == 'NAME_TAKEN') {
        addNotification({
          message: `Nieuwe organisatie aanmaken mislukt; De naam ${org.name} is al in gebruik.`,
          theme: SnackbarTheme.error,
        })
      } else if (error.data == 'CODE_TAKEN') {
        addNotification({
          message: `Nieuwe organisatie aanmaken mislukt; De code ${org.code} is al in gebruik.`,
          theme: SnackbarTheme.error,
        })
      } else if (error.data == 'ORG_ID_TAKEN'){
        addNotification({
          message: `Nieuwe organisatie aanmaken mislukt; De org id ${org.org_id} is al in gebruik.`,
          theme: SnackbarTheme.error,
        })
      }
    })
  loading.value = false
}

const update = async (org: OrganisationUpdate, orgId: string) => {
  loading.value = true
  await updateOrganisation(orgId, org)
    .then(async (response) => {
      currentOrg.value = response.data
      await authStore.fetchMe()
      addNotification(notifications.updateOrgSuccess!)
    })
    .catch((error) => {
      if (error.data == 'NAME_TAKEN') {
        addNotification({
          message: `Organisatie aanpassen mislukt; De naam ${org.name} is al in gebruik.`,
          theme: SnackbarTheme.error,
        })
      } else if (error.data == 'CODE_TAKEN') {
        addNotification({
          message: `Organisatie aanpassen  mislukt; De code ${org.code} is al in gebruik.`,
          theme: SnackbarTheme.error,
        })
      } else if (error.data == 'ORG_ID_TAKEN') {
        addNotification({
          message: `Organisatie aanpassen  mislukt; De code ${org.org_id} is al in gebruik.`,
          theme: SnackbarTheme.error,
        })
      }
    })
  loading.value = false
}

const remove = async (orgId: string) => {
  loading.value = true
  await deleteOrganisation(orgId)
    .then(async () => {
      addNotification(notifications.removeOrgSuccess!)
      router.push({ name: 'beheer.organisation' })
    })
    .catch((response) => {
      console.error(response)
    })
  loading.value = false
}
</script>
