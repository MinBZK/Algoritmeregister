<template>
  <!-- <v-spacer></v-spacer>
  <v-footer class="site-footer">
    <div class="wrapper">
      <div
        class="column"
        v-for="column in footerTranslated"
        :key="column.title"
      >
         <h2>{{ column.title }}</h2> 

        <ul>
          <li v-for="page in column.pages" :key="page.label">
            <NuxtLink :to="`/footer${page.path}`">
              {{ page.label }}
            </NuxtLink>
          </li>
        </ul>
      </div>
    </div>
  </v-footer> -->
  <div class="footer row--footer" role="contentinfo">
    <div class="container columns">
      <div v-for="column in footerTranslated" :key="column.title">
        <div class="">
          <ul class="list list--linked">
            <li
              class="list__item"
              v-for="page in column.pages"
              :key="page.label"
            >
              <NuxtLink :to="`/footer${page.path}`">
                {{ page.label }}
              </NuxtLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import footer from '@/config/footer'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const footerTranslated = computed(() => {
  return footer.map((column) => {
    column.title = t(`footerColumns.${column.key}`)
    column.pages.map((page) => {
      page.label = t(`paths.${page.path}`)
      return page
    })
    return column
  })
})
</script>
