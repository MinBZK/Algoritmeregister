// Utilities
import { defineStore } from 'pinia'
import Keycloak from 'keycloak-js'
import { Organisation } from '@/types/organisation'
import { useLocalStorage } from '@vueuse/core'
import { getOrganisationList } from '@/services/organisation'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    keycloak: {} as Keycloak,
    APIurl: 'http://localhost:8000/api',
    organisations: [] as Organisation[],
    selectedOrg: null as Organisation | null,
    loading: false as boolean,
  }),
  getters: {
    canPublish(): boolean {
      const role = this.keycloak.tokenParsed?.role
      return role === 'publisher' || role === 'admin'
    },
    canRemove(): boolean {
      const role = this.keycloak.tokenParsed?.role
      return role === 'admin'
    },
    canAddOrg(): boolean {
      const role = this.keycloak.tokenParsed?.role
      return role === 'admin'
    },
    canEditOrg(): boolean {
      const role = this.keycloak.tokenParsed?.role
      return role === 'publisher' || role === 'admin'
    },
  },
  actions: {
    async fetchOrganisations() {
      this.loading = true
      try {
        this.organisations = (await getOrganisationList()).data
      } catch (error) {
        console.error('Unable to fetch organisation list', error)
      } finally {
        this.loading = false
      }
    },
    selectOrganisation(orgId: string) {
      const organisation = this.organisations.find((org) => org.code === orgId)
      if (!organisation) {
        throw new Error(
          'Selected organisation is not found in organisations array.'
        )
      }
      useLocalStorage('webform-selected-org', {}).value = organisation
      this.selectedOrg = organisation
    },
  },
})
