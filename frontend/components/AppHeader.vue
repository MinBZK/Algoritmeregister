<template>
  <div class="skiplinks">
    <a href="#content">Ga direct naar inhoud</a>
  </div>
  <header id="header">
    <div>
      <figure>
        <img alt="Overheidlogo" src="../assets/images/logo.svg" class="logo" />
      </figure>
      <div class="logo-caption">Algoritmes in de overheid</div>
    </div>
  </header>

  <div id="bar" class="bar-wrapper">
    <div class="bar-wrapper-content">
      <div class="center-flex">
        <NuxtLink to="/">
          {{ title }}
        </NuxtLink>
      </div>
      <nav>
        <ul>
          <li v-for="nR in navigationRoutes" :key="nR.name">
            <NuxtLink :to="nR.path">
              {{ nR.meta.title }}
            </NuxtLink>
          </li>
        </ul>
      </nav>
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

const router = useRouter()
const routes = router.getRoutes()
const navigationRoutes = computed(() => {
  return routes
    .filter((r) => {
      const routeName = typeof r.name === 'string' ? r.name : ''
      return (props.pages || []).includes(routeName)
    })
    .map((r) => {
      r.meta.title = t(`paths.${r.path}`)
      console.log(r.path)
      return r
    })
})
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
  display: flex;
  align-items: center;
  justify-content: center;
}

#header div {
  width: $page-width;
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

.bar-wrapper nav,
.bar-wrapper div {
  padding: 0;
}

.bar-wrapper-content {
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
</style>
