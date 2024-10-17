<template>
  <user-drawer
    v-model="showDrawer"
    :user="selectedUser"
    @add="add"
    @save="update"
    @remove="remove"
  />
  <div class="d-flex justify-space-between align-center">
    <h2>Overzicht</h2>
    <AlgregButton
      class="my-4"
      theme="primary"
      width="200px"
      @confirm=";[(selectedUser = null), (showDrawer = true)]"
    >
      Gebruiker toevoegen
    </AlgregButton>
  </div>
  <div class="w-25">
    <v-text-field
      v-model="options.search"
      label="Zoek naar een gebruiker"
      variant="outlined"
      clearable
      @keyup.enter="getThisPage(options)"
      @click:clear="getThisPage(options)"
    />
  </div>
  <v-data-table-server
    v-model:items-per-page="options.itemsPerPage"
    v-model="selectedUser"
    :headers="headers"
    :items="users"
    hover
    :items-length="totalUsers"
    :loading="loading"
    :search="options.search"
    :items-per-page-options="[10, 25, 50]"
    @update:options="getThisPage"
    @update:items-per-page="(itemsPerPage: number) => getThisPage({...options, itemsPerPage})"
    @click:row="selectUser"
  >
    <template #item.groups="item">
      <span
        v-for="(group, index) in item?.item.organisations"
        :key="group.code"
      >
        <span v-if="index != 0">,</span> {{ group.name }}
      </span>
    </template>
    <template #item.roles="item">
      <span
        v-for="(role, index) in parseRoles(item?.item.roles ?? [])"
        :key="role"
      >
        <span v-if="index != 0">,</span> {{ role }}
      </span>
    </template>
    <template #item.all_groups_access="item">
      <div class="d-flex justify-center">
        <v-icon v-if="item?.item.roles.includes('all_groups')" color="success">
          mdi-check
        </v-icon>
        <v-icon v-else color="error">
          mdi-close
        </v-icon>
      </div>
    </template>
    <template #item.activated="item">
      <div class="d-flex justify-center">
        <v-icon v-if="!item?.item.roles.includes('disabled')" color="success">
          mdi-check
        </v-icon>
        <v-icon v-else color="error">
          mdi-close
        </v-icon>
      </div>
    </template>
  </v-data-table-server>
</template>

<script setup lang="ts">
import AlgregButton from '@/components/AlgregButton.vue'
import UserDrawer from '@/components/user-management/UserDrawer.vue'
import { notifications } from '@/config/notifications'
import { getUsers, deleteUser, createUser, updateUser } from '@/services/user'
import { SnackbarTheme, useSnackbarStore } from '@/store/snackbar'
import { User, UserNew, UserUpdate } from '@/types/user'
import { ref } from 'vue'

const { add: addNotification } = useSnackbarStore()

const showDrawer = ref<boolean>(false)
const loading = ref<boolean>(false)
const totalUsers = ref<number>(300)
const users = ref<User[]>([])
const options = ref<DataTableOptions>({ itemsPerPage: 10, page: 1 })

interface DataTableOptions {
  itemsPerPage: number
  page: number
  search?: string
}

const getThisPage = async (newOptions: DataTableOptions) => {
  loading.value = true
  // Store current settings
  options.value = newOptions
  await getUsers({
    q: newOptions.search,
    limit: newOptions.itemsPerPage,
    skip: (newOptions.page - 1) * newOptions.itemsPerPage,
  })
    .then((response) => {
      totalUsers.value = response.data.count
      users.value = response.data.users
    })
    .catch((response) => {
      console.error(response)
      if (response.status == 424) {
        addNotification({
          message: 'Error 424: Het ophalen van gebruikersgegevens is mislukt.',
          theme: SnackbarTheme.error,
        })
      }
    })
    .finally(() => (loading.value = false))
}

const remove = async (user_id: string) => {
  loading.value = true
  await deleteUser(user_id)
    .then(() => {
      addNotification(notifications.removeUserSuccess!)
      showDrawer.value = false
      users.value = users.value.filter((user) => user.id != user_id)
    })
    .catch((response) => console.error(response))
  loading.value = false
}

const add = async (user: UserNew) => {
  loading.value = true
  await createUser(user)
    .then(async () => {
      addNotification(notifications.addUserSuccess!)
      showDrawer.value = false
      await getThisPage(options.value)
    })
    .catch((response) => {
      console.error(response)
      if (response.data == 'INVALID_EMAIL') {
        addNotification(notifications.addUserErrorInvalidEmail!)
      } else if (response.data == 'NOT_UNIQUE_USERNAME') {
        addNotification(notifications.addUserErrorNotUniqueUsername!)
      }
    })
  loading.value = false
}

const update = async (user: UserUpdate, user_id: string) => {
  loading.value = true
  await updateUser(user_id, user)
    .then(async () => {
      addNotification(notifications.updateUserSuccess!)
      showDrawer.value = false
      await getThisPage(options.value)
    })
    .catch((response) => {
      console.error(response)
    })
  loading.value = false
}

const headers = [
  { title: 'Voornaam', key: 'first_name', sortable: false, width: '10%' },
  { title: 'Achternaam', key: 'last_name', sortable: false, width: '10%' },
  { title: 'E-mailadres', key: 'username', sortable: false, width: '15%' },
  { title: 'Organisatie(s)', key: 'groups', sortable: false },
  { title: 'Speciale rol(len)', key: 'roles', sortable: false },
  {
    title: 'Toegang tot alle groepen',
    key: 'all_groups_access',
    sortable: false,
    width: '8%',
  },
  { title: 'Geactiveerd', key: 'activated', sortable: false, width: '7%' },
]

const selectUser = (_: PointerEvent, v: { item: User }) => {
  showDrawer.value = true
  selectedUser.value = v.item
}
const selectedUser = ref<User | null>(null)

const parseRoles = (roles: string[]) => {
  const excludedRoles = ['disabled', 'all_groups']
  const roleMapping: Record<string, string> = {
    admin: 'Beheerder',
    ictu: 'ICTU',
    orgdetail: 'Organisatiedetail',
  }
  let newRoles = roles.filter((role) => !excludedRoles.includes(role))
  return newRoles.map((role) => roleMapping[role] ?? role)
}
</script>
