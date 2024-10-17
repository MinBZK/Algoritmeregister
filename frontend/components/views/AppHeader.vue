<template>
  <header class="header">
    <div class="header__start">
      <div class="container">
        <button
          type="button"
          class="hidden-desktop button button--icon-hamburger"
          data-handler="toggle-nav"
          aria-controls="nav"
          tabindex="3"
          :aria-expanded="menuExpanded ? 'true' : 'false'"
          @click="menuExpanded = !menuExpanded"
        >
          Menu
        </button>
        <div class="logo">
          <NuxtLink :to="localePath(`/`)" tabindex="2">
            <img
              src="../../assets/images/logo.svg"
              alt="Logo Overheid.nl, ga naar de startpagina"
            />
          </NuxtLink>
          <div class="logo__you-are-here">
            <p class="visually-hidden">U bent nu hier:</p>
            <p>{{ t(`logoCaption`) }}</p>
          </div>
        </div>
      </div>
    </div>
    <nav
      id="nav"
      class="header__nav"
      :class="!menuExpanded && 'header__nav--closed'"
    >
      <div class="container header-content">
        <ul class="header__primary-nav list list--unstyled">
          <li
            v-for="item in navigationItems"
            :key="item.label"
            :class="{
              active: item.highlightOnRoutes.includes(
                currentRoute.name as string
              ),
            }"
          >
            <NuxtLink
              :to="localePath({ name: item.routeName })"
              class="focus-border"
              >{{ item.label }}</NuxtLink
            >
          </li>
        </ul>
        <LanguagePicker class="language-picker" />
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
const { t } = useI18n()

const localePath = useLocalePath()

const navigationItems = computed(() => [
  {
    label: t('navigation.home'),
    routeName: 'index',
    highlightOnRoutes: ['index', 'index___nl', 'index___en'],
  },
  {
    label: t('navigation.algorithmRegister'),
    routeName: 'algoritme',
    highlightOnRoutes: [
      'algoritme',
      'algoritme___nl',
      'algoritme___en',
      'algoritme-lars___nl',
      'algoritme-lars___en',
    ],
  },
  {
    label: t('navigation.organisatie'),
    routeName: 'organisatie',
    highlightOnRoutes: [
      'organisatie',
      'organisatie___en',
      'organisatie___nl',
      'organisatie-orgCode___nl',
      'organisatie-orgCode___en',
    ],
  },
  {
    label: t('navigation.dashboard'),
    routeName: 'dashboard',
    highlightOnRoutes: ['dashboard', 'dashboard___nl', 'dashboard___en'],
  },
])
const currentRoute = useRoute()
const menuExpanded = ref(true)

onMounted(() => {
  menuExpanded.value = false
})

// set expanded to false after route change
watch(currentRoute, () => (menuExpanded.value = false))
</script>

<style scoped lang="scss">
.active a {
  background-color: $secondary;
  color: $primary-darker !important;
}
a:focus {
  background-color: $secondary;
  color: $primary-dark;
}

.header-content {
  max-width: 1375px;
  padding: 0 1em;
  display: flex;
  justify-content: space-between;
}
</style>
