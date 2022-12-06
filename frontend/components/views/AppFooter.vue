<template>
  <div class="footer row--footer" role="contentinfo">
    <div class="container columns">
      <div>
        {{ t('footer.text') }}&nbsp;<NuxtLink :to="'/footer/over'">{{
          t('footer.textAskApply')
        }}</NuxtLink>
      </div>
      <div></div>
      <div v-for="footerKey in footerKeys" :key="footerKey">
        <div class="">
          <ul class="list list--linked">
            <li
              class="list__item"
              v-for="page in footer[footerKey]"
              :key="page.label"
            >
              <NuxtLink
                :to="`/footer${page.path}`"
                v-if="footerKey != 'external'"
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
import footer from '@/config/footer'
// import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const footerKeys = Object.keys(footer)

// const footerTranslated = computed(() => {
//   return footerKeys.map((footerKey) => {
//     footer[footerKey as keyof typeof footer].map((page) => {
//       page.label = t(`paths.${page.path}`)
//       return page
//     })
//   })
// })
</script>
