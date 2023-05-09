<template>
  <div id="page-wrapper">
    <app-header />
    <v-container id="main" class="container mb-10">
      <router-view />
    </v-container>
    <app-footer id="footer" />
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
</script>

<style lang="scss">
@import '@/assets/styles/main.scss';

.container {
  max-width: 1500px;
  padding: 0 2rem;
  min-height: 65vh;
}
#page-wrapper {
  position: relative;
}
#main {
  padding-bottom: 2.5rem;
}
#footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 2.5rem;
  padding-top: 2.5rem;
}
</style>
