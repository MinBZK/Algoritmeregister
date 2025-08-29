// Utilities
import { defineStore } from 'pinia'
import Keycloak from 'keycloak-js'
import { Organisation } from '@/types/organisation'
import { useLocalStorage } from '@vueuse/core'
import { getMe } from '@/services/user'
import { User } from '@/types/user'
import { useSnackbarStore } from './snackbar'
import { notifications } from '@/config/notifications'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    snackbar: useSnackbarStore(),
    keycloak: {} as Keycloak,
    me: {} as User,
    APIurl: 'http://localhost:8000/api',
    organisations: [] as Organisation[],
    selectedOrg: null as Organisation | null,
    loading: false as boolean,
  }),
  getters: {
    roles(): string[] {
      return (this.keycloak.tokenParsed?.roles as string[] | undefined) || []
    },
    canRemove(): boolean {
      return this.roles.includes('admin')
    },
    canAccesDashboard(): boolean {
      return this.roles.includes('ictu')
    },
    canAccesBeheer(): boolean {
      return this.roles.includes('admin')
    },
    canAccesOrgPage(): boolean {
      return this.roles.includes('orgdetail')
    },
    canAccessArchive(): boolean {
      return this.roles.includes('role_1')
    },
    canAddRecord(): boolean {
      return this.roles.includes('role_1')
    },
  },
  actions: {
    async fetchMe() {
      this.loading = true
      await getMe()
        .then((response) => {
          this.me = response.data
          this.organisations = this.me.organisations
        })
        .catch((error) => {
          if ((error.message = 'USER_NOT_ACTIVATED')) {
            this.snackbar.add(notifications.fetchMeErrorDisabled!)
          }
        })
      this.loading = false
    },
    selectOrganisation(orgId: string) {
      const organisation = this.organisations.find((org) => org.org_id === orgId)
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
