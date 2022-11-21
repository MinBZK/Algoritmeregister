<template>
  <Page>
    Algoritme
    {{ data }}
  </Page>
</template>

<script setup>
import Page from "@/components/Page.vue";
import algoritme from "@/services/algoritme";

const route = useRoute();
const id = route.params.id;
const data = await algoritme.getOne(id);

definePageMeta({
  title: "Algoritme details",
});
</script>
