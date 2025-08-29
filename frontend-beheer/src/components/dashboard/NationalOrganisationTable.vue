<template>
  <h1 class="text-h5 px-0">
    Landelijke organisaties
  </h1>
  <p class="text-body-1 py-3">
    Hier wordt getoond hoeveel algoritmebeschrijvingen per ministerie en
    organisatiecluster zijn gepubliceerd in het Algoritmeregister.
  </p>
  <div>
    <table aria-label="Landelijke organisaties">
      <thead>
        <tr>
          <th />
          <th>Ministerie totaal</th>
          <th>KD</th>
          <th>UTO</th>
          <th>BOO</th>
          <th>Overig</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in NationalOrganisationsResults" :key="row.name">
          <td class="word-break">
            {{ row.name }}
          </td>
          <td>
            <b>
              {{ row.Total }}
            </b>
          </td>
          <td>
            <b>
              {{ row.KD }}
            </b>
          </td>
          <td>
            <b>
              {{ row.UTO }}
            </b>
          </td>
          <td>
            <b>
              {{ row.BOO }}
            </b>
          </td>
          <td>
            <b>
              {{ row.Overig }}
            </b>
          </td>
        </tr>
      </tbody>
    </table>
    <p class="text-body-1 pb-4">
      <b>Legenda</b><br><b>KD:</b> Kerndepartement. <b>UTO</b> (Uitvoerende en toezichthoudende
      organisaties): Agentschappen, Inspecties, Zelfstandige bestuursorganen,
      Politie, Rechtspraak, Openbare lichamen voor beroep en bedrijf. <b>BOO</b>
      (Beleids- en overlegondersteunende organisaties): Adviescolleges,
      Interdepartementale commissies, Koepelorganisaties, Regionale
      samenwerkingsorganen. <b>Overig:</b> Organisatie met overheidsbemoeienis,
      Organisatieonderdeel.
    </p>
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
</script>
<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
.word-break {
  word-break: break-word;
}
</style>