<script setup>
import Page from '@/components/Page.vue'
import algoritmeService from '@/services/algoritme'

const route = useRoute()
const id = route.params.id
const algoritme = await algoritmeService.getOne(id)

definePageMeta({
  title: 'Algoritme details',
})
</script>

<template>
  <Page>
    {{ algoritme }}
  </Page>
</template>
