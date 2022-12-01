<template>
  <div class="skiplinks">
    <a href="#content">Ga direct naar inhoud</a>
  </div>
  <header id="header">
    <div>
      <figure>
        <img alt="Overheidlogo" src="../assets/images/logo.svg" class="logo" />
      </figure>
      <div class="logo-caption">{{ t(`logoCaption`) }}</div>
    </div>
  </header>

  <div id="bar" class="bar-wrapper">
    <div class="bar-wrapper-content">
      <div class="center-flex">
        <ul>
          <li
            v-for="item in navigationItems"
            :key="item.label"
            :class="{ active: currentRoute.name == item.routeName }"
          >
            <NuxtLink :to="{ name: item.routeName }">{{ item.label }}</NuxtLink>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const props = defineProps<{
  title?: string
  pages?: string[]
}>()

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

// const router = useRouter()
// const routes = router.getRoutes()
const currentRoute = useRoute()
</script>

<style scoped lang="scss">
figure {
  margin: 0;
  padding: 0;
}
// .logo-wrapper {
//   width: 100%;
//   display: flex;
//   justify-content: center;
//   height: 70px;
// }

.logo-wrapper img {
  height: 70px;
}

#header {
  margin: 0 auto;
  max-width: $page-width;
  padding: 0 $page-side-padding;
}

#header div {
  height: 84px;
}

#header div img {
  width: 180px;
  padding-top: 15px;
}

#header div .logo-caption {
  margin-top: 0px;
  color: $primary-dark;
  margin-top: 5px;
  font-size: 0.8em;
}

.bar-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: $primary;
  height: 59px;
  border-bottom: 9px solid $secondary;
}

.bar-wrapper-content {
  padding: 0 $page-side-padding;
  max-width: $page-width;
  display: flex;
  font-size: 20px;
  width: 100%;
  justify-content: space-between;
}

.bar-wrapper-content div a,
.bar-wrapper-content nav {
  color: white;
}
.center-flex {
  align-items: center;
  display: flex;
}

nav {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  font-size: 80%;
}

nav ul {
  list-style: none;
  display: table;
  vertical-align: middle;
}

nav ul > li {
  display: inline-block;
  vertical-align: middle;
  padding: 0 0 0 1em;
}

.barwapper ul > li a {
  color: white;
  text-decoration: none;
}

.bar-wrapper-content nav a {
  color: white;
  text-decoration: none;
}

.bar-wrapper-content nav a:hover {
  text-decoration: underline;
}

nav ul > li a:hover {
  text-decoration: underline;
}

ul > li {
  display: inline-block;
  height: 50px;
  vertical-align: middle;
  display: table-cell;
  color: white;
  padding: 0 15px;
}

.active {
  background-color: white;
}

ul > li a {
  text-decoration: none;
}

.active a {
  color: $primary-dark !important;
}

ul > li:hover:not(.active) {
  background-color: $secondary;
}

ul > li:hover a {
  color: $primary-dark !important;
}
</style>
