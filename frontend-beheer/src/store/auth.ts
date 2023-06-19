// Utilities
import { defineStore } from 'pinia'
import Keycloak from 'keycloak-js'
import { Organization } from '@/types'
import { OrganizationNames, organizationNames } from '@/config/organization'
import { useLocalStorage } from '@vueuse/core'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    keycloak: {} as Keycloak,
    APIurl: 'http://localhost:8000/api',
    organizations: [] as Organization[],
    selectedOrg: null as Organization | null,
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
        let defaultOrgName = orgId.replaceAll('-', ' ')
        // Regex detects first letter of each word.
        defaultOrgName = defaultOrgName.replace(/\b\w/g, (l: string) =>
          l.toUpperCase()
        )
        const orgName = organizationNames[orgId as keyof OrganizationNames]
        return { id: orgId, name: orgName || defaultOrgName }
      })
    },
    selectOrganization(orgId: string) {
      const organization = this.organizations.find((org) => org.id === orgId)
      if (!organization) {
        throw new Error(
          'Selected organization is not found in organizations array.'
        )
      }
      useLocalStorage('webform-selected-org', {}).value = organization!
      this.selectedOrg = organization!
    },
  },
})
