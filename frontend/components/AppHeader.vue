<template>
  <div class="skiplinks">
    <a href="#content">Ga direct naar inhoud</a>
  </div>
  <header id="header">
    <div id="mainwrapper" class="logo-wrapper ma-0 pa-0">
      <figure>
        <img
          alt="Rijksoverheid Logo"
          src="../assets/images/logo-ro-zonder-caption.svg"
          class="logo-full"
        />
        <img
          alt="Rijksoverheid Logo"
          src="../assets/images/logo-ro-zonder-caption-mobile.svg"
          class="logo-mobile"
        />
        <figcaption class="logo-caption">Rijksoverheid</figcaption>
      </figure>
    </div>
  </header>

  <div id="bar" class="bar-wrapper">
    <div class="bar-wrapper-content">
      <div style="align-items: center; display: flex">
        <NuxtLink to="/">
          {{ title }}
        </NuxtLink>
      </div>
      <nav>
        <ul>
          <!-- <li v-for="p in pages" :key="p">
            <router-link
              :to="{ path: '/' + p.toLowerCase() }"
              aria-current="page"
              >{{ p }}</router-link
            >
          </li> -->
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
const props = defineProps<{
  title?: string
  pages?: string[]
}>()

const router = useRouter()
const routes = router.getRoutes()
const navigationRoutes = routes.filter((r) => {
  const routeName = typeof r.name === 'string' ? r.name : ''
  return (props.pages || []).includes(routeName)
})
</script>

<style scoped lang="scss">
figure {
  margin: 0;
  padding: 0;
}
.logo-wrapper figure {
  display: flex;
  align-items: flex-start;
}

.logo {
  height: 76px;
}
.logo-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  height: 70px;
}

.logo-wrapper img {
  margin-left: 90px;
  height: 70px;
}

.bar-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: $primary;
  height: 76px;
}

.bar-wrapper nav,
.bar-wrapper div {
  padding: 0;
}

.bar-wrapper-content {
  max-width: 1200px;
  display: flex;
  font-size: 26px;
  width: 100%;
  justify-content: space-between;
}

.bar-wrapper-content div a,
.bar-wrapper-content nav {
  color: white;
}

.logo-caption {
  font-family: RO Serif, Calibri, sans-serif;
  font-size: 1rem;
  line-height: 1.1;
  width: 100%;
  max-width: 300px;
  padding: 20px 10px 10px;
  color: #000;
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

@media (min-width: 768px) {
  .logo-caption {
    padding: 50px 12px 25px;
  }

  .logo-wrapper {
    height: 125px;
  }

  .logo-wrapper img {
    height: 125px;
    margin-left: 112px;
  }

  img.logo-full {
    display: block;
  }

  img.logo-mobile {
    display: none;
  }
}

.logo-mobile {
  display: block;
}

.logo-full {
  display: none;
}
</style>
