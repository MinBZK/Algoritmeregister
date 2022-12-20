<template>
  <div class="locale-changer text-grey text-end">
    <span
      v-for="locale in $i18n.availableLocales"
      :key="`locale-${locale}`"
      class="locale"
      @click="setLocale(locale)"
    >
      <template v-if="$i18n.locale !== locale">
        <a> {{ $t(`switchToLanguage.${locale}`) }}</a>
      </template>

      <!-- <template v-else> {{ $t(`locale-${locale}`) }}</template> -->

      <!-- <span v-if="index < $i18n.availableLocales.length - 1">|</span> -->
    </span>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useLocale } from 'vuetify'

const { current } = useLocale()

const composer = useI18n()

const setLocale = (newLocale) => {
  composer.locale.value = newLocale
  current.value = newLocale
}
</script>

<style scoped lang="scss">
input[type='radio'] {
  opacity: 0;
}

label {
  color: $primary;
  cursor: pointer;
}

span {
  padding-left: 0.25em;
  font-size: 85%;
}

span a {
  cursor: pointer;
  color: $primary-dark;
}
</style>
