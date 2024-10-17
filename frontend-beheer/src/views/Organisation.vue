<template>
  <div class="page">
    <h1>Organisatiepagina</h1>
    <p class="mb-3">
      In dit formulier kun je algemene informatie kwijt als je dat wenst.
      Beschrijf in 1.000 woorden hoe jouw organisatie omgaat met algoritmes en
      de publicatie daarover in het Algoritmeregister:
    </p>
    <OrgDetailForm />
    <p class="mt-6 mb-2">
      Geef aan of de pagina gepubliceerd mag worden:
    </p>
    <OptInButton />
  </div>
</template>

<script lang="ts" setup>
import OrgDetailForm from '@/components/organisatie/OrgDetailForm.vue'
import OptInButton from '@/components/organisatie/OptInButton.vue'
import { useAuthStore } from '@/store/auth'
import { watch } from 'vue'
import router from '@/router'
import { useFormDataStore } from '@/store/form-data'
import { onBeforeRouteLeave } from 'vue-router'

const authStore = useAuthStore()
const dataStore = useFormDataStore()

// Abort when no org selected
if (!authStore.selectedOrg) router.push('/')

// Checks routing within website
onBeforeRouteLeave(() => {
  if (dataStore.unsavedChanges) {
    const answer = window.confirm(
      'Wijzigingen die je hebt aangebracht, worden mogelijk niet opgeslagen.'
    )
    if (!answer) return false
  }
})

// Checks other routing (exit browser, back/forward)
const handleBeforeUnload = (event: any) => {
  event.preventDefault()
  event.returnValue = ''
}

watch(
  () => dataStore.unsavedChanges,
  () => {
    if (dataStore.unsavedChanges) {
      window.addEventListener('beforeunload', handleBeforeUnload, {
        capture: true,
      })
    } else {
      window.removeEventListener('beforeunload', handleBeforeUnload, {
        capture: true,
      })
    }
  }
)
</script>

<style scoped lang="scss">
.page {
  max-width: 700px;
}
</style>
