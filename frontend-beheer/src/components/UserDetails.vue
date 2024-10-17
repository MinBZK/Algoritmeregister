<template>
  <div class="user-details">
    <div class="username">
      {{ authStore.keycloak.tokenParsed?.family_name }},
      {{ authStore.keycloak.tokenParsed?.given_name?.[0] }}. ({{
        authStore.keycloak.tokenParsed?.email
      }})
    </div>
    <button class="logout-button" @click="logout">
      Uitloggen
    </button>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

const logout = () => {
  authStore.keycloak.logout()
}
</script>

<style scoped lang="scss">
.logout-button {
  font-size: 0.85em;
}

.logout-button:hover {
  text-decoration: underline;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
</style>
