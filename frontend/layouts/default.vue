<template>
  <div id="content">
    <v-row>
      <v-col class="align-right">
        <LanguagePicker class="align-right"> </LanguagePicker>
      </v-col>
    </v-row>
    <slot />
  </div>
</template>

<script setup lang="ts">
import LanguagePicker from '@/components/LanguagePicker.vue'
import { useI18n } from 'vue-i18n'
const { t, locale } = useI18n()
const title = computed(() => t('homepageTitle'))
useHead({ title, htmlAttrs: { lang: locale } })
</script>

<style scoped>
#layout {
  margin: 0 auto 10px auto;
}

.row {
  display: flex;
}

.align-right {
  margin-left: auto;
}
</style>
