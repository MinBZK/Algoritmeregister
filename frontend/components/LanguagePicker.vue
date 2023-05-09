<template>
  <p>{{ t('selectLanguage') }}:</p>
  <FormOverheidButton
    v-for="(locale, index) in availableLocales"
    :key="index"
    :button-id="locale"
    :align-horizontally="true"
    :label="t(`locales.${locale}`)"
    :style="locale == currentLocale ? 'primary' : 'secondary'"
    :disabled="locale == currentLocale"
    :aria-label="t('switchToLanguage', { language: t('locales.' + locale) })"
    @click="setLocale(locale)"
    @keydown.enter.prevent="changeLocale(locale)"
    @keydown.space.prevent="changeLocale(locale)"
  />
</template>

<script setup lang="ts">
const { setLocale, currentLocale } = useLocale()
const { t } = useI18n()

const availableLocales = ['nl', 'en']

const changeLocale = (locale: string) => {
  document.getElementById(currentLocale.value)?.focus()
  setLocale(locale)
}
</script>

<style scoped lang="scss">
p {
  margin: 0;
}
</style>
