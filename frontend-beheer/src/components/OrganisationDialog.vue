<template>
  <v-dialog
    v-model="model"
    activator="parent"
    width="475"
  >
    <v-card rounded="lg">
      <v-toolbar>
        <v-toolbar-title>
          <v-icon icon="mdi-information-outline" class="mr-2" />
          {{ mode == 'edit' ? `Pas '${initial?.name}' aan:` : '' }}
          {{ mode == 'create' ? 'Maak een nieuwe organisatie:' : '' }}
        </v-toolbar-title>
      </v-toolbar>
      <v-list>
        <v-list-item>
          naam
          <v-text-field v-model="org.name" variant="outlined" />
        </v-list-item>
        <v-list-item>
          code
          <v-text-field v-model="org.code" variant="outlined" />
        </v-list-item>
        <v-list-item>
          type
          <v-select
            v-model="org.type"
            variant="outlined"
            :items="orgTypes"
          />
        </v-list-item>
      </v-list>
      <v-card-text>
        <div class="popup-text pa-2" />
      </v-card-text>
      <v-divider />
      <v-card-actions class="justify-end">
        <v-btn class="text-capitalize" @click="model = false">
          Annuleren
        </v-btn>
        <v-btn
          color="primary"
          class="text-capitalize"
          @click="confirm"
        >
          Doorgaan
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { Organisation, OrgType } from '@/types/organisation'
import { onMounted, ref, watch } from 'vue'

const props = defineProps<{
  initial?: Organisation
  mode: 'edit' | 'create'
}>()

// Implements component v-model
const emit = defineEmits<{
  (e: 'confirm', value: Organisation): void
}>()

const model = ref<boolean>(false)

watch(model, () => {
  if (props.initial) {
    // makes a shallow copy
    org.value = { ...props.initial }
  }
})

const org = ref<Organisation>({ name: '', code: '', type: null })

const orgTypes = Object.values(OrgType).filter(
  (value) => typeof value !== 'number'
)

onMounted(() => {
  if (props.initial) {
    // makes a shallow copy
    org.value = { ...props.initial }
  }
})
const confirm = () => {
  emit('confirm', org.value)
  model.value = false
}
</script>

<style scoped lang="scss">
.popup-text {
  font-size: 1.1rem;
  color: #4b4b4b;
}

:deep(.v-btn) {
  font-size: 1rem;
}
</style>
