<template>
  <header class="header">
    <div class="header__start">
      <div class="container">
        <button
          type="button"
          class="hidden-desktop button button--icon-hamburger"
          data-handler="toggle-nav"
          aria-controls="nav"
          :aria-expanded="menuExpanded ? 'true' : 'false'"
          @click="menuExpanded = !menuExpanded"
        >
          Menu
        </button>
        <div class="logo">
          <a href="../"
            ><img
              src="../../assets/images/logo.svg"
              alt="Logo Overheid.nl, ga naar de startpagina"
          /></a>
          <div class="logo__you-are-here">
            <p class="visually-hidden">U bent nu hier:</p>
            <p>{{ t(`logoCaption`) }}</p>
          </div>
          <div class="header__meta">
            <LanguagePicker class="align-right"> </LanguagePicker>
          </div>
        </div>
      </div>
    </div>
    <nav
      class="header__nav"
      :class="!menuExpanded && 'header__nav--closed'"
      id="nav"
    >
      <div class="container">
        <ul class="header__primary-nav list list--unstyled">
          <li
            v-for="item in navigationItems"
            :key="item.label"
            :class="{ active: currentRoute.name == item.routeName }"
          >
            <NuxtLink :to="{ name: item.routeName }">{{ item.label }}</NuxtLink>
          </li>
        </ul>
        <!-- <a
          href="#other-sites"
          class="hidden-desktop"
          data-handler="toggle-other-sites"
          data-decorator="init-toggle-other-sites"
          aria-controls="other-sites"
          aria-expanded="false"
          data-decorator-initialized="true"
          ><span class="visually-hidden">Andere sites binnen&nbsp;</span>
          &nbsp;Overheid.nl</a
        > -->
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import LanguagePicker from '@/components/LanguagePicker.vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const navigationItems = computed(() => [
  {
    label: t('navigation.home'),
    routeName: 'index',
  },
  {
    label: t('navigation.algorithmRegister'),
    routeName: 'algoritme',
  },
])
const currentRoute = useRoute()
const menuExpanded = ref(false)

// set expanded to false after route change
watch(currentRoute, () => (menuExpanded.value = false))
</script>

<style scoped lang="scss">
.active a {
  background-color: $secondary;
  color: $primary-darker !important;
}
</style>
