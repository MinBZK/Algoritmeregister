<template>
  <h1 class="text-h5 px-0">
    Landelijke organisaties
  </h1>
  <p class="text-body-1 py-3">
    Hier wordt getoond hoeveel algoritmebeschrijvingen per ministerie en
    organisatiecluster zijn gepubliceerd in het Algoritmeregister.
  </p>
  <div>
    <v-row>
      <v-col>
        <v-data-table
          items-per-page="20"
          :headers="headers"
          :items="NationalOrganisationsResults"
        >
          <template #item.name="item">
            {{ item!.value }}
          </template>
          <template #item.Total="item">
            {{ item!.value }}
          </template>
          <template #item.KD="item">
            <b>
              {{ item!.value }}
            </b>
          </template>
          <template #item.UTO="item">
            <b>
              {{ item!.value }}
            </b>
          </template>
          <template #item.BOO="item">
            <b>
              {{ item!.value }}
            </b>
          </template>
          <template #item.Overig="item">
            <b>
              {{ item!.value }}
            </b>
          </template>
        </v-data-table>
        <p class="text-body-1 pb-4">
          <b>Legenda</b><br><b>KD:</b> Kerndepartement. <b>UTO</b> (Uitvoerende en toezichthoudende
          organisaties): Agentschappen, Inspecties, Zelfstandige bestuursorganen,
          Politie, Rechtspraak, Openbare lichamen voor beroep en bedrijf. <b>BOO</b>
          (Beleids- en overlegondersteunende organisaties): Adviescolleges,
          Interdepartementale commissies, Koepelorganisaties, Regionale
          samenwerkingsorganen. <b>Overig:</b> Organisatie met overheidsbemoeienis,
          Organisatieonderdeel.
        </p>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { getNationalOrganisations } from '@/services/nationalorganisations'
import { ref } from 'vue'
import type { NationalOrganisationsCount } from '@/types/nationalorganisations'

const NationalOrganisationsResults = ref<NationalOrganisationsCount[]>([])
const retrieveNationalOrganisations = async () => {
  const result = await getNationalOrganisations()
  NationalOrganisationsResults.value = result.data
}
retrieveNationalOrganisations()

const headers = [
  { title: 'Organisatie', key: 'name'},
  { title: 'Ministerie totaal', key: 'Total' },
  { title: 'KD', key: 'KD' },
  { title: 'UTO', key: 'UTO' },
  { title: 'BOO', key: 'BOO' },
  { title: 'Overig', key: 'Overig' },
]

</script>