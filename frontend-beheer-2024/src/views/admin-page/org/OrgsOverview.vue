<template>
  <div class="d-flex justify-space-between align-center">
    <h2>Overzicht</h2>
    <algreg-button
      class="my-4"
      theme="primary"
      width="200px"
      @confirm="$router.push({ name: 'orgView', params: { orgCode: 'new' } })"
    >
      Organisatie toevoegen
    </algreg-button>
  </div>
  <div class="w-25">
    <v-text-field
      v-model="options.search"
      label="Zoek naar een organisatie"
      variant="outlined"
      clearable
      @keyup.enter="getThisPage(options)"
      @click:clear="getThisPage(options)"
    />
  </div>
  <v-data-table-server
    v-model:items-per-page="options.itemsPerPage"
    :loading="loading"
    :headers="headers"
    hover
    :items="organisations"
    :items-per-page-options="[10, 25, 50, 100]"
    :items-length="totalOrgs"
    :search="options.search"
    @update:items-per-page="(itemsPerPage: number) => getThisPage({...options, itemsPerPage})"
    @update:options="getThisPage"
    @click:row="selectOrganisation"
  >
    <template #item.show_page="item">
      <v-icon v-if="item?.item?.show_page" color="success">
        mdi-check
      </v-icon>
      <v-icon v-else color="error">
        mdi-close
      </v-icon>
    </template>
  </v-data-table-server>
</template>
<script setup lang="ts">
import AlgregButton from '@/components/AlgregButton.vue'
import { getOrganisations } from '@/services/organisation'
import { Organisation } from '@/types/organisation'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const options = ref<DataTableOptions>({ itemsPerPage: 50, page: 1 })
const loading = ref<boolean>(false)
const totalOrgs = ref<number>(0)

interface DataTableOptions {
  itemsPerPage: number
  page: number
  search?: string
}

const organisations = ref<Organisation[]>([])
const getThisPage = async (newOptions: DataTableOptions) => {
  loading.value = true
  // Store current settings
  options.value = newOptions
  await getOrganisations({
    q: newOptions.search,
    limit: newOptions.itemsPerPage,
    skip: (newOptions.page - 1) * newOptions.itemsPerPage,
  })
    .then((response) => {
      totalOrgs.value = response.data.count
      organisations.value = response.data.organisations
    })
    .catch((response) => {
      console.error(response)
    })
  setTimeout(() => {
    loading.value = false
  }, 1000)
}

const router = useRouter()
const selectOrganisation = (_: PointerEvent, v: { item: Organisation }) => {
  router.push({ name: 'orgView', params: { orgCode: v.item.code } })
}
const headers = [
  { title: 'Naam', key: 'name', sortable: false, width: '30%' },
  { title: 'Code', key: 'code', sortable: false },
  { title: 'Type', key: 'type', sortable: false },
  { title: 'Gekozen Flow', key: 'flow', sortable: false, width: '10%' },
  {
    title: 'Openbare organisatiepagina',
    key: 'show_page',
    sortable: false,
    width: '15%',
  },
]
</script>
