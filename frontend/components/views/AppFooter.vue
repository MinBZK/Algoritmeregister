<template>
  <div class="footer row--footer" role="contentinfo">
    <div class="container columns">
      <div class="bottom-margin">
        {{ p('footer.text') }}
        <NuxtLink :to="localePath('/footer/meedoen')">
          {{ p('footer.textForLink') }}
        </NuxtLink>
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
  </div>
</template>

<script setup lang="ts">
import footer from '@/config/footer'
const { t } = useI18n()

const { p } = useTextLoader()

const localePath = useLocalePath()

const footerKeys = Object.keys(footer)
</script>

<style scoped lang="scss">
.row--footer {
  padding: 0.75em;
  padding-bottom: 0;
}

.footer {
  margin-top: 3em;
  height: auto;
}
</style>
