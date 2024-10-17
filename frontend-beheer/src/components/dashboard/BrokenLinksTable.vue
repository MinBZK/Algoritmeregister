<template>
  <h1 class="text-h5 px-0">Gebroken Links</h1>
  <p class="text-body-1 py-3">
    Hier wordt per dag getoond hoeveel verwijzingen in gepubliceerde
    algoritmebeschrijvingen voorkomen welke niet (meer) werken of waarvan de
    reactietijd te langzaam is (meer dan 5 seconden). Deze controle is in
    ontwikkeling. Het is mogelijk dat wel-werkende verwijzingen onterecht
    gerapporteerd worden.
  </p>
  <div>
    <div class="rows">
      <div class="row">
        <table aria-label="Gebrokenlinks in gepubliceerde algoritmebeschrijvingen">
          <thead>
            <tr>
              <th class="u-columnwidth-10p">Algoritme</th>
              <th class="u-columnwidth-15p">Organisatie</th>
              <th class="u-columnwidth-60p">Gebroken link</th>
              <th class="u-columnwidth-5p">Code</th>
              <th class="u-columnwidth-10p">Datum</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in brokenLinksResults" :key="record.id">
              <td>
                <a
                  :href="`https://algoritmes.overheid.nl/nl/algoritme/${record.lars}`"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ record.lars }}
                </a>
              </td>
              <td>{{ record.organisation }}</td>
              <td>
                <ul class="remove-bullet-point-list">
                  <li
                    v-for="(brokenLink, index) in record.broken_links"
                    :key="index"
                  >
                    <a
                      :href="formatLink(brokenLink[0])"
                      target="_blank"
                      rel="noopener noreferrer"
                      >{{ brokenLink[0] }}</a
                    >
                  </li>
                </ul>
              </td>
              <td>
                <ul class="remove-bullet-point-list">
                  <li
                    v-for="(brokenLink, index) in record.broken_links"
                    :key="index"
                  >
                    {{ brokenLink[1] }}
                  </li>
                </ul>
              </td>
              <td>{{ new Date(record.create_dt).toLocaleDateString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getBrokenLinks } from '@/services/brokenlinks'
import type { BrokenLink } from '@/types/brokenlink'
import { ref } from 'vue'

const brokenLinksResults = ref<BrokenLink[]>([])
const retrieveBrokenLinks = async () => {
  const result = await getBrokenLinks()
  brokenLinksResults.value = result.data
}
retrieveBrokenLinks()

const formatLink = (link: string) => {
  if (!link.startsWith('http://') && !link.startsWith('https://')) {
    return `http://${link}`
  }
  return link
}
</script>
<style scoped lang="scss">
.remove-bullet-point-list {
  list-style-type: none;
}

.u-columnwidth-5p {
  width: 5%;
}
.u-columnwidth-10p {
  width: 10%;
}
.u-columnwidth-15p {
  width: 15%;
}
.u-columnwidth-20p {
  width: 20%;
}
.u-columnwidth-25p {
  width: 25%;
}
.u-columnwidth-30p {
  width: 30%;
}
.u-columnwidth-40p {
  width: 40%;
}
.u-columnwidth-50p {
  width: 50%;
}
td,
th {
  padding: 10px;
}
</style>
