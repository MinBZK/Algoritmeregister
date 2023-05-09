<template>
  <div>
    <div class="row--footer" role="contentinfo">
      <v-container class="small-container">
        <v-row justify="end">
          <ul class="list list--linked">
            <li
              v-for="page in footer"
              :key="page.key"
              class="list__item"
            >
              <ExternalLink :href="page.path">
                {{ page.label }}
              </ExternalLink>
            </li>
          </ul>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import footer from '@/config/footer'
import ExternalLink from '@/components/ExternalLink.vue'
</script>

<style lang="scss">
.small-container {
  max-width: 1200px;
}
.list__item a {
  font-size: 0.85em !important;
}
</style>
