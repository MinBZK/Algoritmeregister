<template>
  <div class="orgtype-button-wrapping">
    <OrgTypeButton
      v-for="orgType in availableTypes"
      :key="orgType.type"
      :value="orgType.type"
      :style="getButtonStyle(orgType.type)"
      @click="buttonClicked(orgType.type)"
    />
  </div>
</template>

<script setup lang="ts">
import OrgTypeButton from './OrgTypeButton.vue'
import { OrgType } from 'types/organisation'
import { OrganisationFilterGroup } from 'types/filter'

const props = defineProps<{
  availableTypes?: OrganisationFilterGroup[]
  modelValue?: OrgType
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', modelValue: string | undefined): void
}>()

const buttonClicked = (orgType: string): void => {
  if (props.modelValue === orgType) {
    emit('update:modelValue', undefined)
  } else {
    emit('update:modelValue', orgType)
  }
}

const getButtonStyle = (orgType: string): 'active' | 'open' | 'disabled' => {
  if (props.modelValue === orgType) return 'active'
  if (props.modelValue === undefined) return 'open'
  return 'disabled'
}
</script>

<style lang="scss">
.orgtype-button-wrapping {
  display: flex;
  flex-wrap: wrap;
  column-gap: 0.75em;
}
</style>
