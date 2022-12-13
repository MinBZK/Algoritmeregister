<template>
  <div class="footer row--footer" role="contentinfo">
    <div class="container columns">
      <div class="bottom-margin">
        {{ t('footer.text') }}&nbsp;<NuxtLink :to="'/footer/over'">{{
          t('footer.textAskApply')
        }}</NuxtLink>
      </div>
      <div></div>
      <div v-for="footerKey in footerKeys" :key="footerKey">
        <div class="">
          <ul class="list list--linked">
            <li
              v-for="page in footer[footerKey]"
              :key="page.label"
              class="list__item"
            >
              <NuxtLink
                v-if="footerKey != 'external'"
                :to="`/footer${page.path}`"
              >
                {{ t(`footer.paths.${page.key}`) }}
              </NuxtLink>
              <a
                v-if="footerKey == 'external'"
                :href="page.path"
                target="_blank"
                class="is-external"
                >{{ t(`footer.paths.${page.key}`) }}</a
              >
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import footer from '@/config/footer'
const { t } = useI18n()

const footerKeys = Object.keys(footer)
</script>

<style scoped lang="scss">
.bottom-margin {
  padding-bottom: 1.75em;
}
</style>
