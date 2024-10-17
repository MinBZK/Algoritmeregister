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
    roles(): string[] {
      return (this.keycloak.tokenParsed?.roles as string[] | undefined) || []
    },
    canPublish(): boolean {
      // Temp: Only published role in ICTU_LAST is relevant here.
      return this.roles.includes('ictu')
    },
    canRemove(): boolean {
      return this.roles.includes('admin')
    },
    canAccesOrgPage(): boolean {
      return this.roles.includes('orgdetail')
    },
    canAccesDashboard(): boolean {
      return this.roles.includes('ictu')
    },
  },
  actions: {
    async fetchOrganisations() {
      this.loading = true
      try {
        this.organisations = (await getOrganisationList()).data.organisations
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
