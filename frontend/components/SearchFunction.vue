<template>
  <div class="wrapper-1">
    <div class="wrapper-2">
      <v-text-field
        hide-details
        bg-color="white"
        color="primary"
        :label="searchHint"
        variant="outlined"
        :value="value"
        @input="$emit('input', $event.target.value)"
        @keyup.enter="$emit('doSearch')"
        prepend-inner-icon="mdi-magnify"
      ></v-text-field>
      <ButtonVue
        isAttached="left"
        v-if="!xs"
        :label="search"
        icon="mdi-magnify"
        @click="$emit('doSearch')"
      />
    </div>
    <div class="text-right">
      <div v-if="xs">
        <ButtonVue
          isAttached="top"
          :label="search"
          icon="mdi-magnify"
          @click="$emit('doSearch')"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ButtonVue from '@/components/form/Button.vue'
import { useI18n } from 'vue-i18n'
import { useDisplay } from 'vuetify'

const { t } = useI18n()
const { xs } = useDisplay()

const emit = defineEmits(['input', 'doSearch'])

const props = defineProps<{
  value: string
}>()

const search = computed(() => t('search'))
const searchHint = computed(() => t('searchHint'))
</script>

<style scoped lang="css">
.wrapper-2 {
  display: flex;
}
.wrapper-1 {
  margin-bottom: 10px;
}
.v-text-field :deep(label) {
  font-size: 1.1em;
}
</style>
