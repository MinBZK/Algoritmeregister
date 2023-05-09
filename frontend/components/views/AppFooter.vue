<template>
  <div class="footer row--footer" role="contentinfo">
    <div class="container columns">
      <div class="bottom-margin">
        {{ t('footer.text') }}&nbsp;<NuxtLink
          :to="localePath('/footer/over')"
          >{{ t('footer.textAskApply') }}</NuxtLink
        >.
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
                :to="localePath(`/footer${page.path}`)"
              >
                {{ t(`footer.paths.${page.key}`) }}
              </NuxtLink>
              <ExternalLink v-if="footerKey == 'external'" :href="page.path">{{
                t(`footer.paths.${page.key}`)
              }}</ExternalLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="after-footer">
      <slot name="after-footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import footer from '@/config/footer'
const { t } = useI18n()
const localePath = useLocalePath()

const footerKeys = Object.keys(footer)
</script>

<style scoped lang="scss">
.bottom-margin {
  padding-bottom: 1.75em;
}

.after-footer {
  padding: 1em 0;
}
</style>
