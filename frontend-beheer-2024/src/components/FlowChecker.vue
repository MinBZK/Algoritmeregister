<template>
  <template v-if="loading > 0">
    <v-progress-circular
      indeterminate
      :size="21"
      :width="3"
    /> &nbsp; Aan het
    laden...
  </template>
  <p v-else-if="!flowStructure">
    (Nog) Geen publicatieproces beschikbaar.
  </p>
  <v-form
    v-else
    v-model="valid"
    @submit.prevent="saveRoles"
  >
    <strong> Stel hier het publicatieproces in </strong> <br>
    Gekozen proces: {{ flowStructure.alias }}
    <div class="flow-warning">
      <span> Let op! </span>
      Een gebruiker kan altijd maar deelnemen aan 1 type publicatieproces. Als
      een gebruiker toegang heeft tot meerdere organisaties, zorg dan eerst dat
      deze gebruiker geen rollen meer heeft voor andere publicatieprocessen. Dit
      kan je doen door zijn/haar rollen te controleren bij het
      gebruikersoverzicht.
    </div>
    <div v-for="(role, n) in flowStructure?.roles" :key="n">
      <p>
        {{ role.alias }}
      </p>
      <v-select
        v-model="role.members"
        :items="users"
        multiple
        item-title="username"
        return-object
        variant="outlined"
        :rules="[(value: any[]) => minRequiredRule(value, role.min_required)]"
      >
        <template #selection="{ item }">
          {{ item.raw.first_name }} {{ item.raw.last_name }}:
          {{ item.raw.username }}
        </template>
      </v-select>
    </div>
    <div>
      <algreg-button
        :disabled="!valid"
        type="submit"
        width="68%"
        class="mr-2"
      >
        Opslaan
      </algreg-button>
      <algreg-button
        :disabled="valid"
        theme="delete"
        width="30%"
        :warn-with-dialog="true"
        dialog-text="Je staat op het punt een foutieve of onvolledige instelling op te slaan. Hiermee kan het publicatieproces van deze organisatie breken. Weet je het zeker?"
        dialog-title="Publicatieproces verkeerd ingevuld"
        label="Forceer opslaan"
        @confirm="saveRoles"
      />
    </div>
  </v-form>
</template>

<script setup lang="ts">
import AlgregButton from './AlgregButton.vue'
import { getFlowInstructions } from '@/services/flow'
import { getUsers, updateUser } from '@/services/user'
import { Flow } from '@/types/flow'
import { User } from '@/types/user'
import { ref, watch } from 'vue'
import { minRequiredRule } from '@/utils/rules'
import { useSnackbarStore } from '@/store/snackbar'
import { arrayToggleValue } from '@/utils'

const { add: addNotification } = useSnackbarStore()

const props = defineProps<{
  flow?: string
  orgId?: string
}>()

const loading = ref<number>(0)
const valid = ref<boolean>(true)

const users = ref<User[]>([])
const getUsersInScope = async () => {
  if (!props.orgId) return
  loading.value++
  let users_by_all_groups_role: User[] = []
  let users_by_org: User[] = []
  await getUsers({ role: 'all_groups' }).then((response) => {
    users_by_all_groups_role = response.data.users
  })
  await getUsers({ org: props.orgId }).then((response) => {
    users_by_org = response.data.users
  })
  // De-duplicate users
  const allUsers: User[] = [...users_by_all_groups_role, ...users_by_org]
  const uniqUsers: User[] = []
  allUsers.forEach((user) => {
    const selectedUsernames = uniqUsers.map((user) => user.username)
    if (!selectedUsernames.includes(user.username)) {
      uniqUsers.push(user)
    }
  })
  users.value = uniqUsers
  loading.value--
}
getUsersInScope()

const flowStructure = ref<Flow>()
const getFlow = async () => {
  loading.value++
  if (!props.orgId) return
  await getFlowInstructions(props.orgId).then((response) => {
    flowStructure.value = response.data
  })
  loading.value--
}
getFlow()

const saveRoles = async () => {
  if (!flowStructure.value) return
  // Determine need for updating per user
  users.value.forEach(async (user) => {
    let updatedRoles = [...user.roles]
    // Assigns or removes roles based on their new membership.
    let needsUpdate = false
    flowStructure.value!.roles.forEach((role) => {
      const userHasRole = role.members
        .map((m) => m.username)
        .includes(user.username)
      const userHadRole = user.roles.includes(role.key)
      updatedRoles = arrayToggleValue(updatedRoles, userHasRole, role.key)
      if (userHadRole !== userHasRole) needsUpdate = true
    })
    if (needsUpdate) {
      await updateUser(user.id, { roles: updatedRoles }).then(() => {
        addNotification({ message: `Gebruiker ${user.username} aangepast` })
      })
    }
  })
  addNotification({
    message: 'De publicatieproces-instellingen zijn opgeslagen.',
  })
  await getUsersInScope()
  await getFlow()
}

watch(
  () => [props.orgId, props.flow],
  async () => {
    getUsersInScope()
    getFlow()
  }
)
</script>

<style scoped lang="scss">
.flow-warning {
  span {
    color: red;
  }
  font-size: 0.7em;
}
</style>
