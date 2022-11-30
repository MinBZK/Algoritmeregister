<template>
  <v-spacer></v-spacer>
  <v-footer class="site-footer">
    <div class="wrapper">
      <div
        class="column"
        v-for="column in footerTranslated"
        :key="column.title"
      >
        <!-- <h2>{{ column.title }}</h2> -->

        <ul>
          <li v-for="page in column.pages" :key="page.label">
            <NuxtLink :to="`/footer${page.path}`">
              {{ page.label }}
            </NuxtLink>
          </li>
        </ul>
      </div>
    </div>
  </v-footer>
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

<style scoped lang="scss">
.site-footer .column {
  position: relative;
}

.site-footer .column .hst-fab {
  position: absolute !important;
}

.site-footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
  background-color: $tertiary;
  border-top: 14px solid $secondary;
  padding-top: 0px;
  padding-bottom: 0px;
}

.site-footer > .wrapper {
  display: flex;
  flex-basis: 100%;
  flex-wrap: wrap;
  max-width: 1200px;
  align-items: flex-start;
  justify-content: flex-start;
  -webkit-margin-end: -16px;
  margin-inline-end: -16px;
  -webkit-margin-start: -16px;
  margin-inline-start: -16px;
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.site-footer .column {
  flex-grow: 0;
  flex-shrink: initial;
  flex-basis: 50%;
  max-width: 50%;
  -webkit-padding-end: 16px;
  padding-inline-end: 16px;
  -webkit-padding-start: 16px;
  padding-inline-start: 16px;
}

@media (min-width: 768px) {
  .site-footer .column {
    flex-grow: 0;
    flex-shrink: initial;
    flex-basis: 25%;
    max-width: 25%;
    -webkit-padding-end: 16px;
    padding-inline-end: 16px;
    -webkit-padding-start: 16px;
    padding-inline-start: 16px;
  }
}

@media (min-width: 1200px) {
  .site-footer .column {
    flex-grow: 0;
    flex-shrink: initial;
    flex-basis: 16.6666666667%;
    max-width: 16.6666666667%;
    -webkit-padding-end: 16px;
    padding-inline-end: 16px;
    -webkit-padding-start: 16px;
    padding-inline-start: 16px;
  }
}

.site-footer .column h2,
.site-footer .column li,
.site-footer .column a,
.site-footer .column a:hover {
  text-decoration: underline;
}

a {
  color: $primary-dark;
}

a:hover {
  color: $primary;
}

.site-footer .column h2 {
  font-size: 1.6018066406rem;
  line-height: 1.2485901539;
  font-weight: normal;
  margin-bottom: 1rem;
}

.site-footer .column ul {
  margin-bottom: 0;
  list-style: none !important;
  -webkit-margin-start: 0 !important;
  margin-inline-start: 0 !important;
}

.site-footer .column ul li,
.site-footer .column ul li > h2,
.site-footer .column ul a > h3,
.site-footer .column ul a > h4 {
  font-size: 1.125rem;
  line-height: 19.2px;
  font-weight: normal;
}

@media (min-width: 768px) {
  .site-footer .column ul li,
  .site-footer .column ul li > h2,
  .site-footer .column ul a > h3,
  .site-footer .column ul a > h4 {
    line-height: 21.6px;
  }
}

@media (min-width: 992px) {
  .site-footer .column ul li,
  .site-footer .column ul li > h2,
  .site-footer .column ul a > h3,
  .site-footer .column ul a > h4 {
    line-height: 24px;
  }
}

.site-footer .column ul li,
.site-footer .column ul a {
  -webkit-margin-after: 0.75rem;
  margin-block-end: 0.75rem;
}

.site-footer .column ul li > a {
  -webkit-margin-after: 0;
  margin-block-end: 0;
}

.site-footer .column ul a {
  -webkit-padding-start: calc((8.4px + 0.75rem) * 0.8);
  padding-inline-start: calc((8.4px + 0.75rem) * 0.8);
  position: relative;
  display: block;
  text-decoration: none;
  font-size: 1em;
  line-height: inherit;
  font-weight: normal;
  -webkit-padding-before: 6.4px;
  padding-block-start: 6.4px;
  -webkit-padding-after: 6.4px;
  padding-block-end: 6.4px;
}

@media (min-width: 768px) {
  .site-footer .column ul a {
    -webkit-padding-start: calc((8.4px + 0.75rem) * 0.9);
    padding-inline-start: calc((8.4px + 0.75rem) * 0.9);
  }
}

@media (min-width: 992px) {
  .site-footer .column ul a {
    -webkit-padding-start: calc((8.4px + 0.75rem) * 1);
    padding-inline-start: calc((8.4px + 0.75rem) * 1);
  }
}

@media (min-width: 768px) {
  .site-footer .column ul a {
    -webkit-padding-before: 7.2px;
    padding-block-start: 7.2px;
  }
}

@media (min-width: 992px) {
  .site-footer .column ul a {
    -webkit-padding-before: 8px;
    padding-block-start: 8px;
  }
}

@media (min-width: 768px) {
  .site-footer .column ul a {
    -webkit-padding-after: 7.2px;
    padding-block-end: 7.2px;
  }
}

@media (min-width: 992px) {
  .site-footer .column ul a {
    -webkit-padding-after: 8px;
    padding-block-end: 8px;
  }
}

.site-footer .column ul a:before {
  display: inline-flex;
  align-items: center;
  content: '';
  font-family: 'RO Icons';
  font-size: 0.7rem;
  font-weight: normal;
  line-height: inherit;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  width: 6.72px;
  -webkit-padding-before: 6.4px;
  padding-block-start: 6.4px;
  height: 25.6px;
  text-indent: -0.1em;
  position: absolute;
  inset-block-start: -1px;
  inset-inline-start: 0;
}

@media (min-width: 768px) {
  .site-footer .column ul a:before {
    width: 7.56px;
  }
}

@media (min-width: 992px) {
  .site-footer .column ul a:before {
    width: 8.4px;
  }
}

@media (min-width: 768px) {
  .site-footer .column ul a:before {
    -webkit-padding-before: 7.2px;
    padding-block-start: 7.2px;
  }
}

@media (min-width: 992px) {
  .site-footer .column ul a:before {
    -webkit-padding-before: 8px;
    padding-block-start: 8px;
  }
}

@media (min-width: 768px) {
  .site-footer .column ul a:before {
    height: 28.8px;
  }
}

@media (min-width: 992px) {
  .site-footer .column ul a:before {
    height: 32px;
  }
}

.site-footer .column ul a:hover {
  text-decoration: underline;
}

.site-footer .column ul a:hover:before {
  text-decoration: none;
}

.site-footer .column ul a.external:before {
  content: '';
  font-family: 'RO Icons';
  font-size: 0.595rem;
  font-weight: normal;
  line-height: inherit;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

[dir='rtl'] .site-footer .column ul a:before {
  -webkit-transform: rotate(-180deg);
  transform: rotate(-180deg);
}

[dir='rtl'] .site-footer .column ul a.external:before {
  -webkit-transform: rotate(-90deg);
  transform: rotate(-90deg);
}

.site-footer
  .column
  ul
  p:not(.article-meta):not(.meta):not(.superheading):not(.copyright) {
  font-size: 0.8888888889rem;
  line-height: 1.40625;
  font-weight: normal;
  color: #000;
  -webkit-margin-after: 0;
  margin-block-end: 0;
}

.site-footer .column ul p.meta {
  font-size: 0.8888888889rem;
  line-height: 1.6875;
  font-weight: normal;
  color: #535353;
  margin: 0;
  margin-top: 0.5rem;
}

.site-footer .column ul li {
  margin-bottom: 0;
}

.site-footer .column ul a:visited:before {
  color: $primary-dark;
}

@media (min-width: 768px) {
  .site-footer .column:first-child {
    margin-left: 50%;
  }
}

@media (min-width: 1200px) {
  .site-footer .column:first-child {
    margin-left: 66.666667%;
  }
}

.site-footer .payoff {
  flex-grow: 0;
  flex-shrink: initial;
  flex-basis: 100%;
  max-width: 100%;
  -webkit-padding-end: 16px;
  padding-inline-end: 16px;
  -webkit-padding-start: 16px;
  padding-inline-start: 16px;
  margin-bottom: 2rem;
}

@media (min-width: 768px) {
  .site-footer .payoff {
    flex-grow: 0;
    flex-shrink: initial;
    flex-basis: 50%;
    max-width: 50%;
    -webkit-padding-end: 16px;
    padding-inline-end: 16px;
    -webkit-padding-start: 16px;
    padding-inline-start: 16px;
  }
}

@media (min-width: 1200px) {
  .site-footer .payoff {
    flex-grow: 0;
    flex-shrink: initial;
    flex-basis: 66.6666666667%;
    max-width: 66.6666666667%;
    -webkit-padding-end: 16px;
    padding-inline-end: 16px;
    -webkit-padding-start: 16px;
    padding-inline-start: 16px;
  }
}

.site-footer .payoff span {
  color: #fff;
  font-family: 'RO Serif';
  font-size: 2.0272865295rem;
  line-height: 0.9865403685;
  font-weight: normal;
  font-style: italic;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

@media print {
  .site-footer {
    display: none;
  }
}
</style>
