<template>
  <v-navigation-drawer
    :model-value="modelValue"
    temporary
    location="right"
    :width="550"
    @update:model-value="(e) => $emit('update:modelValue', e)"
  >
    <v-form
      ref="form"
      v-model="valid"
      @submit.prevent="save"
    >
      <v-container>
        <h3 class="mb-3">
          Gegevens
        </h3>
        <v-text-field
          v-model="attributes.username"
          :disabled="!!user"
          variant="outlined"
          label="E-mailadres"
          :rules="[requiredRule, emailRule]"
        />
        <v-text-field
          v-model="attributes.first_name"
          variant="outlined"
          label="Voornaam"
          :rules="[requiredRule]"
        />
        <v-text-field
          v-model="attributes.last_name"
          variant="outlined"
          label="Achternaam"
          :rules="[requiredRule]"
        />
        <v-autocomplete
          v-model="attributes.groups"
          multiple
          :items="organisations"
          label="Organisaties"
          class="mb-3"
          return-object
          item-title="name"
          variant="outlined"
          hide-details
        />
        <div class="d-inline-flex align-center">
          <v-switch
            v-model="allGroups"
            inset
            hide-details
            class="mr-3"
            color="warning"
          />
          <div>Heeft toegang tot alle groepen</div>
        </div>
        <br>
        <div class="d-inline-flex align-center">
          <v-switch
            v-model="activated"
            inset
            hide-details
            class="mr-3"
            color="success"
          />
          <div>Geactiveerd</div>
        </div>
        <br>
        <div class="d-inline-flex align-center">
          <v-switch
            v-model="orgDetail"
            inset
            hide-details
            class="mr-3"
            color="success"
          />
          <div>Heeft toegang tot organisatie-detailpagina</div>
        </div>
        <br>
        Uniek ID:
        <p class="mb-4">
          {{ user?.id || '-' }}
        </p>
        <div class="d-inline-flex w-100">
          <AlgregButton type="submit" class="mr-2">
            {{ !!user ? 'Opslaan' : 'Aanmaken' }}
          </AlgregButton>
          <AlgregButton
            :disabled="!user"
            theme="delete"
            warn-with-dialog
            dialog-title="Deze actie kan niet ongedaan gemaakt worden."
            dialog-text="Weet je zeker dat je deze gebruiker wilt verwijderen?"
            @confirm="$emit('remove', user!.id)"
          >
            Verwijderen
          </AlgregButton>
        </div>
      </v-container>
    </v-form>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { User, UserNew, UserUpdate } from '@/types/user'
import { ref, watch } from 'vue'
import AlgregButton from '../AlgregButton.vue'
import { VForm } from 'vuetify/lib/components/index.mjs'
import { Organisation } from '@/types/organisation'
import { getOrganisations } from '@/services/organisation'
import { requiredRule, emailRule } from '@/utils/rules'
import { arrayToggleValue } from '@/utils'

interface UserInDrawer {
  username: string
  first_name: string
  last_name: string
  groups: Organisation[]
  roles: string[]
}

const props = defineProps<{
  user: User | null
  modelValue: boolean
}>()

watch(
  () => props.user,
  () => {
    form.value?.resetValidation()
    // Update local attributes based on prop update
    attributes.value = {
      username: props.user?.username || '',
      first_name: props.user?.first_name || '',
      last_name: props.user?.last_name || '',
      groups: props.user?.organisations || [],
      roles: props.user?.roles || [],
    }
    activated.value = !props.user?.roles.includes('disabled') ?? true
    allGroups.value = props.user?.roles.includes('all_groups') ?? false
    orgDetail.value = props.user?.roles.includes('orgdetail') ?? false
  }
)

const attributes = ref<UserInDrawer>({
  username: '',
  first_name: '',
  last_name: '',
  groups: [],
  roles: [],
})

const form = ref<VForm>()
const valid = ref<boolean>(true)
const allGroups = ref<boolean>(false)
const activated = ref<boolean>(true)
const orgDetail = ref<boolean>(false)

const save = () => {
  if (!valid.value) return
  // Three roles are separated so they have to be joined in again.
  let roles = attributes.value.roles
  roles = arrayToggleValue(roles, !activated.value, 'disabled')
  roles = arrayToggleValue(roles, allGroups.value, 'all_groups')
  roles = arrayToggleValue(roles, orgDetail.value, 'orgdetail')
  if (props.user) {
    const user: UserUpdate = {
      ...attributes.value,
      roles,
      groups: attributes.value.groups.map((group) => group.org_id),
    }
    emit('save', user, props.user.id)
  } else {
    const user: UserNew = {
      ...attributes.value,
      roles,
      groups: attributes.value.groups.map((group) => group.org_id),
    }
    emit('add', user)
  }
}

const organisations = ref<Organisation[]>([])
const fetchOrganisations = async () => {
  try {
    organisations.value = (await getOrganisations()).data.organisations
  } catch (error) {
    console.error('Unable to fetch organisation list', error)
  }
}
fetchOrganisations()

const emit = defineEmits<{
  (e: 'update:modelValue', modelValue: boolean): void
  (e: 'remove', user_id: string): void
  (e: 'add', user: UserNew): void
  (e: 'save', user: UserUpdate, user_id: string): void
}>()
</script>
