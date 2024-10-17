<template>
  <v-navigation-drawer
    v-model="layoutStore.showTemplateDrawer"
    temporary
    location="right"
    :width="450"
    color="grey-background"
  >
    <v-toolbar class="mx-2 pr-3" color="grey-background">
      <v-toolbar-title>
        <strong> Kies een sjabloon </strong>
      </v-toolbar-title>
      <v-btn icon @click.stop="layoutStore.showTemplateDrawer = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-container class="mx-2 pr-6 pt-0">
      <span class="select-header"> Kies een Leverancier </span>
      <v-select
        v-model="selectedSupplier"
        class="mt-1"
        return-object
        variant="outlined"
        item-title="name"
        rounded="lg"
        :items="suppliers"
        density="comfortable"
        @update:model-value="selectedAlgorithm = undefined"
      />
      <span
        v-if="selectedSupplier"
        class="select-header"
      >Kies een sjabloon</span>
      <v-select
        v-if="selectedSupplier && selectedSupplier.algorithm_descriptions"
        v-model="selectedAlgorithm"
        class="mt-1"
        rounded="lg"
        variant="outlined"
        density="comfortable"
        :items="selectedSupplier.algorithm_descriptions"
        item-title="name"
        return-object
      />
      <algreg-button
        theme="primary"
        :disabled="!selectedAlgorithm"
        class="add-sjabloon-button"
        @confirm="confirm"
      >
        Sjabloon Invoegen
      </algreg-button>
      <div class="explainer mt-3">
        <span>
          Sommige leveranciers hebben al een beschrijving van hun algoritmes
          aangeleverd. Deze kan je hier selecteren als startpunt voor jouw eigen
          algoritmebeschrijving.
        </span>
        <div class="color-red-text-decoration mt-3">
          Let op! Deze actie overschrijft de huidige data in het formulier.
        </div>
      </div>
    </v-container>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { useLayoutStore } from '@/store/layout'
import { useFormDataStore } from '@/store/form-data'
import { computed, ref, watch } from 'vue'
import AlgregButton from '@/components/AlgregButton.vue'
import { AlgorithmDescription, Supplier } from '@/types/templates'
import { getTemplate, getTemplateList } from '@/services/templates'

const dataStore = useFormDataStore()
const layoutStore = useLayoutStore()

const standardVersion = computed(() => dataStore.data.standard_version)

const suppliers = ref<Supplier[]>([])

const getSuppliers = async () =>
  (suppliers.value = (await getTemplateList(standardVersion.value)).data)

const selectedSupplier = ref<Supplier | undefined>(undefined)
const selectedAlgorithm = ref<AlgorithmDescription | undefined>(undefined)

const confirm = async () => {
  if (!selectedAlgorithm.value) return

  const algorithm = await getTemplate(
    standardVersion.value,
    selectedAlgorithm.value?.id
  )
  dataStore.data = algorithm.data
}

const openWatcher = computed(() => layoutStore.showTemplateDrawer)
watch(openWatcher, () => {
  if (openWatcher.value) {
    getSuppliers()
  }
})
</script>

<style scoped lang="scss">
.explainer {
  font-size: 0.75em !important;
}

.color-red-text-decoration {
  color: rgb(232, 0, 0);
  font-weight: bold;
}

.select-header {
  font-weight: 400;
  font-size: 0.75em;
}

.add-sjabloon-button {
  width: 60% !important;
}
</style>
