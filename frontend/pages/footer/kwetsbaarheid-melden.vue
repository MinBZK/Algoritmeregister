<template>
  <div>
    <div v-html="p('Footer: Kwetsbaarheid melden.content')" />
    <button class="button" @click="redirectURL">
      {{ t('reportVulnerability') }}
    </button>
  </div>
</template>

<script setup lang="ts">
const { p } = useTextLoader()
const { t } = useI18n()

const redirectURL = () => {
  const url = 'https://www.ncsc.nl/contact/kwetsbaarheid-melden'
  window.open(url, '_blank')
}

useHead({ title: p('Footer: Kwetsbaarheid melden.pageTitle') })
providePageTitle({
  title: 'Footer: Kwetsbaarheid melden.pageTitle',
  labelType: 'preditor-index',
})
</script>
