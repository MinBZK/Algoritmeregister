import { normalizeURL } from 'ufo'
import type { Algoritme } from '@/types/algoritme'
import algoritmeService from '@/services/algoritme'
import organisationService from '@/services/organisation'
import type { LanguageCode } from '@/types/textLoader'
import type {
  OrganisationCodeResponse,
  OrganisationPage,
  OrganisationRelationResponse,
} from '@/types/organisation'

const stringFormat = (stringValue: string) => {
  let value = stringValue.toLowerCase()
  value = value.replaceAll(/[^a-zA-Z0-9 ]/g, '')
  // Some names have two spaces, the following line ensures this does not become '--'.
  value = value.replaceAll('  ', '-')
  value = value.replaceAll(' ', '-')
  return value.replace(/-+$/, '')
}

export default defineNuxtRouteMiddleware(async (to, from) => {
  const locale = to.path.split('/')[1] as LanguageCode
  const params = (to.params.params as string[]) || []
  if (to.path.includes('/organisatie/')) {
    const orgCode = params.length > 1 ? params.at(-2)! : params[0]
    const orgIdPattern =
      /^(gm\d{4}|mnre\d{4}|oorg\d{5}|pv\d{2}|so\d{4}|ws\d{4}|zb\d{6}|\d{12}|\d{6}|\d{8})$/g
    if (orgIdPattern.test(orgCode)) {
      const orgId = orgCode
      const organisation = useState<OrganisationPage | null>(
        'organisatie',
        () => null
      )
      if (
        !organisation.value ||
        organisation.value.algoritme_versions[0]?.org_id !== orgId
      ) {
        const { data } = await organisationService.getOne(
          orgId,
          mapLocaleName(locale)
        )
        organisation.value = data.value as OrganisationPage
      }
      const orgHierarchy = useState<OrganisationRelationResponse | null>(
        'orgHierarchy',
        () => null
      )
      const { data } = await organisationService.getOrgRelationById(orgId)
      orgHierarchy.value = data.value as OrganisationRelationResponse
      if (orgHierarchy.value?.hierarchy_path) {
        const orgName = stringFormat(organisation.value.name)
        const expectedPath = `/${locale}/organisatie/${orgHierarchy.value.hierarchy_path}/${orgId}/${orgName}`
        if (normalizeURL(to.fullPath) === normalizeURL(expectedPath)) return
        return navigateTo({ path: expectedPath })
      }
      const slug = organisation.value.algoritme_versions[0]?.code
        ? organisation.value.algoritme_versions[0].code
        : stringFormat(organisation.value.name)
      const fallbackPath = `/${locale}/organisatie/${orgId}/${slug}`
      if (normalizeURL(to.fullPath) === normalizeURL(fallbackPath)) return
      return navigateTo({ path: fallbackPath })
    }

    const organisationIdentifier = useState<OrganisationCodeResponse | null>(
      'organisatieIdentifier',
      () => null
    )
    organisationIdentifier.value =
      await organisationService.getOrgIdByCode(orgCode)
    if (organisationIdentifier.value?.code === orgCode) {
      const newPath = `/${locale}/organisatie/${organisationIdentifier.value.org_id}/${organisationIdentifier.value.code}`
      if (normalizeURL(to.fullPath) === normalizeURL(newPath)) return
      return navigateTo(newPath)
    }
  }
  if (to.path.includes('/algoritme/')) {
    const algoritme = useState<Algoritme | null>('algoritme', () => null)
    const lars = params.length > 1 ? params.at(-2)! : params[0]
    if (params.length === 1) {
      if (lars.includes('C')) return
      const { data: algoritmeData } = await algoritmeService.getOne(
        lars,
        mapLocaleName(locale)
      )
      algoritme.value = algoritmeData.value as Algoritme
      const algoName = stringFormat(algoritme.value.name)
      const org_id = algoritme.value.org_id
      const orgHierarchy = useState<OrganisationRelationResponse | null>(
        'orgHierarchy',
        () => null
      )
      const { data: orgData } =
        await organisationService.getOrgRelationById(org_id)
      orgHierarchy.value = orgData.value as OrganisationRelationResponse
      if (orgHierarchy.value?.hierarchy_path) {
        return navigateTo({
          path: `/${locale}/algoritme/${orgHierarchy.value.hierarchy_path}/${org_id}/${lars}/${algoName}`,
        })
      }
      return navigateTo({
        path: `/${locale}/algoritme/${org_id}/${lars}/${algoName}`,
      })
    }
    if (
      lars &&
      (!algoritme.value ||
        algoritme.value.lars !== lars ||
        locale !== from.path.split('/')[1])
    ) {
      const { data: algoritmeData } = await algoritmeService.getOne(
        lars,
        mapLocaleName(locale)
      )
      algoritme.value = algoritmeData.value as Algoritme
    }
  }
})
