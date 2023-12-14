<template>
  <div class="language-picker">
    <button
      class="language-button"
      :data-selected="dropdown"
      @click="dropdown = !dropdown"
    >
      {{ buttonText }}
    </button>
    <div class="dropdown-content">
      <button
        v-for="lang in locales"
        :key="lang.code"
        tab-index="1"
        :class="{ 'lang-active': lang.code == locale }"
        class="lang-select-button"
        @click="changeLocale(lang.code)"
      >
        {{ lang.name }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const { setLocale, currentLocale } = useLocale()
const { t, locale } = useI18n()

const locales = [
  { code: 'nl', name: 'Nederlands' },
  {
    code: 'en',
    name: 'English',
  },
]

const dropdown = ref(false)

const changeLocale = (locale: string) => {
  document.getElementById(currentLocale.value)?.focus()
  setLocale(locale)
  dropdown.value = false
}

const buttonText = computed(
  () => t('language-picker.language') + ': ' + t(`locales.${locale.value}`)
)
</script>

<style scoped lang="scss">
.language-picker {
  z-index: 1;
  width: 12em;
}

.language-button {
  width: inherit;
  background-color: $primary;
  color: white;
  font-size: 0.85em;
  cursor: pointer;

  height: 100%;
  text-align: center;
  border: none;
}

.language-button:before {
  position: relative;
  right: 0.4em;
  top: 0.2em;
  transform: scale(0.9);
  display: inline-block;
  content: url('./assets/images/icons/icon-globe.svg');
}
.language-button[data-selected='true']:before {
  content: url('./assets/images/icons/icon-globe-dark.svg');
}

.language-button:after {
  display: inline-block;
  transform: scale(0.5, 0.7);
  content: url('./assets/images/icons/icon-language-picker-chevron.svg');
}
.language-button[data-selected='true']:after {
  content: url('./assets/images/icons/icon-language-picker-chevron-dark.svg');
  transform: scale(0.5, 0.7) rotate(180deg);
}

.language-button[data-selected='true'] {
  background-color: $secondary;
  color: $primary-darker;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: $secondary;
  width: inherit;
  box-shadow: 0px 10px 15px -3px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.lang-select-button {
  text-align: center;
  color: $primary-darker;
  padding: 0.75em 1em;
  font-size: 0.85em;
  margin: 0.75em;
  text-decoration: none;
  display: block;
  cursor: pointer;
  width: -webkit-fill-available;
  width: -moz-available;
  border: 0;
  background-color: $secondary;
}

.lang-select-button:hover {
  background-color: $primary;
  color: white !important;
}
.lang-select-button:focus {
  background-color: $primary;
  color: white !important;
}

.language-button[data-selected='true'] ~ .dropdown-content {
  display: block;
}

.lang-active {
  background-color: $primary !important;
  color: white !important;
}
</style>
