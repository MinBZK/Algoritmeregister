<template>
  <div>
    <v-btn
      class="text-lowercase elevation-0 text-body-1 mb-2"
      block
      color="purple"
      border
    >
      <span id="btn-title"> Gebruik een sjabloon </span>
      <v-dialog
        v-model="dialog"
        activator="parent"
        width="600"
      >
        <v-card rounded="1">
          <v-toolbar color="purple">
            <v-toolbar-title> Sjabloonselectie </v-toolbar-title>
          </v-toolbar>
          <v-card-text class="intro-text">
            Sommige leveranciers hebben al een beschrijving van hun algoritmes
            aangeleverd. Deze kan je hier selecteren als startpunt voor jouw
            eigen algoritmebeschrijving.
            <span style="color: red; text-decoration: underline">
              Let op! Deze actie overschrijft de huidige data in het formulier.
            </span>
          </v-card-text>
          <v-list>
            <!-- <v-list-item>
              <v-text-field
                v-model="searchtext"
                style="margin-top: 1em"
                variant="outlined"
                label="Algoritmebeschrijving zoeken"
                density="comfortable"
                hide-details
              />
            </v-list-item> -->
            <v-list-item>
              Leveranciers
              <v-select
                v-model="selectedSupplier"
                return-object
                variant="outlined"
                item-title="name"
                :items="suppliers"
                density="comfortable"
                @update:model-value="selectedAlgoId = undefined"
              />
            </v-list-item>
            <v-list-item class="algo-list">
              <v-item-group
                v-model="selectedAlgoId"
                selected-class="bg-grey-lighten-2"
              >
                <v-list>
                  <v-item
                    v-for="algo in selectedSupplier?.algorithm_descriptions"
                    :key="algo.name"
                    v-slot="{ selectedClass, toggle }"
                  >
                    <v-list-item :class="selectedClass" @click="toggle">
                      {{ algo.name }}
                    </v-list-item>
                  </v-item>
                </v-list>
              </v-item-group>
            </v-list-item>
          </v-list>
          <v-card-text>
            <div class="popup-text pa-2">
              {{
                selectedDescription?.name
                  ? `Sjabloon van ${selectedSupplier?.name}: ${selectedDescription?.name}`
                  : '&nbsp;'
              }}
            </div>
          </v-card-text>
          <v-divider />
          <v-card-actions class="justify-end">
            <v-btn class="text-capitalize" @click="dialog = false">
              Annuleren
            </v-btn>
            <v-btn
              color="primary"
              class="text-capitalize"
              :disabled="!selectedDescription"
              @click="confirm"
            >
              Overnemen
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Supplier } from '@/types/templates'
import { useFormDataStore } from '@/store/form-data'
import { getTemplateList, getTemplate } from '@/services/templates'
const dialog = ref(false)

const dataStore = useFormDataStore()
const standardVersion = computed(() => dataStore.data.standard_version)

const suppliers = ref<Supplier[]>([])
const getSuppliers = async () =>
  (suppliers.value = (await getTemplateList(standardVersion.value)).data)
getSuppliers()

const selectedSupplier = ref<Supplier | undefined>(undefined)

const confirm = async () => {
  dialog.value = false
  if (!selectedDescription.value) return

  const algorithm = await getTemplate(
    standardVersion.value,
    selectedDescription.value?.id
  )
  dataStore.data = algorithm.data
}

const selectedAlgoId = ref<number>()
const selectedDescription = computed(() => {
  if (typeof selectedAlgoId.value === 'undefined') return
  return selectedSupplier.value?.algorithm_descriptions[selectedAlgoId.value]
})
</script>

<style scoped lang="scss">
.intro-text {
  font-size: 0.8em !important;
}

.algo-list {
  max-height: 300px;
  height: 300px;
}
:deep(.algo-list > .v-list-item__content) {
  height: inherit;
  overflow-y: scroll;
}
</style>
