<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'
import LanguagePicker from '@/components/LanguagePicker.vue'

const x = useI18n()
const { t } = x
const helloName = computed(() => t('hello', { name: 'Terry' }))
</script>

<template>
  <div>
    <NuxtLoadingIndicator
      color="repeating-linear-gradient(to right,#01689b 0%,#81c0df 50%,#4fb6e9 100%)"
      :height="5"
    />

    {{ helloName }}
    <LanguagePicker />

    <!-- <h1>{{ $t('hello', { name: 'vue-i18n' }) }}</h1>
    

    <div class="locale-changer">
      <form>
        <label for="locale-select">{{ $t('language') }}: </label>
        <select id="locale-select" v-model="$i18n.locale">
          <option
            v-for="locale in $i18n.availableLocales"
            :key="`locale-${locale}`"
            :value="locale"
          >
            {{ locale }}
          </option>
        </select>
      </form>
    </div> -->

    <AppHeader title="Algoritmeregister" :pages="['algoritme']" />

    <NuxtPage />
  </div>
</template>

<style>
#content {
  width: 1200px;
  margin: 0 auto;
  padding-top: 0.5em;
}
</style>
