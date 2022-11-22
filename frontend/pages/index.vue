<template>
  <Page :title="`Homepage`">
    <v-row>
      <v-col :cols="10">
        <v-text-field
          v-model="searchQuery"
          label="Zoek op organisatie, titel of omschrijving"
          variant="outlined"
          @keyup.enter="doSearch"
        ></v-text-field>
      </v-col>
      <v-col :cols="2"
        ><v-btn color="secondary" size="x-large" @click="doSearch"
          >Zoek</v-btn
        ></v-col
      >
    </v-row>
  </Page>
</template>

<script setup>
import Page from '@/components/PageWrapper.vue'

const searchQuery = ref('')

const doSearch = () => {
  const router = useRouter()
  router.push(`/algoritme?q=${searchQuery.value}`)
}
</script>
