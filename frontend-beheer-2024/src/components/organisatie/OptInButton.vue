<template>
  <div class="custom-flex-container">
    <v-switch
      v-model="optedIn"
      :disabled="loading"
      inset
      hide-details
      color="green"
      :error="!optedIn"
    />
    <v-progress-circular
      v-if="loading"
      indeterminate
      :size="44"
      :width="8"
    />
    <span v-if="optedIn && !loading">
      De pagina is <a :href="orgLink" target="_blank">hier</a> te vinden.
    </span>
    <span v-else> De pagina is niet gepubliceerd. </span>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useAuthStore } from '@/store/auth'
import { updateOrganisationOptIn } from '@/services/organisation'

const authStore = useAuthStore()

const loading = ref<boolean>(false)

const optedIn = ref<boolean>(authStore.selectedOrg!.show_page)
watch(optedIn, async () => {
  loading.value = true
  try {
    const response = await updateOrganisationOptIn(
      authStore.selectedOrg!.code,
      optedIn.value
    )
    authStore.selectedOrg = response.data
  } catch (e) {
    console.error(e)
  }
  setTimeout(() => {
    loading.value = false
  }, 3000)
})

const orgLink = computed(() => {
  const baseURL =
    import.meta.env.MODE == 'production'
      ? `https://${window.location.host}`
      : import.meta.env.VITE_PREVIEW_URL

  return baseURL + '/nl/organisatie/' + authStore.selectedOrg?.code
})
</script>
<style scoped lang="scss">
.custom-flex-container {
  display: inline-flex;
  align-items: center;
  column-gap: 1em;
}
</style>
