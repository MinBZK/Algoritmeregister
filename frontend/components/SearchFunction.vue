<template>
  <v-col :cols="10">
    <v-text-field
      bg-color="white"
      color="primary"
      :label="searchHint"
      variant="outlined"
      :value="value"
      @input="$emit('input', $event.target.value)"
      @keyup.enter="$emit('doSearch')"
      prepend-inner-icon="mdi-magnify"
    ></v-text-field> </v-col
  ><v-col>
    <ButtonVue :label="search" icon="mdi-magnify" @click="$emit('doSearch')" />
  </v-col>
</template>

<script setup lang="ts">
import ButtonVue from '@/components/form/Button.vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const emit = defineEmits(['input', 'doSearch'])

const props = defineProps<{
  value: string
}>()

const search = computed(() => t('search'))
const searchHint = computed(() => t('searchHint'))
</script>

<style lang="scss"></style>
