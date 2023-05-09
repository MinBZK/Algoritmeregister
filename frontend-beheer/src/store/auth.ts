// Utilities
import { defineStore } from 'pinia'
import Keycloak from 'keycloak-js'
import { Organization } from '@/types'
import { useLocalStorage } from '@vueuse/core'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    keycloak: {} as Keycloak,
    APIurl: 'http://localhost:8000/api',
    organizations: [] as Organization[],
    selectedOrg: useLocalStorage<Organization>(
      'webform-selected-org',
      {} as Organization
    ),
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
  },
  actions: {
    fetchOrganizations() {
      const keycloakOrgStrings = this.keycloak.tokenParsed?.group
      if (!keycloakOrgStrings || keycloakOrgStrings.length === 0) {
        return
      }
      this.organizations = keycloakOrgStrings.map((orgString: string) => {
        const orgId = orgString.split('/')?.pop()
        if (!orgId) {
          throw new Error('Could not parse Keycloak organization string.')
        }
        let orgName = orgId.replaceAll('-', ' ')
        orgName = orgName.replace(/\b\w/g, (l: string) => l.toUpperCase())
        return { id: orgId, name: orgName }
      })
      try {
        this.selectOrganization(this.selectedOrg.id)
      } catch {
        this.selectedOrg = this.organizations[0]!
      }
    },
    selectOrganization(orgId: string) {
      const organization = this.organizations.find((org) => org.id === orgId)
      if (!organization) {
        throw new Error(
          'Selected organization is not found in organizations array.'
        )
      }
      this.selectedOrg = organization!
    },
  },
})
