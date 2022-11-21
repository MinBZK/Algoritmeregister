<script setup>
import Page from '@/components/Page.vue'
import algoritmeService from '@/services/algoritme'

definePageMeta({
  title: 'Algoritmeoverzicht',
})

const keys = {
  id: 'project_id',
  name: 'naam',
}

const columnKeys = Object.keys(keys)
const algoritmes = await algoritmeService.getAll()
</script>

<template>
  <Page>
    <!-- <div v-for="a in algoritmes">{{ a }}</div> -->
    <v-table>
      <thead>
        <tr>
          <th v-for="key in columnKeys" :key="key" style="text-align: left">
            {{ keys[key] }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="algoritme in algoritmes" :key="algoritme.project_id">
          <td v-for="key in columnKeys" :key="key">
            <template v-if="key === 'name'">
              <NuxtLink :to="`/algoritme/${algoritme.project_id}`">
                {{ algoritme[keys[key]] }}
              </NuxtLink> </template
            ><template v-else>
              {{ algoritme[keys[key]] }}
            </template>
          </td>
        </tr>
      </tbody>
    </v-table>
  </Page>
</template>
